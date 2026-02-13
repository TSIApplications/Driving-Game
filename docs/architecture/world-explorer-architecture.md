# World Explorer Architecture Specification

## 1) Engine Selection

### Recommendation: **Unreal Engine 5 (World Partition + Chaos Physics)**

For a large-scale driving game with high terrain coverage and realism goals, Unreal Engine 5 is the recommended baseline.

#### Why Unreal Engine 5
- **Physics fidelity:** Chaos provides robust rigid-body simulation, suspension modeling support, tire-force integration options (native and plugin-driven), and deterministic-enough behavior for replay validation with controlled settings.
- **Terrain streaming at scale:** World Partition, Data Layers, One File Per Actor, and built-in HLOD workflows are mature for open-world streaming.
- **Tooling:** Strong editor profiling suite (Unreal Insights, Stat commands), landscape tools, foliage systems, PCG framework, cinematic tooling, and packaging support for large projects.

#### Considered Alternative: Unity HDRP
Unity HDRP + DOTS streaming can be viable, especially with custom stack ownership, but would typically require additional engineering to match UE5’s out-of-the-box open-world partitioning and mature HLOD/landscape workflows.

---

## 2) Modular Runtime Systems

Architecture follows a **module-oriented, data-driven, service-locator + event-bus hybrid** pattern.

### 2.1 Vehicle Physics System
**Responsibilities**
- Vehicle dynamics simulation (engine, transmission, differential, suspension, tire model).
- Surface-aware traction and damage/wear modifiers.
- Input abstraction (keyboard/controller/wheel) and assists (ABS, TCS, stability).

**Key modules**
- `VehicleCoreComponent`
- `PowertrainModel`
- `TireAndSurfaceModel`
- `AssistController`
- `VehicleReplicationAdapter` (if multiplayer/ghosts later)

**Data sources**
- Vehicle config assets (`VehicleSpec` DataAsset)
- Surface response table (`SurfacePhysicsProfile`)

### 2.2 Terrain Streaming System
**Responsibilities**
- Stream world chunks by player position, speed, and heading prediction.
- Maintain memory budget and enforce priority queues.

**Key modules**
- `ChunkStreamingCoordinator`
- `LODPolicyEvaluator`
- `MemoryBudgetController`
- `StreamingTelemetryChannel`

### 2.3 Map Manager
**Responsibilities**
- Country/region lifecycle, active map context, minimap/world map indexing.
- Points of interest registration and discovery state.

**Key modules**
- `WorldMapRegistry`
- `RegionActivationService`
- `POIIndex`

### 2.4 Mission System
**Responsibilities**
- Mission definitions, prerequisites, branching conditions, rewards.
- Trigger orchestration (location, speed, time, inventory/vehicle state).

**Key modules**
- `MissionDefinitionStore`
- `MissionRuntimeStateMachine`
- `ObjectiveEvaluator`
- `RewardDistributor`

### 2.5 AI Traffic / Pedestrians
**Scope strategy**
- **Phase 1:** Vehicle traffic only on primary roads.
- **Phase 2 (optional):** Pedestrians in high-density zones.

**Key modules**
- `TrafficSpawner`
- `LaneGraphNavigator`
- `TrafficBehaviorController`
- `CrowdZoneController` (optional)

### 2.6 Save/Profile System
**Responsibilities**
- Player progression, discovered landmarks, mission state, preferences.
- Versioned save schema with migration pipeline.

**Key modules**
- `SaveGameSerializer`
- `ProfileRepository`
- `SaveMigrationService`
- `CloudSyncAdapter` (optional)

---

## 3) Data-Driven Content Pipeline

Use manifests as the source of truth for world composition and content registration.

### 3.1 Manifest approach
Depending on engine conventions:
- **Unreal:** DataAssets + JSON import/export for external authoring.
- **Unity alternative:** ScriptableObjects + JSON mirror for build-time validation.

### 3.2 Country/Map manifest schema
Example (`CountryManifest.json`):

```json
{
  "countryId": "it",
  "displayNameKey": "country.it.name",
  "version": "1.2.0",
  "regions": [
    {
      "regionId": "it_tuscany",
      "bounds": { "min": [0,0], "max": [51200,51200] },
      "chunkSet": "chunks/it_tuscany",
      "biomeProfile": "mediterranean_hills"
    }
  ],
  "roadGraph": "nav/it_roads_v3",
  "landmarkManifest": "landmarks/it_landmarks_v5",
  "missionPack": "missions/it_pack_main"
}
```

### 3.3 Pipeline stages
1. **Authoring:** Designers update map/landmark/mission assets.
2. **Validation:** CI schema validation, reference checks, memory budget rules.
3. **Build prep:** Generate streaming chunk tables, HLOD manifests, nav partitions.
4. **Packaging:** Bundle by country/region for optional DLC deployment.

---

## 4) Landmark Prefab Schema

Each landmark should be represented with a standardized prefab/actor schema.

