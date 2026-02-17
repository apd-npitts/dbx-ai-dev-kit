"""Databricks MCP Server — hosted as a Databricks App.

Wraps the ai-dev-kit MCP server with Streamable HTTP transport
so the Databricks AI Playground can connect to it as a tool source.
"""

from databricks_mcp_server.server import mcp

# ASGI app for uvicorn — Streamable HTTP on /mcp
# stateless_http=True so each request is independent (no session affinity needed)
app = mcp.http_app(path="/mcp", stateless_http=True)
