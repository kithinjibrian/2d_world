# CONTEXT.md — Vellum (2d_world)

Session handoff file. Updated at the end of every session.
Read at the start of the next session alongside CLAUDE.md, MEMORY.md, and DECISIONS.md.

Every session has a name and a state: open | closed.
A session is closed only after CONTEXT.md is committed and pushed.

---

## SESSION 1 — 2026-09-03 — Context system setup — closed

Branch: setup/context-system

### WHAT WAS DONE

Built the full context engineering system described in `setup.md` and tailored it to this repo
rather than leaving the guide's placeholders in place.

The repo held only a GPL licence, a one-line README, and an untracked `vellum-monograph.html` — an
18-slide, 17-plate natural history of Vellum, self-contained, no build step. There was no source
code, no package manager, and no tests, so the guide's TypeScript-shaped rules (Result types,
service/controller layers, npm commands) had nothing to attach to.

The user chose "documents now, code later" with unknowables recorded as open decisions rather than
guessed. So the code-specific rules are present but explicitly marked `[CODE — BLOCKED]` and inert
until DECISION-001 resolves, and every value that could not be read from the repo became a numbered
open decision instead of an invented default.

The substantive work was reading the monograph in full and deriving real project rules from it. The
result is a **CANON RULE** — the seven kinds of life, the fixed numbers, and six structural
prohibitions (no third direction, no sight or colour, no closed ring of tissue, no tunnel networks,
the profile test) — plus a design system documenting the eight colour tokens that genuinely exist
and, honestly, the two places where the document does not follow its own rules.

Three real defects were found while reading and recorded rather than fixed, since fixing them was
outside this session's scope:
- The navigator's `roman` array is hardcoded to 18 entries; a 19th slide gets an `undefined` label
  with no error.
- The SVG plate classes hardcode hex values instead of referencing the colour tokens.
- TOC buttons are built with `innerHTML`; safe only while every `data-t` is author-written.

