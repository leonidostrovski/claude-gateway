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

if __name__ == "__main__":
    mcp.run(transport="sse")
