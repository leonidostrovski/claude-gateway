# Claude Gateway — MCP Server

MCP server running on LXC container (192.168.20.108) providing homelab tools to claude.ai/code sessions.

## Available tools

| Tool | Description |
|---|---|
| `ping` | Ping any host on the network |
| `ssh_run` | Run shell commands on any host via SSH |
| `http_request` | Make HTTP/HTTPS requests to local services |

## Add a new tool

1. Open this repo in claude.ai/code
2. Ask Claude: *"Add a new tool that does X"*
3. Claude edits `server.py` and runs `deploy.sh` via `ssh_run`
4. Start a new session to pick up the new tool

## Container info

- Host: `192.168.20.108` (LXC 9000 on proxmox04)
- MCP server: `/opt/claude-mcp/server.py`
- Service: `rc-service claude-mcp restart`
- ngrok tunnel: `https://patronage-gear-devious.ngrok-free.dev`
- SSH key: `/root/.ssh/claude_gateway`
