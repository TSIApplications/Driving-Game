#!/usr/bin/env python3
"""Validate country map metadata files.

Usage:
    python3 scripts/validate_map_metadata.py content/maps/*.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

MAP_ID_PATTERN = re.compile(r"^[a-z]{3}_map_v\d{3}$")
LANDMARK_ID_PATTERN = re.compile(
    r"^[a-z]{3}_(hero|standard|proxy)_[a-z0-9]+(?:_[a-z0-9]+)*_v\d{3}$"
)

REQUIRED_PATHS = [
    "map_id",
    "country.iso3",
    "country.display_name",
    "biome.primary_biome",
    "road_style.road_hierarchy",
    "weather_profile.seasonality_model",
    "mission_hooks",
    "landmark_set",
]


def get_path(data: dict[str, Any], dotted_path: str) -> Any:
    value: Any = data
    for key in dotted_path.split("."):
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: unable to parse JSON ({exc})"]

    if not isinstance(payload, dict):
        return [f"{path}: root must be a JSON object"]

    for req in REQUIRED_PATHS:
        value = get_path(payload, req)
        if value is None:
            errors.append(f"{path}: missing required field '{req}'")

    map_id = payload.get("map_id")
    if isinstance(map_id, str):
        if not MAP_ID_PATTERN.match(map_id):
            errors.append(
                f"{path}: invalid map_id '{map_id}' (expected country_iso3_map_v###)"
            )
    else:
        errors.append(f"{path}: map_id must be a string")

    mission_hooks = payload.get("mission_hooks")
    if not isinstance(mission_hooks, list) or len(mission_hooks) == 0:
        errors.append(f"{path}: mission_hooks must be a non-empty array")

    landmarks = payload.get("landmark_set")
    if not isinstance(landmarks, list):
        errors.append(f"{path}: landmark_set must be an array")
        return errors

    if len(landmarks) < 5:
        errors.append(f"{path}: landmark_set must contain at least 5 landmarks")

    for idx, landmark in enumerate(landmarks):
        if not isinstance(landmark, dict):
            errors.append(f"{path}: landmark_set[{idx}] must be an object")
            continue

        landmark_id = landmark.get("landmark_id")
        if not isinstance(landmark_id, str):
            errors.append(f"{path}: landmark_set[{idx}].landmark_id must be a string")
            continue

        if not LANDMARK_ID_PATTERN.match(landmark_id):
            errors.append(
                f"{path}: invalid landmark_id '{landmark_id}' "
                "(expected country_iso3_<tier>_<slug>_v###)"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate map metadata JSON files")
    parser.add_argument("files", nargs="+", help="JSON files to validate")
    args = parser.parse_args()

    had_errors = False

    for file_arg in args.files:
        path = Path(file_arg)
        if not path.exists():
            print(f"{path}: file does not exist", file=sys.stderr)
            had_errors = True
            continue

        file_errors = validate_file(path)
        if file_errors:
            had_errors = True
            for err in file_errors:
                print(err, file=sys.stderr)

    if had_errors:
        return 1

    print(f"Validated {len(args.files)} file(s): OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
