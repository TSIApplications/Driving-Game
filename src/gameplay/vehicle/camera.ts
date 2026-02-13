export type CameraMode = "chase" | "hood" | "cinematic-replay";

export interface CameraSmoothing {
  positionLerp: number;
  rotationLerp: number;
  velocityLead: number;
}

export interface CollisionAvoidance {
  sphereRadiusMeters: number;
  minDistanceMeters: number;
  maxDistanceMeters: number;
  wallSoftness: number;
}

export interface CameraProfile {
  mode: CameraMode;
  fovDegrees: number;
  offset: { x: number; y: number; z: number };
  lookAtOffset: { x: number; y: number; z: number };
  smoothing: CameraSmoothing;
  collision: CollisionAvoidance;
}

export const chaseCam: CameraProfile = {
  mode: "chase",
  fovDegrees: 76,
  offset: { x: 0, y: 1.6, z: -5.2 },
  lookAtOffset: { x: 0, y: 1, z: 4 },
  smoothing: {
    positionLerp: 0.16,
    rotationLerp: 0.18,
    velocityLead: 0.55,
  },
  collision: {
    sphereRadiusMeters: 0.4,
    minDistanceMeters: 1.7,
    maxDistanceMeters: 5.8,
    wallSoftness: 0.22,
  },
};

export const hoodCam: CameraProfile = {
  mode: "hood",
  fovDegrees: 84,
  offset: { x: 0, y: 1.25, z: 1.8 },
  lookAtOffset: { x: 0, y: 1.1, z: 16 },
  smoothing: {
    positionLerp: 0.25,
    rotationLerp: 0.22,
    velocityLead: 0.2,
  },
  collision: {
    sphereRadiusMeters: 0.2,
    minDistanceMeters: 0.1,
    maxDistanceMeters: 0.8,
    wallSoftness: 0.12,
  },
};

export const cinematicReplayCam: CameraProfile = {
  mode: "cinematic-replay",
  fovDegrees: 68,
  offset: { x: 2.6, y: 2.1, z: -7.8 },
  lookAtOffset: { x: 0, y: 0.9, z: 2.2 },
  smoothing: {
    positionLerp: 0.08,
    rotationLerp: 0.11,
    velocityLead: 0.9,
  },
  collision: {
    sphereRadiusMeters: 0.6,
    minDistanceMeters: 2,
    maxDistanceMeters: 8.5,
    wallSoftness: 0.28,
  },
};
