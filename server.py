import subprocess, paramiko, urllib.request, urllib.error, json, ssl
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("claude-homelab", host="0.0.0.0", port=8000)

@mcp.tool()
def ping(host: str, count: int = 4) -> str:
    """Ping a host and return latency results"""
    result = subprocess.run(["ping", "-c", str(count), host],
                            capture_output=True, text=True, timeout=30)
    return result.stdout or result.stderr

@mcp.tool()
def ssh_run(host: str, command: str, user: str = "root", port: int = 22) -> str:
    """Run a command on a remote host via SSH"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user,
                   key_filename="/root/.ssh/claude_gateway", timeout=10)
    _, stdout, stderr = client.exec_command(command)
    out = stdout.read().decode()
    err = stderr.read().decode()
    client.close()
    return out + (f"\n[stderr]: {err}" if err else "")

@mcp.tool()
def http_request(url: str, method: str = "GET", headers: dict = None,
                 body: str = None, verify_ssl: bool = False) -> str:
    """Make an HTTP/HTTPS request to any local or remote service"""
    ctx = ssl.create_default_context()
    if not verify_ssl:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    req_headers = headers or {}
    if body and "Content-Type" not in req_headers:
        req_headers["Content-Type"] = "application/json"

    body_bytes = body.encode() if body else None
    req = urllib.request.Request(url, body_bytes, req_headers, method=method.upper())

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            content = r.read().decode(errors="replace")
            return f"Status: {r.status}\n{content}"
    except urllib.error.HTTPError as e:
        content = e.read().decode(errors="replace")
        return f"Status: {e.code}\n{content}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def restart_mcp_container() -> str:
    """Restart LXC container 9000 (this MCP server) on proxmox04.

    SSHes to proxmox04 and runs 'pct restart 9000' in the background.
    The ngrok tunnel and MCP service will reconnect in ~30 seconds.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect("proxmox04", username="root",
                       key_filename="/root/.ssh/claude_gateway", timeout=10)
        # Run in background with short delay so this SSH session closes cleanly
        # before the container stops
        _, stdout, _ = client.exec_command(
            "nohup bash -c 'sleep 2 && pct restart 9000' >/dev/null 2>&1 &"
        )
        stdout.read()
        client.close()
        return (
            "Container 9000 restart initiated on proxmox04. "
            "The MCP session will drop and reconnect in ~30 seconds."
        )
    except Exception as e:
        return f"Error connecting to proxmox04: {e}"

if __name__ == "__main__":
    mcp.run(transport="sse")
