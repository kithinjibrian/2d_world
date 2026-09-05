# DECISIONS.md — Vellum (2d_world)

Tracks architectural and design questions that are open, deferred, or resolved.

Rules:
- Every open decision blocks implementation of the code it affects.
- The AI must not implement anything that depends on an open decision.
- When a decision is resolved, move it to the RESOLVED section and record the outcome.
- Once resolved, copy the outcome to MEMORY.md as an architectural decision.

---

## OPEN — Requires human input before implementation

### DECISION-015 — Where does dimension checking happen?

**Status:** open
**Raised:** 2026-09-05 — Session 6
**Resolved by:** human
**Blocks:** `PRPs/units-layer.md`. It changes the module's public API, so it cannot be deferred past
approval.

**Question:** Are dimensions carried at runtime by every quantity, or checked only at boundaries and
in tests?

**Options:**
- A) **Runtime `Quantity` everywhere.** Every value carries its dimension; every operation checks.
  Catches everything, including mistakes inside kernels. Costs a wrapper object or a dtype on every
  array operation — real overhead in an inner loop, and DECISION-009 means sweeping a grid of worlds,
  so inner-loop cost is multiplied by the size of the scan.
- B) **Test-time only.** Plain numpy floats everywhere. Dimensions are declared symbolically and
  asserted against formulas in tests, never carried by values. Zero runtime cost. Misses any error
  in a code path no test exercises.
- C) **Boundaries and tests — `Quantity` at module edges, raw arrays inside kernels.** Public
  functions accept and return dimensioned quantities and validate on the way in; internal numerics
  operate on unwrapped arrays. Costs one check per call rather than per element.

**Notes:** Recommend **C**. The failure this module exists to prevent is a constant or a formula
entering with the wrong dimensions — that happens at definition and at composition, which are
exactly the boundaries, not inside a loop that has already been handed correct arrays. C catches
essentially the whole risk class at a cost that does not scale with the grid, and it keeps kernels
as plain numpy, which is also what keeps them readable and fast.

A is the safest and the one to choose if the scan turns out to be cheaper than expected or if
correctness worries outweigh throughput. B is the cheapest and is defensible only because the
discriminating tests in the units PRP catch the realistic mistakes — but it leaves no guard on code
written later by a session that forgets to write the test.

Whichever is chosen, the named-dimension table stays and the three discriminating tests stay; this
decision only governs whether dimensions ride along with values at runtime.

---

### DECISION-012 — What counts as habitable?

**Status:** open
**Raised:** 2026-09-05 — Session 5
**Resolved by:** human
**Blocks:** The scan. DECISION-009 makes habitability the *output* of a parameter sweep, which is
only meaningful once there is a criterion deciding which grid points count.

**Question:** Scanning for habitable worlds requires a predicate. What is it?

**Options:**
- A) **Liquid water somewhere on the surface**, at some point in the orbit. Simplest, and it maps
  directly onto the basins the terrain layer will produce.
- B) **A stable surface temperature band** — habitable means the climate does not run away in either
  direction over some interval. Harder, and it interacts with the `T³` emission law, which is a
  weaker stabilising feedback than the 3D quartic and so makes runaway *more* likely. This is
  arguably the more interesting criterion precisely because 2D climate is twitchier.
- C) **An energy budget adequate for photosynthesis** at the surface, given `1/r` flux dilution.
- D) A conjunction of the above.

**Notes:** Recommend starting with A as a coarse screen (it is cheap and it prunes most of the grid)
and layering B onto the survivors, since B is the expensive one and the one whose answer is not
obvious in advance. C depends on abstracted radiation (`docs/AXIOMS.md` §4) and so cannot yet be a
finding about 2D physics — it would be a consequence of a chosen parameter.

The criterion must be recorded as a **world-selection predicate, not an axiom.** It says which
worlds are interesting to us; it says nothing about which worlds exist.

---

### DECISION-013 — Does chemistry get any representation?

