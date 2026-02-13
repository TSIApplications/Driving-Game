# Production Content Pipeline for Country Maps

## 1) Canonical Country-Map Template

Use a single canonical schema for every shipped country map. Each map package must include:

- `map_id`: `country_iso3_map_v###`
- `country`
  - `iso3`
  - `display_name`
  - `region`
- `biome`
  - `primary_biome`
  - `secondary_biomes[]`
  - `vegetation_density`
  - `terrain_profile` (flat / rolling / mountainous / mixed)
- `road_style`
  - `road_hierarchy` (highway / arterial / rural / trails)
  - `surface_types[]` (asphalt / dirt / gravel / cobble)
  - `lane_marking_profile`
  - `roadside_props_profile`
- `weather_profile`
  - `seasonality_model`
  - `time_of_day_lighting_sets[]`
  - `weather_events[]` (clear / rain / snow / fog / storm)
  - `hazard_modifiers`
- `landmark_set[]`
  - `landmark_id`
  - `tier` (`hero`, `standard`, `proxy`)
  - `category`
  - `location`
  - `cultural_notes`
- `mission_hooks[]`
  - `mission_hook_id`
  - `hook_type` (delivery / pursuit / exploration / race / narrative)
  - `landmarks_involved[]`
  - `difficulty_band`

### Canonical map metadata (required)

Each map must provide at minimum:

- `map_id`
- `country.iso3`
- `country.display_name`
- `biome.primary_biome`
- `road_style.road_hierarchy`
- `weather_profile.seasonality_model`
- `mission_hooks` (non-empty array)
- `landmark_set` (minimum 5 entries)

---

## 2) GIS-Inspired Reference Ingestion Workflow

### Phase A — Source Intake

1. Acquire approved source datasets:
   - Terrain heightmaps (DEM-style)
   - Surface/landcover texture references
   - Road network vectors
2. Record source metadata:
   - Source authority
   - License terms
   - Resolution/scale
   - Capture date and known gaps

### Phase B — Normalization & Conversion

1. Reproject all spatial data into the project coordinate convention.
2. Normalize terrain assets:
   - Height range clamp
   - Erosion/noise cleanup pass
   - Tile boundaries stitched for streaming
3. Normalize texture sets:
   - Albedo/normal/roughness standards
   - Shared biome palette mapping
4. Normalize road vectors:
   - Topology cleanup
   - Class remapping into game road hierarchy
   - Spline conversion for runtime roads

### Phase C — Authoring Hand-off

1. Export map-authoring bundle:
   - `terrain/heightmap.*`
   - `textures/*.set`
   - `roads/network.*`
   - `sources.yml`
2. Generate initial placement candidates for settlements + landmarks.
3. Open map package branch and assign environment + world art owners.

---

## 3) Landmark Creation Tiers

### Hero landmarks (high-detail)

- 1–3 per map (or more for dense urban regions)
- Cinematic quality mesh/material pass
- Bespoke storytelling props and lighting treatment
- Close-range gameplay interaction supported
- Required: cultural reference review + performance profiling

### Standard landmarks (mid-detail)

- Core world anchors for route readability
- Mid-poly assets with reusable kit pieces
- Readable silhouette from driving distance
- Optional mission tie-ins

### Distant proxies (low-detail)

- Skyline/background anchors only
- Ultra-low-cost geometry + baked materials
- HLOD/impostor ready
- No close interaction expected

---

## 4) Automated Validation Scripts

Add validation to CI and local author workflows:

- Script: `scripts/validate_map_metadata.py`
- Input: one or more JSON map definition files
- Checks:
  - Required metadata fields exist
  - `landmark_set` length >= 5
  - Landmark IDs follow naming convention
  - Map ID follows versioned naming convention

### Example usage

```bash
python3 scripts/validate_map_metadata.py content/maps/*.json
```

### CI integration (recommended)

- Run validator on every content PR touching `content/maps/`.
- Fail fast if any map has missing metadata or fewer than 5 landmarks.
- Publish per-file error summary as PR annotation.

---

## 5) Naming & Version Conventions

### Map ID format

- `country_iso3_map_v###`
- Examples:
  - `jpn_map_v001`
  - `bra_map_v014`

Rules:

- ISO3 must be lowercase 3-letter country code.
- Version must be zero-padded 3 digits.
- Increment version for gameplay-significant, world-layout, or metadata contract changes.

### Landmark ID format

- `country_iso3_<tier>_<slug>_v###`
- Examples:
  - `jpn_hero_tokyo_tower_v001`
  - `bra_standard_lapa_arches_v003`
  - `usa_proxy_desert_butte_a_v010`

Rules:

- `<tier>` must be one of: `hero`, `standard`, `proxy`.
- `<slug>` uses lowercase snake_case.
- Landmark version increments on model/material/placement changes that affect gameplay or readability.

---

## 6) Content Review Gates

Every map must pass the following gates before release branch merge:

1. **Art quality gate**
   - Composition/readability sign-off
   - Landmark tier fidelity meets target
   - Texture/material consistency check
2. **Cultural accuracy gate**
   - Regional architecture/style review
   - Naming and signage localization review
   - Sensitive content audit
3. **Performance gate**
   - Frame-time budget on min-spec hardware
   - Streaming memory budget compliance
   - Traffic + mission load stress test

Recommended gate ownership:

- Art Director (art quality)
- Cultural Consultant/Research Lead (accuracy)
- Technical Art + Performance Engineering (performance)

---

## 7) Rollout Plan (Wave-Based)

### Wave 0 — Pipeline hardening

- Build 2–3 pilot countries end-to-end.
- Validate tooling, naming, review gates, and CI checks.

### Wave 1 — Vertical slice (first 20 countries)

- Deliver representative biome/region diversity.
- Include full mission-hook coverage and landmark tier mix.
- Use this wave to lock production velocity metrics.

### Wave 2+ — Batch releases

- Release in predictable batches (e.g., 10–15 countries per batch).
- Prioritize by:
  - Player demand signals
  - Regional diversity gaps
  - Asset reuse opportunities
- Maintain backlog of stretch countries requiring bespoke hero-landmark investment.

### Ongoing maintenance

- Quarterly refresh pass on top maps.
- Backport systemic improvements to older map versions when feasible.
- Deprecate outdated map versions with migration notes.
