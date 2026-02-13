# World Explorer (Global Map System Prototype)

This repository now includes a data-driven prototype for the **World Explorer** PC game:

- Data-driven map loader for all 195 countries.
- Core keyboard/controller-ready arcade driving physics.
- Placeholder map generation pipeline (5 landmarks per country).
- One-command Windows build pipeline for `.exe` generation.

## Quick Start (development)

```bash
python scripts/generate_starter_maps.py
python -m pip install -r requirements.txt
PYTHONPATH=src python main.py --country "Canada"
```

Controls: `W/A/S/D` or Arrow Keys.

## Global Map System

Country source list: `data/countries.txt` (195 entries).

Each generated country map lives in:

- `maps/<country-slug>/map.json`

Each map has:

- terrain profile
- spawn point
- map size
- 5 placeholder landmarks

## Master Build Script (.exe)

On Windows, run:

```bat
python build.py
```

or:

```bat
build_world_explorer.bat
```

This script:

1. Regenerates all 195 starter maps.
2. Installs dependencies.
3. Packages a playable executable via PyInstaller.

Expected output:

- `dist/WorldExplorer.exe`
