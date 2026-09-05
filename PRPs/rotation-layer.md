## FEATURE: Vellum turns on itself, and therefore has a day.

## OBJECTIVE

`sim/rotation/` gives Vellum a spin: a rotation rate, a surface frame that turns relative to
inertial space, and the day that follows. Done means a point on the surface passes through daylight
and night as the world turns, insolation at that point depends on where it is and what time it is
rather than on orbital distance alone, and the viewer shows the lit arc.

Vellum currently revolves but does not rotate, so **no part of its surface ever faces away from
Kell**. There is no night anywhere on the world. This layer is what fixes that.

## CONTEXT

- Starting state: `sim/units/`, `sim/star/`, `sim/orbit/`, `sim/surface/`, `sim/view/` complete.
  Nothing anywhere in the simulation rotates.
- Ending state: `sim/rotation/`, `sim/tests/rotation/`, and a lit-arc drawable in the viewer.
- Related existing code: `sim/orbit/insolation.py` computes flux at the planet from distance alone —
  this layer makes it a function of surface position and time too. `sim/view/camera.py` already
  converts surface coordinates to world positions and will need the rotating frame.
- Axioms this depends on: **T0.1** (two dimensions), **T0.2** (Newtonian mechanics, conserved
  angular momentum), **T2.2** (radiation) for the insolation half.
- Abstracted layers this leans on: **Kell's luminosity**, as before — so absolute insolation values
  are consequences of a chosen parameter. The *geometry* of day and night is not: it follows from
  T0.1 and is a genuine result.
- New free parameters introduced: **the rotation rate**, a world constant. Requires approval.
- Open decisions that block this: **none.**

### What is derivable, and was checked before writing this

1. **Angular momentum is a signed scalar**, not a vector: there is no axis in the plane for it to
   point along. Already established in `sim/orbit/analysis.py`.
2. **The moment of inertia of a uniform disc is `MR²/2`** — verified by integration with a per-area
   density. Identical to the three-dimensional coefficient. Another case where 2D does *not* differ,
   and worth a test for the same reason kinematic viscosity has one.
3. **The terminator is two points, not a curve.** In three dimensions it is a great circle; here the
   surface is a closed curve, so day and night are two arcs meeting at two points.
4. **The lit fraction is `arccos(R/d)/π`**, tending to exactly one half for a distant star. At
   `d/R = 2` it is a third; at `d/R = 10`, 0.468.
5. **A 2D planet flies apart when its surface moves at orbital speed.** Breakup is
   `ω_max = √(G₂M)/R`, so the surface speed at breakup is `√(G₂M) = v_c` — and since circular speed
   in two dimensions is the same at every radius, that is the same speed as an orbit anywhere.
6. **Total intercepted power is `F·2R`** — the disc presents a cross-section of length `2R` — and
   integrating `F·cos(incidence)` over the lit arc gives exactly that. Verified numerically.
7. **There is no axial tilt**, because there is no axis to tilt in a plane. Seasons come from
   eccentricity alone, which `docs/AXIOMS.md` §3 already records.

## IMPLEMENTATION REQUIREMENTS

### Must Do

- **A rotation state**: rate `ω` (a world constant) and a phase that advances with time. Phase is
  taken modulo `2π` so it is exactly periodic and cannot drift over long runs.
- **Surface ↔ inertial frame conversion.** A point at surface coordinate `s` sits at inertial angle
  `2πs/C + φ(t)`. Surface coordinates are body-fixed: a rock stays at the same `s` forever. This is
  the whole content of the layer and everything else follows from it.
- **The sub-stellar point** as a function of time: the surface coordinate directly facing Kell.
- **Day and night as arcs**, with the two terminator points. Use the exact `arccos(R/d)` geometry,
  not the distant-star approximation — the approximation is wrong by 6% at `d/R = 10` and the exact
  form is no harder.
- **Insolation at a surface point**: `F·cos(incidence)` when lit, exactly zero when not. `F` comes
  from the existing `flux_at`, so the distance dependence is not reimplemented.
- **Report the breakup rate**, and **raise** on a rotation rate at or above it. A world spinning
  itself apart is not a world; returning one silently would be the same failure as a stub that
  answers everything.
- **Distinguish sidereal from solar day.** They differ by the orbital angular rate, and conflating
  them is the classic error. Both are reported and the difference is tested.
- **A lit-arc drawable** for the viewer: the day side drawn distinctly from the night side, with the
  terminator points marked. Without it there is nothing to see, and the request was to watch the
  planet spin.

### Must NOT Do

- **No oblateness and no deformation.** A spinning body bulges; modelling that needs material
  response, which is abstracted at T2.4. The disc stays circular and the assumption is declared.
- **No tides, no tidal locking, no spin-orbit coupling.** Each is its own PRP.
- **No axial tilt, and do not add a parameter for one.** A disc has no axis to tilt in a plane.
  A parameter that must always be zero is an invitation to set it.
