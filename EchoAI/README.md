# EchoAI

**AI Agent Gateway & Runtime** — a multi-session, multi-client service layer that bridges any frontend to any LLM agent backend over WebSocket JSON-RPC.

EchoAI sits between client applications (VS Code, CLI, Teams Bot, desktop IDE, …) and agent engines (EchoCode, Claude Code). It owns session lifecycle, persistent storage, plugin hosting, memory, scheduled tasks, and a rich streaming event protocol — so every client gets the same capabilities without reimplementing them.

---

## ✨ Highlights

- **🔌 Multi-Client WebSocket Gateway** — Any client that speaks WebSocket JSON-RPC can connect: VS Code extensions, desktop apps, CLI tools, chat bots, browser panels. Multiple clients can share the same gateway simultaneously.
- **🤖 Pluggable Agent Backends** — Ships with `EchoAgent` (wrapping [EchoCode](../EchoCode/), recommended — 17 tools, sub-agents, background tasks, multi-protocol LLM, hooks, vision, cost tracking) and `ClaudeAgent` (wrapping Claude Code via Anthropic SDK, lightweight alternative). Switching backend is a one-line config change.
- **🧠 Persistent Memory** — Local vector semantic search via [fastembed](https://github.com/Anush008/fastembed-rs) (ONNX, no external API). 3-stage "Dreaming" consolidation: extract → merge → archive. Structured identity files (`SOUL.md`, `USER.md`, `MEMORY.md`) survive across sessions.
- **🔧 Plugin & Tool System** — Built-in tools (messaging, email, cron, memory) plus a plugin registry that lets external services inject their own tools at runtime via `plugin.register`.
- **🚀 Skills Management** — Install, uninstall, trust-gate, and serve Markdown-defined skill packs. Three scopes: global, workspace, builtin.
- **⚡ Streaming Event Protocol** — 10+ real-time event types pushed over WebSocket: token streaming, thinking chain, tool lifecycle, sub-agent tracking, background task status, cost updates, interactive Q&A.
- **🔄 Session Lifecycle** — Create / close (free memory) / delete (purge data) / restore sessions. Per-session model selection persisted to DB. In-flight steering injection. Cooperative abort.
- **💾 SQLite Persistence** — Sessions, conversation turns (with full step history), and cron jobs stored in WAL-mode SQLite. Resume any conversation after restart.
- **💸 Cost Tracking** — Per-turn token usage (input / output / cache) accumulated at session level, pushed to clients via `usage/update` events.
- **🌍 Cross-Platform** — Single native binary for Windows (x64), Linux (x64), macOS (ARM64).

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│           Clients (VS Code / Desktop IDE / CLI / Bot)       │
└──────────────────────────┬─────────────────────────────────┘
                           │  WebSocket JSON-RPC
┌──────────────────────────▼─────────────────────────────────┐
│                      EchoAI Gateway                         │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Session     │  │   Plugin     │  │   Skill          │  │
│  │   Manager     │  │   Registry   │  │   Service         │  │
│  │              │  │   (runtime   │  │   (install/list/  │  │
│  │  create/close │  │    tool inj.) │  │    trust/view)   │  │
│  │  /delete/get  │  │              │  │                   │  │
│  └──────┬───────┘  └──────┬───────┘  └───────────────────┘  │
│         │                 │                                  │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌───────────────────┐  │
│  │  Agent       │  │   Memory     │  │   Cron            │  │
│  │  Manager     │  │   Plugin     │  │   Scheduler       │  │
│  │  (LRU ×8)   │  │  (fastembed  │  │   (7-field cron   │  │
│  │              │  │   + dreaming)│  │    expressions)   │  │
│  └──┬───────┬──┘  └──────────────┘  └───────────────────┘  │
│     │       │                                               │
│  ┌──▼────┐ ┌▼──────────┐                                   │
│  │ Echo  │ │ Claude     │  ← Pluggable agent backends       │
│  │ Agent │ │ Agent      │                                   │
│  │(Echo- │ │(Claude Code│                                   │
│  │ Code) │ │ + MCP)     │                                   │
│  └───────┘ └────────────┘                                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Built-in Tools                                     │   │
│  │  send_message · send_email · list_robots            │   │
│  │  set_cron · delete_cron · list_crons                │   │
│  │  memory_search · record_task                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  SQLite Store (WAL mode)                            │   │
│  │  sessions · turns (with steps JSON) · crons         │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Key design principles:**

- **Gateway, not engine** — EchoAI does not run the LLM loop itself. It delegates to pluggable agent backends (EchoCode, Claude Code) and focuses on session orchestration, persistence, and client communication.
- **Multi-session, multi-client** — Multiple WebSocket clients can connect simultaneously. Each session has its own agent instance with independent context.
- **LRU agent caching** — At most 8 agent instances kept in memory (configurable). Least-recently-used agents are evicted; their sessions survive in SQLite.
- **Plugin-driven extensibility** — The Memory plugin, Cron plugin, and any external plugin register tools into the gateway. The agent sees a unified tool list regardless of source.

---

## 📡 WebSocket JSON-RPC Protocol

EchoAI exposes a single WebSocket endpoint. All communication uses [JSON-RPC 2.0](https://www.jsonrpc.org/specification).

### Client → Server (Requests)

| Method | Description |
|---|---|
| `auth` | Authenticate with a token |
| `chat.completions` | Start a conversation turn (params: `session_key`, `prompt`, `model`, `workspace`, `attachments`) |
| `chat.cancel` | Abort the current running turn |
| `chat.enqueue` | Inject a steering prompt while agent is running |
| `background.cancel` | Cancel a background task by ID |
| `session.list` | List all sessions (returns `session_key`, `name`, `current_model`, timestamps) |
| `session.get` | Get a single session's metadata |
| `session.rename` | Rename a session |
| `session.close` | Close a session (free agent memory, keep data) |
| `session.delete` | Delete a session and all its turns |
| `session.history` | Load conversation history (paginated turns with full step data) |
| `session.compact` | Trigger manual context compaction |
| `model.list` | List available models + current model for a session |
| `model.set` | Switch the active model for a session (persisted) |
| `question.answer` | Reply to an agent's interactive question |
| `skill.list` | List installed skills (grouped by scope: global / workspace / builtin) |
| `skill.view` | View a skill's content |
| `skill.install` | Install a skill from a path |
| `skill.uninstall` | Uninstall a skill |
| `skill.update` | Update an installed skill |
| `skill.add_trust` | Mark a skill as trusted |
| `cron.list` | List active cron jobs |
| `cron.delete` | Delete a cron job |
| `plugin.register` | Register an external plugin (injects tools into the agent) |
| `plugin.unregister` | Remove a registered plugin |
| `plugin.list` | List registered plugins |

### Server → Client (Notifications)

All streamed via `chat.event` with a `type` + `event` discriminator:

| Type | Event | Payload |
|---|---|---|
| `token` | `append` | Incremental LLM text output |
| `thinking` | `append` | Chain-of-thought reasoning text |
| `tool` | `create` | Tool call started (name, input) |
| `tool` | `update` | Tool execution result |
| `question` | `create` | Agent asks the user a question (options, multi-select) |
| `steering` | `create` | Steering prompt confirmed |
| `usage` | `update` | Token usage + context window stats |
| `background` | `create` | Background task started (task_id, description) |
| `background` | `update` | Background task status change (done / failed / cancelled) |
| `turn` | `end` | Conversation turn completed |

---

## 🤖 Agent Backends

### EchoAgent (default, recommended)

Wraps [EchoCode](../EchoCode/) — a high-performance Rust-native coding agent. EchoAgent is the fully-featured backend with the richest capability set. EchoAI maps EchoCode's streaming events 1:1 to the WebSocket protocol.

Capabilities inherited from EchoCode:
- **17 built-in tools** — file I/O (`read`/`write`/`edit`), search (`grep`/`find`/`ls`), execution (`bash`), web (`web_fetch`/`web_search`), agent control (`subagent`/`todo`/`plan_mode`/`ask_user`), background tasks (`wait`/`cancel_background_task`)
- **5 specialised sub-agents** — GeneralPurpose, Explore, Plan, Verification, DeepResearch
- **Multi-protocol LLM** — Chat Completions, OpenAI Responses API, Anthropic Messages — auto-selected per model
- **Background tasks** — Bash auto-promotes after 2 min, JSONL logs, `wait` tool for interleaving parallel work
- **Multi-tier context compaction** — micro-compact, LLM-powered summarization, image eviction, hard truncate, circuit breaker
- **Hooks v2** — 12-event lifecycle hooks for plugins to observe or modify agent behaviour
- **Vision** — Read images from disk and pass to vision-capable models
- **Cost tracking** — Per-call token usage with LiteLLM pricing data
- **Skills & plugins** — User / project / builtin scopes, MCP tool servers (stdio + HTTP/SSE)
- **SWE-bench Verified: 89.8% Pass@1** — industry-leading autonomous coding performance

### ClaudeAgent (lightweight alternative)

Wraps [Claude Code](https://docs.anthropic.com/en/docs/claude-code) via the Anthropic Agent SDK. Simpler setup but fewer features compared to EchoAgent:

- MCP bridge for gateway tool injection (spawns a local HTTP→MCP stdio shim)
- Stream event mapping (`text_delta`, `thinking_delta`, tool calls)
- Interactive Q&A via `AskUserQuestion` hook interception
- Steering via `queue_message()`
- Auto-approve mode with permission bypass

Select the backend in `config.yaml`:

```yaml
agents:
  backend: echo_agent       # echo_agent | claude_code

# Or use Claude Code:
agents:
  backend: claude_code
```

---

## 🧠 Memory System

The Memory plugin provides persistent, semantic-searchable memory across sessions, scoped by workspace:

- **Vector Embeddings** — [fastembed](https://github.com/Anush008/fastembed-rs) with BGE-small-en-v1.5 ONNX model, runs locally with zero external API calls.
- **Workspace-Scoped Search** — Search and record operations are automatically scoped to the current session's workspace (project directory). Different projects maintain separate memory contexts.
- **Dreaming Consolidation** — A 3-stage background process:
  1. **Extract** — After N turns, pull key facts from the conversation
  2. **Merge** — Deduplicate and consolidate with existing memories
  3. **Archive** — Promote to `MEMORY.md` as curated long-term memory
- **Structured Files** — `IDENTITY.md` (agent identity), `SOUL.md` (behaviour guidelines), `USER.md` (user profile), `MEMORY.md` (long-term memory) — all managed under `~/.echoai/memory/`.
- **Project Diary** — `record_task` writes to `memory/<project>/` subdirectories, keeping per-project task history separate.
- **Tools Exposed** — `memory_search` (semantic search) and `record_task` (write to daily diary) are injected into the agent's tool list.

---

## ⏰ Cron Scheduler

The Cron plugin provides persistent scheduled tasks:

- 7-field cron expressions: `sec min hour dom mon dow year`
- One-shot mode (`run_once: true`) for single-fire reminders
- Persisted to SQLite — survives gateway restarts
- When a job fires, the message is delivered to the agent as a new conversation turn
- Tools exposed: `set_cron`, `delete_cron`, `list_crons`

---

## 🔧 Plugin Registry

External services can register as plugins at runtime, injecting tools the agent can call:

```
→ plugin.register { name: "weather", tools: [...], callback_url: "..." }
← OK

# Agent now sees "weather_get_forecast" as an available tool.
# When called, EchoAI forwards the invocation to the plugin's callback.
```

Built-in plugins (Memory, Cron) use the same registry mechanism internally.

---

## 🚀 Skills Management

Markdown-formatted skill packs that define reusable workflows for the agent:

```
~/.echoai/skills/            # global — available in all sessions
<workspace>/.echoai/skills/  # workspace — project-specific
<plugin>/skills/             # builtin — shipped with plugins
```

Each skill is a directory with `SKILL.md` (YAML frontmatter + prompt template). Skills require a trust gate on first use — clients call `skill.add_trust` to approve.

Manage via RPC: `skill.list`, `skill.install`, `skill.uninstall`, `skill.view`, `skill.update`.

---

## 📥 Install

### Pre-built binaries (recommended)

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/EchoWorker/EchoAIStore/main/EchoAI/install.ps1 | iex
```

Or download archives manually from [Releases](https://github.com/EchoWorker/EchoAIStore/releases?q=echoai) (look for `echoai-v*` tags).

| Platform | Archive |
|---|---|
| Windows x64 | `echoai-windows-x64.zip` |
| Linux x64 | `echoai-linux-x64.tar.gz` |
| macOS ARM64 | `echoai-darwin-arm64.tar.gz` |

### Build from source

Prerequisites: Rust 1.75+ (2021 edition)

```bash
cargo build --release
./target/release/echoai onboard    # interactive first-time setup
./target/release/echoai gateway    # start the WebSocket server
```

> **Note:** If you use [EchoWork](../EchoWork/) (desktop IDE), EchoAI is already bundled inside — no separate install needed.

---

## 🚀 Quick Start

### Prerequisites

- An LLM provider API key (OpenAI, Anthropic, etc.)
- Configure via [EchoCode](../EchoCode/) config (`~/.echoai/echocode.toml`)

### CLI Commands

```bash
echoai onboard             # interactive configuration wizard
echoai gateway             # start WebSocket JSON-RPC server
echoai gateway --port 9000 # override port (default: 8081, 0 = random)
echoai session list        # list saved sessions
echoai session show <id>   # show session turns
echoai session rename <id> <name>
echoai session clear <id>  # delete a session
echoai cron list           # list cron jobs
echoai cron add --name daily --schedule "0 0 9 * * * *" "good morning"
echoai cron delete <id>
echoai update              # self-update to latest version
```

---

## ⚙️ Configuration

`~/.echoai/config.yaml`:

```yaml
# Agent backend
agents:
  backend: echo_agent        # echo_agent | claude_code

# Logging
logging:
  level: info              # trace | debug | info | warn | error
  dir: "~/.echoai/logs"
  max_files: 10

# SMTP (for send_email tool)
smtp:
  host: "smtp.example.com"
  port: 587
  username: "user"
  password: "pass"
  from: "ai@example.com"
  starttls: true

# Plugins
plugins:
  - type: server
    enabled: true
    protocol: jsonrpc      # jsonrpc | http
    bind: tcp              # tcp | uds | pipe
    host: "127.0.0.1"
    port: 8081             # 0 = random port, writes gateway.lock
    token: "your-auth-token"

  - type: cron
    enabled: true

  - type: memory
    enabled: true
    memory_home: "~/.echoai/memory"
    dreaming: true
    n_results: 6
```

The agent backend (EchoCode) has its own config at `~/.echoai/echocode.toml` — see [EchoCode docs](../EchoCode/) for model/provider setup.

---

## 📦 Project Structure

```
src/
├── main.rs                  CLI entry — gateway / onboard / session / cron / update
├── cli/
│   ├── gateway.rs           WebSocket server startup
│   ├── onboard.rs           Interactive first-time setup wizard
│   ├── agent.rs             Standalone agent REPL (no gateway)
│   ├── update.rs            Self-update
│   └── commands.rs          Session & cron CLI subcommands
├── config/
│   ├── schema.rs            YAML config structs (Server / Cron / Memory / Agent / SMTP / Log)
│   └── loader.rs            Config loading + save + path resolution
├── context.rs               Global AppState (store, plugins, agent manager, tools, event bus)
├── agent/
│   ├── manager.rs           Agent lifecycle + LRU cache (evict by workspace)
│   ├── echo_agent.rs        EchoCode wrapper — spawns client, maps events
│   ├── claude/
│   │   ├── agent.rs         Claude Code wrapper — MCP bridge, event mapping
│   │   ├── event_mapper.rs  MessageProcessor + Q&A interception
│   │   ├── mcp_bridge.rs    HTTP→MCP stdio shim for gateway tool injection
│   │   ├── tool_names.rs    Tool name normalization
│   │   └── models.rs        Model config from claudecode.toml
│   ├── question.rs          Interactive Q&A coordinator (agent ↔ client)
│   ├── lru_cache.rs         Generic LRU cache with async eviction
│   └── base.rs              BaseAgent trait definition
├── plugins/
│   ├── server/
│   │   ├── dispatch.rs      JSON-RPC method routing (30+ RPCs)
│   │   ├── connection.rs    WebSocket connection state
│   │   └── ws.rs            WebSocket server + gateway.lock
│   ├── registry.rs          Plugin registration + runtime tool injection
│   ├── memory/
│   │   ├── plugin.rs        Memory plugin (fastembed init + dreaming)
│   │   └── bridge.rs        Memory ops: search, recall, record_task, context injection
│   ├── cron.rs              Cron scheduler plugin
│   └── base.rs              Plugin trait definition
├── service/
│   ├── turn.rs              Turn execution — streams agent events → chat.event notifications
│   ├── session.rs           Session CRUD + history loading
│   ├── skill.rs             Skill management (list / install / uninstall / trust / view)
│   ├── model_catalog.rs     Model listing + per-session model tracking
│   ├── history.rs           History loading with step deserialization
│   └── plugin.rs            Plugin lifecycle management
├── store/
│   ├── session.rs           SQLite persistence — sessions + turns (JSON steps) + migrations
│   ├── cron.rs              Cron job persistence
│   └── models.rs            SessionRecord / TurnRecord data models
├── tools/
│   ├── builtin.rs           send_message / send_email / list_robots
│   ├── cron_tools.rs        set_cron / delete_cron / list_crons
│   ├── memory_tools.rs      memory_search / record_task
│   └── traits.rs            Tool trait definition
├── events/
│   └── bus.rs               In-process event bus
├── models/
│   ├── steps.rs             Step type definitions (Token / Tool / Question / Usage / …)
│   └── serialize.rs         Step JSON serialization
├── paths.rs                 Platform-aware path resolution (~/.echoai/)
├── task_context.rs          Per-task context (session key, workspace)
└── utils/                   Shared utilities
```

---

## 🏠 Ecosystem

EchoAI is the middle layer of a 3-tier system:

| Layer | Repo | Role |
|---|---|---|
| **EchoCode** | [EchoCodeRust](../EchoCode/) | Rust agent engine — LLM loop, 17 tools, sub-agents, compaction, hooks, sessions |
| **EchoAI** (this repo) | [EchoAI](https://github.com/EchoWorker/EchoAI) | Gateway service — multi-session management, SQLite persistence, WebSocket API, plugin host, memory, cron |
| **EchoWork** | [EchoWork](../EchoWork/) | Desktop IDE — Tauri app with file explorer, Git integration, chat panel, code preview, AI config UI |

EchoAI can also run standalone as a headless service for chatbots, automation pipelines, or custom integrations.

---

## 🛠️ Development

```bash
cargo build              # debug build
cargo build --release    # release build
cargo check              # type check
cargo test               # run tests

# Run in dev mode (debug logging)
cargo run -- gateway --verbose

# Override port
cargo run -- gateway --port 0
```

---

## 📄 License

[AGPL-3.0](LICENSE)
