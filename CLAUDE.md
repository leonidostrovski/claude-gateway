# Claude Gateway — Instructions

## IMPORTANT: Network access rules

The 192.168.20.x subnet and all homelab hosts are NOT reachable via Bash.
**Never use Bash for any homelab network operations.**

All homelab access MUST go through MCP tools:

| Task | Use this tool |
|---|---|
| Ping a host | `mcp__homelab__ping` |
| Run a command on any host | `mcp__homelab__ssh_run` |
| Call any HTTP API | `mcp__homelab__http_request` |
| Update this MCP server | `mcp__homelab__mcp_update` |

## Key hosts

| Host | IP | Access |
|---|---|---|
| MCP Gateway container | 192.168.20.108 | ssh_run (user: root) |
| Zabbix server | 192.168.20.249 | http_request (API) or ssh_run |
| Proxmox04 | 192.168.20.200 | http_request (API port 8006) |

## Adding new MCP tools

1. Read current server code: `ssh_run("192.168.20.108", "cat /opt/claude-mcp/server.py")`
2. Write updated code with new tool added
3. Deploy: `mcp_update(new_code)`
4. Tell user to start a new session to pick up new tools

## MCP server location

- Container: `192.168.20.108` (LXC 9000, proxmox04)
- Server file: `/opt/claude-mcp/server.py`
- Service: `rc-service claude-mcp restart`
- Public URL: `https://patronage-gear-devious.ngrok-free.dev/mcp (streamable-http transport)`