**Status:** open
**Raised:** 2026-09-03 — Session 3 (as DECISION-009b). Split out 2026-09-05 — Session 5.
**Resolved by:** human
**Blocks:** Anything where composition matters qualitatively — atmospheric evolution in particular.

**Question:** T1.3 abstracts matter's microstructure entirely, so composition is currently a small
set of bulk species with assumed properties. Is that enough?

**Notes:** One consequence makes this less academic than it looks: because there is **no atmospheric
escape at all** in 2D, composition is strictly cumulative — a 2D planet keeps every gas it ever
acquires, forever. An atmosphere that only ever accumulates may need more compositional structure
than a single bulk species can carry, or it may not; that is the question. Cheap to defer, and it
should be deferred until the atmosphere layer actually needs it.

---

### DECISION-014 — Grey or spectral radiative transfer?

**Status:** open
**Raised:** 2026-09-03 — Session 3 (as DECISION-009c). Split out 2026-09-05 — Session 5.
**Resolved by:** human
**Blocks:** The climate layer. Not the star stub, which sits above this.

**Question:** Is radiative transfer grey (frequency-independent) or spectral?

**Notes:** Recommend grey until DECISION-013 says composition matters. Spectral transfer layered on
top of an abstracted electromagnetism (T1.2) and an abstracted chemistry (T1.3) would be false
precision — detailed frequency structure resting on posited opacities is not more truthful than a
single band, only more expensive.

---

### DECISION-004 — Tokenising the monograph's typography scale

**Status:** open
**Raised:** 2026-09-03 — Session 1
**Resolved by:** human
**Blocks:** Any change introducing a new font size. Lower priority since Session 3 — the monograph
is now frozen reference material rather than the active work.

**Question:** `docs/DESIGN.md` requires every visual value to come from a token, but only the eight
colours are tokenised. Font sizes are 14 hardcoded px values.

**Options:**
- A) Tokenise now, in its own PRP. Touches nearly every stylesheet rule; no test to catch regression.
- B) **Freeze the current scale and document it as-is.** The 14 existing sizes are the permitted set;
  a fifteenth needs approval. Zero regression risk, enforceable by inspection today.
- C) Leave it. The DESIGN RULE stays partially unenforceable.

**Notes:** Recommend B, and `docs/DESIGN.md` is already written on that assumption. Worth revisiting
properly when the simulation starts generating plates, since generated output should be tokenised
from the start regardless of what happens to the hand-written rules.

---

## DEFERRED — Acknowledged, not yet needed

### DECISION-007 — Accessibility of the monograph

**Status:** deferred
**Raised:** 2026-09-03 — Session 1
**Revisit when:** The monograph is published to a real audience, or is regenerated from simulation
output — a regeneration is the natural moment to fix it, since the markup is being rewritten anyway.

**Question:** The navigator hides 17 of 18 sections with `display:none`, has no landmark regions, no
live region announcing slide changes, and the plates have captions but no `<title>`/`aria-label`.

**Notes:** Safe to defer while this is a private artefact. Listed as KNOWN ISSUE 4 in CLAUDE.md so it
is not fixed piecemeal.

---

### DECISION-008 — Publishing and hosting

**Status:** deferred
**Raised:** 2026-09-03 — Session 1
**Revisit when:** There are simulation results worth showing, or the monograph is ready to share.

**Question:** Where does the monograph live for readers — GitHub Pages, a published Artifact, a
downloaded file, print/PDF? And separately: are simulation outputs (world files, figures) published
alongside it, or kept local?

**Notes:** Affects font loading (Google Fonts needs a network; an offline or print target needs
embedding or a fallback that holds up) and world-file size limits if generated data is ever shipped.

---

## RESOLVED

### DECISION-009 — How are a world's dimensionless ratios chosen?

**Status:** resolved
**Raised:** 2026-09-03 — Session 3. Reframed Session 4.
**Resolved:** 2026-09-05 — Session 5

