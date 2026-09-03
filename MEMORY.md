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

## CURRENT PROJECT STATE

### Fully Working
- `vellum-monograph.html` — 18 slides, 17 inline SVG plates, keyboard and button navigation. Frozen
  reference material.
- The context system: CLAUDE.md, MEMORY.md, CONTEXT.md, DECISIONS.md, CHANGELOG.md, `.llmignore`,
  `PRPs/`, `docs/`, `reports/`.
- `docs/AXIOMS.md` — tiered axioms (§1), natural units and dimensions (§2), established
  consequences (§3), and the abstraction ledger (§4). Settled and usable.

### In Progress
- Nothing. No simulation code exists.

### Not Started
- The entire simulation. `sim/` does not exist yet.
- No world has been instantiated — the dimensionless ratios that define one are DECISION-009.

---

## NEXT SESSION START POINT

Read CLAUDE.md, then this file, then DECISIONS.md, then CONTEXT.md — in that order. Then read
`docs/AXIOMS.md` in full; it is the anchor for everything and it was restructured in Session 4.

**The first PRP is the units layer**, and Session 4 made it much smaller than it looked. Natural
units (`G₂ = 1`, `σ₂ = 1`, plus a reference mass and length) remove the need to invent any
magnitude, so the module is mechanical: fix the base dimensions — mass, length, time, temperature —
express everything else as a product of powers, and check it automatically. Its tests are dimensional
assertions, written before any physics, and they must include that dimensionless results really are
dimensionless: in natural units a slip is easier to miss, because the offending constant is 1.

It does not depend on DECISION-009 or DECISION-010, so it can be written and approved while both are
open.

Two questions for the user when convenient, neither blocking that PRP:
- **DECISION-009a** — are the dimensionless ratios that define a world fixed, tuned, or scanned?
  Recommendation: scanned, because it is the only option that makes habitability an answer rather
  than an assumption.
- **DECISION-010** — derive Kell from 2D stellar structure, or stub its luminosity behind a real
  interface and reach terrain sooner?

Layer order after the units layer: star → orbit → planet → surface → water → air → life. Each layer
is only trustworthy if the one beneath it was finished and verified first. Do not start a layer
before the one below it passes its invariant tests.

Do not edit `vellum-monograph.html`. It is frozen; it gets regenerated, not corrected.
