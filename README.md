# Databricks MCP Server App

Host the [ai-dev-kit](https://github.com/databricks-solutions/ai-dev-kit) MCP server as a Databricks App — giving the AI Playground 50+ tools to build on Databricks using natural language.

## What This Is

A **3-file wrapper** that takes the open-source `databricks-mcp-server` (stdio transport) and deploys it as a Databricks App with Streamable HTTP transport. The Playground auto-discovers all tools.

```
app.py            # 4 lines — import server, expose as HTTP
app.yaml          # Databricks App config
requirements.txt  # Pull ai-dev-kit from GitHub
```

## Setup

### Prerequisites
- Databricks CLI v0.229.0+ (`databricks --version`)
- A Databricks workspace with Apps enabled
- Authenticated CLI profile (`databricks auth login --host <url> --profile <name>`)

### Deploy

```bash
./deploy.sh <profile-name> [app-name]

# Example:
./deploy.sh fe-vm-serverless-jsr0s9 databricks-mcp-server
```

### Connect to AI Playground

1. Open your workspace → **AI Playground**
2. Select a model with the **Tools enabled** label
3. Click **Tools** → **Add tool** → **MCP Servers**
4. Add your app's MCP endpoint: `https://<app-url>/mcp`
5. The Playground auto-discovers all 50+ tools

## Demo Script: Build an AI Agent in 5 Prompts

Once connected in the Playground:

1. **"Create a catalog called `demo_agent` and a schema called `product_data` inside it"**
   → Uses Unity Catalog tools

2. **"Create a table `demo_agent.product_data.product_docs` with columns: id INT, title STRING, content STRING, and insert 10 sample product FAQ rows"**
   → Uses SQL tools

3. **"Create a vector search index on the product_docs table using the content column"**
   → Uses Vector Search tools

4. **"Build a Knowledge Assistant called product-helper that uses the vector search index as its knowledge source"**
   → Uses Agent Bricks tools

5. **"What's the status of the product-helper serving endpoint?"**
   → Uses Serving tools

Switch to the workspace UI — everything was created live.

## Architecture

```
AI Playground ──Streamable HTTP──▶ Databricks App (this repo)
                                        │
                                        ▼
                                  ai-dev-kit MCP Server
                                  (50+ tools via FastMCP)
                                        │
                                        ▼
                              Databricks APIs (SDK)
                              ├── SQL Warehouses
                              ├── Unity Catalog
                              ├── Jobs / Pipelines
                              ├── Vector Search
                              ├── Model Serving
                              ├── Agent Bricks
                              ├── AI/BI Dashboards
                              ├── Genie
                              └── ...
```
