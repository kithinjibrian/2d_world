# MEMORY.md — Vellum (2d_world)

Records resolved architectural decisions and current project state.
Read this at the start of every session before writing any code.

Open questions do not belong here — they live in `DECISIONS.md`.

---

## ARCHITECTURAL DECISIONS

### 1. The simulation is the authority; the monograph is a hypothesis

**Decision:** Vellum's physics is derived from first principles in two dimensions. Where the
simulation and `vellum-monograph.html` disagree, the simulation is right. The monograph is a prior
document written before anything was checked, and an eventual output target.

**Why:** User direction in Session 3: *"we will discover our own physics. we are the ones doing the
sim."* The value of the result depends entirely on it being derived rather than fitted. A world
tuned to reproduce a guess teaches nothing about two-dimensional physics; it only reproduces the
guess with extra steps.

**Rules out:** Tuning any parameter to match a monograph number. Treating monograph values as
specifications, acceptance criteria, or test assertions. Correcting the monograph's physics by hand
— it gets regenerated from simulation output.

**Supersedes:** the previous decision 5, "Vellum's canon is closed and lives in the monograph",
recorded in Session 1 and reversed in Session 3.

---

### 2. Every quantity is an axiom, a world constant, or a derived result

**Decision:** Nothing enters the world by fiat. Each number is one of: an axiom (a free choice, in
`docs/AXIOMS.md` §1), a world constant (an initial condition for one world instance), or a derived
result carrying a reference to what derived it. Anything else is a bug.

**Why:** Removing the monograph as an anchor removes the thing that was keeping the world honest.
This is its replacement. Without an explicit axiom list, "we derive our own physics" degrades into
typing in whatever number looks right, and the degradation is invisible — the code still runs.

**Rules out:** Unattributed constants. Hand-placed phenomena that should emerge (storms, basins,
distributions). Free parameters that appear without a DECISIONS.md entry.

---

### 3. Axioms are tiered, and what is abstracted is written down

**Decision:** `docs/AXIOMS.md` §1 layers the axioms: Tier 0 geometry and mechanics, Tier 1 the
fundamental interactions, Tier 2 the effective theories. Each tier declares what it *cannot* derive,
and §4 collects those declarations into an abstraction ledger.

**Why:** The instinct to define a few fundamental forces and derive everything else is right in
spirit and impossible in practice — the chain from forces to a climate is not computable in any
number of dimensions. Nobody derives Navier–Stokes by simulating molecules. So the honest structure
is a stack of effective theories whose *form* the geometry constrains and whose *parameters* are
declared. The declarations are the point: without them, a posited number is indistinguishable from a
derived one, and a result that merely reflects a choice gets reported as a discovery.

**Rules out:** A single fundamental layer generating everything. Any module standing in for an
abstracted layer without saying so, or returning a plausible default where it cannot honestly answer.

---

### 4. Gravity is postulated, because 2+1D general relativity is empty

**Decision:** Gravity is a direct attractive force, `F = G₂m₁m₂/r`, not spacetime curvature (T1.1).

**Why:** Not a simplification — a replacement, because geometric gravity does not exist in two
spatial dimensions. The graviton has `d(d−3)/2` propagating degrees of freedom, which is exactly
zero at d=3. In three dimensions the Riemann tensor is algebraically determined by the Ricci tensor
(there is no Weyl tensor), so vacuum forces Ricci to vanish and therefore Riemann too: spacetime is
flat wherever there is no matter. A point mass produces only a conical defect, and masses in that
geometry feel nothing. Nothing orbits, there are no gravitational waves, and there are no black
holes without a cosmological constant. Doing gravity "properly" with GR in 2D yields no gravity.

**Rules out:** Any geometric treatment of gravity. Also rules out a session spending a week
discovering this independently — which is the main reason it is recorded here.

---

### 5. Natural units, not SI; physics lives in dimensionless ratios

**Decision:** `G₂ ≡ 1`, `σ₂ ≡ 1`, with a chosen reference mass and length fixing the remaining
scales. All computation is in natural units; SI conversion happens only in display code. A world is
characterised by dimensionless ratios, not by constant values.

