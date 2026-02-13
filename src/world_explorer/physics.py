from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class ControlState:
    throttle: float = 0.0
    brake: float = 0.0
    steer: float = 0.0


@dataclass
class CarState:
    x: float
    y: float
    heading: float = 0.0
    velocity: float = 0.0


class DrivingPhysics:
    """Arcade-oriented physics tuned for responsive off-road handling on PC."""

    def __init__(self) -> None:
        self.max_speed = 62.0
        self.max_reverse_speed = -18.0
        self.engine_accel = 35.0
        self.brake_accel = 65.0
        self.drag = 4.0
        self.roll_resistance = 1.2
        self.steer_rate = 2.3
        self.grip = 6.0

    def step(self, car: CarState, controls: ControlState, dt: float, terrain_grip: float = 1.0) -> CarState:
        accel = controls.throttle * self.engine_accel
        if controls.brake > 0:
            accel -= controls.brake * self.brake_accel * (1 if car.velocity > 0 else -1)

        speed_sign = 1 if car.velocity >= 0 else -1
        drag_force = (self.drag * car.velocity * abs(car.velocity) * 0.01) + (self.roll_resistance * speed_sign)
        car.velocity += (accel - drag_force) * dt
        car.velocity = max(self.max_reverse_speed, min(self.max_speed, car.velocity))

        target_turn = controls.steer * self.steer_rate * max(0.2, min(1.0, abs(car.velocity) / self.max_speed))
        heading_delta = (target_turn * terrain_grip) * dt
        car.heading += heading_delta

        lateral_loss = max(0.1, min(1.0, terrain_grip * (self.grip / 6.0)))
        forward = car.velocity * lateral_loss
        car.x += math.cos(car.heading) * forward * dt * 10
        car.y += math.sin(car.heading) * forward * dt * 10
        return car
