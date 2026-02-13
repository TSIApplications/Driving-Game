export type InputDevice = "keyboard" | "controller";

export interface AxisResponse {
  deadzone: number;
  sensitivity: number;
  exponent: number;
  invert?: boolean;
}

export interface ControlProfile {
  id: string;
  device: InputDevice;
  steering: AxisResponse;
  throttle: AxisResponse;
  brake: AxisResponse;
  handbrake: AxisResponse;
  assists: {
    steeringFilterHz: number;
    throttleRampUpPerS: number;
    throttleRampDownPerS: number;
  };
}

export const keyboardProfile: ControlProfile = {
  id: "keyboard-default-v1",
  device: "keyboard",
  steering: { deadzone: 0, sensitivity: 1.05, exponent: 1.25 },
  throttle: { deadzone: 0, sensitivity: 1, exponent: 1.05 },
  brake: { deadzone: 0, sensitivity: 1, exponent: 1.08 },
  handbrake: { deadzone: 0, sensitivity: 1, exponent: 1 },
  assists: {
    steeringFilterHz: 10,
    throttleRampUpPerS: 5,
    throttleRampDownPerS: 8,
  },
};

export const controllerProfile: ControlProfile = {
  id: "controller-default-v1",
  device: "controller",
  steering: { deadzone: 0.1, sensitivity: 1.15, exponent: 1.8 },
  throttle: { deadzone: 0.06, sensitivity: 1.08, exponent: 1.4 },
  brake: { deadzone: 0.06, sensitivity: 1.1, exponent: 1.35 },
  handbrake: { deadzone: 0.08, sensitivity: 1, exponent: 1.2 },
  assists: {
    steeringFilterHz: 12,
    throttleRampUpPerS: 4,
    throttleRampDownPerS: 7,
  },
};

export function applyAxisResponse(rawInput: number, response: AxisResponse): number {
  const sign = Math.sign(rawInput);
  const magnitude = Math.abs(rawInput);

  if (magnitude <= response.deadzone) {
    return 0;
  }

  const normalized = (magnitude - response.deadzone) / (1 - response.deadzone);
  const curved = Math.pow(normalized, response.exponent) * response.sensitivity;
  const shaped = Math.min(1, Math.max(0, curved));
  const directional = sign * shaped;
  return response.invert ? -directional : directional;
}