**Why:** SI is calibrated to our universe, so there is no correct SI value for a constant of another
one, and searching for it is a category error. Normalising the constants makes the choice of scales
disappear and leaves only what was ever physically meaningful — the ratios. This also makes the hard
question tractable: instead of inventing magnitudes, a world is specified by a handful of ratios
that can be scanned.

**Rules out:** SI values outside the display layer. Reasoning about magnitudes by analogy with
Earth. It also reduces the units layer from a design problem to mechanical bookkeeping — base
dimensions fixed, everything else a product of powers, checked automatically.

**Still true, and the reason the bookkeeping matters:** density is kg·m⁻², pressure is N·m⁻¹, `G₂`
is m²·kg⁻¹·s⁻². A 3D constant used here does not crash; it produces a plausible float that means
nothing and surfaces several modules later as an untraceable result. In natural units a dimensional
slip is *easier* to miss, because the offending constant is 1 — so dimensional tests come first.

---

### 6. Electromagnetism is abstracted

**Decision:** No Maxwell solver. Light, radiative transport and material cohesion are posited at
Tier 2 with declared parameters (DECISION-011).

**Why:** A 2D Maxwell solver is a project in itself and yields no chemistry regardless, since matter's
microstructure is abstracted at T1.3 either way. Acceptable only because it is declared — the cost is
that light is posited rather than derived, and any result resting on it is a consequence of a choice.

**Rules out:** Presenting radiation results as findings about 2D physics without qualification.
Silent defaults in modules standing in for EM — they raise instead.

If EM is ever added, 2D changes it: the magnetic field is a scalar, the photon has one polarization
state, and the electric force falls as `1/r`.

---

### 7. Python, with numpy as the workhorse

**Decision:** Python 3.11+, numpy, scipy, matplotlib, pytest, mypy, ruff. Simulation in `sim/`. No
game engine, no ECS, no simulation framework.

**Why:** Vellum's structures are 1D periodic arrays, which is numpy's native domain. Two properties
make the fit unusually good rather than merely acceptable:

- The atmosphere is genuinely two-dimensional, so an FFT-based 2D vorticity solver *is* Vellum's
  atmosphere rather than a reduced model of one. The inverse energy cascade — storms consolidating
  and persisting — emerges instead of being scripted.
- Nothing passes anything on the surface, so an array of bodies sorted by position stays sorted for
  the life of every body in it. See decision 8.

**Rules out:** A framework layer. Notebook-driven development. The usual argument against Python for
simulation (per-agent loops do not vectorise), which mostly does not apply here.

---

### 8. The array index is the spatial index, permanently

**Decision:** Surface bodies are held in an array sorted by position. That order never changes except
by birth and death. Neighbours are `i±1`. No spatial hash, no quadtree, no broad phase, no re-sort.

**Why:** A topological consequence of two dimensions: two solid bodies on a line cannot exchange
order without passing through each other. It is not an optimisation or an approximation — it is a
theorem, and it means the naive data structure is also the optimal one.

**Rules out:** Every conventional spatial-partitioning structure. Any code that re-sorts by position
each tick — if that appears necessary, something has violated the ordering invariant and that is a
bug worth finding.

---

### 9. Determinism is a hard requirement

**Decision:** A seed reproduces a world byte-for-byte. Every random source is an explicitly seeded
`numpy.random.Generator` threaded down from the world constructor. Generation is separate from
query; worlds persist as data-only files and are loaded read-only.

**Why:** A world you cannot regenerate is a world you cannot study. Findings need to be
re-examinable, and a result that cannot be reproduced is an anecdote. The failure mode is silent —
an unseeded call works perfectly until the day you need that specific world back.

**Rules out:** Module-level `np.random.*`, the `random` module, clock or environment reads during
generation, dependence on set or dict iteration order for numerical results. Pickling world state,
for the separate reason that unpickling executes code.

---

### 10. Exceptions, not Result types

**Decision:** Ordinary Python exceptions, all subclassing `VellumError`. Validation at module
boundaries. `mypy --strict` on `sim/`. No Result/Either types.

**Why:** The Result pattern earns its ceremony in a language with a compiler that can check
exhaustiveness. Python has neither checked exceptions to route around nor a compiler to enforce the
discipline, so porting the pattern costs readability and returns nothing. Static checking comes from
mypy instead.

