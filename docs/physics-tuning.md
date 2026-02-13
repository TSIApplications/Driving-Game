# Physics Tuning Baseline

This document captures iterative tuning outcomes for handling, traction, control response, and camera behavior. Values below are the locked baseline for `sport-sedan-v1` unless explicitly superseded.

## Iterative tuning sessions

| Session | Focus | Track/Surface | Key changes | Outcome vs target feel |
| --- | --- | --- | --- | --- |
| S1 | Core suspension + COM | Dry handling loop (asphalt) | Front travel from 0.19 -> 0.21 m; rear rebound +8%; roll transfer gain 0.68 -> 0.71 | Reduced snap oversteer at curb strikes, neutral mid-corner balance |
| S2 | Tire + terrain | Gravel split + mud shortcut | Gravel lateral grip 0.70 -> 0.74; mud rolling resistance 1.48 -> 1.60 | Predictable power slide on gravel, slower but controllable mud exits |
| S3 | Input profiles | Keyboard + gamepad slalom | Controller steering deadzone 0.08 -> 0.10; keyboard steering exponent 1.15 -> 1.25 | Better stick center stability and cleaner keyboard lane transitions |
| S4 | Camera comfort | Mixed elevation stage | Chase cam wall softness 0.18 -> 0.22; cinematic position lerp 0.10 -> 0.08 | Fewer camera pops near cliffs, smoother replay pacing |
| S5 | Braking/slope metrics | Wet descent + rock incline | Brake exponent 1.30 -> 1.35; COM pitch transfer 0.60 -> 0.63 | Better threshold-braking modulation and less uphill wheel-hop |

## Baseline parameters

### Handling and drivetrain

- Suspension travel: front `0.21 m`, rear `0.23 m`
- Tire friction peak near `slipRatio 0.10` at longitudinal `1.12`, lateral `1.06`
- Drivetrain: AWD, final drive `3.92`, LSD bias `2.7`
- Center of mass: height `0.46 m`, pitch transfer `0.63`, roll transfer `0.71`

### Input response

- Keyboard: no deadzone, steering sensitivity `1.05`, exponent `1.25`
- Controller: steering deadzone `0.10`, trigger deadzone `0.06`, steering exponent `1.8`

### Terrain traction scales

| Terrain | Longitudinal | Lateral | Rolling resistance |
| --- | --- | --- | --- |
| Asphalt | 1.00 | 1.00 | 1.00 |
| Gravel | 0.80 | 0.74 | 1.18 |
| Sand | 0.58 | 0.52 | 1.45 |
| Mud | 0.50 | 0.46 | 1.60 |
| Snow | 0.44 | 0.38 | 1.28 |

## Physics acceptance criteria (locked)

### Lap consistency

- On the benchmark asphalt loop, 5 consecutive clean laps must fall within **±1.8%** of the median lap time.
- Maximum single-lap deviation must remain under **2.4%**.

### Stopping distance bands

- From `100 kph` to `0` on dry asphalt: **37 m to 43 m**.
- From `80 kph` to `0` on gravel: **36 m to 44 m**.
- From `60 kph` to `0` on snow: **34 m to 43 m**.

### Slope climb thresholds

- Sustained climb in first gear on high-grip dirt: minimum **27°** grade without rollback.
- Short burst climb on rock/gravel mixed surface: minimum **31°** for at least **3.0 s**.
- On snow, maintain controlled ascent at **18°** with lateral slip under **8°**.

## Validation protocol

1. Warm tires with one out-lap and one braking pass.
2. Run benchmark sequence in fixed weather and fuel state.
3. Capture telemetry HUD stream and export lap summary.
4. Compare against criteria above; if any metric drifts outside bounds, open a retuning task before release.
