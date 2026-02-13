from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pygame

from world_explorer.map_loader import MapLoader
from world_explorer.physics import CarState, ControlState, DrivingPhysics

WINDOW_W = 1280
WINDOW_H = 720
TERRAIN_GRIP = {
    "desert": 0.7,
    "forest": 0.9,
    "mountain": 0.8,
    "coastal": 0.95,
    "urban": 1.0,
    "plains": 0.92,
}
TERRAIN_COLOR = {
    "desert": (214, 184, 122),
    "forest": (84, 134, 88),
    "mountain": (110, 110, 115),
    "coastal": (140, 196, 225),
    "urban": (130, 130, 130),
    "plains": (156, 186, 117),
}


def run() -> None:
    parser = argparse.ArgumentParser(description="World Explorer prototype")
    parser.add_argument("--country", default="Canada", help="Country map name from data/countries.txt")
    parser.add_argument("--maps-root", default="maps", help="Path to generated maps folder")
    args = parser.parse_args()

    loader = MapLoader(Path(args.maps_root))
    country_map = loader.load(args.country)

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(f"World Explorer - {country_map.country}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22)

    car = CarState(x=country_map.spawn[0], y=country_map.spawn[1])
    physics = DrivingPhysics()

    running = True
    while running:
        dt = min(clock.tick(60) / 1000.0, 0.05)
        controls = ControlState()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        controls.throttle = 1.0 if keys[pygame.K_w] or keys[pygame.K_UP] else 0.0
        controls.brake = 1.0 if keys[pygame.K_s] or keys[pygame.K_DOWN] else 0.0
        controls.steer = float((keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT]))

        grip = TERRAIN_GRIP.get(country_map.terrain, 0.9)
        car = physics.step(car, controls, dt, terrain_grip=grip)

        screen.fill(TERRAIN_COLOR.get(country_map.terrain, (100, 100, 100)))

        for landmark in country_map.landmarks:
            pygame.draw.circle(screen, (240, 80, 60), (int(landmark["x"]), int(landmark["y"])), 10)

        car_rect = pygame.Rect(0, 0, 42, 24)
        car_rect.center = (int(car.x), int(car.y))
        pygame.draw.rect(screen, (20, 20, 20), car_rect, border_radius=4)

        hud = font.render(
            f"{country_map.country} | Terrain: {country_map.terrain} | Speed: {car.velocity:.1f} | WASD/Arrows",
            True,
            (255, 255, 255),
        )
        screen.blit(hud, (18, 14))
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
