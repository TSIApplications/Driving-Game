# Art Direction Standards

## 1) Lighting Model

### Time-of-Day Presets
Use deterministic presets with fixed key values so shots are reproducible across machines and builds.

| Preset | Sun Elevation | Color Temperature | Sky/Atmosphere | Exposure Bias | Use Case |
|---|---:|---:|---|---:|---|
| Dawn | 6–12° | 3800–4500K | High aerial perspective, warm horizon | -0.3 | Early commute, moody opening shots |
| Midday | 55–80° | 5600–6500K | Neutral scattering, highest contrast | 0.0 | Gameplay readability, benchmark captures |
| Golden Hour | 8–15° | 3200–4200K | Warm directional light, elongated shadows | -0.2 | Cinematic travel moments |
| Dusk | 2–8° | 3000–3800K | Cool zenith + warm horizon split | -0.4 | Transition scenes |
| Night (Moonlit) | <2° | 7000–9000K moon + local practicals | Low ambient, high practical contrast | -1.0 | City driving, headlights focus |

**Rules**
- Only one active world preset at runtime; blends happen over fixed 90s transition windows.
- Capture baselines for each biome with identical camera path and weather state.
- Avoid ad-hoc light actors in shipping maps; use preset-owned light rigs.

### Volumetrics
- Enable volumetric fog globally with biome-specific density profiles.
- Height fog should preserve road readability at 100m: avoid extinction values that hide lane boundaries.
- Volumetric light shafts allowed only for sun and hero practicals (stadiums, tunnels, ports).
- Cloud shadows and volumetric shadowing must be synchronized with sun direction from preset rig.

### Shadow Cascade Strategy
- 4 cascades for directional sun shadowing on High+ tiers; 3 on Medium; 2 on Low.
- Split distribution (near to far):
  - **High/Ultra**: 10m / 35m / 120m / 350m
  - **Medium**: 12m / 45m / 180m
  - **Low**: 20m / 120m
- Stabilize cascades to reduce shimmer during high-speed driving.
- Vehicle self-shadowing must remain enabled in all tiers; far terrain shadows can degrade by tier.

## 2) Biome-Driven Visual Language
To prevent one-off asset duplication, each region must use a shared biome kit and regional LUT.

### Core Biome Kits
- **Temperate Urban**: concrete, asphalt patch variants, painted metal, storefront glass, utility clutter.
- **Arid Desert**: bleached rock sets, sand accumulation decals, dry shrubs, sun-faded signage.
- **Alpine Forest**: conifer variants, wet rock/moss materials, fog cards, timber architecture set.
- **Coastal**: salt-stained concrete, rusted metal trims, sea-wall modules, wind-bent vegetation.
- **Industrial Corridor**: modular warehouses, pipe kits, hazard paint decal library, gravel yards.

### Biome Kit Rules
- Each biome ships with:
  - 1 terrain material family (base + 3 blend layers)
  - 1 prop taxonomy (small/medium/large clutter + hero prop set)
  - 1 decal pack (wear, dirt, leaks, road markings)
  - 1 color grading LUT profile
- New map content must source at least 85% of placed assets from the target biome kit.
- One-off hero assets are capped at 15% of region asset count and require art review sign-off.

## 3) Post-Processing Presets

### Regional Color Grading
- Each biome defines a LUT with a neutral fallback.
- White balance target by biome:
  - Temperate Urban: neutral (D55–D65)
  - Arid Desert: warm bias (+300 to +600K perceived)
  - Alpine Forest: cool shadows / neutral highlights
  - Coastal: slight cyan lift in mids, controlled saturation
  - Industrial: reduced saturation with preserved hazard-color readability

### Motion Blur Limits
- Camera motion blur shutter equivalent:
  - Ultra/High: 0.35 max
  - Medium: 0.25 max
  - Low: 0.15 max
- Per-object blur for fast vehicles remains enabled at all tiers but scales sample count.
- Disable exaggerated blur in competitive or precision-driving modes.

### Anti-Aliasing Policy
- **Primary**: Temporal AA (or TSR/TAAU equivalent) for all tiers.
- **Ultra/High**: high-quality temporal resolve + sharpening clamp.
- **Medium**: balanced temporal resolve with reduced history weight.
- **Low**: performance temporal mode; avoid FXAA fallback unless platform constrained.
- Specular aliasing control is mandatory via roughness floor and normal map mip bias tuning.

## 4) Visual QA Checklist
Use this checklist during content lock, regression, and pre-release visual parity sweeps.

### Fidelity Parity
- [ ] Time-of-day presets match approved baseline captures for each biome.
- [ ] Material response remains consistent across weather and time transitions.
- [ ] Biome kit usage meets 85/15 reuse-to-hero ratio.
- [ ] Regional LUTs preserve gameplay-critical color signals (traffic lights, hazards, UI markers).

### Artifact Detection
- [ ] No visible shadow cascade popping in standard chase camera at highway speed.
- [ ] No volumetric banding/pixel crawl in dawn/dusk shots.
- [ ] No texture streaming stalls on common route stress tests.
- [ ] No obvious LOD popping within primary driving cone.
- [ ] No TAA ghosting trails exceeding 3 frames on high-contrast moving objects.
- [ ] No overbloom clipping in nighttime emissive-heavy zones.

### Cross-Tier Validation
- [ ] Ultra/High/Medium/Low presets produce deterministic output from fixed seeds and captures.
- [ ] Gameplay readability retained at Low (road edges, signs, lane markings, obstacles).
- [ ] Performance and visual captures archived per build for comparison.