**Rules out:** Result/Either types. Bare `except:` without re-raise. Silent clamping of
out-of-range values. Letting non-finite values propagate — kernels check and raise.

---

### 11. The monograph is a single self-contained file, frozen

**Decision:** `vellum-monograph.html` keeps its own styles, scripts, and all plates as inline SVG,
with no build step, opening from `file://`. It is not edited by hand while frozen; generated plates
are written in as inline SVG, never linked as external assets.

**Why:** The document's durability is the point, and it matters more once the document is a
generated artefact rather than less — output from a simulation should still be readable by someone
who has neither the simulation nor a server.

**Rules out:** External stylesheets, scripts, or image files. A bundler. Runtime fetches, which
`file://` blocks anyway.

---

### 12. A world is scanned for, not chosen

**Decision:** The dimensionless ratios characterising a world are swept over a grid. Habitability is
an **output** of the sweep. A world is then picked from inside the habitable region and the reason
recorded (DECISION-009).

**Why:** It is the only option that makes habitability falsifiable rather than assumed. Fixing the
ratios by fiat risks producing no world at all; tuning them guarantees one but forfeits the claim
that Vellum was found rather than built — and that claim is the whole reason for deriving the physics
instead of importing it. The sweep also produces a map of which two-dimensional worlds can hold a
lit, stable surface, which is a result in its own right.

**Rules out:** Any single-world code path. Three architectural consequences follow and are not
optional:
- **Every layer runs at two fidelities** — a cheap screening path over the whole grid, and the full
  solve for one point. A layer supporting only the full solve cannot be scanned, and adding a
  screening path afterwards means rewriting it.
- **Determinism becomes load-bearing**, not a nicety. Each grid point is a parameter tuple plus a
  seed, and a result that cannot be reproduced exactly means nothing.
- **Scans are versioned data products.** A scan carries the code version and grid that produced it.
  Run against changed physics it is a different scan, never an update of the old one.

---

### 13. Kell is stubbed behind its real interface

**Decision:** The star's public surface is defined now and implemented as a supplied luminosity.
The 2D stellar-structure solve comes later, without callers changing (DECISION-010).

**Why:** It reaches the surface layers in a session or two rather than a week, and it composes with
decision 12 rather than fighting it: under a scan, a stubbed luminosity is simply **another axis of
the sweep**. Deriving Kell later does not invalidate the scan — it *collapses a dimension of it*, by
predicting luminosity from stellar mass instead of sweeping it independently. That is a better place
to derive a star from than the beginning, because by then a map will show which luminosities matter.

**Rules out:** Treating any stellar quantity as derived. Three conditions bind the stub, and without
them it is the bad kind of shortcut:
- Luminosity is tagged in the abstraction ledger (`docs/AXIOMS.md` §4), never as a derived value.
- **The stub raises** for spectrum, radius, lifetime and evolution. It never returns a plausible
  default — a stub that answers everything is never revisited and quietly becomes the model.
- Any result depending on it is reported as a consequence of a chosen parameter, not a finding about
  stellar physics.

---

### 14. Dimensions are checked at module boundaries, not in kernels

**Decision:** `Quantity` (a magnitude plus a `Dimension`) is what public functions accept and
return. `Quantity.magnitude(expected)` validates and unwraps to a plain float or array; the numerics
inside work on raw numpy (DECISION-015).

**Why:** The mistake this guards against happens at definition and composition — writing `G₂M/r²`,
or giving a constant the wrong dimensions — not inside a loop that has already been handed correct
arrays. Boundary checking therefore catches essentially the whole risk class at one check per call
rather than one per element, which matters because scanning multiplies any inner-loop cost by the
size of the grid.

Requiring the caller to name the expected dimension at the unwrap site is the load-bearing part: it
forces the caller to state what it believes it is holding, and that belief is what gets checked.

**Rules out:** Carrying units through inner loops. Dimensioned array types. Any units dependency —
the layer is ~120 lines of `Fraction` exponent arithmetic and owes nothing to `pint`.

---

### 15. The units layer defines no three-dimensional form, deliberately

