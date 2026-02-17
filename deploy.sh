#!/bin/bash
# Deploy the MCP server as a Databricks App
# Usage: ./deploy.sh <profile-name> [app-name]

set -euo pipefail

PROFILE="${1:?Usage: ./deploy.sh <profile-name> [app-name]}"
APP_NAME="${2:-mcp-ai-dev-kit}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Get current user
USER_EMAIL=$(databricks current-user me --profile "$PROFILE" -o json | python3 -c "import sys,json; print(json.load(sys.stdin)['userName'])")
WORKSPACE_PATH="/Workspace/Users/${USER_EMAIL}/${APP_NAME}"

echo "Deploying ${APP_NAME} to ${WORKSPACE_PATH}..."

# Sync project files to workspace
databricks sync "$SCRIPT_DIR" "$WORKSPACE_PATH" \
  --profile "$PROFILE" \
  --watch=false

# Create the app (ignore error if it already exists)
databricks apps create "$APP_NAME" \
  --description "AI Dev Kit MCP Server — 50+ Databricks tools for AI Playground" \
  --profile "$PROFILE" 2>/dev/null || echo "App already exists, redeploying..."

# Deploy
databricks apps deploy "$APP_NAME" \
  --source-code-path "$WORKSPACE_PATH" \
  --profile "$PROFILE"

echo ""
echo "Deployed! Getting app URL..."
databricks apps get "$APP_NAME" --profile "$PROFILE" -o json | python3 -c "
import sys, json
app = json.load(sys.stdin)
url = app.get('url', 'pending...')
status = app.get('status', {}).get('state', 'unknown')
print(f'  App URL: {url}')
print(f'  MCP endpoint: {url}/mcp')
print(f'  Status: {status}')
print(f'  Logs: {url}/logz')
"
