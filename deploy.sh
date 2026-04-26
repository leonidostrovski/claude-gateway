#!/bin/bash
# Deploy server.py to the gateway container and restart MCP server
CONTAINER="192.168.20.108"
echo "Deploying server.py to $CONTAINER..."
scp -i /root/.ssh/claude_gateway -o StrictHostKeyChecking=no \
    server.py root@$CONTAINER:/opt/claude-mcp/server.py
echo "Restarting MCP server..."
ssh -i /root/.ssh/claude_gateway -o StrictHostKeyChecking=no \
    root@$CONTAINER "rc-service claude-mcp restart"
echo "Done. Start a new claude.ai/code session to pick up new tools."
