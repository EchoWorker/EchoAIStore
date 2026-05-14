# EchoWork Changelog

All notable changes to EchoWork will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.x] — 2026-05-13 → 2026-05-14

First public preview. Core functionality and CI pipeline established.

### Added

**Application shell**
- VS Code-style three-pane layout: ActivityBar / Sidebar / PreviewPanel + ChatPanel.
- Custom title bar with global file search (`Ctrl/Cmd+K`).
- Welcome page when no workspace or no chat session is active.
- Multi-workspace support; recent workspaces list.

**Chat & AI integration**
- WebSocket JSON-RPC client to EchoAI gateway (`session.completions`, `session.history`, etc.).
- Adapt EchoAI event-protocol v0.2 `(type, event)` dispatch.
- Context token usage indicator in the input box (e.g. `45K / 200K`).
- Streaming text, thinking blocks, tool-call cards, plan-review cards, sub-agent cards.
- Session tabs with rename / clear / delete; per-session draft preservation.
- Slash commands (`/compact`, `/clear`).
- Steering: send messages while a turn is running.

**File explorer & preview**
- Workspace file tree with copy / paste / delete shortcuts.
- Code preview powered by CodeMirror 6 (syntax highlighting, line numbers, themes).
- VS Code-style in-file search panel (`Ctrl/Cmd+F`) with case / word / regex toggles and match counter.
- Markdown preview with outline, image lightbox, Mermaid diagrams, LaTeX.
- Spreadsheet preview powered by Univer.
- Web preview (HTML), with element-inspector mode.
- Diff view (CodeMirror Merge).
- Tool-call cards with clickable file paths that open in the preview pane.
- Right-click context menus on file tree and Git changed files.

**Git integration**
- Source Control panel: stage / unstage / discard / commit / push / pull / sync.
- Inline file context menu: open file, open changes, copy absolute / relative path.
- AI-assisted commit message generation.
- Source Control Graph (commit timeline) per repo.

**Cross-platform**
- Windows x64 build.
- macOS Apple Silicon build (Intel currently not built).
- macOS native traffic-light buttons via `titleBarStyle: Overlay`.
- macOS application menu (EchoWork / Edit / Window) using Tauri preset items.
- Platform-aware keyboard shortcut formatting (`Ctrl+K` ↔ `⌘K`).
- Path separator normalization across platforms.

**Distribution**
- GitHub Actions workflow (`echowork-v*` tag triggers build).
- Multi-target build matrix: `x86_64-pc-windows-msvc` + `aarch64-apple-darwin`.
- Tauri auto-updater integrated; signed update manifest.
- Release artifacts published to this repo (`EchoWorker/EchoAIStore`); `echowork-latest` pointer release used as the updater endpoint.
- In-app **EchoAI missing dialog**: detects when `echoai` binary is not found and guides the user to install it.
- Crash reporter: `window.onerror` + `unhandledrejection` + top-level `AppErrorBoundary`, logs flushed immediately to disk.

### Known limitations

- Not signed with an OS code-signing certificate. macOS Gatekeeper / Windows SmartScreen will warn on first launch.
- macOS Intel and Linux are not yet built.
- The first installed version cannot OTA-update itself; users must download a newer version manually once. Subsequent versions update in-app.
- EchoAI must be installed separately (see prerequisite section in README).

---

> Older internal iterations exist in the source repository's git history. This file tracks public releases only.
