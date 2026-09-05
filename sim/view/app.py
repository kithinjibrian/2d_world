"""The window and the event loop.

Thin by design. All the coordinate work is in sim.view.camera, all the
dispatch is in sim.view.scene, and both are pure and tested headless. What is
left here is SDL setup, key handling, and a frame loop -- little enough to be
checked by reading.

Controls
--------
    drag            pan; on the ground, walks along it and changes height
    scroll / + -    zoom about the cursor, on the ground too
    arrow keys      pan; left/right walks along the ground when zoomed in
    [ ]             step along Vellum's orbit
    space           run or pause time -- watch the world turn
    f               follow Vellum (default) or hold position
    home            reframe the whole system
    esc / q         quit

The window is resizable, and opens at most of the desktop.

Axioms used: none. The viewer computes no physics.
Abstracts: nothing directly.

Depends on: pygame, sim.orbit, sim.star, sim.view.*
Used by: run as ``python -m sim.view.app``
"""

from __future__ import annotations

import numpy as np
import pygame

from sim.orbit import Trajectory, circular_speed, integrate
from sim.rotation import Spin, breakup_rate
from sim.star import Kell
from sim.surface import Terrain
from sim.units import LENGTH, LUMINOSITY, MASS, TIME, VELOCITY, Quantity
from sim.view.bands import ScaleBand
from sim.view.camera import Camera
from sim.view.geometry import Disc
from sim.view.render import OrbitTrace, PlanetDisc, ScaleBar, StarDisc, TerrainTrace
from sim.view.scene import Scene

__all__ = ["main", "run"]

_BACKGROUND = (14, 18, 16)
_ZOOM_STEP = 1.25
_PAN_FRACTION = 0.08
_TIMESTEP = 2e-3
_MIN_WIDTH = 960
_MIN_HEIGHT = 600


def _demo_world() -> tuple[Kell, Trajectory, Disc, Terrain, Spin]:
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
        # Enough octaves that terrain still has detail throughout the GROUND
        # band. At 22 the resolution floor sat above the whole band, so the
        # closest zoom showed invented smoothness.
        octaves=34,
    )
    # WORLD CONSTANT: a rotation rate, about a third of breakup, giving
    # roughly a hundred days to the orbit. Not derived -- see DECISION on the
    # rotation layer and docs/AXIOMS.md section 4.
    mass = Quantity(3.0e-6, MASS)
    spin = Spin(rate=100.0, circumference=planet.circumference, mass=mass)
    assert spin.rate < breakup_rate(mass, planet.circumference)
    return star, trajectory, planet, terrain, spin


def _default_size() -> tuple[int, int]:
    """Return a window size filling most of the desktop.

    Queried rather than hardcoded: a fixed 1280x800 is a postage stamp on a
    large display and does not fit a small one.
    """
    info = pygame.display.Info()
    width = max(_MIN_WIDTH, int(info.current_w * 0.88))
    height = max(_MIN_HEIGHT, int(info.current_h * 0.82))
    return width, height


def run(width: int | None = None, height: int | None = None) -> None:
    """Open the window and run until the user quits."""
    pygame.init()
    pygame.display.set_caption("Vellum")
    if width is None or height is None:
        width, height = _default_size()
    surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    star, trajectory, planet, terrain, spin = _demo_world()
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
    #: Where on the closed surface the camera sits once zoomed past the planet.
    anchor = 0.0
    #: Height above that point. Dragging vertically on the ground changes it.
    anchor_height = 0.0
    dragging = False
    #: Whether time advances on its own. Watching the world turn needs it.
    running_clock = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode(
                    (event.w, event.h), pygame.RESIZABLE
                )
                camera = camera.resized(event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 2):
                dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button in (1, 2):
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                camera, following, anchor, anchor_height = _on_drag(
                    camera, planet, following, anchor, anchor_height,
                    float(event.rel[0]), float(event.rel[1]),
                )
            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                camera, anchor, anchor_height = _on_zoom(
                    camera, planet, following, anchor, anchor_height,
                    _ZOOM_STEP**event.y, float(mx), float(my),
                )
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
                # Some setups still deliver the wheel as legacy button presses.
                mx, my = pygame.mouse.get_pos()
                camera, anchor, anchor_height = _on_zoom(
                    camera, planet, following, anchor, anchor_height,
                    _ZOOM_STEP if event.button == 4 else 1.0 / _ZOOM_STEP,
                    float(mx), float(my),
                )
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running_clock = not running_clock
            elif event.type == pygame.KEYDOWN:
                camera, step, following, running, anchor = _on_key(
                    event.key, camera, step, following, running, planet, width, anchor
                )

        if running_clock:
            step += 1
        # The planet moves along its orbit; the viewer only reads the state.
        position = trajectory.positions[step % len(trajectory.positions)]
        planet = Disc(
            centre_x=float(position[0]),
            centre_y=float(position[1]),
            circumference=planet.circumference,
        )
        scene = _rebuild(
            star, trajectory, planet, terrain, spin, step * _TIMESTEP, running_clock
        )
        looking = _camera_for(camera, planet, following, anchor, anchor_height)

        surface.fill(_BACKGROUND)
        scene.draw(looking, surface)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def _on_drag(
    camera: Camera,
    planet: Disc,
    following: bool,
    anchor: float,
    anchor_height: float,
    rel_x: float,
    rel_y: float,
) -> tuple[Camera, bool, float, float]:
    """Handle one drag step. Returns (camera, following, anchor, height).

    Two regimes, because one behaviour cannot serve both:

    **Following, zoomed in past the planet** — a horizontal drag walks along
    the ground and a vertical drag changes height above it. Free-panning here
    would leave the planet within a few pixels of travel and show empty space,
    which is the same failure as centring on the planet's centre. Walking wraps,
    because the surface has no edge.

    **Otherwise** — the camera pans and following is dropped. It has to be
    dropped: with follow on, the camera is re-centred every frame and a drag
    would move the pointer while the view stayed put.

    The sign convention is that whatever is under the pointer stays under it.
    """
    metres = camera.metres_per_pixel
    on_the_ground = following and camera.span <= planet.circumference

    if on_the_ground:
        # Screen y grows downward, so dragging down raises the viewpoint.
        return (
            camera,
            True,
            (anchor - rel_x * metres) % planet.circumference,
            max(0.0, anchor_height + rel_y * metres),
        )

    return (
        camera.panned(-rel_x * metres, rel_y * metres),
        False,
        anchor,
        anchor_height,
    )


