from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

TERRAINS = ["desert", "forest", "mountain", "coastal", "urban", "plains"]


def slugify(country: str) -> str:
    return (
        country.lower()
        .replace("'", "")
        .replace(",", "")
        .replace(".", "")
        .replace(" ", "-")
        .replace("/", "-")
    )


def deterministic_points(country: str, count: int = 5) -> list[tuple[int, int]]:
    digest = hashlib.sha256(country.encode("utf-8")).digest()
    points = []
    for i in range(count):
        a = digest[i * 2]
        b = digest[i * 2 + 1]
        x = 140 + (a % 980)
        y = 120 + (b % 520)
        points.append((x, y))
    return points


def generate(countries_file: Path, maps_root: Path) -> int:
    countries = [line.strip() for line in countries_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    for idx, country in enumerate(countries):
        terrain = TERRAINS[idx % len(TERRAINS)]
        folder = maps_root / slugify(country)
        folder.mkdir(parents=True, exist_ok=True)
        landmarks = [
            {
                "name": f"{country} Landmark {n + 1}",
                "type": "placeholder",
                "x": p[0],
                "y": p[1],
            }
            for n, p in enumerate(deterministic_points(country, 5))
        ]
        payload = {
            "country": country,
            "terrain": terrain,
            "size": [2400, 1400],
            "spawn": [200.0, 200.0],
            "landmarks": landmarks,
        }
        (folder / "map.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return len(countries)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate starter maps for all countries")
    parser.add_argument("--countries", default="data/countries.txt")
    parser.add_argument("--maps-root", default="maps")
    args = parser.parse_args()

    total = generate(Path(args.countries), Path(args.maps_root))
    print(f"Generated {total} starter maps in {args.maps_root}")
