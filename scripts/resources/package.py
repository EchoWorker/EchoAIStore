#!/usr/bin/env python3
"""Build one catalog resource as a reproducible tar.bz2 archive."""
from __future__ import annotations
import argparse, bz2, hashlib, io, json, os, shutil, tarfile, tempfile
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen

EPOCH = 0


def load_resource(catalog: Path, resource_id: str) -> dict:
    data = json.loads(catalog.read_text(encoding="utf-8"))
    matches = [r for r in data["resources"] if r["id"] == resource_id]
    if len(matches) != 1:
        raise ValueError(f"resource id must occur exactly once: {resource_id}")
    return matches[0]


def safe_relative(value: str) -> PurePosixPath:
    p = PurePosixPath(value)
    if p.is_absolute() or not p.parts or any(x in ("", ".", "..") for x in p.parts) or "\\" in value:
        raise ValueError(f"unsafe relative path: {value}")
    return p


def download(url: str, destination: Path) -> None:
    req = Request(url, headers={"User-Agent": "EchoAIStore-resource-packager/1"})
    with urlopen(req, timeout=120) as response, destination.open("wb") as out:
        shutil.copyfileobj(response, out, 1024 * 1024)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_members(archive: tarfile.TarFile):
    for member in archive.getmembers():
        safe_relative(member.name)
        if member.issym() or member.islnk() or not (member.isdir() or member.isfile()):
            raise ValueError(f"unsupported entry in upstream archive: {member.name}")
        yield member


def materialize(resource: dict, root: Path, source_dir: Path | None) -> Path:
    destination = root / resource["destination"]
    destination.mkdir(parents=True)
    source = resource["source"]
    if source_dir:
        for name in resource["key_files"]:
            src, dst = source_dir / Path(*safe_relative(name).parts), destination / Path(*safe_relative(name).parts)
            if not src.is_file():
                raise FileNotFoundError(src)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        return destination
    if source["kind"] == "huggingface-revision":
        base = f"https://huggingface.co/{source['repository']}/resolve/{source['revision']}"
        for name in source["files"]:
            dst = destination / Path(*safe_relative(name).parts)
            dst.parent.mkdir(parents=True, exist_ok=True)
            download(f"{base}/{name}", dst)
    elif source["kind"] == "tar-bz2-files":
        upstream = root / "upstream.tar.bz2"
        download(source["url"], upstream)
        actual = sha256(upstream)
        if actual != source["sha256"]:
            raise ValueError(f"upstream SHA-256 mismatch: expected {source['sha256']}, got {actual}")
        wanted = source["files"]
        found: dict[str, tarfile.TarInfo] = {}
        with tarfile.open(upstream, "r:bz2") as tf:
            for member in safe_members(tf):
                basename = PurePosixPath(member.name).name
                if member.isfile() and basename in wanted and basename not in found:
                    found[basename] = member
            missing = sorted(set(wanted) - set(found))
            if missing:
                raise ValueError(f"upstream archive missing files: {missing}")
            for upstream_name, output_name in wanted.items():
                dst = destination / Path(*safe_relative(output_name).parts)
                dst.parent.mkdir(parents=True, exist_ok=True)
                extracted = tf.extractfile(found[upstream_name])
                if extracted is None:
                    raise ValueError(f"cannot read {upstream_name}")
                with extracted, dst.open("wb") as out:
                    shutil.copyfileobj(extracted, out)
    else:
        raise ValueError(f"unsupported source kind: {source['kind']}")
    return destination


def deterministic_archive(directory: Path, output: Path) -> None:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as tf:
        paths = [directory] + sorted(directory.rglob("*"), key=lambda p: p.relative_to(directory.parent).as_posix())
        for path in paths:
            arcname = path.relative_to(directory.parent).as_posix()
            info = tf.gettarinfo(str(path), arcname)
            info.uid = info.gid = 0
            info.uname = info.gname = "root"
            info.mtime = EPOCH
            info.mode = 0o755 if path.is_dir() else 0o644
            if path.is_file():
                with path.open("rb") as f:
                    tf.addfile(info, f)
            else:
                tf.addfile(info)
    output.write_bytes(bz2.compress(raw.getvalue(), compresslevel=9))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--resource-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path, help="offline test input matching key_files")
    args = parser.parse_args()
    resource = load_resource(args.catalog, args.resource_id)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        directory = materialize(resource, Path(tmp), args.source_dir)
        archive = args.output_dir / resource["asset"]
        deterministic_archive(directory, archive)
    metadata = {"id": resource["id"], "asset": resource["asset"], "size_bytes": archive.stat().st_size, "sha256": sha256(archive)}
    (args.output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metadata, sort_keys=True))

if __name__ == "__main__":
    main()
