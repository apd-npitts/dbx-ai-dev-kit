from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def render_text(value: str, replacements: dict[str, str]) -> str:
    for key, replacement in replacements.items():
        value = value.replace(f"{{{{ {key} }}}}", replacement)
    return value


def render_value(value, replacements: dict[str, str]):
    if isinstance(value, str):
        return render_text(value, replacements)
    if isinstance(value, list):
        return [render_value(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: render_value(item, replacements) for key, item in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the Genie space template to JSON.")
    parser.add_argument("--template", default="src/genie/genie_space.template.yml")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--warehouse-id", required=True)
    args = parser.parse_args()

    template_path = Path(args.template)
    with template_path.open("r", encoding="utf-8") as handle:
        template = yaml.safe_load(handle)

    payload = render_value(
        template,
        {
            "catalog": args.catalog,
            "schema": args.schema,
            "warehouse_id": args.warehouse_id,
        },
    )

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
