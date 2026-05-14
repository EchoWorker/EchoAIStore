# EchoWork

EchoWork is a desktop AI collaboration workspace — file explorer, code preview, AI chat, all in one window.

> **Prerequisites**: EchoWork requires the [EchoAI](../EchoAI/) backend. Install it before running EchoWork.

---

## Download

Latest builds: see [Releases](https://github.com/EchoWorker/EchoAIStore/releases?q=echowork) (look for tags starting with `echowork-v`).

| Platform | File |
|---|---|
| Windows x64 | `EchoWork_*_x64-setup.exe` |
| macOS Apple Silicon | `EchoWork_*_aarch64.dmg` |

> macOS Intel and Linux are not yet supported.

---

## Install

### Windows
1. Download `EchoWork_*_x64-setup.exe` from the latest `echowork-v*` release.
2. Run the installer. Click **More info → Run anyway** if SmartScreen warns about an unknown publisher.

### macOS (Apple Silicon)
1. Download `EchoWork_*_aarch64.dmg`.
2. Open the DMG, drag **EchoWork.app** to **Applications**.
3. First launch is blocked by Gatekeeper (no Apple code signing yet):
   - Right-click **EchoWork.app → Open** → click **Open** in the dialog. **OR**
   - **System Settings → Privacy & Security → "Open Anyway"** next to the EchoWork message.

You only need to bypass Gatekeeper / SmartScreen once.

---

## Auto-update

EchoWork checks for updates on startup (silently). When a new version is available, you'll see an "Update Available" dialog inside the app — one click to download and install.

The updater verifies signatures with a Tauri-managed key, independent of OS code signing.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## Source

- Source code: [EchoWorker/EchoWork](https://github.com/EchoWorker/EchoWork) (private)
- Releases: [Releases tab](https://github.com/EchoWorker/EchoAIStore/releases?q=echowork)