**Question:** Natural units removed the question of what `G₂` and `σ₂` are worth — both are 1 by
construction. What remained is the only physical content: the dimensionless ratios characterising a
particular Vellum, and how they get chosen. Fixed by fiat, tuned until a habitable world exists, or
scanned?

**Outcome:** **Scanned.** The ratios are swept over a grid; habitability is an *output* of the sweep,
not an assumption built into it. A world is then chosen from inside the habitable region, and the
reason for the choice is recorded.

**Rationale:** It is the only option that makes habitability falsifiable rather than assumed. Fixing
by fiat risks producing no world at all; tuning guarantees a world but forfeits the claim that it was
found rather than built — and that claim is the entire point of deriving the physics instead of
importing it. Scanning costs the most work and yields a map of which two-dimensional worlds can
support a lit, stable surface, which is itself among the more interesting results the project could
produce.

**Consequences for the architecture** — these are load-bearing and are recorded in MEMORY.md:
- The simulation must run in **two fidelities**: a cheap screening model evaluated over the whole
  grid, and the full layer stack for a chosen point. A design that only supports the full stack
  cannot scan.
- Determinism becomes a stronger requirement, not a nicety: every grid point is a parameter tuple
  plus a seed and must be exactly reproducible for its result to mean anything.
- Scan results are a **data product** — they persist, they are versioned against the code that
  produced them, and a scan run against changed physics is a different scan.

**Copied to MEMORY.md:** yes

---

### DECISION-010 — Derive Kell, or stub its luminosity?

**Status:** resolved
**Raised:** 2026-09-03 — Session 3
**Resolved:** 2026-09-05 — Session 5

**Question:** Is the star derived from 2D stellar structure, or treated as a boundary condition so
the planet can be built sooner?

**Outcome:** **Stubbed, behind the real interface** (option C). The star's public surface is defined
now and implemented as an input; the structure solve arrives later without callers changing.

**Rationale:** It reaches terrain in a session or two rather than a week, and — the part that makes
it more than a shortcut — it composes cleanly with DECISION-009. Under a scan, a stubbed luminosity
is simply **another axis of the parameter sweep** rather than a placeholder to be embarrassed about.
Deriving Kell later does not invalidate the scan; it *collapses a dimension of it*, by predicting
luminosity from stellar mass instead of sweeping it independently. That is a strictly better position
to derive the star from, because by then there will be a map showing which luminosities matter.

**Binding conditions on the stub** — without these it is the bad kind of shortcut:
- The luminosity is tagged as an **abstraction in `docs/AXIOMS.md` §4**, never as a derived quantity.
- The stub **raises** when asked for anything it cannot honestly supply — spectrum, radius, lifetime,
  evolution. It never returns a plausible default. A stub that answers everything is never revisited.
- Any result depending on it is reported as a consequence of a chosen parameter, not a finding about
  two-dimensional physics.

**Copied to MEMORY.md:** yes

---

### DECISION-011 — Is electromagnetism modelled or abstracted?

**Status:** resolved
**Raised:** 2026-09-03 — Session 4
**Resolved:** 2026-09-03 — Session 4

**Question:** Does Vellum have an explicit electromagnetic field, or is light and material behaviour
supplied as an effective theory?

**Outcome:** Abstracted. There is no Maxwell solver. Radiative transport and material cohesion are
posited at Tier 2 with declared parameters, recorded in the abstraction ledger at
`docs/AXIOMS.md` §4. The interface is shaped so EM could be added later.

**Rationale:** A 2D Maxwell solver is a project in itself and still yields no chemistry, because
T1.3 abstracts matter's microstructure regardless. The cost is that light is posited rather than
derived — acceptable only because it is declared: any module standing in for EM carries an
`Abstracts:` line and must raise rather than return a plausible default where it cannot honestly
answer.

If it is ever added, 2D changes EM substantially: the magnetic field is a scalar rather than a
vector, the photon has one polarization state instead of two, and the electric force falls as `1/r`.

