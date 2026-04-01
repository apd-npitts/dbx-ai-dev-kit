# Repo Map

## Core Files

- `databricks.yml`: top-level bundle config and target definitions
- `resources/pipelines.yml`: pipeline resource definition
- `resources/jobs.yml`: orchestration job definition
- `src/pipelines/genie_demo_pipeline/transformations/telemetry_pipeline.py`: bronze, silver, and gold logic
- `src/genie/genie_space.template.yml`: Genie source-of-truth config

## Why This Layout Works Well For Demos

- Assets are small and easy for Codex to edit live
- Bundle resources are separated from business logic
- Notebooks are explicit, readable, and easy to expand
- Genie configuration is versioned alongside the tables it relies on
