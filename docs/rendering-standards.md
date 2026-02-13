# Rendering Standards

## 1) Texture and Material Standards

### PBR Workflow
- Mandatory metal/roughness PBR workflow for all opaque materials.
- Base color textures must not contain baked lighting or AO shadows.
- Physically plausible value ranges:
  - Dielectric base color reflectance: avoid near-black/near-white extremes.
  - Metallic is binary-biased (0 or 1) unless justified by blended surfaces.
- Normal maps authored in tangent space and validated for consistent handedness.

### Texel Density Targets
Targets are measured at gameplay camera distance and represent on-screen consistency.

| Asset Class | Target Density | Acceptable Range |
|---|---:|---:|
| Hero vehicles (exterior) | 1024 px/m | 896–1152 px/m |
| Vehicle interiors | 768 px/m | 640–896 px/m |
| Landmark architecture | 768 px/m | 640–896 px/m |
| Standard environment props | 512 px/m | 384–640 px/m |
| Terrain detail layers | 256 px/m | 192–320 px/m |

Rules:
- Density may exceed target only on focal hero assets approved in review.
- UV mirroring is allowed for symmetric assets if decals/unique damage remain believable.

### Channel Packing Rules
Use consistent packed maps to reduce memory and sampling overhead.

- **ORM pack (default)**:
  - R = Ambient Occlusion
  - G = Roughness
  - B = Metallic
- Alpha channel reserved for masked opacity or material feature toggle only.
- Do not repurpose ORM channels per-asset; pipeline consistency is required.
- Emissive masks should be separate unless platform profile explicitly permits packing.

## 2) LOD / HLOD Budgets

### Vehicles
| Class | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---:|---:|---:|---:|
| Player/hero vehicle | 120k tris | 70k | 35k | 12k |
| Traffic vehicle | 60k tris | 30k | 14k | 6k |

- LOD switch distances should be speed-aware to minimize popping in chase camera.
- Wheel silhouette fidelity prioritized through LOD2.

### Environment Props
| Prop Size | LOD0 | LOD1 | LOD2 |
|---|---:|---:|---:|
| Small clutter | 2k tris | 900 | 300 |
| Medium prop | 8k tris | 3k | 1k |
| Large prop | 20k tris | 8k | 3k |

### Landmarks and HLOD
- Landmark unique meshes: target 150k–400k tris for LOD0 depending on footprint.
- Landmarks require at least 4 authored LODs plus HLOD cluster representation.
- HLOD cluster budgets:
  - Urban dense cells: <= 250k tris per cluster
  - Suburban/rural cells: <= 180k tris per cluster
- HLOD transition must be dithered and validated from 60–200 km/h camera speeds.

## 3) Performance Tiers and Deterministic Scalability

Define fixed, deterministic scalability groups. Avoid hidden auto-tuning that causes capture drift.

| Tier | Target Use | Shadow Cascades | Volumetrics | Texture Pool | View Distance | Post FX |
|---|---|---:|---|---|---|---|
| Ultra | High-end GPU | 4 (350m) | Full-resolution + local lights | 100% baseline budget | 100% | Full |
| High | Recommended | 4 (300m) | Full with reduced sample count | 85% | 90% | Full |
| Medium | Mid-range | 3 (180m) | Half-res volumetrics | 70% | 75% | Balanced |
| Low | Min spec | 2 (120m) | Minimal/half-res, sun only | 55% | 60% | Essential only |

Deterministic controls:
- Lock each tier to explicit numeric values in config (no dynamic overrides).
- Use fixed random seeds for foliage/prop variation in performance tests.
- Capture validation route with scripted weather/time to compare tiers build-to-build.
- Any tier value change requires benchmark rerun and approval from rendering + art leads.

## 4) Visual QA Checklist

### Fidelity and Consistency
- [ ] PBR validation passes: albedo, roughness, and metallic within approved ranges.
- [ ] Texel density checks pass for sampled assets in each class.
- [ ] Channel packing conforms to ORM standard without exceptions.
- [ ] LOD transitions are not perceptible under standard gameplay camera movement.

### Artifact and Stability Checks
- [ ] No z-fighting on layered road decals and lane markings.
- [ ] No normal-map inversion seams on mirrored UV assets.
- [ ] No moiré/specular sparkle at medium-long distances.
- [ ] No ghosting/smearing beyond policy thresholds in motion-heavy scenes.
- [ ] No missing mip levels or late-streaming placeholder textures.

### Tier Compliance
- [ ] Ultra/High/Medium/Low settings match documented deterministic values.
- [ ] Benchmarks meet frame-time targets without violating visual policies.
- [ ] Regression captures reviewed against previous approved build.
