# Genie + Codex Demo Workspace

This repo is a clean Databricks demo workspace for showing how `Codex`, the Databricks `ai-dev-kit`, and `Genie` can work together to create and evolve real assets such as notebooks, jobs, and Lakeflow pipelines.

The structure is intentionally simple and editable so you can use it live in front of an audience, ask Codex to make changes, and show the result as first-class Databricks resources instead of slideware.

## What This Repo Is For

Use this repo when you want to demonstrate workflows like:

- generating or refining notebooks with Codex
- building or updating Databricks Jobs from natural-language requirements
- creating a Lakeflow Spark Declarative Pipeline for bronze, silver, and gold tables
- preparing governed tables for Genie Spaces
- iterating quickly with `uv`, Databricks Asset Bundles, and ai-dev-kit tooling

## Repo Layout

```text
databricks.yml                                # Bundle entrypoint
resources/
  jobs.yml                                    # Multi-task demo job
  pipelines.yml                               # Lakeflow pipeline resource
src/
  notebooks/
    01_seed_demo_data.py                      # Creates schema, volume, and raw demo data
    02_validate_demo_outputs.py               # Checks pipeline outputs
  pipelines/
    genie_demo_pipeline/
      transformations/
        telemetry_pipeline.py                 # Bronze/silver/gold pipeline logic
  genie/
    genie_space.template.yml                  # Source-of-truth Genie prompt/config scaffold
scripts/
  generate_iot_demo_data.py                   # Local synthetic data generator
  render_genie_space_payload.py               # Renders Genie config to JSON
docs/
  demo-flow.md                                # Suggested live demo flow
  codex-prompts.md                            # Prompt ideas for live Codex use
  repo-map.md                                 # Quick orientation guide
```

## Quick Start

### 1. Install local tooling

```bash
uv sync
```

### 2. Configure bundle variables

Update values at deploy time as needed:

```bash
databricks bundle validate -t dev --var="catalog=main,schema=genie_codex_demo,volume_name=demo_assets,warehouse_id=<warehouse-id>"
```

### 3. Deploy the demo assets

```bash
databricks bundle deploy -t dev --var="catalog=main,schema=genie_codex_demo,volume_name=demo_assets,warehouse_id=<warehouse-id>"
```

### 4. Run the orchestration job

The demo job seeds raw data, refreshes the pipeline, and validates outputs:

```bash
databricks bundle run demo_orchestration_job -t dev --var="catalog=main,schema=genie_codex_demo,volume_name=demo_assets,warehouse_id=<warehouse-id>"
```

## Demo Story

The sample assets model an operations telemetry scenario:

- a notebook generates raw IoT-style telemetry data into a Unity Catalog volume
- a Lakeflow pipeline builds bronze, silver, and gold tables
- a Databricks Job orchestrates the notebook and pipeline together
- a Genie Space template points at the curated gold tables for natural-language exploration

This gives you a clean narrative for showing:

1. Codex creating or modifying an asset
2. ai-dev-kit tools wiring that asset into Databricks resources
3. Genie answering questions over the resulting data model

## Local Utilities

Generate local demo files:

```bash
uv run python scripts/generate_iot_demo_data.py --output-dir demo_data
```

Render the Genie template into a JSON payload you can use with `create_or_update_genie`:

```bash
uv run python scripts/render_genie_space_payload.py --catalog main --schema genie_codex_demo --warehouse-id <warehouse-id>
```

## Suggested Next Moves

- Tailor the table names and prompts to your company's domain
- Add one or two notebook variations you want Codex to create live
- Pre-create the schema and warehouse permissions in your demo workspace
- Use the prompts in [docs/codex-prompts.md](/c:/Users/noahp/Code/dbx-ai-dev-kit/docs/codex-prompts.md) as your live script