### FILES CREATED OR MODIFIED

    CLAUDE.md                        — behavioral rules; canon rule, architecture rules, anti-patterns,
                                       known issues; code rules present but marked [CODE — BLOCKED]
    MEMORY.md                        — six resolved decisions derived from the monograph as it stands
    CONTEXT.md                       — this file; session log
    DECISIONS.md                     — six open decisions, two deferred
    CHANGELOG.md                     — 0.1.0 records the monograph; Unreleased records this system
    README.md                        — rewritten from one line to a project and system orientation
    .llmignore                       — protected paths, in sync with CLAUDE.md
    PRPs/TEMPLATE.md                 — PRP template, extended with a mandatory canon check
    PRPs/DISCOVERY.md                — interview protocol; question 7 stops on any missing fact
    docs/DESIGN.md                   — real tokens, the 14 existing font sizes, plate SVG classes
    docs/CODE_STYLE.md               — documentation rules; adds Layer 3, canon references
    docs/source/README.md            — how the raw-context layer is used, and by whom
    docs/source/*/TEMPLATE.md        — meeting, research, stakeholder, constraint templates
    docs/specs|decisions|incidents|status/README.md — document structures, locked before writing
    reports/TEMPLATE.md              — EOD report template
    reports/2026-09-03.md            — this session's EOD report

`vellum-monograph.html` was read in full but not modified, and is now tracked.

### TESTS WRITTEN

None. There is no test runner and adding one is DECISION-002. The navigator is the only testable
code in the repo; four behaviours worth asserting are listed in that decision entry.

Verification performed instead: every colour token, font size, and SVG class documented in
`docs/DESIGN.md` was extracted from the stylesheet rather than recalled, and every canon fact in
CLAUDE.md was quoted from the monograph text.

### DECISIONS MADE

- The project is documents now, code later — code rules written but blocked, rather than omitted or
  activated against an unchosen stack (MEMORY.md #6).
- `vellum-monograph.html` is the canon, and an absent fact is a decision rather than a detail
  (MEMORY.md #5). This is the rule the rest of the system exists to enforce.
- Unknowable values were not defaulted. No file-size limit, test runner, or stack was invented.
- The guide's `CLAUDE.md` template was not copied verbatim. Rules that could not answer "what
  mistake does this prevent?" for this repo were replaced with ones derived from the monograph.
- `setup.md` is treated as external reference material, listed in `.llmignore` and never edited.

### PENDING DECISIONS OPENED

- DECISION-001 — Runtime and language for simulation code (blocks all code)
- DECISION-002 — Test framework, and whether the navigator is retrofitted with tests
- DECISION-003 — File size limit (recommendation recorded: no limit for documents, 300 for code)
- DECISION-004 — Whether to tokenise the type scale (recommendation recorded: freeze and document)
- DECISION-005 — Whether the monograph stays a single file (recommendation recorded: yes)
- DECISION-006 — What the project is actually for — blocks prioritisation of everything
- DECISION-007 — Accessibility target (deferred)
- DECISION-008 — Publishing and hosting (deferred)

### STILL OPEN AT CLOSE

- **Not pushed.** The branch `setup/context-system` is committed locally only. The remote is
  `git@github.com:kithinjibrian/2d_world.git`; pushing needs the user's go-ahead.
- Git identity was unset in this repo and was configured locally (not globally) as
  `kithinjibrian <brian.kithinji@massa-advisors.ai>`. Correct it if that is the wrong authorship.
- Six open decisions block essentially all downstream work. DECISION-006 is the one that matters.
- The three defects listed above are recorded, not fixed. Each needs a PRP.
- The DESIGN RULE is only partially enforceable until DECISION-004 resolves.

---

## SESSION 2 — 2026-09-03 — Git identity correction — closed

Branch: setup/context-system

### WHAT WAS DONE

Resolved the authorship item left open at the close of Session 1.

Git had no identity configured on this machine, so Session 1 set one repo-locally as a stopgap and
flagged it for correction. The user supplied the correct address. The identity is now set globally
in `~/.gitconfig` as `kithinjibrian <kithinjibrian369@gmail.com>`, and the repo-local override was
removed so the global value actually applies here rather than being shadowed.

Session 1's two commits were re-authored to match. Both were local and unpushed, so the rewrite was
safe; the initial commit `d535259` is the user's own and was left untouched. Commit hashes for the
two session commits changed as a result — `e86d716` → `ad71b42` and `54b08da` → `9e4087d`.

Session 1's entry above still records the old address. That is deliberate: past sessions are
append-only under the PROTECTED FILES rule in CLAUDE.md, so the record stands as written and this
entry supersedes it.

### FILES CREATED OR MODIFIED

    CONTEXT.md    — this entry
    ~/.gitconfig  — global user.name and user.email (outside the repo)

No project file changed. CHANGELOG.md was deliberately not updated: nothing observable shipped, and
the CHANGELOG rule excludes changes a reader cannot see or feel.

### TESTS WRITTEN

None. Verified directly instead: `git config --get user.email` resolves to the global value with no
local override, and `git log --format='%an <%ae> | %cn <%ce>'` shows both author and committer
corrected on both commits.

### DECISIONS MADE

- The identity is global, not repo-local, since the user asked for it to be permanent.
- Session 1's commits were rewritten rather than left with the wrong author, because they were
  unpushed and created in this session. Nothing that had left the machine was touched.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- **Still not pushed.** The branch `setup/context-system` is local only. Remote is
  `git@github.com:kithinjibrian/2d_world.git`.
- Everything else carried over from Session 1: six open decisions, DECISION-006 the blocking one,
  and three recorded defects each needing a PRP.

---

## SESSION 3 — 2026-09-03 — Simulation reframe — closed

Branch: setup/context-system

### WHAT WAS DONE

Reversed the central rule of the system built in Session 1, on user direction: *"don't worry about
the monograph. we will discover our own physics. we are the ones doing the sim."*

Session 1 made `vellum-monograph.html` the canon and every fact in it binding. That is now
backwards. The simulation is the authority; the monograph is a prior hypothesis written before
anything was checked, and an eventual output target. The CANON RULE is replaced by a **DERIVATION
RULE**: every quantity is an axiom, a world constant, or a derived result, and carries a reference
saying which. That discipline is what replaces the monograph as the thing keeping the world honest —
without it, "we derive our own physics" degrades into typing in whatever number looks right, and the
degradation is invisible because the code still runs.

Created `docs/AXIOMS.md` as the new anchor. Section 1 (the axiom list) is DRAFT pending DECISION-009.
Sections 2 and 3 are settled and were the substantive work of the session: the dimensions of
physical quantities in 2D, and the consequences already derivable from two dimensions — no escape
velocity, no atmospheric escape at all, `1/r` flux, `T³` emission, ~105° of apsidal regression per
orbit, the inverse turbulent cascade, wave tails from the failure of Huygens' principle in even
dimensions, recurrent random walks, and the topological prohibitions on rings and tunnels.

Two findings worth carrying forward. **Dimensions are the project's most dangerous silent failure:**
in 2D, density is kg·m⁻², pressure is N·m⁻¹, and `G₂` is m²·kg⁻¹·s⁻² — a 3D constant used here does
not crash, it produces a plausible float that means nothing and surfaces three modules later as an
untraceable climate number. Hence a units layer as module zero, with dimensional tests written
before any physics. **And the earlier "canon as test suite" plan was exactly wrong** under the new
frame: asserting monograph numbers would lock the simulation to a guess and disguise the lock as
verification. Tests now assert invariants — conservation, boundedness, topology, ordering,
finiteness — which hold for every world and every seed and do not presuppose the answer.

Resolved five decisions and opened two.

### FILES CREATED OR MODIFIED

    docs/AXIOMS.md        — NEW. Axioms (draft), 2D dimensions table, established consequences
    CLAUDE.md             — CANON RULE → DERIVATION RULE; TESTING and ERROR HANDLING unblocked and
                            rewritten for Python; stack, commands, architecture, anti-patterns
    MEMORY.md             — eight decisions, replacing the six read out of the monograph
    DECISIONS.md          — 001/002/003/005/006 resolved; 009 and 010 opened; 004 reprioritised
    docs/CODE_STYLE.md    — rewritten for Python; Layer 3 is now derivation references, not plate
                            references; numerical-code rules added
    PRPs/TEMPLATE.md      — canon check → derivation check; test section split three ways
    PRPs/DISCOVERY.md     — question 7 now asks which axioms, and whether a new free parameter
    README.md             — rewritten around the simulation and the 2D physics
    CHANGELOG.md          — Unreleased updated
    .llmignore            — Python caches, generated worlds, lockfiles; monograph marked frozen
    CONTEXT.md            — this entry

No simulation code was written. `sim/` does not exist; it arrives with the first approved PRP.

### TESTS WRITTEN

None — there is nothing to test yet. The testing *policy* changed substantially and is recorded in
the TESTING RULE in CLAUDE.md and in DECISION-002.

Verification performed: the apsidal-precession result was derived from the effective potential
rather than recalled. For `F ∝ 1/r`, the radial and angular frequencies stand in the ratio `√2`, so
the apsidal angle is `π/√2 ≈ 127.3°`, successive perihelia are `254.6°` apart, and the apsis line
regresses ~105° per orbit — seasons cycle in ~3.4 orbits, not the monograph's ~900 years. This is
also confirmed qualitatively by Bertrand's theorem, which permits closed orbits only for inverse-
square and harmonic laws. **The first orbital integrator should re-confirm this numerically before
anything is built on it.**

### DECISIONS MADE

- DECISION-006 resolved: simulation, built slowly, physics derived from first principles.
- DECISION-001 resolved: Python 3.11+, numpy/scipy/matplotlib/pytest/mypy/ruff, no framework.
- DECISION-002 resolved: pytest; dimensional, invariant and regression tests; no monograph numbers.
- DECISION-003 resolved: 300 lines for code, no limit for documents.
- DECISION-005 resolved: the monograph stays a single self-contained file.
- Result types rejected for Python — exceptions plus `mypy --strict` instead. The Result pattern
  earns its ceremony against a compiler that checks exhaustiveness; Python has none, so it costs
  readability and returns nothing.

### PENDING DECISIONS OPENED

- DECISION-009 — the axiom set. Specifically 9a: are `G₂` and `σ₂` fixed by fiat with habitability
  left as a discovered outcome, tuned so a habitable world is guaranteed, or scanned as a parameter
  space? Recommendation: scan. This is philosophical as much as technical — one direction makes
  Vellum found, the other makes it designed.
- DECISION-010 — derive Kell from 2D stellar structure first, or stub its luminosity behind a real
  interface and reach terrain sooner? Recommendation: derive, given the stated intent to go slowly.

### STILL OPEN AT CLOSE

- **Still not pushed.** Branch `setup/context-system` is local only.
- DECISION-009 and DECISION-010 both gate the layer order, though neither blocks the first PRP.
- `docs/AXIOMS.md` §1 is DRAFT and labelled as such.
- The monograph's three recorded defects are unchanged and now lower priority — it is frozen, and
  the natural moment to fix them is when it is regenerated.

---

## SESSION 4 — 2026-09-03 — Tiered axioms — closed

Branch: setup/context-system

### WHAT WAS DONE

Restructured `docs/AXIOMS.md` from a flat list of six axioms into three tiers, on user direction:
define a few fundamental forces and let the rest follow, with electromagnetism abstracted for now.

**Tier 0** is geometry and mechanics — two dimensions, Newtonian mechanics, a non-relativistic
regime. **Tier 1** is the fundamental interactions — gravity, plus explicit declarations that
electromagnetism and matter's microstructure are *not* modelled. **Tier 2** is the effective
theories — thermodynamics, radiation, fluids, solids — each with a form the geometry constrains and
parameters that are world constants.

The tiering carries one correction to the user's framing, recorded because it will otherwise be
rediscovered: **the chain from fundamental forces up to a climate is not computable**, in any number
of dimensions. Nobody derives Navier–Stokes by simulating molecules. So the honest structure is not
one fundamental layer generating everything but a stack of effective theories, and the thing that
keeps that honest is each tier declaring what it *cannot* derive. Those declarations are collected
in a new **abstraction ledger** (§4) — the single place recording everything posited rather than
derived, so a result reflecting a choice can never be reported as a finding about 2D physics.

**Gravity.** The user's instinct that gravity must be a direct attractive force was right, and for a
stronger reason than stated. Geometric gravity is not merely awkward in 2D — it is empty. The
graviton carries `d(d−3)/2` propagating degrees of freedom, which is exactly zero at d=3. In three
dimensions the Riemann tensor is algebraically determined by Ricci (there is no Weyl tensor), so
vacuum forces both to vanish and spacetime is flat wherever there is no matter. A point mass
produces only a conical defect; masses in that geometry feel nothing, and nothing orbits
(Deser–Jackiw–'t Hooft 1984). Doing gravity "properly" with GR in 2D yields no gravity at all, so it
must be postulated. Recorded in T1.1 and MEMORY.md decision 4 specifically so a future session does
not spend a week discovering it.

**Units.** The user's concern that picking units and dimensions would be hard turned out to be
largely dissolvable. There is no correct SI value for another universe's constant, so the project
now works in natural units: `G₂ ≡ 1`, `σ₂ ≡ 1`, with a chosen reference mass and length fixing the
rest — `[G₂] = L²M⁻¹T⁻²` fixes the time unit as `L_ref/√M_ref`, and `[σ₂] = MLT⁻³Θ⁻³` then fixes
temperature. Two reference choices and two normalisations fix all four base units. What survives is
the only thing that was ever physical: **dimensionless ratios**. That reframes DECISION-009 from
"invent magnitudes" to "choose a handful of ratios", which is both tractable and scannable, and it
reduces the units layer from a design problem to mechanical bookkeeping.

One consequence worth carrying: in natural units a dimensional slip is *easier* to miss, because the
offending constant is 1. So the dimensional tests must also assert that dimensionless results really
are dimensionless.

### FILES CREATED OR MODIFIED

    docs/AXIOMS.md        — restructured into tiers; natural-units section; abstraction ledger;
                            T1.1 rewritten with the 2+1D GR argument
    CLAUDE.md             — tiered axiom references; two new DERIVATION RULE prohibitions (no SI
                            outside display, no posited result presented as a discovery); a new
                            anti-pattern; a fourth derivation-reference form for abstracted layers
    MEMORY.md             — decisions 3–6 replaced and expanded: tiered axioms, postulated gravity,
                            natural units, abstracted EM. Renumbered to 11, cross-refs fixed
    DECISIONS.md          — 009 reframed around dimensionless ratios; 011 opened and resolved
    docs/CODE_STYLE.md    — `Abstracts:` line required; fourth reference form; natural-units rule
    PRPs/TEMPLATE.md      — derivation check gains abstraction and natural-units criteria
    PRPs/DISCOVERY.md     — new question 8 on the abstraction ledger
    README.md, CHANGELOG.md, CONTEXT.md

No simulation code. `sim/` still does not exist.

### TESTS WRITTEN

None. Two derivations were done by hand and both should be re-confirmed in code:
- The 2+1D graviton count, `d(d−3)/2 = 0`, cross-checked against the Riemann/Ricci component count
  in three dimensions (6 and 6, no Weyl tensor).
- The natural-units scheme closes: `G₂ = 1` fixes `T_ref = L_ref/√M_ref`, and `σ₂ = 1` then fixes
  the temperature unit. This should be asserted directly in the units layer's tests.

### DECISIONS MADE

- DECISION-011 resolved: electromagnetism abstracted, not modelled.
- Axioms are tiered, and each tier declares what it cannot derive.
- Natural units adopted; SI confined to the display layer.
- Gravity is postulated rather than geometric, for the reason above.

### PENDING DECISIONS OPENED

None new. DECISION-009 was reframed rather than opened — it is now about which dimensionless ratios
define a world and whether they are fixed, tuned or scanned.

### STILL OPEN AT CLOSE

- **Still not pushed.** Branch `setup/context-system` is local, now eight commits.
- DECISION-009 (dimensionless ratios; fixed, tuned or scanned) and DECISION-010 (derive Kell or stub
  it) remain open. Neither blocks the first PRP.
- The apsidal precession result and the graviton count are hand derivations awaiting numerical
  confirmation.

---

## SESSION 5 — 2026-09-05 — Scan and stub resolved — open

Branch: setup/context-system

---

## NEXT SESSION START POINT

Open a new session entry in this file first, with state `open` and the branch name, and commit it.

Then read CLAUDE.md, MEMORY.md, DECISIONS.md, and this file — in that order. Then read
`docs/AXIOMS.md` in full; it was restructured in Session 4 and is the anchor for everything.

**Write the PRP for the units layer.** Session 4 made it much smaller than it first looked: natural
units remove the need to invent any magnitude, so the module is mechanical — fix the base dimensions
(mass, length, time, temperature), express everything else as a product of powers, check it
automatically. Its tests are dimensional assertions written before any physics, and they must include
that dimensionless results really are dimensionless, since in natural units a slip hides behind a
constant equal to 1. It is unblocked by both open decisions.

Two questions for the user when convenient, neither blocking that PRP:
- **DECISION-009a** — are the dimensionless ratios defining a world fixed, tuned, or scanned?
  Recommendation: scanned.
- **DECISION-010** — derive Kell from 2D stellar structure, or stub its luminosity behind a real
  interface and reach terrain sooner?

Layer order after the units layer: star → orbit → planet → surface → water → air → life. Do not
start a layer before the one below it passes its invariant tests.

Do not edit `vellum-monograph.html`. It is frozen; it gets regenerated, not corrected.
