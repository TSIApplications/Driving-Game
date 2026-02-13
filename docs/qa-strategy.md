# QA Strategy

## Scope and Objectives
This document defines the quality strategy for the Driving Game, with a focus on deterministic content validation, gameplay stability, performance consistency, compatibility, and localization readiness.

## 1) Test Pyramid

### Unit Tests (broadest layer)
Primary target: fast, deterministic checks of gameplay math and physics helpers.

- Validate acceleration, braking, and steering helper functions.
- Verify collision response utility math (impulse, damping, restitution).
- Assert waypoint distance/heading calculations and mission scoring formulas.
- Run on every commit and pull request.

### Integration Tests (middle layer)
Primary target: subsystem boundaries and content wiring.

- Map loading tests for all shipping map assets.
- Mission trigger tests for start/complete/fail conditions.
- Save/load transition checks between map and mission states.
- Run on every pull request and nightly.

### Automated Soak Tests (top layer)
Primary target: long-running stability of world streaming and runtime systems.

- 2h, 6h, and 12h unattended drive loops across multiple map regions.
- Stress continuous asset streaming while forcing camera and vehicle traversal patterns.
- Capture crashes, memory growth, streaming hitch counts, and mission event dropouts.
- Run nightly (2h) and weekly (6h/12h).

## 2) Deterministic Map Validation Test
Add a deterministic content validation test suite (`map_validation_deterministic`) with fixed seed and strict assertions:

- Assert exactly **195 maps present** in the build manifest.
- Assert every map contains **>= 5 landmarks**.
- Fail with explicit map IDs for violations.
- Gate all content merges and release branches.

Example acceptance checks:

- `assert_eq!(map_count, 195)`
- `assert!(all_maps.iter().all(|m| m.landmarks.len() >= 5))`

## 3) Performance Test Suite
Implement an automated performance suite that runs per quality tier (Low/Medium/High/Ultra) and target platform profile.

### Metrics
- **Frame time**: average, P95, P99, max spike count.
- **Memory**: baseline footprint, peak usage, leak trend over 60 minutes.
- **Load durations**: cold boot to menu, map load, mission start/restart.

### Execution
- Standardized benchmark routes and camera paths.
- Fixed weather/time-of-day presets to reduce variance.
- Three-run median aggregation per scenario.

### Suggested pass targets (to be finalized with engineering)
- Frame time P95 under budget for target FPS tier.
- No unbounded memory growth in 60-minute run.
- Map and mission load durations under per-platform thresholds.

## 4) Compatibility Matrix
Maintain a compatibility matrix with explicit pass/fail/known-issue status.

### OS
- Windows 10/11
- Ubuntu LTS (if supported)
- SteamOS (if supported)

### GPU tiers
- Minimum spec GPU
- Recommended spec GPU
- High-end GPU

### Controllers/Input
- Keyboard + mouse
- Xbox controller
- PlayStation controller
- Generic XInput/DirectInput-compatible pads

For each combination, track:

- Launch success
- Input mapping correctness
- Performance tier achieved
- Blocking defects and workarounds

## 5) Localization QA
Localization QA covers country names, landmark labels, and mission text in all supported locales.

### Checks
- Terminology consistency (country naming conventions per locale).
- Landmark label length/overflow and UI clipping.
- Mission text grammar, context, and variable substitution correctness.
- Font fallback and glyph coverage (including diacritics and non-Latin scripts where applicable).
- Right-to-left layout validation if RTL locales are supported.

### Process
- Automated string key completeness check before string freeze.
- Linguistic QA pass by native or certified reviewers.
- In-context screenshot review for high-risk UI panels.

## Reporting and Ownership
- QA owns test execution status and defect triage.
- Engineering owns fixes and regression test updates.
- Production owns milestone readiness reviews based on this strategy.