**Decision:** `sim/units/` contains no `DENSITY_3D`, no inverse-square helper, no 3D constant. The
named-dimension table is 2D only, and a test asserts the forbidden names are absent.

**Why:** A name that exists can be selected by accident; a name that does not exist cannot. It is the
cheapest available enforcement of the project's second anti-pattern, and it costs nothing.

Verified rather than assumed: substituting each 3D form in turn — inverse-square gravity, per-volume
density, `T⁴` emission, per-area flux, per-area pressure, and the 3D dynamic viscosity — makes
between 4 and 11 tests fail. The suite catches every one.

**Rules out:** Adding a 3D name "for comparison" or "for the tests". The comparison lives inside the
discriminating tests, which construct the wrong form locally and assert it is wrong.

---

### 16. Precession is a poor diagnostic of integration quality in a log potential

**Decision:** The orbit layer's guard against a bad integrator is the stability of the orbit's
**radius**, not the stability of its measured precession.

**Why:** The orbit PRP asserted that a non-symplectic integrator would manufacture spurious apsidal
precession. That was tested in Session 9 and is **false for this potential**. Forward Euler inflated
the orbit's maximum radius from 1.10 to 2.13 over 1500 time units while the measured apsidal sweep
moved by less than 0.001°.

The reason is that a logarithmic potential is scale-invariant — `r → kr` with `t → kt` leaves the
equation of motion unchanged — so an orbit inflated by numerical energy is very nearly a rescaled
copy of itself, keeping its shape and its apsidal angle. Precession is protected here in a way it
would not be under an inverse-square force.

The symplectic requirement stands, for the reason that actually bites: **flux goes as `1/r`**, so a
silently doubled orbital radius halves the insolation with no symptom anywhere in the precession
measurement. That is precisely the plausible-wrong-number failure the project is built to catch,
located somewhere other than where it was predicted.

**Rules out:** Using a precession measurement as evidence that an integrator is sound. Adaptive
stepping, which breaks symplecticity. Trusting a physics justification that has not been mutated
and re-run — this one survived a PRP review and a full implementation before failing its first
real test.

---

### 17. The viewer is a skeleton built before what it will show

**Decision:** A desktop viewer using `pygame-ce`, built now against Kell and the orbit, and grown as
each layer lands (DECISION-016). Camera logic is pure and headless-testable; only the drawing and
event loop touch a display.

**Why:** For a project whose whole subject is what a two-dimensional world looks like, being able to
see it is not a luxury at the end — it is feedback on every layer while that layer is being written.
The cost is some throwaway iteration; the alternative is building five layers without ever looking
at any of them.

`pygame-ce` over `pyglet` because pyglet is OpenGL and its pipeline is float32. Spanning system scale
to ground scale is eleven orders of magnitude, which needs float64 throughout — with SDL2 the
arithmetic stays in Python and only integer pixels reach the renderer.

**Rules out:** Any GPU path. A `World` aggregate invented from two layers. Computing anything in the
viewer — it draws what the simulation produced, or the picture is evidence of nothing.

**The rule that will be quietly violated if it is not written down:** render camera-relative,
`(world − focus) * scale`, never `world * scale`. At a focus 1e11 m from the origin a metre of detail
is below float64's resolution of the absolute coordinate and comfortably inside it for the relative
one.

---

### 18. What actually breaks across eleven orders of magnitude

**Decision:** The viewer composes positions hierarchically — `anchor + offset`, never summed
absolutely — and surface bodies are held as (surface coordinate, height) rather than as world
positions. Scale bands are **dimensionless ratios** of viewport span to planet circumference.

**Why:** Three claims were tested in Session 11 and two were wrong.

*Camera-relative transforms do not buy float64 precision here.* With a focus 1e11 away and two
points a metre apart, the relative and absolute forms both give exactly 100 px. Eleven orders of
magnitude sit comfortably inside float64's sixteen digits. What the absolute form breaks is **pixel
coordinate magnitude**: 1e11 at 100 px/unit is 1e13 pixels and SDL takes C ints that stop at 2.1e9.
The renderer overflows long before the float does.

