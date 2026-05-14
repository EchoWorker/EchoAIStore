# EchoAI

AI Agent gateway and runtime — connects frontends (VS Code, Obsidian, Teams, WeChat, …) to LLM agent backends through a unified WebSocket JSON-RPC protocol.

## Install

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.ps1 | iex
```

After installation, restart your terminal and verify:
```bash
echoai --version
```

### Update

```bash
echoai update
```

### Supported platforms

| Platform | Architecture |
|---|---|
| Windows | x64 |
| Linux | x64 |
| macOS | arm64 (Apple Silicon) |

## Quick start

```bash
# Start the gateway server (for VS Code / Obsidian / other clients)
echoai gateway

# Or start an interactive REPL directly
echoai agent

# Single prompt (non-interactive)
echoai agent -p "hello"
```

First run auto-creates `~/.echoai/config.yaml` with default settings.

## Commands

| Command | Description |
|---|---|
| `echoai gateway` | Start the WebSocket JSON-RPC server |
| `echoai agent` | Interactive agent REPL |
| `echoai agent -p "..."` | Single prompt, non-interactive |
| `echoai onboard` | Initialize config (auto-runs on first use) |
| `echoai update` | Self-update to latest version |
| `echoai session list` | List all sessions |
| `echoai session show <key>` | Show session turns |
| `echoai cron list` | List cron jobs |
| `echoai --version` | Show version |

### Global flags

```bash
echoai -b claude_code gateway    # Override agent backend
echoai -b echo_agent agent       # Works with any subcommand
```

## Configuration

Config file location: `~/.echoai/config.yaml`

```yaml
agents:
  backend: echo_agent        # or claude_code

logging:
  level: INFO
  file: echoai.log

plugins:
  - name: server
    type: server
    enabled: true
    host: 127.0.0.1
    port: 8083

  - name: cron
    type: cron
    enabled: true

  - name: memory
    type: memory
    enabled: true
```

### Agent backends

| Backend | Description |
|---|---|
| `echo_agent` | Self-hosted agent via EchoCode (supports multiple LLM providers) |
| `claude_code` | Anthropic Claude Code CLI (requires `npm install -g @anthropic-ai/claude-code`) |

## Architecture

```
Client (VS Code / Obsidian / …)
    ↕  WebSocket JSON-RPC
EchoAI Gateway
    ├── Agent Manager (echo_agent / claude_code)
    ├── Session Store (SQLite)
    ├── Cron Scheduler
    ├── Memory Plugin (vector search + dreaming)
    └── Tool Registry (send_message, send_email, memory_search, …)
```

## Data directory

All runtime data is stored in `~/.echoai/`:

```
~/.echoai/
├── config.yaml      # Configuration
├── session.db       # Sessions & turns (SQLite)
├── cron.db          # Cron jobs (SQLite)
├── echoai.log       # Gateway log
├── gateway.lock     # Singleton lock
├── memory/          # Vector memory store
└── bin/             # Binary (if installed via script)
```

## Requirements

- **Windows**: Visual C++ Runtime (most systems already have it)
- **Linux**: glibc 2.38+ (Ubuntu 24.04+, Fedora 39+, etc.)
- **macOS**: macOS 12+ (Apple Silicon)
- **For `claude_code` backend**: Node.js + `npm install -g @anthropic-ai/claude-code`

## Feedback

For issues and feature requests, please contact the EchoWorker team.
