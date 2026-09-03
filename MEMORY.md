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

### 3. Two spatial dimensions change every constant's dimensions

**Decision:** A units layer with 2D dimensions is module zero, and no physical constant enters the
codebase except through it. Density is kg·m⁻², pressure is N·m⁻¹, `G₂` is m²·kg⁻¹·s⁻², radiated flux
scales as `T³`, and flux dilutes as `1/r`.

**Why:** This is the project's most dangerous silent failure. A 3D constant used in 2D does not
crash — it produces a plausible float that means nothing, and the error surfaces several modules
later as a climate number that cannot be traced. Dimensional tests written before physics tests
catch it at the boundary.

**Rules out:** Importing numerical constants from 3D references. Reasoning about magnitudes by
analogy with Earth.

---

### 4. Python, with numpy as the workhorse

**Decision:** Python 3.11+, numpy, scipy, matplotlib, pytest, mypy, ruff. Simulation in `sim/`. No
game engine, no ECS, no simulation framework.

**Why:** Vellum's structures are 1D periodic arrays, which is numpy's native domain. Two properties
make the fit unusually good rather than merely acceptable:

- The atmosphere is genuinely two-dimensional, so an FFT-based 2D vorticity solver *is* Vellum's
  atmosphere rather than a reduced model of one. The inverse energy cascade — storms consolidating
  and persisting — emerges instead of being scripted.
- Nothing passes anything on the surface, so an array of bodies sorted by position stays sorted for
  the life of every body in it. See decision 5.

**Rules out:** A framework layer. Notebook-driven development. The usual argument against Python for
simulation (per-agent loops do not vectorise), which mostly does not apply here.

---

### 5. The array index is the spatial index, permanently

**Decision:** Surface bodies are held in an array sorted by position. That order never changes except
by birth and death. Neighbours are `i±1`. No spatial hash, no quadtree, no broad phase, no re-sort.

**Why:** A topological consequence of two dimensions: two solid bodies on a line cannot exchange
order without passing through each other. It is not an optimisation or an approximation — it is a
theorem, and it means the naive data structure is also the optimal one.

**Rules out:** Every conventional spatial-partitioning structure. Any code that re-sorts by position
each tick — if that appears necessary, something has violated the ordering invariant and that is a
bug worth finding.

---

### 6. Determinism is a hard requirement

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

### 7. Exceptions, not Result types

**Decision:** Ordinary Python exceptions, all subclassing `VellumError`. Validation at module
boundaries. `mypy --strict` on `sim/`. No Result/Either types.

**Why:** The Result pattern earns its ceremony in a language with a compiler that can check
exhaustiveness. Python has neither checked exceptions to route around nor a compiler to enforce the
discipline, so porting the pattern costs readability and returns nothing. Static checking comes from
mypy instead.

**Rules out:** Result/Either types. Bare `except:` without re-raise. Silent clamping of
out-of-range values. Letting non-finite values propagate — kernels check and raise.

---

### 8. The monograph is a single self-contained file, frozen

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
- `docs/AXIOMS.md` §2 (dimensions) and §3 (established consequences) — derived, settled, usable.

### In Progress
- Nothing. No simulation code exists.

### Not Started
- The entire simulation. `sim/` does not exist yet.
- `docs/AXIOMS.md` §1, the axiom list, is DRAFT pending DECISION-009.

---

## NEXT SESSION START POINT

Read CLAUDE.md, then this file, then DECISIONS.md, then CONTEXT.md — in that order. Then read
`docs/AXIOMS.md` in full; it is the anchor for everything.

Two decisions gate the first line of code:

- **DECISION-009 (the axiom set)** — specifically 9a: are `G₂` and `σ₂` fixed by fiat with
  habitability left as a discovered outcome, tuned so a habitable world is guaranteed, or scanned as
  a parameter space? Recommendation recorded: scan.
- **DECISION-010 (Kell)** — derive the star from 2D stellar structure first, or stub its luminosity
  behind a real interface and reach terrain sooner? Recommendation recorded: derive, given the
  stated intent to build slowly.

The first PRP is the **units and dimensions layer**, and it does not depend on either decision — it
can be written and approved while they are still open. It is small, it is dull, and it is the single
highest-leverage module in the project: it is what prevents 3D constants from silently entering a 2D
world. Its tests are dimensional assertions, written before any physics.

The intended layer order after that is: star → orbit → planet → surface → water → air → life. Each
layer is only trustworthy if the one beneath it was finished and verified first.
