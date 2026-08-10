import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / "resources" / f"{name}.py")
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return module

package = load("package")
verify = load("verify")

class ResourceScriptsTest(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / "resources" / "catalog.json").read_text(encoding="utf-8"))

    def test_catalog_is_valid(self):
        verify.validate_catalog(self.catalog)

    def test_unsafe_paths_are_rejected(self):
        for value in ("../model", "/model", "a\\model"):
            with self.assertRaises(ValueError):
                verify.safe_path(value)

    def test_archives_are_deterministic_and_manifest_has_sha(self):
        resource = self.catalog["resources"][0]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "source"; source.mkdir()
            for name in resource["key_files"]:
                path = source / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(name)
            outputs = []
            for n in ("one", "two"):
                work = root / n; directory = package.materialize(resource, work, source)
                archive = root / f"{n}.tar.bz2"; package.deterministic_archive(directory, archive); outputs.append(archive)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            assets = root / "assets"; assets.mkdir(); target = assets / resource["asset"]; target.write_bytes(outputs[0].read_bytes())
            one_catalog = {"schema_version": 1, "resources": [resource]}
            manifest = verify.make_manifest(one_catalog, assets, "1.2.3-test")
            self.assertRegex(manifest["resources"][0]["archive"]["sha256"], r"^[0-9a-f]{64}$")
            verify.validate_manifest(one_catalog, manifest, assets)

if __name__ == "__main__":
    unittest.main()
