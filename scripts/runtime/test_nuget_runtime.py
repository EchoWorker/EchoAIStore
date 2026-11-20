import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import nuget_runtime as runtime


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.package = self.root / "fixture.nupkg"

    def make_package(self, entries):
        with zipfile.ZipFile(self.package, "w") as archive:
            for name, content in entries.items():
                archive.writestr(name, content)

    def test_three_targets_select_exact_entry_and_versioned_name(self):
        self.make_package({entry: target.encode() for target, (entry, _) in runtime.TARGETS.items()})
        for target, (_, name) in runtime.TARGETS.items():
            with self.subTest(target=target):
                library = runtime.extract_runtime(self.package, target, self.root / target)
                self.assertEqual(library.name, name)
                self.assertEqual(library.read_bytes(), target.encode())

    def test_bad_hash_rejected_before_signature_or_extraction(self):
        self.package.write_bytes(b"tampered")
        with patch.object(runtime.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
                runtime.verify_package(self.package)
            run.assert_not_called()

    def test_signature_verification_pins_microsoft_certificate(self):
        self.package.write_bytes(b"fixture")
        digest = hashlib.sha256(b"fixture").hexdigest()
        with patch.object(runtime, "PACKAGE_SHA256", digest), patch.object(runtime.subprocess, "run") as run:
            runtime.verify_package(self.package)
            args = run.call_args.args[0]
            self.assertIn("--all", args)
            self.assertEqual(args[args.index("--certificate-fingerprint") + 1], runtime.AUTHOR_SHA256)
            self.assertTrue(run.call_args.kwargs["check"])

    def test_signature_failure_is_not_ignored(self):
        self.package.write_bytes(b"fixture")
        with patch.object(runtime, "PACKAGE_SHA256", hashlib.sha256(b"fixture").hexdigest()), patch.object(
            runtime.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "dotnet")
        ):
            with self.assertRaises(subprocess.CalledProcessError):
                runtime.verify_package(self.package)

    def test_missing_entry_and_wrong_target_rejected(self):
        self.make_package({"other/library": b"data"})
        for target in ["unsupported", "aarch64-apple-darwin"]:
            with self.subTest(target=target), self.assertRaises(KeyError):
                runtime.extract_runtime(self.package, target, self.root / "out")
        self.assertFalse((self.root / "out").exists())

    def test_empty_runtime_rejected(self):
        entry, _ = runtime.TARGETS["x86_64-pc-windows-msvc"]
        self.make_package({entry: b""})
        with self.assertRaisesRegex(ValueError, "Empty runtime"):
            runtime.extract_runtime(self.package, "x86_64-pc-windows-msvc", self.root / "out")
        self.assertFalse((self.root / "out").exists())


if __name__ == "__main__":
    unittest.main()
