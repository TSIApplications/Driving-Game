export type TerrainType = "sand" | "asphalt" | "mud" | "snow" | "gravel";

export interface TerrainTractionModifier {
  terrain: TerrainType;
  longitudinalGripScale: number;
  lateralGripScale: number;
  rollingResistanceScale: number;
  wheelSlipDamping: number;
}

export const terrainTractionTable: Record<TerrainType, TerrainTractionModifier> = {
  asphalt: {
    terrain: "asphalt",
    longitudinalGripScale: 1,
    lateralGripScale: 1,
    rollingResistanceScale: 1,
    wheelSlipDamping: 0.95,
  },
  gravel: {
    terrain: "gravel",
    longitudinalGripScale: 0.8,
    lateralGripScale: 0.74,
    rollingResistanceScale: 1.18,
    wheelSlipDamping: 0.84,
  },
  sand: {
    terrain: "sand",
    longitudinalGripScale: 0.58,
    lateralGripScale: 0.52,
    rollingResistanceScale: 1.45,
    wheelSlipDamping: 0.78,
  },
  mud: {
    terrain: "mud",
    longitudinalGripScale: 0.5,
    lateralGripScale: 0.46,
    rollingResistanceScale: 1.6,
    wheelSlipDamping: 0.7,
  },
  snow: {
    terrain: "snow",
    longitudinalGripScale: 0.44,
    lateralGripScale: 0.38,
    rollingResistanceScale: 1.28,
    wheelSlipDamping: 0.66,
  },
};

export function getTerrainTraction(terrain: TerrainType): TerrainTractionModifier {
  return terrainTractionTable[terrain];
}
