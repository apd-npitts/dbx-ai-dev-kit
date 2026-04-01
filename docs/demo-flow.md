# Demo Flow

## Suggested 15-Minute Story

1. Show the repo map and explain that this is a sandbox for Codex-driven Databricks asset generation.
2. Ask Codex to update a notebook, job, or pipeline in real time.
3. Deploy with Databricks Asset Bundles.
4. Run the orchestration job to seed data and refresh the pipeline.
5. Show the gold tables.
6. Create or update a Genie Space from the template in `src/genie/`.
7. Ask business-style questions in Genie and connect the answers back to the generated assets.

## Good Live Edits

- Add a new KPI column to `gold_device_daily_summary`
- Add a new notebook task to the job
- Change the Genie instructions to reflect your company's language
- Add an additional sample question for executives

## Fallback Plan

If live deployment is slow:

- show the repo changes Codex made
- open the notebooks and pipeline files directly
- render the Genie payload locally with `uv run python scripts/render_genie_space_payload.py ...`
- walk through the intended `databricks bundle run` command
