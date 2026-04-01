from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path


DEVICE_TYPES = ["compressor", "freezer", "meter", "pump"]
REGIONS = ["central", "east", "south", "west"]


def build_event(index: int) -> dict[str, object]:
    now = datetime.now(timezone.utc)
    event_ts = now - timedelta(minutes=index * 3)
    return {
        "device_id": f"device-{index % 200:04d}",
        "device_type": DEVICE_TYPES[index % len(DEVICE_TYPES)],
        "region": REGIONS[index % len(REGIONS)],
        "site_id": f"site-{(index % 18) + 1:03d}",
        "event_ts": event_ts.isoformat(),
        "temperature_c": round(random.uniform(55, 100), 2),
        "battery_pct": round(random.uniform(5, 100), 2),
        "pressure_kpa": round(random.uniform(90, 145), 2),
        "status_code": "ALERT" if index % 13 == 0 else "OK",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate local telemetry demo data.")
    parser.add_argument("--output-dir", default="demo_data", help="Directory to write JSON files into.")
    parser.add_argument("--rows", type=int, default=2500, help="Number of telemetry events to generate.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    raw_dir = output_dir / "raw" / "telemetry_events"
    raw_dir.mkdir(parents=True, exist_ok=True)

    rows = [build_event(index) for index in range(args.rows)]
    output_file = raw_dir / "telemetry_events.json"
    with output_file.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")

    print(f"Wrote {len(rows)} telemetry events to {output_file}")


if __name__ == "__main__":
    main()
