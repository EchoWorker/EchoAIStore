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

## Get started

```bash
echoai gateway    # Start the server
echoai agent      # Interactive REPL
echoai agent -p "hello"  # Single prompt
```

First run auto-creates `~/.echoai/config.yaml`.

## Commands

| Command | Description |
|---|---|
| `echoai gateway` | Start the WebSocket JSON-RPC server |
| `echoai agent` | Interactive agent REPL |
| `echoai agent -p "..."` | Single prompt, non-interactive |
| `echoai onboard` | Initialize config |
| `echoai -b claude_code gateway` | Override agent backend |
