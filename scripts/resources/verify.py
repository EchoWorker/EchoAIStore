#!/usr/bin/env python3
"""Validate catalogs/releases and assemble a manifest from packaged archives."""
from __future__ import annotations
import argparse, hashlib, json, re, tarfile
from pathlib import Path, PurePosixPath

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
SHA = re.compile(r"^[0-9a-f]{64}$")


def fail(message: str): raise ValueError(message)
def read_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()

def safe_path(value: str):
    p = PurePosixPath(value)
    if p.is_absolute() or not p.parts or "\\" in value or any(x in ("", ".", "..") for x in p.parts): fail(f"unsafe path: {value}")

def validate_catalog(data: dict):
    if data.get("schema_version") != 1 or set(data) != {"schema_version", "resources"}: fail("invalid catalog envelope")
    if not data["resources"]: fail("empty catalog")
    ids, assets, destinations = set(), set(), set()
    required = {"id","owner","label_key","required","version","destination","asset","source","key_files"}
    for r in data["resources"]:
        if set(r) != required: fail(f"invalid catalog fields for {r.get('id')}")
        for field, seen in (("id", ids), ("asset", assets), ("destination", destinations)):
            if r[field] in seen: fail(f"duplicate {field}: {r[field]}")
            seen.add(r[field])
        safe_path(r["destination"])
        if not r["asset"].startswith("echoai-resource-") or not r["asset"].endswith(".tar.bz2"): fail(f"invalid asset: {r['asset']}")
        if not r["key_files"] or len(set(r["key_files"])) != len(r["key_files"]): fail(f"invalid key_files: {r['id']}")
        for p in r["key_files"]: safe_path(p)
        source = r["source"]
        if source.get("kind") == "huggingface-revision":
            if not re.fullmatch(r"[0-9a-f]{40}", source.get("revision", "")): fail("Hugging Face revision must be a commit")
            for p in source.get("files", []): safe_path(p)
        elif source.get("kind") == "tar-bz2-files":
            if not SHA.fullmatch(source.get("sha256", "")): fail("upstream archive SHA-256 is required")
            for a, b in source.get("files", {}).items(): safe_path(a); safe_path(b)
        else: fail(f"unsupported source kind: {source.get('kind')}")


def inspect_archive(path: Path, resource: dict):
    top = resource["destination"]
    expected = {f"{top}/{p}" for p in resource["key_files"]}
    names = set()
    with tarfile.open(path, "r:bz2") as tf:
        for m in tf:
            safe_path(m.name.rstrip("/"))
            if m.issym() or m.islnk() or not (m.isdir() or m.isfile()): fail(f"unsafe archive type: {m.name}")
            if PurePosixPath(m.name).parts[0] != top: fail(f"wrong top directory: {m.name}")
            names.add(m.name.rstrip("/"))
    missing = expected - names
    if missing: fail(f"archive {path.name} missing key files: {sorted(missing)}")


def make_manifest(catalog: dict, assets: Path, version: str) -> dict:
    if not SEMVER.fullmatch(version): fail(f"invalid resources version: {version}")
    tag = f"echoai-resources-v{version}"
    base = f"https://github.com/EchoWorker/EchoAIStore/releases/download/{tag}"
    output = {"schema_version": 1, "release": {"version": version, "tag": tag, "base_url": base}, "resources": []}
    for r in catalog["resources"]:
        archive = assets / r["asset"]
        if not archive.is_file(): fail(f"missing archive: {archive}")
        inspect_archive(archive, r)
        output["resources"].append({k: r[k] for k in ("id","owner","label_key","required","version","destination","key_files")} | {"archive": {"asset": r["asset"], "url": f"{base}/{r['asset']}", "format": "tar.bz2", "size_bytes": archive.stat().st_size, "sha256": hash_file(archive)}})
    return output


def validate_manifest(catalog: dict, manifest: dict, assets: Path):
    release = manifest.get("release", {}); version = release.get("version", "")
    if manifest.get("schema_version") != 1 or not SEMVER.fullmatch(version): fail("invalid manifest envelope/version")
    tag = f"echoai-resources-v{version}"; base = f"https://github.com/EchoWorker/EchoAIStore/releases/download/{tag}"
    if release != {"version": version, "tag": tag, "base_url": base}: fail("manifest release URL/tag mismatch")
    by_id = {r["id"]: r for r in manifest.get("resources", [])}
    if len(by_id) != len(manifest.get("resources", [])) or set(by_id) != {r["id"] for r in catalog["resources"]}: fail("catalog/manifest ids differ")
    wanted = {r["asset"] for r in catalog["resources"]}
    actual = {p.name for p in assets.iterdir() if p.is_file() and p.name.endswith(".tar.bz2")}
    if actual != wanted: fail(f"archive asset set differs: expected {sorted(wanted)}, got {sorted(actual)}")
    for c in catalog["resources"]:
        m=by_id[c["id"]]; archive=m.get("archive", {}); path=assets/c["asset"]
        if not SHA.fullmatch(archive.get("sha256", "")): fail(f"SHA-256 required: {c['id']}")
        if archive != {"asset": c["asset"], "url": f"{base}/{c['asset']}", "format": "tar.bz2", "size_bytes": path.stat().st_size, "sha256": hash_file(path)}: fail(f"archive metadata mismatch: {c['id']}")
        for key in ("owner","label_key","required","version","destination","key_files"):
            if m.get(key) != c[key]: fail(f"manifest/catalog {key} mismatch: {c['id']}")
        inspect_archive(path, c)


def main():
    p=argparse.ArgumentParser(); p.add_argument("--catalog",type=Path,required=True); p.add_argument("--assets",type=Path); p.add_argument("--version"); p.add_argument("--manifest",type=Path); p.add_argument("--assemble",action="store_true"); p.add_argument("--output",type=Path)
    a=p.parse_args(); catalog=read_json(a.catalog); validate_catalog(catalog)
    if a.assemble:
        if not (a.assets and a.version and a.output): fail("assemble requires --assets, --version and --output")
        manifest=make_manifest(catalog,a.assets,a.version); a.output.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        sums="".join(f"{r['archive']['sha256']}  {r['archive']['asset']}\n" for r in manifest["resources"]); (a.output.parent/"SHA256SUMS").write_text(sums,encoding="utf-8")
    elif a.manifest:
        if not a.assets: fail("manifest verification requires --assets")
        validate_manifest(catalog,read_json(a.manifest),a.assets)
    print("resource validation passed")
if __name__ == "__main__": main()
