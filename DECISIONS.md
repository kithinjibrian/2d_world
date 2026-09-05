# DECISIONS.md — Vellum (2d_world)

Tracks architectural and design questions that are open, deferred, or resolved.

Rules:
- Every open decision blocks implementation of the code it affects.
- The AI must not implement anything that depends on an open decision.
- When a decision is resolved, move it to the RESOLVED section and record the outcome.
- Once resolved, copy the outcome to MEMORY.md as an architectural decision.

---

## OPEN — Requires human input before implementation

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

### DECISION-017 — Is terrain a raster, or a field evaluable at any resolution?

**Status:** resolved
**Raised:** 2026-09-05 — Session 10
**Resolved:** 2026-09-05 — Session 12

**Question:** Is `h(s)` a sampled array, or represented so it can be evaluated at arbitrary position
and arbitrary resolution?

**Outcome:** **Both** (option C) — an **evaluable procedural base field plus a sampled residual**.
The base is queried at whatever resolution the caller needs; the residual is a sampled array added
on top, for anything that modifies the ground after generation.

**But not by spectral synthesis, which was the recommendation and does not work at this scale.**
A Fourier sum over integer wavenumbers gives exact periodicity for free, which is why it was
proposed — but resolving detail of wavelength `λ` on a surface `C` around needs `C/λ` coefficients,
and it costs `O(k)` per sample. Measured while writing the PRP:

| target detail | Fourier coefficients | fBm octaves |
|---|---|---|
| 10 km | 3,840 | 12 |
| 100 m | 384,000 | 19 |
| **1 m** | **38,400,000** | **26** |

Metre detail on a 38,400 km surface needs 38 million coefficients. It is not tractable, and the
"regenerate detail at any zoom" property the whole decision rests on would have been lost at the
first serious zoom.

The base field is therefore **periodic multi-octave gradient noise (fBm)**: a seeded integer hash on
a lattice whose index is taken modulo the octave's cell count, so periodicity is still exact by
construction, while cost is `O(octaves)` — about 26 hash evaluations for metre detail, independent
of position. It keeps every property that motivated option A and drops the one that made it
impossible.

**Rationale for the residual half:** the impact cycle is, in the monograph's phrase, the metronome
of Vellum's biology, and erosion follows water. Both modify the ground after it is generated, and
neither can be expressed by changing a noise coefficient. A sampled residual is the only way to
represent "this crater is here now", and it costs nothing while it is empty.

**Consequences:**
- Terrain has a **resolution floor**: `C / 2^octaves`. It is finite, must be reported, and the layer
  must say what it is rather than silently returning smooth ground below it.
- **Terrain statistics are abstracted, not derived.** Nothing in `docs/AXIOMS.md` predicts a
  roughness exponent — that would need tectonics and erosion, which are not modelled. Roughness and
  amplitude are world constants, and a new entry goes in the §4 ledger. Any result depending on the
  shape of the ground is a consequence of a choice.

**Copied to MEMORY.md:** yes

---

### DECISION-016 — A viewer, and the dependency it needs

**Status:** resolved
**Raised:** 2026-09-05 — Session 10
**Resolved:** 2026-09-05 — Session 10

**Question:** The user wants to zoom continuously from the whole system down to the planet's ground.
Where does that render, and when is it built? The STACK in CLAUDE.md is closed, so a rendering
dependency is a decision rather than an implementation detail.

**Outcome:** A **desktop window using `pygame-ce`**, built as a **skeleton now** and grown as each
layer lands. `pygame-ce` is added to STACK; it is the first dependency added since the project
began.

**Rationale:** User direction on both forks. `pygame-ce` over `pyglet` because pyglet is OpenGL-based
and its pipeline is float32, which fights the central difficulty here — spanning eleven orders of
magnitude from system scale to ground demands float64 throughout. With SDL2 all camera arithmetic
stays in Python floats and only integer pixels reach the renderer, so precision is a Python concern
and stays solvable.

Building the skeleton before the layers it will display is deliberate: every subsequent layer becomes
visible the moment it lands, so terrain, water and air get looked at while they are being built
rather than afterwards. For a project whose entire subject is what a two-dimensional world looks
like, that feedback is worth more than the throwaway iterations it costs.

**Consequences:**
- STACK gains `pygame-ce`. The list is closed again after it.
- The viewer's logic must be **testable headless** — the camera and transforms are pure functions
  with no pygame import, and the drawing layer stays thin enough to be trivially correct.
  `SDL_VIDEODRIVER=dummy` covers what remains.
- Rendering must be **camera-relative**. Never transform an absolute world coordinate: at a focus
  1e11 m from the origin, a metre of detail is below float64's resolution of the absolute value but
  well within it for a relative one.
- It raises DECISION-017: terrain must be decided as a raster or an evaluable field before the
  surface layer is written.

**Copied to MEMORY.md:** yes

---

### DECISION-015 — Where does dimension checking happen?

**Status:** resolved
**Raised:** 2026-09-05 — Session 6
**Resolved:** 2026-09-05 — Session 7

**Question:** Are dimensions carried at runtime by every quantity, or checked only at boundaries and
in tests?

**Outcome:** **At module boundaries.** `Quantity` pairs a magnitude with a `Dimension` and is what
public functions accept and return; `Quantity.magnitude(expected)` validates and unwraps to a plain
float or array for the numerics inside. Kernels stay raw numpy.

**Rationale:** The failure this layer exists to catch — a constant or a formula composed with the
wrong dimensions — happens at definition and composition, which are exactly the boundaries. It does
not happen inside a loop already holding correct arrays. So boundary checking catches essentially
the whole risk class at one check per call rather than one per element, which matters because
DECISION-009 multiplies any inner-loop cost by the size of the parameter scan.

Naming the expected dimension at the unwrap site turned out to be the load-bearing part, not an
inconvenience: it makes the caller state what it believes it is holding, and that belief is what
gets checked.

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
