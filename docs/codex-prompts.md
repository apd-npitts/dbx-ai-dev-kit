# Codex Prompt Ideas

Use prompts like these during the demo.

## Notebooks

- Create a new notebook in `src/notebooks/` that profiles `gold_device_daily_summary` and highlights the top device types by critical events.
- Update `01_seed_demo_data.py` so it also generates a `humidity_pct` column and keep the code notebook-friendly.

## Jobs

- Add a final notebook task to the demo job that writes a daily executive summary table after the pipeline refresh.
- Update the job to pass `catalog`, `schema`, and `volume_name` consistently to every notebook task.

## Pipelines

- Extend the pipeline to track `humidity_pct` from bronze through gold and surface a new hourly humidity metric.
- Add a materialized view for top at-risk sites over the last 24 hours.

## Genie

- Rewrite the Genie instructions for a retail operations audience.
- Add five stronger sample questions for an executive stakeholder.
- Convert `src/genie/genie_space.template.yml` into a payload I can send to `create_or_update_genie`.
