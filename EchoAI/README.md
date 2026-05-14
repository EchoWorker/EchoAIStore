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

### EchoCode configuration (`echocode.toml`)

When using the `echo_agent` backend, EchoCode requires its own configuration for LLM provider settings.

**File location:**
- Global: `~/.echoai/echocode.toml`
- Project: `{project}/.echoai/echocode.toml` (overrides global)

**Merge order:** Global → Project → Environment variables (highest priority)

**Minimal example** (Anthropic):

```toml
model = "anthropic/claude-sonnet-4-20250514"

[provider.anthropic]
api_key = "sk-ant-..."
```

**Minimal example** (OpenAI):

```toml
model = "openai/gpt-4o"

[provider.openai]
api_key = "sk-..."
```

**Full reference:**

```toml
# ── Model ────────────────────────────────────────────────────────
# Format: "provider/model-name"
# Examples: "anthropic/claude-sonnet-4-20250514", "openai/gpt-4o",
#           "google/gemini-2.5-pro", "deepseek/deepseek-chat"
model = "anthropic/claude-sonnet-4-20250514"
max_tokens = 16384
# temperature = 0.7
# thinking_level = "medium"    # minimal|low|medium|high|max (Anthropic/Google only)

# ── Providers ────────────────────────────────────────────────────
# Default provider settings (applied to all providers as fallback)
[provider]
# api_key = "sk-..."           # fallback API key for all providers
# base_url = "http://localhost:8080/v1"  # fallback base URL (e.g. local proxy)
# protocol = "chat_completions"  # chat_completions | responses | anthropic_messages

# Per-provider configuration
[provider.anthropic]
api_key = "sk-ant-..."
# base_url = "https://api.anthropic.com/v1"

[provider.openai]
# api_key = "sk-..."
# base_url = "https://api.openai.com/v1"

[provider.google]
# api_key = "AIza..."
# base_url = "https://generativelanguage.googleapis.com/v1beta/openai"

# Any OpenAI-compatible endpoint:
# [provider.deepseek]
# api_key = "sk-..."
# base_url = "https://api.deepseek.com/v1"

# [provider.ollama]
# base_url = "http://localhost:11434/v1"

# [provider.openrouter]
# api_key = "sk-or-..."
# base_url = "https://openrouter.ai/api/v1"

# ── Compaction ───────────────────────────────────────────────────
[compaction]
enabled = true
max_context_ratio = 0.85       # trigger compaction at 85% context usage
preserve_recent_turns = 4

# ── Permissions ──────────────────────────────────────────────────
[permissions]
mode = "auto"                  # auto|suggest|ask

# ── Model registry ───────────────────────────────────────────────
# Define context_window and capabilities for models not in the built-in list.
# This is required for correct compaction behavior — without it, unknown models
# default to 200K context window.
# Key must match the "provider/model" format used in the model field.

# [models."ollama/my-local-model"]
# context_window = 128000
# supports_thinking = false
# supports_vision = false

# [models."deepseek/deepseek-r1"]
# context_window = 64000
# supports_thinking = true
```

**Supported providers:** Anthropic, OpenAI, Google, DeepSeek, Groq, Mistral, Cohere, Together, Fireworks, OpenRouter, Ollama, Perplexity, XAI, and any OpenAI-compatible endpoint.

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
├── config.yaml      # EchoAI gateway configuration
├── echocode.toml    # EchoCode agent configuration (model, API keys, etc.)
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
