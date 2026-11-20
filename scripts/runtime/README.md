# Pinned ONNX Runtime from NuGet
The EchoAI release workflow uses the official native CPU package `Microsoft.ML.OnnxRuntime` 1.24.2 from https://www.nuget.org/api/v2/package/Microsoft.ML.OnnxRuntime/1.24.2.
- Package SHA256: `782564D3D68E87269EA1812CC94710AD06FE014FAF093F01A6F89D0BD58719D3`.
- Microsoft author certificate SHA256: `566A31882BE208BE4422F7CFD66ED09F5D4524A5994F50CCC8B05EC0528C1353`.
- Nuspec source commit: `058787ceead760166e3c50a0a4cba8a833a6f53f` (release branch `rel-1.24.2`).
The package was downloaded and verified with `dotnet nuget verify --all --certificate-fingerprint ...`. The Microsoft author signature has a trusted February 2026 timestamp; verification succeeds even though the author certificate subsequently expired. Do not bypass signature, timestamp, TLS, or hash checks.
`nuget_runtime.py` downloads, checks the exact package hash and pinned signing certificate, extracts one exact native entry, and calls `OrtGetApiBase()->GetVersionString()` before packaging. Use Python 3.12+ and .NET SDK 10. The script exits unsuccessfully on download, signature, hash, entry, load, or version errors.
```powershell
python scripts/runtime/nuget_runtime.py --download --target x86_64-pc-windows-msvc --package "$env:TEMP/microsoft.ml.onnxruntime.1.24.2.nupkg" --output "$env:TEMP/echoai-runtime"
python -m unittest discover -s scripts/runtime -p 'test_*.py'
```
The same script runs natively on Linux and macOS using their Rust target names. Product filenames and ONNX version are unchanged. There is no fallback to an unverified mirror or another version.
Local validation (2026-11-20): verified signed real package; extracted all three native entries; isolated Windows DLL load reported 1.24.2 and existing EchoAI debug executable `--version` succeeded; WSL Ubuntu 22.04 loaded the Linux library as 1.24.2 and `ldd` found all dependencies. These CPU loader checks succeeded without the package's optional providers_shared libraries. This does not prove GPU/provider or full model inference compatibility.
macOS arm64 entry was extracted but not executed locally. The release runner now performs native runtime version checking and a packaged EchoAI `--version` smoke test. The edited workflow has not been dispatched remotely yet; local tests are not proof of GitHub pipeline success.
