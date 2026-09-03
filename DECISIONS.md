# DECISIONS.md — Vellum (2d_world)

Tracks architectural and design questions that are open, deferred, or resolved.

Rules:
- Every open decision blocks implementation of the code it affects.
- The AI must not implement anything that depends on an open decision.
- When a decision is resolved, move it to the RESOLVED section and record the outcome.
- Once resolved, copy the outcome to MEMORY.md as an architectural decision.

---

## OPEN — Requires human input before implementation

### DECISION-009 — Which dimensionless ratios define a world, and how are they chosen?

**Status:** open
**Raised:** 2026-09-03 — Session 3. Reframed 2026-09-03 — Session 4.
**Resolved by:** human
**Blocks:** Any world instantiation. Does not block the units layer or the axioms themselves.

**Question:** Session 4 settled the axiom tiers and adopted natural units, which dissolves the
original form of this question. There is no longer a value of `G₂` or `σ₂` to choose — both are 1 by
construction, and the reference mass and length fix the remaining scales (`docs/AXIOMS.md` §2). What
is left is the only thing that was ever physical: **the dimensionless ratios that characterise a
particular Vellum.**

Candidates: Kell's mass to Vellum's; orbital radius to planetary radius; atmospheric scale height to
radius; thermal to gravitational binding energy; the atmosphere's Reynolds number.

**9a — how are those ratios chosen?**
- A) **Fixed by fiat, habitability discovered.** Pick a set, run, and find out whether a living world
  is even possible. Honest, and the result means something — but there may be no Vellum at the end.
- B) **Tuned so a habitable world exists.** Guarantees a world; costs the claim that it was found
  rather than built.
- C) **Scanned.** Treat habitability as output: sweep the ratios, map which regions give a stable lit
  surface, then pick a world from inside that region and record why. Most work, best answer, and it
  turns "why is Vellum like this" into a plot rather than an assertion.

**9b — is chemistry given any representation?** T1.3 abstracts matter entirely, so composition is
currently a small set of bulk species with assumed properties. Confirm that is enough, or decide what
minimal representation is needed.

**9c — is radiative transfer grey or spectral?** Grey is far cheaper and adequate for a first
climate; spectral is needed only if composition is ever to matter qualitatively. Given T1.2 abstracts
electromagnetism, spectral transfer would be false precision on top of a posited layer — grey is
probably right until that changes.

**Notes:** 9a is the real fork, and it is philosophical as much as technical: one direction makes
Vellum found, the other makes it designed. Recommend C — the habitability map is itself one of the
more interesting results available, and it is the only option that makes the answer falsifiable.

---

### DECISION-010 — Derive Kell, or stub its luminosity?

**Status:** open
**Raised:** 2026-09-03 — Session 3
**Resolved by:** human
**Blocks:** The build order after the units layer. Does not block the units layer itself.

**Question:** Is the star derived from stellar structure in 2D, or treated as a boundary condition
with an assumed luminosity so the planet can be built sooner?

**Options:**
- A) **Derive Kell first.** 2D hydrostatic equilibrium and radiative transport under `T³`, producing
  luminosity, radius, and lifetime as results. Nothing downstream rests on an invented constant, and
  a 2D star is genuinely unexplored territory. Roughly a week before anything looks like a world.
- B) **Stub the luminosity, build the planet, derive Kell later.** Terrain and water within a session
  or two. The risk is the usual one: a stub that works is rarely revisited, and every downstream
  number inherits an arbitrary constant.
- C) **Stub it behind the real interface.** Define the star's public surface now, implement it as a
  constant, and swap in the derivation later without touching callers. Mitigates B's risk if — and
  only if — the stub raises loudly rather than returning a plausible default.

**Notes:** The user's stated preference is to build slowly, which favours A. Recommend A if the
appetite is there, C if you want to see terrain this week. If C, the stub value must be tagged as an
axiom in `docs/AXIOMS.md` so it cannot quietly become a derived-looking number.

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