*The real precision floor is in storing an absolute coordinate at all.* One ulp at 1e11 is about 15
microns, so ground detail finer than that cannot be represented as an absolute position however it
is transformed. Composing from the planet centre instead keeps the arithmetic near the planet's
radius, where an ulp is nanometres. This is why surface positions live in surface coordinates — the
same 1D periodic array the simulation already wanted.

*Scale bands in absolute units were simply wrong.* The simulation works in natural units where the
orbital radius is about 1, so metre-based thresholds put every zoom level in one band. A band means
"how much of the world can I see", which is a ratio — consistent with the project's position that
only dimensionless ratios are physically meaningful.

**Rules out:** Any GPU path (float32 cannot even represent 1e11+1 distinctly). Absolute world
positions for anything on the ground. Thresholds in absolute units anywhere in the viewer.

---

### 19. Terrain is procedural noise, not a spectral sum, and its shape is chosen

**Decision:** `h(s)` is periodic multi-octave gradient noise — a seeded integer hash on a lattice
whose index is taken modulo each octave's cell count — plus an optional sampled residual for
post-generation modification (DECISION-017).

**Why the noise and not a Fourier sum:** spectral synthesis was recommended three times before it
was costed, and it does not work here. Resolving wavelength `λ` on a surface `C` around needs `C/λ`
coefficients at `O(k)` per sample. Metre detail on 38,400 km is **38 million coefficients**; fBm
needs **26 octaves** at `O(octaves)`. The property the whole decision rested on — regenerate detail
at any zoom — would have been lost at the first serious zoom. The lattice modulo keeps periodicity
exact by construction, which was spectral synthesis's other attraction, so nothing is given up.

**Why a residual as well:** craters and eroded channels cannot be expressed by changing a noise
parameter. A sampled array is the only representation of "this is here now", and it costs nothing
while empty.

**Rules out:** A global Fourier terrain. A 2D heightmap — the surface is a closed curve, so `h` takes
one coordinate and an API taking two misunderstands the world. Any claim that terrain has unlimited
detail: the floor is `C / 2**octaves`, it is finite, and the layer reports it rather than inventing
flatness below it.

**And the part most easily forgotten:** terrain statistics are **abstracted, not derived**. Nothing
in the axioms predicts a roughness exponent. Roughness and amplitude are world constants, recorded
in the §4 ledger, so no result about mountains or slopes is a finding about two-dimensional physics.

---

### 20. The octave decay that delivers a spectral slope is off by one from the obvious formula

**Decision:** Octave amplitudes fall as `2**(-(β-1)·n/2)` to deliver `P(k) ~ k^-β`, not
`2**(-β·n/2)`.

**Why:** The obvious derivation says power at octave `n` goes as `A_n²`, so `A_n ∝ 2^(-βn/2)` gives
`P(k) ~ k^-β`. Measured, that produces a slope of `-(β+1)`. The missing factor is **mode density**:
in one dimension the octave band `[2^n, 2^(n+1))` contains about `2^n` Fourier modes, so power *per
mode* carries an extra `k^-1`. Verified across decay exponents — `p = 0.5, 1.0, 1.5` measure
`-1.98, -2.96, -3.92`, i.e. `slope = -(2p+1)` exactly.

**Rules out:** Trusting a spectral normalisation that has not been measured against an FFT of the
field it produces. The error is invisible by inspection — the terrain looks perfectly plausible at
either exponent, and only a spectrum test distinguishes fractal ground from ground that is merely
rough.

---

### 21. Limits and thresholds in the viewer are ratios, and this was learned twice

**Decision:** Zoom limits, like scale bands, are expressed as the fraction of the world the viewport
spans — `MIN_SPAN_RATIO` and `MAX_SPAN_RATIO` — never as absolute pixels per world unit.

**Why:** Decision 18 already established that scale *bands* in absolute units are meaningless when
the simulation works in natural units. The zoom *limits* were left absolute in the same file, and
capped at 1e9 px per world unit they made the GROUND band unreachable on a world 3.8e-5 units
around. The same error, in a second place, surviving the fix to the first.

Two other defects shipped alongside it, both invisible to the tests that existed. The star was drawn
with an unculled radius — 0.02 world units is twenty million pixels at close zoom — and filled the
viewport with gold. And following Vellum centred on the planet's *centre*, which is correct only
while the planet fits in the viewport; past that it puts the camera inside the world with the ground
thousands of pixels off-screen.

