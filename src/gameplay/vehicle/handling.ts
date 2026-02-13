export type DriveLayout = "FWD" | "RWD" | "AWD";

export interface SuspensionSetup {
  travelMeters: number;
  springRateNPerM: number;
  dampingCompressionNsPerM: number;
  dampingReboundNsPerM: number;
  antiRollStiffness: number;
}

export interface TireFrictionCurvePoint {
  slipRatio: number;
  longitudinalGrip: number;
  lateralGrip: number;
}

export interface TireCompoundModel {
  name: string;
  curve: TireFrictionCurvePoint[];
  peakTemperatureC: number;
  wearRate: number;
}

export interface DrivetrainTorqueBand {
  rpm: number;
  torqueNm: number;
}

export interface DrivetrainSetup {
  layout: DriveLayout;
  torqueCurve: DrivetrainTorqueBand[];
  finalDriveRatio: number;
  gearRatios: number[];
  limitedSlipBias: number;
}

export interface CenterOfMassBehavior {
  baseHeightMeters: number;
  longitudinalBias: number;
  lateralBias: number;
  pitchTransferGain: number;
  rollTransferGain: number;
}

export interface HandlingModel {
  id: string;
  suspension: {
    front: SuspensionSetup;
    rear: SuspensionSetup;
  };
  tire: TireCompoundModel;
  drivetrain: DrivetrainSetup;
  centerOfMass: CenterOfMassBehavior;
}

export const sportSedanHandling: HandlingModel = {
  id: "sport-sedan-v1",
  suspension: {
    front: {
      travelMeters: 0.21,
      springRateNPerM: 46500,
      dampingCompressionNsPerM: 3800,
      dampingReboundNsPerM: 5200,
      antiRollStiffness: 1.18,
    },
    rear: {
      travelMeters: 0.23,
      springRateNPerM: 42000,
      dampingCompressionNsPerM: 3400,
      dampingReboundNsPerM: 5000,
      antiRollStiffness: 1.05,
    },
  },
  tire: {
    name: "road-sport",
    peakTemperatureC: 84,
    wearRate: 0.013,
    curve: [
      { slipRatio: 0, longitudinalGrip: 0.3, lateralGrip: 0.32 },
      { slipRatio: 0.04, longitudinalGrip: 0.9, lateralGrip: 0.85 },
      { slipRatio: 0.1, longitudinalGrip: 1.12, lateralGrip: 1.06 },
      { slipRatio: 0.16, longitudinalGrip: 1.04, lateralGrip: 0.99 },
      { slipRatio: 0.24, longitudinalGrip: 0.87, lateralGrip: 0.82 },
    ],
  },
  drivetrain: {
    layout: "AWD",
    finalDriveRatio: 3.92,
    gearRatios: [3.22, 2.08, 1.46, 1.12, 0.9, 0.74],
    limitedSlipBias: 2.7,
    torqueCurve: [
      { rpm: 1000, torqueNm: 215 },
      { rpm: 2000, torqueNm: 298 },
      { rpm: 3000, torqueNm: 355 },
      { rpm: 4300, torqueNm: 388 },
      { rpm: 5400, torqueNm: 360 },
      { rpm: 6500, torqueNm: 332 },
    ],
  },
  centerOfMass: {
    baseHeightMeters: 0.46,
    longitudinalBias: -0.05,
    lateralBias: 0,
    pitchTransferGain: 0.63,
    rollTransferGain: 0.71,
  },
};