**Copied to MEMORY.md:** yes

---

### DECISION-006 — What the project is for

**Status:** resolved
**Raised:** 2026-09-03 — Session 1
**Resolved:** 2026-09-03 — Session 3

**Question:** Is Vellum a finished monograph to extend, a worldbuilding corpus, or the design
substrate for a simulation?

**Outcome:** A simulation, built slowly, starting with the world. The physics is derived from first
principles rather than taken from the monograph.

**Rationale:** User direction: *"we will discover our own physics. we are the ones doing the sim."*
This inverts the relationship between the two artefacts — the monograph becomes a prior hypothesis
and an eventual output target, and the simulation becomes the authority.

**Copied to MEMORY.md:** yes

---

### DECISION-001 — Runtime and language

**Status:** resolved
**Raised:** 2026-09-03 — Session 1
**Resolved:** 2026-09-03 — Session 3

**Question:** What does the simulation run on?

**Outcome:** Python 3.11+ with numpy, scipy, matplotlib, pytest, mypy, ruff. Simulation in `sim/`;
the monograph stays a separate self-contained document with no build step. No game engine, ECS, or
simulation framework.

**Rationale:** Vellum's structures are 1D periodic arrays, which is numpy's native domain. Two
properties make the fit unusually good. First, the atmosphere is genuinely two-dimensional, so an
FFT-based 2D vorticity solver *is* the atmosphere rather than an approximation of one. Second,
nothing passes anything on the surface, so an array of bodies sorted by position stays sorted
permanently — the array index is a complete spatial index that never needs rebuilding. The usual
reason to avoid Python for simulation (per-agent loops do not vectorise) largely does not apply.

**Copied to MEMORY.md:** yes

---

### DECISION-002 — Test framework and what gets tested

**Status:** resolved
**Raised:** 2026-09-03 — Session 1
**Resolved:** 2026-09-03 — Session 3

**Question:** What runs the tests, and what do they assert?

**Outcome:** `pytest`, in `sim/tests/`, mirroring the source tree. Three test kinds, in order:
dimensional (2D units are correct), invariant (conservation, boundedness, topology, ordering,
finiteness — true for every world and seed), and regression (a seeded world is byte-reproducible).
No test may assert a number taken from the monograph.

**Rationale:** The earlier plan was to make the monograph's numbers an executable test suite. The
Session 3 reframe makes that exactly wrong — it would lock the simulation to a guess and disguise
the lock as verification. Invariants are the durable version: they hold across every world, they
catch real bugs, and they do not presuppose the answer.

The monograph's navigator remains untested. It is frozen reference material now, so retrofitting
tests is not worth a session; if it is ever regenerated, the generator gets the tests instead.

**Copied to MEMORY.md:** yes

---

### DECISION-003 — File size limit

**Status:** resolved
**Raised:** 2026-09-03 — Session 1
**Resolved:** 2026-09-03 — Session 3

**Question:** What is the maximum line count for a file?

**Outcome:** 300 lines for code. No limit for documents.

**Rationale:** A line limit on prose splits an argument at an arbitrary point. Code has no such
excuse, and 300 lines is a reasonable ceiling for a numerical module — past that, a physics module is
usually doing two things.

**Copied to MEMORY.md:** yes

---

### DECISION-005 — Does the monograph stay a single file?

**Status:** resolved
**Raised:** 2026-09-03 — Session 1
**Resolved:** 2026-09-03 — Session 3

**Question:** Does `vellum-monograph.html` remain one self-contained file as it grows?

**Outcome:** Yes. It stays a single file with no build step, opening from `file://`. Generated plates
are written into it as inline SVG, not linked as external assets.

**Rationale:** The property that makes the document durable is that it needs nothing installed to
open. That matters more once it becomes a generated artefact, not less: a document produced by a
simulation should still be readable by someone who has neither the simulation nor a server.

**Copied to MEMORY.md:** yes
