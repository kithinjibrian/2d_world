## FEATURE: A window that zooms continuously from the whole Kell system down to Vellum's ground.

## OBJECTIVE

`sim/view/` opens a desktop window showing the simulation, and lets you zoom without limit between
two extremes: the whole system with Vellum's rosette orbit around Kell, and a stretch of ground a
few metres across. Panning along the surface wraps, because the surface is a closed curve with no
edge.

Done means the zoom gesture is continuous and precise across all eleven orders of magnitude, the
camera logic is fully tested without a display, and each future layer can add itself to the view by
implementing one small protocol.

This is a **skeleton** (DECISION-016). Today it draws Kell, the orbit, and Vellum as a bare disc,
because nothing below planetary scale exists yet. It is built first so that terrain, water and air
are visible the moment they land rather than afterwards.

## CONTEXT

- Starting state: `sim/units/`, `sim/orbit/`, `sim/star/` complete. No rendering code, no `World`
  aggregate, nothing below planetary scale.
- Ending state: `sim/view/` and `sim/tests/view/`; `pygame-ce` added to `pyproject.toml` and STACK.
- Related existing code: `sim/orbit/integrator.py` for `Trajectory`, `sim/star/kell.py` for `Kell`.
- Axioms this depends on: **T0.1** only. The viewer computes no physics — it draws what other layers
  produce, and a viewer that computes anything is a viewer that can disagree with the simulation.
- Abstracted layers this leans on: none directly, but everything it draws about the star rests on
  Kell's stubbed luminosity. Nothing in the view may be read as a physical result.
- New free parameters introduced: **none.** Camera state is presentation, not physics.
- Open decisions that block this: **none.** DECISION-017 (terrain representation) is raised by this
  work but blocks the *surface* layer, not the skeleton.

## IMPLEMENTATION REQUIREMENTS

### Must Do

- **Split pure from impure, and put almost everything in the pure half.**
  - `sim/view/camera.py` — focus, scale, transforms, wrapping, visible-range culling, scale bands.
    **Imports no pygame.** This is where the difficulty lives and where the tests go.
  - `sim/view/render.py` — thin drawing on a pygame surface. Thin enough to be obviously correct.
  - `sim/view/app.py` — window, event loop, input handling.

  A viewer is normally hard to test. Here it need not be: only the last two files touch a display.

- **Transform camera-relative, never absolute.** Screen position is
  `(world − focus) * scale + centre`, computed in float64, converted to pixels last. **Never**
  `world * scale`. At a focus 1e11 m from the origin, a metre of detail survives the relative form
  and is lost in the absolute one. This is the single requirement most likely to be quietly violated
  and it has a dedicated test.

- **Handle the closed surface.** Position along the surface is periodic with the world's
  circumference. Panning wraps; the visible arc may straddle the seam and must render as one
  continuous stretch. Surface position maps to the plane as `θ = 2πx/L`, `r = R + h` — one
  representation for both regimes, so the transition from "a straight-looking stretch of ground" to
  "a closed circle" needs no special case.

- **Define named scale bands** — system, planetary, regional, ground — with explicit boundaries in
  metres per pixel. Each drawable declares which bands it appears in. This is the level-of-detail
  story, and keeping it declarative means a new layer answers one question rather than editing the
  renderer.

- **Define a `Drawable` protocol** with the scale bands it appears in and a `draw(camera, target)`.
  Registration is a list. Do not build a scene graph, an event bus, or a plugin system — the cost of
  adding the fourth layer must be adding one class.

- **Cull with the sorted-order invariant.** When a layer holds bodies sorted by surface position,
  the visible set is two binary searches (`searchsorted`), not a scan and not a spatial index. The
  first law guarantees that order never changes; the viewer should be the first thing to exploit it.

- **Show the scale.** A readout of metres per pixel and a scale bar, always. Without it, eleven
  decades of zoom become disorienting within seconds.

- **Stay deterministic and read-only.** The viewer never mutates simulation state and never advances
  it as a side effect of drawing. If it animates, it steps an explicit clock.

### Must NOT Do

- **Do not compute physics.** No integrating, no deriving, no unit conversion beyond display
  formatting. A viewer that computes can disagree with the simulation, and then the picture is
  evidence of nothing.
- **Do not invent a `World` aggregate.** It will be needed eventually; inventing it now, from two
  layers, guesses at an interface that four unwritten layers have to live with. Take `Kell` and
  `Trajectory` directly.
- **Do not add terrain, water, atmosphere or life.** None exists. Draw Vellum as a bare disc and
  leave the hooks.
- **Do not use OpenGL, shaders, or any GPU path.** float32 in the pipeline defeats the precision
  requirement, which is the actual hard part of this feature.
- **No GUI toolkit, no panels, no widgets, no editing.** Keyboard and mouse only.
- **No screenshot, video export, or recording.** Later, with a PRP.
- **Do not put SI conversion anywhere but the display formatting.** Natural units everywhere else.

