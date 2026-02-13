export interface CollisionEvent {
  impulseN: number;
  relativeVelocityMps: number;
  otherBodyTag: string;
  timeMs: number;
}

export interface VehicleTelemetry {
  speedKph: number;
  slipAngleDeg: number;
  suspensionForceN: {
    frontLeft: number;
    frontRight: number;
    rearLeft: number;
    rearRight: number;
  };
  collisions: CollisionEvent[];
}

export interface DebugHudState {
  enabled: boolean;
  showGraphs: boolean;
  maxCollisionEvents: number;
}

export const defaultHudState: DebugHudState = {
  enabled: true,
  showGraphs: true,
  maxCollisionEvents: 6,
};

export function trimCollisionEvents(
  telemetry: VehicleTelemetry,
  maxEvents: number,
): VehicleTelemetry {
  return {
    ...telemetry,
    collisions: telemetry.collisions.slice(-maxEvents),
  };
}

export function formatTelemetry(telemetry: VehicleTelemetry): string[] {
  const lines = [
    `Speed: ${telemetry.speedKph.toFixed(1)} kph`,
    `Slip angle: ${telemetry.slipAngleDeg.toFixed(1)} deg`,
    `Suspension force (N): FL ${telemetry.suspensionForceN.frontLeft.toFixed(0)} | FR ${telemetry.suspensionForceN.frontRight.toFixed(0)} | RL ${telemetry.suspensionForceN.rearLeft.toFixed(0)} | RR ${telemetry.suspensionForceN.rearRight.toFixed(0)}`,
  ];

  const collisions = telemetry.collisions.map(
    (event) =>
      `Collision @${event.timeMs}ms: ${event.otherBodyTag} | impulse ${event.impulseN.toFixed(0)} N | relV ${event.relativeVelocityMps.toFixed(2)} m/s`,
  );

  return [...lines, ...collisions];
}