def _on_zoom(
    camera: Camera,
    planet: Disc,
    following: bool,
    anchor: float,
    anchor_height: float,
    factor: float,
    cursor_x: float,
    cursor_y: float,
) -> tuple[Camera, float, float]:
    """Zoom about the cursor. Returns (camera, anchor, height).

    Away from the surface this is ``Camera.zoomed_about``. On the ground it
    cannot be: following re-centres the camera every frame, so moving the focus
    is undone before it is ever drawn -- which is why every scroll zoomed to the
    middle of the window regardless of where the pointer was. The analogue is to
    move the *anchor* so the surface point under the cursor stays under it.

    That works because the camera is rolled to local vertical on the ground, so
    screen x runs along the surface and screen y runs away from it.
    """
    zoomed = camera.zoomed(factor)
    if not (following and camera.span <= planet.circumference):
        return camera.zoomed_about(factor, cursor_x, cursor_y), anchor, anchor_height

    along = cursor_x - camera.width * 0.5
    away = camera.height * 0.5 - cursor_y
    before_metres = camera.metres_per_pixel
    after_metres = zoomed.metres_per_pixel

    surface_under_cursor = anchor + along * before_metres
    height_under_cursor = anchor_height + away * before_metres
    return (
        zoomed,
        (surface_under_cursor - along * after_metres) % planet.circumference,
        max(0.0, height_under_cursor - away * after_metres),
    )


def _camera_for(
    camera: Camera,
    planet: Disc,
    following: bool,
    anchor: float,
    anchor_height: float = 0.0,
) -> Camera:
    """Return where the camera should actually be looking this frame.

    While the whole planet fits in the viewport, centring on its centre is
    right. Once it does not, centring on the centre puts the camera *inside*
    the world with the ground far off-screen, so the focus moves to a point on
    the surface instead. Pure, so the transition is testable without a display.
    """
    if not following:
        return camera
    if camera.band is ScaleBand.SYSTEM:
        # Do not chase the planet while the whole system is in view. Following
        # a body that is orbiting drags the entire background across the window
        # -- the star slides past and the system appears to move. At this scale
        # the system is the subject and the planet is the thing moving in it.
        return camera
    if camera.span > planet.circumference:
        return camera.focused_on(planet.centre_x, planet.centre_y)
    return camera.focused_on_surface(planet, anchor, anchor_height).aligned_to_surface(
        planet, anchor
    )


def _rebuild(
    star: Kell,
    trajectory: Trajectory,
    planet: Disc,
    terrain: Terrain,
    spin: Spin | None = None,
    time: float = 0.0,
    clock_running: bool = True,
) -> Scene:
    scene = Scene()
    scene.add(StarDisc(star))
    scene.add(OrbitTrace(trajectory))
    scene.add(PlanetDisc(planet))
    ground = TerrainTrace(planet, terrain, spin=spin)
    ground.time = time
    scene.add(ground)
    bar = ScaleBar(terrain, spin)
    bar.time = time
    bar.clock_running = clock_running
    scene.add(bar)
    return scene


def _on_key(
    key: int,
    camera: Camera,
    step: int,
    following: bool,
    running: bool,
    planet: Disc,
    width: int,
    anchor: float,
) -> tuple[Camera, int, bool, bool, float]:
    """Handle one key press. Returns the new state."""
    pan = camera.width * _PAN_FRACTION * camera.metres_per_pixel
    if key in (pygame.K_ESCAPE, pygame.K_q):
        return camera, step, following, False, anchor
    if key in (pygame.K_PLUS, pygame.K_EQUALS):
        return camera.zoomed(_ZOOM_STEP), step, following, running, anchor
    if key == pygame.K_MINUS:
        return camera.zoomed(1.0 / _ZOOM_STEP), step, following, running, anchor
    if key in (pygame.K_LEFT, pygame.K_RIGHT):
        direction = -1.0 if key == pygame.K_LEFT else 1.0
        if following and camera.span <= planet.circumference:
            # Walking along the ground. Wraps, because the surface has no edge.
            return camera, step, following, running, anchor + direction * pan
        return camera.panned(direction * pan, 0.0), step, False, running, anchor
    if key == pygame.K_UP:
        return camera.panned(0.0, pan), step, False, running, anchor
    if key == pygame.K_DOWN:
        return camera.panned(0.0, -pan), step, False, running, anchor
    if key == pygame.K_LEFTBRACKET:
        return camera, step - 200, following, running, anchor
    if key == pygame.K_RIGHTBRACKET:
        return camera, step + 200, following, running, anchor
    if key == pygame.K_f:
        return camera, step, not following, running, anchor
    if key == pygame.K_HOME:
        return (
            Camera(0.0, 0.0, width / 6.0, camera.width, camera.height, camera.reference_length),
            step,
            False,
            running,
            anchor,
        )
    return camera, step, following, running, anchor


def main() -> None:
    """Entry point for ``python -m sim.view.app``."""
    run()


if __name__ == "__main__":
    main()
