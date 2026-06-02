# EchoWork

**An AI-native desktop IDE built with [Tauri](https://tauri.app/) + React.**

EchoWork is the visual interface for the EchoAI ecosystem. It connects to the EchoAI backend (which hosts the [EchoCode](https://github.com/EchoWorker/EchoCodeRust) agent engine), giving you an integrated development environment where AI assists with coding, file management, Git workflows, and project exploration — all in a native desktop app.

<p align="center">
  <img src="https://raw.githubusercontent.com/EchoWorker/EchoWork/main/docs/images/main-workspace.png" alt="EchoWork main workspace" width="900" />
</p>

> **Prerequisites**: EchoWork requires the [EchoAI](../EchoAI/) backend. Install it before running EchoWork.

---

## ✨ Highlights

- **AI Chat Panel** — Multi-model streaming (Claude, GPT, Gemini, DeepSeek, 30+ models), inline code blocks, markdown rendering, image attachments, steering (type while AI works).
- **File Explorer** — Browse, create, rename, copy/paste, drag-and-drop. Watches the filesystem for live updates.
- **Code Preview** — CodeMirror 6 with syntax highlighting, Ctrl+F search, word wrap, line numbers, dark/light themes.
- **Git Integration** — Stage, unstage, commit, diff, discard changes, view commit graph — all from the sidebar.
- **Spreadsheet Viewer** — Open `.xlsx`/`.xls` files with full Univer rendering (formulas, styles, merged cells, themes).
- **Markdown Preview** — Rich rendering with Ctrl+F full-text search (CSS Custom Highlight API).
- **Skills System** — Browse, install, and manage AI skill packs from the sidebar. Trust-on-first-use security model.
- **Screenshot & Annotate** — Capture screen regions and paste into chat as image attachments.
- **Background Tasks** — Live task bar showing running bash commands and sub-agents, with cancel/status tracking.
- **Turn File Summary** — After each AI turn, see which files were modified with one-click diff viewing.
- **Cost & Token Monitoring** — Live context usage in the input bar, per-session cost tracking.
- **Setup Wizard** — First-run wizard walks you through API key configuration and model verification.
- **Auto-Update** — Built-in updater with SHA256 checksum verification.
- **Cross-Platform** — Windows and macOS, with platform-appropriate menus and shortcuts.
- **i18n** — English and Chinese language support.

---

## 📥 Download

Latest builds: see [Releases](https://github.com/EchoWorker/EchoAIStore/releases?q=echowork) (look for tags starting with `echowork-v`).

| Platform | File |
|---|---|
| Windows x64 | `EchoWork_*_x64-setup.exe` |
| macOS Apple Silicon | `EchoWork_*_aarch64.dmg` |

> macOS Intel and Linux are not yet supported.

---

## 🛠️ Install

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

## 🔄 Auto-update

EchoWork checks for updates on startup (silently). When a new version is available, you'll see an "Update Available" dialog inside the app — one click to download and install.

The updater verifies signatures with a Tauri-managed key, independent of OS code signing.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Desktop Shell | Tauri v2 (Rust) |
| Frontend | React 18, TypeScript, Zustand, TailwindCSS |
| Code Editor | CodeMirror 6 |
| Spreadsheet | Univer |
| Git | libgit2 (via git2-rs) |
| AI Backend | EchoAI + EchoCode (Rust) |

---

## 🏠 Ecosystem

| Layer | Role |
|---|---|
| **[EchoCode](https://github.com/EchoWorker/EchoCodeRust)** | Rust AI agent engine — LLM protocols, 17 tools, compaction, sessions, hooks |
| **[EchoAI](../EchoAI/)** | Service layer — multi-session management, DB persistence, WebSocket API, plugin host |
| **EchoWork** (this) | Desktop IDE — file explorer, Git, chat, code preview |

---

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md).

---

## 📄 Source & License

- Source code: [EchoWorker/EchoWork](https://github.com/EchoWorker/EchoWork) (AGPL-3.0)
- Releases: [Releases tab](https://github.com/EchoWorker/EchoAIStore/releases?q=echowork)