- **No surface temperature, no thermal lag, no climate.** This layer gives the *illumination*;
  what the ground does with it is a climate layer.
- **Do not reimplement flux.** Call `sim.orbit.insolation.flux_at`.
- **Do not change the meaning of existing surface coordinates.** They are already body-fixed; this
  layer adds the rotating frame around them and must not silently redefine `s`.

## DERIVATION CHECK

- [ ] Every quantity is an axiom, a world constant, or a derived result
- [ ] No constant or scaling law imported from a 3D reference — the lit fraction is the 2D geometry,
      not a hemisphere
- [ ] Dimensions match `docs/AXIOMS.md` §2; angular velocity is `T⁻¹`, angular momentum `M L² T⁻¹`
- [ ] Nothing tuned to reproduce a monograph number — its 19.4-hour day is **not** a target
- [ ] Nothing hand-placed: the terminator is computed, never positioned
- [ ] The rotation rate is listed above and approved
- [ ] Absolute insolation values are reported as resting on the stubbed luminosity
- [ ] All computation in natural units
- [ ] No random source

New free parameters requiring human approval: **the rotation rate.**

## ERROR HANDLING REQUIREMENTS

- A non-finite or negative rotation rate raises `ValueError`. Zero is legal and means the current
  behaviour — a tidally frozen world with permanent day on one arc.
- A rate at or above breakup raises `ValueError` naming the breakup rate.
- Insolation raises `InvariantError` on a non-finite result.
- **Night returns exactly zero, not a small number.** A terminator that leaks a little light would
  make "is it dark here" a question of tolerance.

## SECURITY CONSIDERATIONS

- No file read or written, no network, no deserialisation, no `eval`.
- No external input beyond parameters from calling code.
- No restricted category applies.

## TESTS TO WRITE

**Dimensional:**
- [ ] Angular velocity is `T⁻¹`; angular momentum is `M L² T⁻¹`; insolation carries FLUX

**Invariant — the substance:**
- [ ] **Total intercepted power equals `F·2R`.** Integrating `F·cos(incidence)` over the lit arc
      must give exactly the flux times the disc's cross-section. This is the strongest check
      available and catches any error in the incidence geometry
- [ ] The lit fraction is `arccos(R/d)/π`, and tends to 1/2 as the star recedes
- [ ] Exactly two terminator points, always
- [ ] Night is exactly zero, everywhere on the dark arc
- [ ] Phase is exactly periodic: advancing by `2π/ω` returns the identical surface geometry
- [ ] A surface coordinate is body-fixed: it does not move relative to the surface as the world turns
- [ ] Moment of inertia of a uniform disc is `MR²/2` — the case that does *not* differ from 3D
- [ ] Determinism: the same rate and time give the same state

**Physical results:**
- [ ] Every point on the surface sees day and night over one rotation, for a non-zero rate
- [ ] With a zero rate, one arc is in permanent daylight and the opposite arc never sees the star —
      which is what Vellum has today
- [ ] Sidereal and solar day differ, and the difference matches the orbital angular rate
- [ ] Breakup: the surface speed at `ω_max` equals `√(G₂M)`, the circular orbital speed

**Error paths:**
- [ ] Negative, non-finite and above-breakup rates each raise

**Viewer:**
- [ ] The lit-arc drawable declares its bands and draws at each
- [ ] The lit arc moves as the phase advances

## ROLLBACK PLAN

- Branch to return to: `main` at the camera-roll commit.
- State: `rm -rf sim/rotation sim/tests/rotation`, remove the lit-arc drawable. Nothing else depends
  on it.
- Anything irreversible: none.

## ACCEPTANCE CRITERIA

- [ ] The intercepted-power identity holds to a stated tolerance — **and fails if `cos(incidence)`
      is dropped**, verified by mutation as every layer before it has been
- [ ] The lit fraction fails if the distant-star approximation replaces the exact `arccos(R/d)`
- [ ] Derivation check fully ticked
- [ ] `pytest`, headless `pytest`, `mypy --strict sim/`, `ruff check sim/` all pass
- [ ] `docs/AXIOMS.md` §3 gains: the terminator is two points; the lit fraction; breakup at orbital
      surface speed; the moment of inertia that does not change
- [ ] `docs/AXIOMS.md` §4 gains oblateness as an abstraction
- [ ] MEMORY.md decision 22 is updated — Vellum spins now
- [ ] No new dependency; no file over 300 lines
- [ ] CHANGELOG.md updated; CONTEXT.md session closed

## VALIDATION

- `.venv/bin/pytest` and the headless run; `mypy`; `ruff`
- `.venv/bin/python -m sim.view.app` — **watch it turn.** Zoom to the ground and confirm a point
  passes from day into night, and that the terminator crosses the view. Session 14 established that
  a visual feature is not validated by asserting pixels changed; this one must be looked at.
- Report the measured lit fraction against `arccos(R/d)/π` and the intercepted power against `F·2R`.
