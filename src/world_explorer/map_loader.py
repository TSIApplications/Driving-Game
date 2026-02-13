from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CountryMap:
    country: str
    terrain: str
    landmarks: list[dict[str, Any]]
    size: tuple[int, int]
    spawn: tuple[float, float]


class MapLoader:
    """Loads country maps from generated JSON files in maps/<slug>/map.json."""

    def __init__(self, maps_root: Path) -> None:
        self.maps_root = maps_root

    @staticmethod
    def slugify(country: str) -> str:
        return (
            country.lower()
            .replace("'", "")
            .replace(",", "")
            .replace(".", "")
            .replace(" ", "-")
            .replace("/", "-")
        )

    def map_path(self, country: str) -> Path:
        return self.maps_root / self.slugify(country) / "map.json"

    def load(self, country: str) -> CountryMap:
        path = self.map_path(country)
        if not path.exists():
            raise FileNotFoundError(f"Map for '{country}' not found at {path}")

        payload = json.loads(path.read_text(encoding="utf-8"))
        if len(payload.get("landmarks", [])) < 5:
            raise ValueError(f"Map '{country}' has fewer than 5 landmarks")

        return CountryMap(
            country=payload["country"],
            terrain=payload["terrain"],
            landmarks=payload["landmarks"],
            size=tuple(payload.get("size", [2400, 1400])),
            spawn=tuple(payload.get("spawn", [200.0, 200.0])),
        )
