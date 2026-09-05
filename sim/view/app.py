"""The window and the event loop.

Thin by design. All the coordinate work is in sim.view.camera, all the
dispatch is in sim.view.scene, and both are pure and tested headless. What is
left here is SDL setup, key handling, and a frame loop -- little enough to be
checked by reading.

Controls
--------
    scroll / + -    zoom about the cursor
    arrow keys      pan
    [ ]             step along Vellum's orbit
    f               follow Vellum (default) or hold position
    home            reframe the whole system
    esc / q         quit

Axioms used: none. The viewer computes no physics.
Abstracts: nothing directly.

Depends on: pygame, sim.orbit, sim.star, sim.view.*
Used by: run as ``python -m sim.view.app``
"""

from __future__ import annotations

import numpy as np
import pygame

from sim.orbit import Trajectory, circular_speed, integrate
from sim.star import Kell
from sim.surface import Terrain
from sim.units import LENGTH, LUMINOSITY, MASS, TIME, VELOCITY, Quantity
from sim.view.camera import Camera
from sim.view.geometry import Disc
from sim.view.render import OrbitTrace, PlanetDisc, ScaleBar, StarDisc, TerrainTrace
from sim.view.scene import Scene

__all__ = ["main", "run"]

_BACKGROUND = (14, 18, 16)
_ZOOM_STEP = 1.25
_PAN_FRACTION = 0.08


def _demo_world() -> tuple[Kell, Trajectory, Disc, Terrain]:
    """Build the world there is to look at so far.

    A star, an orbit, a disc, and ground. Water, air and life do not exist
    yet; the viewer was built before them (DECISION-016) so each becomes
    visible the moment it lands, and terrain is the first to do so.

    The terrain's amplitude and roughness are **world constants, not derived**
    -- see docs/AXIOMS.md section 4.
    """
    star = Kell(mass=Quantity(1.0, MASS), luminosity=Quantity(1.0, LUMINOSITY))
    speed = circular_speed(star.mass, Quantity(1.0, LENGTH)).scalar(VELOCITY)
    trajectory = integrate(
        mass=star.mass,
        position=Quantity(np.array([1.0, 0.0]), LENGTH),
        velocity=Quantity(np.array([0.0, speed * 1.18]), VELOCITY),
        timestep=Quantity(2e-3, TIME),
        steps=60_000,
    )
    # A surface 3.84e-5 world units around: about a millionth of the orbit, so
    # zooming from the whole system to a stretch of ground spans the eleven
    # decades this viewer exists for.
    planet = Disc(centre_x=1.0, centre_y=0.0, circumference=3.84e-5)
    terrain = Terrain(
        circumference=planet.circumference,
        # WORLD CONSTANT: mountains about a thousandth of the world around.
        amplitude=planet.circumference * 8e-4,
        # WORLD CONSTANT: P(k) ~ k^-2, the fractional-Brownian default.
        roughness=2.0,
        seed=20260905,
        octaves=22,
    )
    return star, trajectory, planet, terrain


def run(width: int = 1280, height: int = 800) -> None:
    """Open the window and run until the user quits."""
    pygame.init()
    pygame.display.set_caption("Vellum")
    surface = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    star, trajectory, planet, terrain = _demo_world()
    scene = _rebuild(star, trajectory, planet, terrain)

    camera = Camera(
        focus_x=0.0,
        focus_y=0.0,
        scale=width / 6.0,
        width=width,
        height=height,
        reference_length=planet.circumference,
    )
    step = 0
    following = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                camera = camera.zoomed_about(_ZOOM_STEP**event.y, float(mx), float(my))
            elif event.type == pygame.KEYDOWN:
                camera, step, following, running = _on_key(
                    event.key, camera, step, following, running, trajectory, planet, width
                )

        # The planet moves along its orbit; the viewer only reads the state.
        position = trajectory.positions[step % len(trajectory.positions)]
        planet = Disc(
            centre_x=float(position[0]),
            centre_y=float(position[1]),
            circumference=planet.circumference,
        )
        scene = _rebuild(star, trajectory, planet, terrain)
        if following:
            camera = camera.focused_on(planet.centre_x, planet.centre_y)

        surface.fill(_BACKGROUND)
        scene.draw(camera, surface)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def _rebuild(
    star: Kell, trajectory: Trajectory, planet: Disc, terrain: Terrain
) -> Scene:
    scene = Scene()
    scene.add(StarDisc(star))
    scene.add(OrbitTrace(trajectory))
    scene.add(PlanetDisc(planet))
    scene.add(TerrainTrace(planet, terrain))
    scene.add(ScaleBar(terrain))
    return scene


def _on_key(
    key: int,
    camera: Camera,
    step: int,
    following: bool,
    running: bool,
    trajectory: Trajectory,
    planet: Disc,
    width: int,
) -> tuple[Camera, int, bool, bool]:
    pan = camera.width * _PAN_FRACTION * camera.metres_per_pixel
    if key in (pygame.K_ESCAPE, pygame.K_q):
        return camera, step, following, False
    if key in (pygame.K_PLUS, pygame.K_EQUALS):
        return camera.zoomed(_ZOOM_STEP), step, following, running
    if key == pygame.K_MINUS:
        return camera.zoomed(1.0 / _ZOOM_STEP), step, following, running
    if key == pygame.K_LEFT:
        return camera.panned(-pan, 0.0), step, False, running
    if key == pygame.K_RIGHT:
        return camera.panned(pan, 0.0), step, False, running
    if key == pygame.K_UP:
        return camera.panned(0.0, pan), step, False, running
    if key == pygame.K_DOWN:
        return camera.panned(0.0, -pan), step, False, running
    if key == pygame.K_LEFTBRACKET:
        return camera, step - 200, following, running
    if key == pygame.K_RIGHTBRACKET:
        return camera, step + 200, following, running
    if key == pygame.K_f:
        return camera, step, not following, running
    if key == pygame.K_HOME:
        return (
            Camera(0.0, 0.0, width / 6.0, camera.width, camera.height, camera.reference_length),
            step,
            False,
            running,
        )
    return camera, step, following, running


def main() -> None:
    """Entry point for ``python -m sim.view.app``."""
    run()


if __name__ == "__main__":
    main()