**Rules out:** Any absolute threshold in the viewer. Drawing a primitive without culling it against
the viewport. Centring on a body's centre at a zoom where the body does not fit.

**And the process lesson, now a rule in CLAUDE.md:** a visual feature is not validated by asserting
that pixels changed. The viewer PRP said to run the app and zoom by hand; headless smoke tests were
run instead, and all three defects were found in seconds by someone actually looking. Where looking
is not possible, walk the whole range and assert sanity at every step — `test_zoom_journey.py`
exists for exactly that and catches all three.

---

### 22. On a closed surface the camera must roll (Vellum now spins — see 23)

**Decision:** The camera carries a roll angle, set to local vertical whenever the view is on the
ground. **Separately: nothing in the simulation rotates.** Vellum has no spin, no day, no night.

**Why the roll:** "up" on a closed surface means radially outward from the planet centre, and that
direction differs at every position — at the far side of the world it is the exact opposite of what
it is here. Without roll the ground tilts as you walk along it and is upside down halfway round.
Verified at eight points around the world: up is up and the ground runs horizontally at every one.

**On spin:** this entry originally recorded that Vellum did not turn on itself. That was resolved by
the rotation layer — see decision 23.

**Rules out:** Drawing anything on the ground without rolling the camera. Treating current
insolation results as day-resolved — they are orbital only.

---

### 23. Vellum spins, and the illumination geometry is exact rather than asymptotic

**Decision:** `sim/rotation/` gives Vellum a rotation rate (a world constant), a body-fixed surface
frame that turns relative to inertial space, and the day that follows. Surface coordinates are
body-fixed: a rock stays at the same `s` forever and the frame turns around it.

**Why the geometry had to be exact:** the natural instinct is that half a world is lit. That is a
*distant-star approximation*. The lit fraction is `arccos(R/d)/π`, which is 0.468 at `d/R = 10` and
exactly one third at `d/R = 2`. Likewise the intercepted power: the familiar `F·2R` cross-section
form is asymptotic, while `L·arcsin(R/d)/π` is exact for a point source and any convex body — 4.7%
apart at `d/R = 2`. Both exact forms are used and both approximations are pinned as failures by
tests.

The intercepted-power identity is the strongest invariant in the layer: it checks the incidence
geometry, the `1/r` flux dilution and the terminator simultaneously, and it caught all three
mutations tried against it — dropping `cos(incidence)`, substituting the distant-star terminator,
and evaluating flux at the planet centre rather than at each surface point.

**Rules out:** Treating the lit hemisphere as half the world. `F·2R` as anything but a limit. Any
axial-tilt parameter — a disc has no axis to tilt in a plane, and a parameter that must always be
zero is an invitation to set it. Oblateness, which is now a ledger entry.

**A finding from the breakup check:** it rejected the first test fixture written against it, at a
rate 3.5× the limit. The check is not decoration — an unphysical world is easy to specify by
accident.

---

### 24. Wrapping on a closed curve lives in one place, and comparison is circular distance

**Decision:** `sim/periodic.py` owns `wrap`, `separation` and `distance`. Positions on the surface
are compared by circular distance, never by subtraction.

**Why:** the wrap subtlety had already produced two defects in two modules before this — the
`fmod(fmod+b, b)` form quantising a micron at the period's ulp, and `%` returning exactly the period
for a tiny negative. It appeared a third time in the rotation layer, which was the signal that it
belongs in one place rather than being reimplemented per module.

`separation` and `distance` exist because of a subtler failure: after exactly one sidereal day the
phase lands 8.9e-16 short of a full turn, so the substellar point returns as `circumference - 1e-21`.
Subtracting says it travelled the whole way round; on a closed curve it did not move at all. **Every
comparison of surface positions must go through circular distance** — the water and life layers will
need it constantly, since "how far apart are these two things" on a closed curve is the shorter way
round and is never more than half the world.

---

### 25. Following is only right when the followed thing is not the subject

**Decision:** The camera does not follow Vellum at SYSTEM zoom. It follows from PLANETARY inward:
the planet's centre while the planet fits the view, a point on its surface once it does not.

