# EchoWork

EchoWork is a desktop AI collaboration workspace — file explorer, code preview, AI chat, all in one window.

EchoWork is the GUI client for [EchoAI](../EchoAI/). EchoAI is required as the backend.

---

## Prerequisites

Install **EchoAI** first (EchoWork talks to it as a local gateway):

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.ps1 | iex
```

EchoWork looks for `echoai` at `~/.echoai/bin/echoai{.exe}`. If it's missing, EchoWork will pop up a friendly install reminder on launch.

---

## Download EchoWork

Latest builds: see [Releases](https://github.com/EchoWorker/EchoAIStore/releases?q=echowork).

| Platform | Download |
|---|---|
| Windows x64 | `EchoWork_x64-setup.exe` from `echowork-vX.Y.Z` release |
| macOS Apple Silicon | `EchoWork_aarch64.app.tar.gz` or `EchoWork_aarch64.dmg` |

> macOS Intel and Linux are not yet supported.

---

## First launch: bypass OS warnings

EchoWork is **not signed with an OS code-signing certificate** (yet). You will see a warning on first launch.

### macOS — Gatekeeper

> "EchoWork can't be opened because Apple cannot check it for malicious software."

1. Right-click **EchoWork.app → Open** → click "Open" in the dialog. **OR**
2. **System Settings → Privacy & Security → "Open Anyway"** next to the EchoWork message.

You only need to do this once.

### Windows — SmartScreen

> "Windows protected your PC"

Click **More info → Run anyway**.

---

## Auto-update

EchoWork checks for updates on startup (silently). When a new version is available, you'll see an "Update Available" dialog inside the app — one click to download and install.

The updater verifies signatures using a Tauri-managed key, independent of OS code signing.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## Source

- Source code: [EchoWorker/EchoWork](https://github.com/EchoWorker/EchoWork) (private)
- Releases: this folder + [Releases tab](https://github.com/EchoWorker/EchoAIStore/releases?q=echowork)
- Issues / feedback: file in source repo, or use in-app feedback
