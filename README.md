# EchoAIStore

Product downloads for EchoWorker.

## Products

| Product | Description | Install |
|---|---|---|
| [EchoAI](EchoAI/) | AI Agent gateway and runtime | [Install guide](EchoAI/README.md) |
| [EchoWork](EchoWork/) | Desktop AI collaboration workspace (GUI client for EchoAI) | [Install guide](EchoWork/README.md) |

## Install order

EchoWork depends on EchoAI. To use EchoWork, install **EchoAI first**, then install EchoWork.

```
1. Install EchoAI    →  follow EchoAI/README.md
2. Install EchoWork  →  follow EchoWork/README.md
```

EchoAI alone (without EchoWork) is also usable — as a CLI agent or as a JSON-RPC gateway for other clients.