### 4.1 Required fields
- `landmarkId` (stable GUID/string)
- `category` (natural, cultural, urban, challenge, hidden)
- `transform` (world placement)
- `meshSet` (high/mid/low LOD refs)
- `collisionProfile` (simple/complex and gameplay channels)
- `discoveryTrigger` (radius/volume + rules)
- `metadata` (historical info, tags, difficulty, photo spots)
- `localizationKeys` (`nameKey`, `descriptionKey`, `subtitleKey`)

### 4.2 Optional fields
- `audioZoneRef`
- `missionHooks`
- `photoModeAnchors`
- `unlockConditions`

### 4.3 Example schema (conceptual)

```json
{
  "landmarkId": "lm_colosseum",
  "category": "cultural",
  "lod": {
    "lod0": "SM_Colosseum_High",
    "lod1": "SM_Colosseum_Mid",
    "lod2": "SM_Colosseum_Low",
    "impostor": "IMP_Colosseum"
  },
  "collision": {
    "type": "simple+complex",
    "channel": "WorldStatic"
  },
  "discoveryTrigger": {
    "shape": "sphere",
    "radius": 150.0,
    "requiresLineOfSight": true,
    "minSpeedKph": 0
  },
  "metadata": {
    "tags": ["rome", "history", "tourist"],
    "score": 250
  },
  "localization": {
    "nameKey": "landmark.colosseum.name",
    "descriptionKey": "landmark.colosseum.desc"
  }
}
```

---

## 5) Asynchronous Loading Strategy

### 5.1 Chunk streaming
- Divide world into fixed-size streaming cells (e.g., 256m–1024m based on density).
- Maintain concentric priority rings around player:
  - **Ring A:** Immediate gameplay-critical cells.
  - **Ring B:** Near visual continuity cells.
  - **Ring C:** Prefetch cells based on heading and velocity.

### 5.2 Impostors + HLOD
- Generate impostors for distant landmarks and dense city blocks.
- Use HLOD cluster generation per region with aggressive merge rules for far distance.
- Swap thresholds tuned per platform profile.

### 5.3 Occlusion culling
- Hardware occlusion for urban scenes.
- Precomputed visibility sets for dense static zones where beneficial.
- Avoid over-culling pop-in by adding hysteresis on visibility transitions.

### 5.4 Async I/O and decompression
- Use non-blocking asset load requests with strict main-thread budget caps.
- Stage loads: metadata -> low LOD -> full quality.
- Background decompression workers with QoS priority by distance and mission relevance.

---

## 6) Backend / Services Strategy

### Offline-first default
Primary architecture should function entirely offline:
- Full single-player progression
- Save/load and discovery systems
- Mission progression
- Local profile stats

### Optional online services (feature flags)
- **Leaderboards:** time trials, route records
- **Telemetry:** performance + gameplay analytics (opt-in)
- **DLC updates:** manifest-driven region/content add-ons

All online integrations should be isolated behind service interfaces:
- `ILeaderboardService`
- `ITelemetryService`
- `IContentUpdateService`

If network is unavailable, game remains fully functional with graceful degradation.

---

## 7) Risk Matrix + Low-End Fallbacks

| Risk | Impact | Likelihood | Detection | Mitigation | Low-End Fallback |
|---|---|---|---|---|---|
| CPU overload from traffic + physics | High | Medium | Frame-time spikes (>16.6/33.3 ms) | Budgeted AI ticks, distance-based update rates | Reduce traffic density, disable pedestrian simulation |
| GPU overload in dense cities | High | High | GPU frame-time telemetry | Aggressive HLOD/impostor usage, material simplification | Lower shadow cascades, disable SSR/volumetrics |
| Streaming stalls (I/O saturation) | High | Medium | Asset load queue latency, hitch metrics | Priority prefetch + background decompression | Increase preload radius for low-speed mode, lock max speed temporarily on weak devices |
| Memory budget overflow | High | Medium | Runtime memory watermark alerts | Strict per-ring budget and eviction policy | Force lower texture pool + shorter view distance |
| Save schema breakage after updates | Medium | Low | Migration test failures | Versioned schema + automatic migration tests | Read-only recovery mode with backup save restore |
| Nav/AI path failures in streamed regions | Medium | Medium | AI stuck detectors | Region-based nav validation in CI | Spawn suppression in invalid zones |

### Platform profile tiers
- **Tier 0 (Low-end):** 30 FPS target, reduced traffic, low foliage density, lower draw distance, simplified physics assists.
- **Tier 1 (Mid):** 60 FPS target, balanced traffic and effects.
- **Tier 2 (High):** 60+ FPS target, full-density traffic, highest LOD distance.

### Runtime adaptive controls
- Dynamic quality scaler for shadows, post-process, and traffic density.
- Emergency hitch guard: temporarily freeze non-critical spawn systems during sustained stalls.

---

## Implementation Notes / Next Steps
1. Finalize engine decision checkpoint with prototype benchmarks (physics stress, city streaming, memory).
2. Implement manifest schema validator in CI.
3. Build vertical slice: one country, two regions, 50 landmarks, basic mission chain.
4. Collect performance telemetry across Tier 0/1/2 and tune LOD/streaming thresholds.