**Why:** following a body that is orbiting drags the entire background across the window. With the
clock running, the star slid past and the system appeared to be moving — the planet was the only
thing standing still, which is exactly backwards. At system scale the system is the subject and the
planet is the thing moving through it; from planetary scale inward, the planet is the subject.

Also: **anything that can shrink below a pixel needs a minimum drawn size.** Vellum's radius at the
opening view is 0.0013 px, so the outline had nothing to draw and the planet was absent from its own
viewer. The star had carried a `max(2, ...)` floor since it was written; the planet did not.

**Rules out:** Following at every zoom. Drawing a body only at its true size.

**And a test that passed for the wrong reason.** The first version asserted "something is drawn near
the planet" — which passed whether or not the planet existed, because the orbit trace runs exactly
through its position. It now checks for Vellum's own marker colour. A visual assertion that cannot
name what it is looking for is not an assertion.

---

## CURRENT PROJECT STATE

### Fully Working
- **`sim/rotation/`** — spin, the rotating surface frame, day and night, the terminator, and
  insolation at a point on the ground. Vellum has a day.
- **`sim/surface/`** — periodic multi-octave gradient noise plus an optional sampled residual.
  Exactly periodic, deterministic, evaluable at any resolution down to `C / 2**octaves`, with the
  floor reported rather than smoothed over.
- **`sim/view/`** — a window that zooms from the whole system to a sliver of surface. Camera,
  bands, geometry and scene are pure and tested headless; only `render.py` and `app.py` touch a
  display. Run with `python -m sim.view.app`.
- **`sim/orbit/`** — two-body integration under `F ∝ 1/r`, the analytic screening path, apsidal
  measurement, and insolation. **`sim/star/`** — Kell, stubbed and raising for anything beyond mass
  and luminosity.
- **`sim/units/`** — the first module. Dimension algebra over four base dimensions with `Fraction`
  exponents, the named-dimension table for 2D, `Quantity` for boundary checking, and the natural
  unit system in which `G₂` and `σ₂` are both 1. 101 tests, `mypy --strict` and `ruff` clean.
- `vellum-monograph.html` — 18 slides, 17 inline SVG plates, keyboard and button navigation. Frozen
  reference material.
- The context system: CLAUDE.md, MEMORY.md, CONTEXT.md, DECISIONS.md, CHANGELOG.md, `.llmignore`,
  `PRPs/`, `docs/`, `reports/`.
- `docs/AXIOMS.md` — tiered axioms (§1), natural units and dimensions (§2), established
  consequences (§3), and the abstraction ledger (§4). Settled and usable.

### In Progress
- Nothing. The orbit layer is complete; the next layer has no PRP yet.

### Not Started
- water, planet, air, life. Erosion and craters, which are what the terrain residual exists for. None has a PRP. Debris and the impact cycle were explicitly
  deferred out of the orbit layer and need one.
- No world has been instantiated. The ratios defining one are swept (decision 12), but the predicate
  deciding which grid points count as habitable is DECISION-012 and still open.

---

## NEXT SESSION START POINT

Read CLAUDE.md, then this file, then DECISIONS.md, then CONTEXT.md, then `docs/AXIOMS.md`.

Vellum has ground. 284 tests, headless, `mypy --strict` and `ruff` clean. Run
`.venv/bin/python -m sim.view.app` and zoom from the whole disc to a stretch of terrain.

**The next PRP is water**, and it is the layer where two dimensions bite hardest. On a closed curve
with no third direction: a basin is a local minimum of `h`, filling it is a 1D problem rather than a
watershed, **rivers cannot branch** because a tributary would have to arrive from a side that does
not exist, and a basin has no drainage network at all — a population sealed in one is sealed
forever. All of that follows from T0.1 and none of it needs new physics. Scope it as basin
detection and filling; leave the anoxic depth and lake stratification to a climate-facing layer.

Also still open: DECISION-012 (habitability, blocks the scan), -013 (chemistry), -014 (grey vs
spectral transfer).

Environment: `.venv/`. Run `.venv/bin/pytest`, `.venv/bin/mypy`, `.venv/bin/ruff check sim/`.

Do not edit `vellum-monograph.html`. It is frozen; it gets regenerated, not corrected.