## DERIVATION CHECK

- [ ] Every quantity is an axiom, a world constant, or a derived result — the viewer introduces none
- [ ] No 3D constant or scaling law; no SI value outside display formatting
- [ ] Dimensions match `docs/AXIOMS.md` §2 wherever a physical quantity is displayed
- [ ] Nothing tuned to reproduce a monograph number
- [ ] Nothing that should emerge is hand-placed — the viewer draws, it does not decorate
- [ ] No new free parameter
- [ ] No abstracted layer leaned on, beyond noting that stellar appearance rests on a stubbed value
- [ ] No random source

New free parameters requiring human approval: **none.**

## ERROR HANDLING REQUIREMENTS

- A non-positive or non-finite zoom scale raises `ValueError`. Zoom is clamped to an explicit
  documented range rather than allowed to reach zero or infinity — and the clamp is a **stated
  limit**, not a silent correction: at the limit the camera reports that it is clamped.
- A non-finite focus raises. Do not repair it.
- A drawable declaring an empty set of scale bands raises at registration — it would silently never
  appear, which is the worst possible failure for a viewer.
- Rendering failures must not be swallowed. A layer that raises while drawing propagates; a viewer
  that quietly skips a broken layer shows a plausible picture of the wrong world.

## SECURITY CONSIDERATIONS

- No file read or written, no network, no deserialisation, no `pickle`, no `eval`.
- All input is keyboard and mouse events from SDL; no external data is parsed.
- No restricted category applies.

## TESTS TO WRITE

Written before implementation. All of these run **headless** — `camera.py` imports no pygame, and
what remains uses `SDL_VIDEODRIVER=dummy`.

**Dimensional:**
- [ ] Scale carries pixels per metre; the displayed readout matches the camera's actual scale
- [ ] Distances presented for display convert through `UnitSystem`, never by an ad-hoc factor

**Precision — the point of the feature:**
- [ ] **Two points one metre apart, viewed at ground zoom with the focus 1e11 m from the origin,
      land on different pixels.** This fails under an absolute transform and passes under a
      camera-relative one. It is the discriminating test, and the acceptance criteria require
      demonstrating that it fails when the transform is made absolute
- [ ] A round trip `screen_to_world(world_to_screen(p)) == p` holds to a stated tolerance at each
      scale band, including the extremes

**Invariant:**
- [ ] Wrapping: panning by exactly one circumference returns the identical view
- [ ] A visible arc straddling the seam yields one contiguous run of geometry, not two disjoint ones
- [ ] Zoom is monotone and reversible: `zoom_in` then `zoom_out` restores the scale exactly
- [ ] Zoom about a cursor keeps the world point under the cursor fixed, at every band
- [ ] Culling by two `searchsorted` calls returns exactly the bodies inside the arc — checked
      against a brute-force scan over random positions
- [ ] Scale bands partition the range with no gap and no overlap

**Behavioural:**
- [ ] A drawable is asked to draw only inside its declared bands
- [ ] Registering a drawable with no bands raises
- [ ] The camera reports when it is clamped at a zoom limit

**Regression:**
- [ ] A fixed camera state produces identical transform output across runs

**Error paths:**
- [ ] Each raise above has a test

## ROLLBACK PLAN

- Branch to return to: `main` at the orbit-layer commit.
- State the codebase should be in: no `sim/view/`, `pygame-ce` removed from `pyproject.toml` and
  STACK. `rm -rf sim/view sim/tests/view`.
- Anything irreversible: none.

## ACCEPTANCE CRITERIA

- [ ] Zooming from system scale to a few metres of ground is continuous, with no jump and no
      visible loss of precision at the fine end
- [ ] **Making the transform absolute rather than camera-relative makes the precision test fail —
      verified, not assumed**, as the units and orbit layers were mutation-checked
- [ ] Panning wraps seamlessly, including across the seam
- [ ] `camera.py` imports nothing from pygame — asserted by a test, as with the screening path
- [ ] The full suite runs headless in CI-like conditions with no display
- [ ] Derivation check fully ticked
- [ ] `pytest`, `mypy --strict sim/`, `ruff check sim/` all pass
- [ ] `pygame-ce` added to STACK in CLAUDE.md, and the list noted closed again
- [ ] No file over 300 lines
- [ ] CHANGELOG.md updated; CONTEXT.md session closed
- [ ] A short note in `docs/` or the module docstring recording how a future layer adds itself —
      one paragraph, not a manual

## VALIDATION

- `.venv/bin/pytest`
- `SDL_VIDEODRIVER=dummy .venv/bin/pytest` — the whole suite, headless
- `.venv/bin/mypy` and `.venv/bin/ruff check sim/`
- Run it and zoom by hand from the full orbit to a metre of ground. The precision requirement is
  the kind that passes its unit test and still looks wrong, so it must also be looked at.
