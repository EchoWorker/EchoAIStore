"""Acquire the pinned Microsoft-signed NuGet CPU runtime, not GitHub releases."""
import argparse
import ctypes
import hashlib
from pathlib import Path
import subprocess
import zipfile

VERSION = "1.24.2"
PACKAGE_URL = f"https://www.nuget.org/api/v2/package/Microsoft.ML.OnnxRuntime/{VERSION}"
PACKAGE_SHA256 = "782564d3d68e87269ea1812cc94710ad06fe014faf093f01a6f89d0bd58719d3"
AUTHOR_SHA256 = "566A31882BE208BE4422F7CFD66ED09F5D4524A5994F50CCC8B05EC0528C1353"
TARGETS = {
    "x86_64-pc-windows-msvc": (
        "runtimes/win-x64/native/onnxruntime.dll", "onnxruntime-1.24.2.dll"),
    "x86_64-unknown-linux-gnu": (
        "runtimes/linux-x64/native/libonnxruntime.so", "libonnxruntime.so.1.24.2"),
    "aarch64-apple-darwin": (
        "runtimes/osx-arm64/native/libonnxruntime.dylib", "libonnxruntime.1.24.2.dylib"),
}


def verify_package(package):
    with package.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != PACKAGE_SHA256:
        raise ValueError(f"NuGet SHA256 mismatch: expected {PACKAGE_SHA256}, got {digest}")
    subprocess.run([
        "dotnet", "nuget", "verify", str(package), "--all",
        "--certificate-fingerprint", AUTHOR_SHA256, "--verbosity", "normal",
        "--force-english-output",
    ], check=True)


def extract_runtime(package, target, output):
    entry, name = TARGETS[target]
    with zipfile.ZipFile(package) as archive:
        info = archive.getinfo(entry)
        if info.file_size == 0:
            raise ValueError(f"Empty runtime entry: {entry}")
        data = archive.read(info)
    output.mkdir(parents=True, exist_ok=True)
    library = output / name
    library.write_bytes(data)
    print(f"Extracted {entry} -> {library}")
    return library


def smoke_runtime(library):
    # OrtApiBase contains GetApi and GetVersionString function pointers.
    call = ctypes.WINFUNCTYPE if hasattr(ctypes, "WINFUNCTYPE") else ctypes.CFUNCTYPE
    class ApiBase(ctypes.Structure):
        _fields_ = [("get_api", ctypes.c_void_p),
                    ("get_version_string", call(ctypes.c_char_p))]
    runtime = ctypes.CDLL(str(library.resolve()))
    runtime.OrtGetApiBase.restype = ctypes.POINTER(ApiBase)
    version = runtime.OrtGetApiBase().contents.get_version_string().decode("ascii")
    if version != VERSION:
        raise ValueError(f"ONNX Runtime version mismatch: expected {VERSION}, got {version}")
    print(f"Loaded ONNX Runtime {version}: {library}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=TARGETS)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    if args.download:
        args.package.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "curl", "--fail", "--location", "--retry", "3", "--max-time", "300",
            "--output", str(args.package), PACKAGE_URL,
        ], check=True)
    verify_package(args.package)
    library = extract_runtime(args.package, args.target, args.output)
    smoke_runtime(library)


if __name__ == "__main__":
    main()
