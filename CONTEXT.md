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

## SESSION 5 — 2026-09-05 — Scan and stub resolved — closed

Branch: setup/context-system

### WHAT WAS DONE

Resolved the two decisions that were gating the layer order. User direction: *"scanned. and stub
kell for now."*

**DECISION-009 — scanned.** The dimensionless ratios defining a world are swept over a grid, and
habitability is an output of the sweep rather than an assumption built into it. This is the choice
that makes habitability falsifiable: fixing the ratios risks producing no world at all, tuning them
guarantees one but forfeits the claim that Vellum was found rather than built.

The consequences are architectural and load-bearing, so they were written into CLAUDE.md as rules
rather than left as intent. **Every layer now needs two fidelities** — a cheap screening path
evaluated over the whole grid, and the full solve for a chosen point. A layer that supports only the
full solve cannot be scanned, and retrofitting a screening path afterwards means rewriting it, so
both get designed at once and the PRP must state what the screening model neglects and why that is
safe for pruning. **Determinism stops being a nicety** and becomes load-bearing, since each grid
point is a parameter tuple plus a seed and an irreproducible point is a meaningless one. **Scans
become versioned data products**, stamped with the code version and grid that produced them — a scan
run against changed physics is a different scan, never an update.

**DECISION-010 — stubbed, behind the real interface.** The observation that makes this more than a
shortcut: under a scan, a stubbed luminosity is not a placeholder but simply **another axis of the
sweep**. Deriving Kell later does not invalidate the scan, it *collapses a dimension of it* by
predicting luminosity from stellar mass instead of sweeping it independently — and it is a better
place to derive a star from than the beginning, because by then there will be a map showing which
luminosities matter.

Three conditions bind the stub, without which it is the bad kind of shortcut: the luminosity is
tagged in the abstraction ledger and never as derived; the stub **raises** for spectrum, radius,
lifetime and evolution rather than returning a plausible default; and any result depending on it is
reported as a consequence of a chosen parameter. A new anti-pattern covers the general case — a stub
that answers everything is never revisited and silently becomes the model.

Split the two leftover sub-questions of the old DECISION-009 into their own entries, and opened the
question the scan immediately implies.

### FILES CREATED OR MODIFIED

    DECISIONS.md          — 009 and 010 resolved; 012 opened (habitability predicate); 013 and 014
                            split out from the old 009b and 009c
    MEMORY.md             — decisions 12 (scanned) and 13 (Kell stubbed) added; state and next-session
                            block rewritten
    CLAUDE.md             — architecture rules 8 and 9 (two fidelities; scans as versioned data
                            products); new anti-pattern 5 on stubs that answer too much
    docs/AXIOMS.md        — status updated; Kell's output declared an input under T2.2; ledger entry
                            for the stubbed luminosity; §2 records that ratios are swept
    CHANGELOG.md          — Unreleased updated
    CONTEXT.md            — this entry
    reports/2026-09-05.md — EOD report

No simulation code. `sim/` still does not exist.

### TESTS WRITTEN

None. Nothing executable exists yet.

### DECISIONS MADE

- DECISION-009 resolved: ratios are scanned; habitability is an output.
- DECISION-010 resolved: Kell stubbed behind its real interface, with binding conditions.

### PENDING DECISIONS OPENED

- **DECISION-012 — what counts as habitable?** Opened because "scanned" is meaningless without a
  predicate deciding which grid points count. Recommendation: liquid water as a cheap coarse screen,
  climate stability layered onto the survivors — the second being the more interesting criterion
  precisely because `T³` emission is a weaker stabilising feedback than the 3D quartic, so a 2D
  climate should be more prone to runaway. Recorded as a **world-selection predicate, not an
  axiom**: it says which worlds interest us, not which worlds exist.
- DECISION-013 — does chemistry get any representation? (was 009b). Sharpened by a consequence
  already in the axioms: with no atmospheric escape at all, composition is strictly cumulative, so
  an atmosphere that only ever accumulates may need more structure than one bulk species can carry.
- DECISION-014 — grey or spectral radiative transfer? (was 009c). Recommendation: grey, since
  spectral detail resting on an abstracted electromagnetism and an abstracted chemistry would be
  false precision rather than more truth.

### STILL OPEN AT CLOSE

- **Still not pushed.** Branch `setup/context-system` is local, ten commits.
- DECISION-012 blocks the scan, though not the units layer.
- The apsidal precession result and the 2+1D graviton count remain hand derivations awaiting
  numerical confirmation.

---

## SESSION 6 — 2026-09-05 — Units layer PRP — closed

Branch: setup/context-system

### WHAT WAS DONE

Wrote `PRPs/units-layer.md`, the first PRP in the project. No code — the PRP rule requires approval
before any is written, and one open decision blocks approval.

The dimensional algebra in the PRP was **derived and checked in a scratch script**, not recalled.
That produced three discriminating tests, each a formula a 3D-trained reflex writes wrongly and
dimensional analysis catches:

- `g = G₂M/r` is an acceleration (`M⁻¹L²T⁻² · M / L = LT⁻²`); the inverse-square form `G₂M/r²` gives
  `T⁻²` and is not.
- `L = 2πR σ₂ T³` is a power (`L · MLT⁻³Θ⁻³ · Θ³ = ML²T⁻³`); the 3D form `4πR²σ₂T⁴` gives `ML³T⁻³Θ`
  and is not.
- `P = ρgh` gives 2D pressure `MT⁻²` with `ρ = ML⁻²`, and 3D pressure `ML⁻¹T⁻²` with `ML⁻³`.

Two findings from the same check, both recorded in the PRP:

- **Reynolds number does not discriminate.** `ρvL/μ` is dimensionless under both the 2D and the 3D
  forms, so it is worthless as a check. It was the obvious candidate for a marquee test and it was
  nearly used as one. The PRP now says explicitly not to add it, and why, so a later session does not
  add it believing it proves something.
- **2D dynamic viscosity is `M T⁻¹`**, not the 3D `M L⁻¹ T⁻¹` — while *kinematic* viscosity is
  `L² T⁻¹` in both. Worth a test precisely because it is the case that does not change: the module
  should not leave a reader believing everything differs in 2D.

The natural-unit closure was confirmed to actually close: `G₂ = 1` forces `T = L/√M`, and `σ₂ = 1`
then forces `Θ = (M L T⁻³)^⅓`, so two display anchors fix all four base units. That becomes an
invariant test.

The PRP's most consequential instruction is a negative one: **define no 3D dimension at all.** Not
`DENSITY_3D`, not an inverse-square helper. A name that exists can be selected by accident; a name
that does not exist cannot. It is the cheapest available enforcement of the anti-pattern the whole
module exists to serve.

### FILES CREATED OR MODIFIED

    PRPs/units-layer.md   — NEW. The first PRP. Blocked on DECISION-015
    DECISIONS.md          — DECISION-015 opened
    CONTEXT.md            — this entry

No code. `sim/` still does not exist.

### TESTS WRITTEN

None — the PRP is not approved, so no implementation exists to test. The test list is written and is
the substance of the PRP.

The dimensional algebra itself was verified in a throwaway script during drafting. That script was
not kept; its results are recorded above and in the PRP, and the real tests will re-derive them.

### DECISIONS MADE

None. One was opened rather than assumed.

### PENDING DECISIONS OPENED

- **DECISION-015 — where does dimension checking happen?** Runtime on every quantity, test-time only,
  or at module boundaries with raw arrays inside kernels. Recommendation: boundaries, because the
  error this module exists to catch happens at definition and composition rather than inside a loop
  already holding correct arrays — and because DECISION-009 multiplies any inner-loop cost by the
  size of the scan. It changes the public API, so it must be answered before approval rather than
  during implementation.

### STILL OPEN AT CLOSE

- **Still not pushed.** Branch `setup/context-system` is local, twelve commits.
- The units PRP awaits DECISION-015 and then explicit approval.
- DECISION-012 still blocks the scan.
- The apsidal precession result and the 2+1D graviton count remain hand derivations awaiting
  numerical confirmation.

---

## SESSION 7 — 2026-09-05 — Units layer implementation — closed

Branch: setup/context-system

### WHAT WAS DONE

DECISION-015 answered (boundaries), `PRPs/units-layer.md` approved, and the units layer implemented
test-first. **This is the project's first code.** 101 tests, `mypy --strict` clean, `ruff` clean.

Tests were written and run before any implementation existed — the first run failed on four
collection errors, which is the correct starting state and is recorded here because a test-first
claim is worth nothing without it.

**The acceptance criterion that mattered was the mutation check**, and it was run rather than
assumed. Each three-dimensional form was substituted in turn and the suite re-run:

    gravity  -> inverse-square          11 failed
    density  -> per volume               5 failed
    emission -> T^4                      8 failed
    flux     -> per area                10 failed
    pressure -> per area                 8 failed
    viscosity-> M L^-1 T^-1              4 failed

Every one is caught. `named.py` was restored byte-identically afterwards and the suite is green.
This is the whole value of the module: it is defined by what it refuses to accept, and a test that
cannot fail would have proved nothing.

**Environment.** Nothing was installed on this machine — no pytest, mypy, ruff or numpy, and no pip
in the stdlib venv (`ensurepip` is absent, as on stock Ubuntu without `python3-venv`). `uv` was
present at `~/.local/bin/uv` with network access, so `.venv/` was created and populated with it.
`uv` is a tool, not a project dependency; `pyproject.toml` declares the real ones and any installer
can read it. Added `.gitignore`, without which the venv would have been committed.

**Two things the type checker and linter caught that are worth recording**, because both are
recurring shapes rather than one-off slips:
- `float ** float` is typed `Any` in typeshed, since a negative base with a fractional exponent is
  complex. `scale_factor` now uses `math.pow`, whose bases are positive by construction. Any future
  module doing exponentiation under `--strict` will hit this.
- A frozen dataclass field annotated `Fraction` makes the *constructor* reject `int`, since the
  generated `__init__` takes the field's declared type. The fields are now `Exponent = Fraction |
  int` with `__post_init__` coercion, and `exponents` is the type-safe accessor returning Fractions.

### FILES CREATED OR MODIFIED

    pyproject.toml             — NEW. Project metadata, pytest/mypy/ruff config
    .gitignore                 — NEW. Caches, .venv, generated worlds
    sim/__init__.py            — NEW
    sim/errors.py              — NEW. VellumError, DimensionError, InvariantError
    sim/units/dimension.py     — NEW. Fraction-exponent dimension algebra
    sim/units/named.py         — NEW. The 2D named-dimension table
    sim/units/quantity.py      — NEW. Boundary type; magnitude() validates and unwraps
    sim/units/system.py        — NEW. Natural units; G2 = 1 and sigma_2 = 1 close the system
    sim/units/constants.py     — NEW. G2 and SIGMA_2 as dimensioned Quantities
    sim/units/__init__.py      — NEW. Public surface
    sim/tests/units/*.py       — NEW. 101 tests across four files
    DECISIONS.md               — DECISION-015 resolved
    MEMORY.md                  — decisions 14 and 15; state and next-session block
    CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

101, in four files, in the three kinds the TESTING RULE requires:

- **Dimensional.** The algebra; the named-dimension table asserted line for line against
  `docs/AXIOMS.md` §2; and the three discriminating cases — `G₂M/r` is an acceleration while
  `G₂M/r²` is not, `2πRσ₂T³` is a power while `4πR²σ₂T⁴` is not, `ρgh` gives 2D pressure only with a
  per-area density. Plus kinematic viscosity as the case that does *not* differ in 2D, and an
  explicit test that no 3D name exists in the registry.
- **Invariant.** Natural-unit closure over five anchor pairs — `G₂` and `σ₂` both evaluate to 1 for
  every one; `T = L/√M` and `Θ = (MLT⁻³)^⅓` confirmed; SI round trip; every base unit and scale
  factor finite; dimensions immutable, hashable, and never mutated by algebra.
- **Regression.** Recorded as not applicable — nothing here is stochastic or generated — so the
  omission reads as deliberate rather than forgotten.

`TestReynoldsDiscriminatesNothing` asserts that `ρvL/μ` is dimensionless under *both* the 2D and 3D
forms. It is a test that documents a non-test, kept so nobody later adds a Reynolds check believing
it proves something.

### DECISIONS MADE

- DECISION-015 resolved: checking at module boundaries.
- `uv` adopted for environment management. Not a project dependency and not added to STACK — it
  installs what `pyproject.toml` declares, and pip would do as well if it existed here.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- **Still not pushed.** Branch `setup/context-system` is local, fourteen commits.
- The apsidal precession result and the 2+1D graviton count remain hand derivations. The orbit
  layer is where precession finally gets checked, and its PRP should make that an acceptance
  criterion.
- DECISION-012 still blocks the scan.
- `scipy` and `matplotlib` are in STACK but not installed; nothing needs them yet.

---

## SESSION 8 — 2026-09-05 — Orbit layer PRP — closed

Branch: sim/orbit-layer

### WHAT WAS DONE

Wrote `PRPs/orbit-layer.md`. No code — it awaits approval.

Before writing it, ran a throwaway integration in the scratchpad to check the predictions the PRP
would be built around, rather than writing a PRP resting on paper derivations. **All five hold**,
and three of them were not previously recorded anywhere:

1. **Circular orbital speed is independent of radius.** `v_c = √(G₂M)`, identical at every distance,
   because a logarithmic potential gives `r·dΦ/dr = G₂M` with no `r` left in it. Verified from
   `r = 0.5` to `r = 50` with a relative radius spread of ~2.5e-9. This is the 2D analogue of a flat
   galactic rotation curve, and it is a striking fact about the world: every circular orbit, however
   far out, moves at the same speed.
2. **Kepler's third law is replaced by `T ∝ r`.** Period is linear in radius, not `r^(3/2)`.
   Fitted exponent 1.0000000000000004.
3. **The apsidal angle is `π/√2 ≈ 127.2792°`**, so pericentre-to-pericentre is `254.5584°` and the
   apsis regresses ≈105.4416° per orbit. Measured `254.5500°` at `v/v_c = 1.02`. The Session 3 hand
   derivation is confirmed.
4. **A season cycles in exactly `2 + √2 ≈ 3.414214` orbits** — a closed form, since
   `360/(360 − 180√2) = 2 + √2`.
5. **Nothing escapes at any speed.** Launched at 100× circular speed the trajectory still turns
   around at finite radius.

**A correction worth recording.** The scratch script mislabelled its own output: it called the
pericentre-to-pericentre sweep the "apsidal angle" and then computed `360 − 2×that`, printing a
nonsensical `−149°/orbit`. The measurement was right; the arithmetic layered on top of it was wrong.
The physics only survived because the raw measured number was compared against the prediction
directly. The PRP now warns about exactly this confusion and requires the function be named for what
it returns.

**Design decisions taken rather than deferred**, each stated in the PRP so they can be argued with:

- **Scope is two-body plus insolation.** Debris and the impact cycle are explicitly excluded to a
  later PRP; including them would double the module and violate the SCOPE RULE. Also excluded:
  N-body, rotation, day length, tides, and obliquity — a disc has no axis to tilt.
- **Velocity-Verlet at fixed timestep, and no adaptive stepping.** Not a preference: a non-symplectic
  integrator *manufactures* apsidal precession, which is the headline quantity being measured. It
  would return a number that looks plausible, is partly numerical, and cannot be told apart from the
  physical answer by inspection. The PRP requires demonstrating this once with forward Euler and
  recording the corrupted number, so the requirement is justified by evidence rather than assertion.
- **A timestep-convergence test is mandatory**, without which prediction 3 is unverified however
  good the number looks.
- **The screening path is the closed forms** from predictions 1–4. Nearly free here, and it
  cross-checks the integrator independently.

The PRP also makes this the first layer to say anything about **T0.3**, the non-relativistic
assumption — the one axiom flagged as unvalidated. It must report peak speed so the assumption can
be checked as soon as a signal speed exists.

### FILES CREATED OR MODIFIED

    PRPs/orbit-layer.md   — NEW. Blocked only on approval
    CONTEXT.md            — this entry

No code. Branched to `sim/orbit-layer`, since `main` now holds released work.

### TESTS WRITTEN

None — not approved. The test list is the substance of the PRP and separates dimensional, invariant,
physical-prediction, screening, regression and error-path tests.

The scratch verification script was not kept; its results are recorded above and in the PRP, and the
real tests will re-derive them.

### DECISIONS MADE

None requiring a DECISIONS.md entry. The integrator and scope choices are implementation decisions
recorded in the PRP, where they can be rejected at approval.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- `PRPs/orbit-layer.md` awaits approval.
- DECISION-012 still blocks the scan.
- `docs/AXIOMS.md` §3 still carries the "to be re-confirmed numerically" caveat on apsidal
  precession. It is now confirmed, but the update is an acceptance criterion of the orbit layer
  rather than a drive-by edit — §3 should record what the code establishes, not what a scratch
  script found.
- The 2+1D graviton count remains a hand derivation. Nothing planned will check it.

---

## SESSION 9 — 2026-09-05 — Orbit layer implementation — closed

Branch: sim/orbit-layer

### WHAT WAS DONE

Implemented the orbit layer test-first. **174 tests**, `mypy --strict` clean, `ruff` clean. Tests
were written and run before any implementation existed; the first run failed on five collection
errors.

`sim/orbit/` integrates the two-body problem under `F ∝ 1/r` with velocity-Verlet, measures the
apsidal angle, and produces insolation. `sim/star/` holds Kell, stubbed. Six consequences of the
force law are now established in code rather than on paper, and `docs/AXIOMS.md` §3 was updated to
say so.

**Two of my own claims were tested and found wrong. Both are recorded rather than quietly fixed.**

**1. The boundedness test was meaningless as designed.** The Session 8 scratch script "confirmed"
that nothing escapes by launching at 100× circular speed and observing a finite maximum radius. That
proves nothing: the turning radius is `r₀·exp(v²/(2G₂M))`, which at 100× circular is about `e^5000`,
so the trajectory had simply not turned around yet. Three tests failed on first run for exactly this
reason.

The honest formulation is now split in two. Where the turn is reachable (1.5–2.5× circular) the
integrated maximum is checked against the analytic turning radius, which also cross-checks the
screening path against the full solve. Where it is not, boundedness is asserted analytically, since
it is a statement about the potential rather than something an integration can demonstrate. A
by-product worth knowing: the turning radius exceeds double precision above roughly **37.7×** the
circular speed, so `radial_turning_radius` raises there with a message saying the trajectory is
still bound and only the number is unrepresentable.

**2. The PRP's justification for requiring a symplectic integrator was wrong.** It claimed a
non-symplectic scheme would manufacture spurious apsidal precession, indistinguishable from the
real thing. Mutating to forward Euler and measuring:

    VERLET  T=1500   sweep=254.5063   energy band  2.26e-08   r_max=1.1043
    EULER   T=1500   sweep=254.5076   energy drift +6.56e-01  r_max=2.1251

Euler inflated the orbit's maximum radius by 93% while the measured sweep moved by 0.0013°. The
reason is that **a logarithmic potential is scale-invariant** — `r → kr` with `t → kt` leaves the
equation of motion unchanged — so an orbit inflated by numerical energy is nearly a rescaled copy of
itself and keeps its shape and apsidal angle. Precession is protected here in a way it would not be
under an inverse-square force.

The requirement stands, for the reason that actually bites: **flux goes as `1/r`**, so a silently
doubled orbital radius halves the insolation with no symptom anywhere in the precession measurement.
That is exactly the plausible-wrong-number failure this project exists to catch, located somewhere
other than predicted. The suite now guards it directly with `TestOrbitScaleDoesNotDrift`, and the
PRP carries a dated FINDING note rather than an edited-away claim.

**A third error, caught mid-check.** The first attempt at the Euler mutation removed the leading
half-kick, which produces *symplectic* Euler (Euler–Cromer), not forward Euler. The suite passed and
I nearly recorded "Euler barely matters" as a finding. It only surfaced because the energy behaviour
looked too good for a scheme that was supposed to be dissipative.

**An API gap surfaced.** `Quantity.magnitude()` returns `float | NDArray`, so every caller had to
narrow by hand — twenty mypy errors across the orbit tests. Added `Quantity.scalar()` and
`Quantity.array()`, which validate dimension *and* shape and return a precise type. This removed a
scattering of `assert isinstance(...)` from the implementation too. Only a real consumer could have
exposed this; the units layer looked complete without it.

### FILES CREATED OR MODIFIED

    sim/orbit/analytic.py      — NEW. Screening path: closed forms, turning radii
    sim/orbit/integrator.py    — NEW. Velocity-Verlet, fixed step, energy and singularity guards
    sim/orbit/analysis.py      — NEW. Conserved quantities; apsidal angle by parabolic refinement
    sim/orbit/insolation.py    — NEW. Flux as L/(2*pi*r)
    sim/orbit/__init__.py      — NEW. Public surface
    sim/star/kell.py           — NEW. The stub. Raises for everything beyond mass and luminosity
    sim/units/quantity.py      — scalar() and array() added
    sim/units/named.py         — LUMINOSITY added
    sim/tests/orbit/*.py       — NEW, four files
    sim/tests/star/test_kell.py — NEW
    docs/AXIOMS.md             — §3 rewritten: six confirmed consequences, caveat removed
    PRPs/orbit-layer.md        — dated FINDING note on the symplectic justification
    MEMORY.md                  — decision 16; state and next-session block
    CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

174 total, 68 new in this layer.

- **Dimensional:** flux carries FLUX and rejects the `1/r²` form; gravity is an acceleration.
- **Invariant:** nothing escapes where demonstrable, and analytically where not; energy bounded not
  secular; angular momentum conserved and scalar in 2D; radius strictly positive; determinism;
  **orbit scale does not drift**, the test that actually catches a bad integrator.
- **Physical predictions:** `v_c` independent of radius over three decades; period exponent 1.0 and
  demonstrably not 1.5; apsidal angle `π/√2` with timestep convergence; monotone drift with
  eccentricity; season cycle `2+√2`.
- **Screening:** analytic and integrated agree; and an AST check that `analytic.py` does not import
  the integrator, so a screening path cannot secretly integrate.
- **Stub:** every unavailable stellar property raises, with `DECISION-010` in the message.

### MUTATION RESULTS

    force law 1/r -> 1/r^2        22 failed   caught
    velocity-Verlet -> Euler      10 failed   caught (via the energy guard, not precession)

### DECISIONS MADE

- The symplectic requirement is retained but re-justified; see MEMORY.md decision 16.
- Radial infall is rejected at validation rather than integrated badly: the potential is singular at
  the origin and a fixed-step scheme cannot resolve it. The closed form is offered instead.
- `Quantity.scalar()` / `.array()` added to the units layer rather than narrowing at call sites.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `sim/orbit-layer` is not merged and not pushed.
- DECISION-012, -013, -014 all still open; they converge on the climate layers.
- Debris and the impact cycle remain deferred and need their own PRP.
- T0.3 is still unvalidated in the sense that no signal speed exists to compare against, though
  `Trajectory.peak_speed` now reports what would be needed.
- The 2+1D graviton count remains a hand derivation with nothing planned to check it.

---

## SESSION 10 — 2026-09-05 — Viewer PRP — closed

Branch: sim/viewer

### WHAT WAS DONE

User asked to be able to zoom from the whole system down to the planet's ground. Ran the discovery,
recorded two decisions, and wrote `PRPs/viewer-layer.md`. No code — it awaits approval.

**Why this is unusually cheap in a two-dimensional world.** Three properties already established
make the viewer far easier than its 3D equivalent. Culling is two binary searches, because ground
bodies are held in an array sorted by surface position and the first law guarantees that order never
changes — no quadtree, no spatial index. Terrain level-of-detail is 1D mipmapping, since `h(x)` is a
single periodic array. And there is no projection at all: the camera is a window on a plane. The
viewer will be the first thing to actually exploit the sorted-order invariant recorded in MEMORY.md
decision 8.

There is also no seam between regimes. Surface position maps to the plane as `θ = 2πx/L`, `r = R+h`,
so a stretch of ground looking straight and the world closing into a circle are the same
representation at different zooms, not two cases.

**The hard part is precision, not graphics.** System scale to ground is eleven orders of magnitude.
Float64 carries ~15–16 digits, so the transform must be camera-relative — `(world − focus) * scale`,
never `world * scale`. At a focus 1e11 m from the origin, a metre of detail is below float64's
resolution of the absolute coordinate and comfortably inside it for the relative one. This is
recorded as an architecture rule, a MEMORY entry, and a discriminating test whose failure under an
absolute transform must be demonstrated rather than assumed.

**A finding that binds a layer not yet written.** The viewer will ask for terrain at eleven different
scales. If `h(x)` is a sampled raster, that fixes a resolution forever and forfeits arbitrary zoom;
if it is an evaluable field — spectral synthesis, a sum of sinusoids at integer wavenumbers — the
viewer regenerates detail at whatever zoom it is at, exactly consistent with the simulation, with no
pyramid and no streaming. Spectral synthesis also makes periodicity on the closed surface exact by
construction rather than stitched. Opened as DECISION-017 so the surface layer is written knowing it.

### DECISIONS MADE

- **DECISION-016 resolved.** A desktop viewer with `pygame-ce`, skeleton now, grown per layer. Both
  forks were the user's: desktop over an HTML canvas, and now over waiting.
  `pygame-ce` over `pyglet` because pyglet is OpenGL and float32 through the pipeline, which fights
  the only genuinely hard requirement here. Verified both are installable and that this machine has
  a display before writing a PRP resting on either.
- `pygame-ce` added to STACK — the first dependency added since the project began. CLAUDE.md now
  states explicitly that the list is closed again.

### PENDING DECISIONS OPENED

- **DECISION-017 — is terrain a raster or an evaluable field?** Blocks the surface layer, not the
  viewer. Recommendation: a spectral base field, plus a sampled residual if the ground is ever
  eroded or cratered.

### FILES CREATED OR MODIFIED

    PRPs/viewer-layer.md   — NEW. Awaits approval
    DECISIONS.md           — 016 resolved, 017 opened
    CLAUDE.md              — pygame-ce added to STACK; new architecture rule 7 (the viewer draws,
                             never computes; render camera-relative)
    MEMORY.md              — decision 17
    CONTEXT.md             — this entry

### TESTS WRITTEN

None — not approved. The test list is the substance of the PRP, and every test in it runs headless:
`camera.py` imports no pygame, and what remains uses `SDL_VIDEODRIVER=dummy`. A viewer is normally
hard to test; here it need not be, because almost all the difficulty is in pure coordinate maths.

### STILL OPEN AT CLOSE

- `PRPs/viewer-layer.md` awaits approval. Branch `sim/viewer` unmerged, unpushed.
- DECISION-012, -013, -014, -017 all open.
- The planet layer and the debris/impact layer both still need PRPs.

---

## SESSION 11 — 2026-09-05 — Viewer implementation — closed

Branch: sim/viewer

### WHAT WAS DONE

Implemented the viewer test-first. **228 tests**, all passing headless, `mypy --strict` and `ruff`
clean. `python -m sim.view.app` opens a window that zooms from the whole system to a sliver of
Vellum's surface.

Structure follows the PRP: `bands.py`, `geometry.py`, `camera.py` and `scene.py` are pure and import
no pygame — a parametrised test enforces that — while `render.py` and `app.py` are thin enough to be
checked by reading. A viewer is normally hard to test; here almost all of it is coordinate
arithmetic, so almost all of it is testable with no display.

**Three claims were measured, and two of mine were wrong.**

*The PRP's precision justification was wrong.* Camera-relative transforms do **not** buy float64
precision at this range: focus 1e11 away, two points a metre apart, relative and absolute both give
exactly 100 px. Eleven orders of magnitude sit comfortably inside float64's sixteen digits. What the
absolute form actually breaks is **pixel coordinate magnitude** — 1e11 at 100 px/unit is 1e13 pixels
and SDL takes C ints that stop at 2.1e9. The renderer overflows long before the float does. (float32
*would* lose it — 1e11+1 is not even representable — which does vindicate choosing SDL2 over
OpenGL.)

*The real precision floor is storing an absolute coordinate at all.* One ulp at 1e11 is ~15 microns,
so ground detail finer than that cannot be an absolute position however it is transformed. Composing
from the planet centre keeps arithmetic near the planet radius where an ulp is nanometres. This is
why surface positions are held as (surface coordinate, height) — the same 1D periodic array the
simulation already wanted, now load-bearing for a second reason.

*Scale bands in absolute units were simply wrong.* They were thresholds in metres, but the
simulation works in natural units where the orbital radius is about 1, so **every** zoom level
reported "ground". A smoke render across twelve decades surfaced it. Bands are now dimensionless
ratios of viewport span to planet circumference, which is both correct and consistent with the
project's position that only ratios are physically meaningful.

**Three bugs found in my own code, two of them by tests that were themselves wrong first.**

- `mod()` wrapped with `fmod(fmod(a,b)+b, b)`, the usual trick for making negatives positive. Adding
  the circumference quantises at *its* ulp — 7.45 nm for a 3.84e7 surface — so a micron of surface
  position lost 0.16% of itself. Invisible in a unit test of `mod`, plainly visible as a wrong pixel
  offset at ground zoom.
- Python's `%` fixes that but has its own edge: `-1e-9 % 3.84e7` returns exactly `3.84e7`, because
  1e-9 is under half an ulp there. That puts a surface position out of `[0, C)` and would break
  index arithmetic downstream. The wrap point now folds to zero.
- `Disc` stored both radius and circumference. They are not independent for a circle, and the two I
  supplied disagreed by 2%, so surface coordinates mapped to arcs 2% short. The class now stores the
  circumference and derives the radius, which makes the inconsistency unrepresentable.

**And the mutation run caught a test that was not testing what it claimed.** Reverting the anchored
transform to an absolute one left the whole suite green. The micron test displaced along *y*, where
the anchor is zero, so the large coordinate was never touched. Rewritten to view the top of the disc
— where the displacement lies along x, the axis carrying the 1e11 offset — it now fails under that
mutation as intended.

### MUTATION RESULTS

    anchored transform -> absolute     1 failed   caught (only after fixing the test)
    mod() -> fmod(fmod+b, b)           2 failed   caught
    seam-aware culling -> single run   1 failed   caught

### FILES CREATED OR MODIFIED

    sim/view/bands.py        — NEW. Dimensionless scale bands
    sim/view/geometry.py     — NEW. Disc, seam-aware culling, coordinate helpers
    sim/view/camera.py       — NEW. Transforms, zoom, hierarchical composition
    sim/view/scene.py        — NEW. Drawable protocol, band dispatch
    sim/view/render.py       — NEW. Star, orbit trace, planet disc, scale bar
    sim/view/app.py          — NEW. Window and event loop
    sim/view/__init__.py     — NEW. Public surface, and how a layer joins the view
    sim/tests/view/*.py      — NEW, four files
    pyproject.toml           — pygame-ce
    CHANGELOG.md, MEMORY.md (decision 18), CONTEXT.md

### TESTS WRITTEN

228 total, 63 new. Purity (four modules import no pygame), transforms and round trips at every
band, hierarchical precision, zoom about a cursor holding its world point fixed at every scale,
clamping that reports itself, band partitioning with no gap or overlap, seam-aware culling checked
against brute force over 60 random arcs, scene dispatch and its two error paths, and headless smoke
renders asserting pixels actually change.

### DECISIONS MADE

- `Disc` derives its radius rather than storing it.
- Scale bands are dimensionless ratios, not absolute lengths.
- Radial-infall-style edge cases in `mod` fold to zero rather than raising: a position half an ulp
  below the wrap point *is* the wrap point.

### PENDING DECISIONS OPENED

None. DECISION-017 was already open and is now the gate on the surface layer.

### STILL OPEN AT CLOSE

- Branch `sim/viewer` is unmerged and unpushed.
- The viewer shows a bare disc: there is no terrain, water or life yet. That was the deal in
  DECISION-016.
- DECISION-012, -013, -014, -017 all open.

---

## SESSION 12 — 2026-09-05 — Surface layer PRP — closed

Branch: sim/surface-layer

### WHAT WAS DONE

Resolved DECISION-017 and wrote `PRPs/surface-layer.md`. No code — it awaits approval.

**The recommendation I had made three times was wrong, and costing it took two minutes.** Spectral
synthesis was proposed in Sessions 3, 10 and 11 as the way to make terrain evaluable at any
resolution: a sum of sinusoids at integer wavenumbers, periodic on the closed surface by
construction. The attraction was real, but nobody had asked what it costs. Resolving wavelength `λ`
on a surface `C` around needs `C/λ` coefficients, at `O(k)` per sample:

    target detail    Fourier coefficients    fBm octaves
    10 km                           3,840             12
    100 m                         384,000             19
    1 m                        38,400,000             26

Metre detail on a 38,400 km surface needs 38 million coefficients. The whole reason for choosing an
evaluable field over a raster — regenerate detail at whatever zoom you are at — would have been lost
at the first serious zoom, and the layer would have had to grow a mipmap pyramid after all.

The fix keeps every property and drops the cost: **periodic multi-octave gradient noise**. Each
octave hashes a lattice index taken **modulo that octave's cell count**, so periodicity is still
exact by construction, and cost is `O(octaves)` — 26 hash evaluations for metre detail, independent
of position or scale.

Two consequences that the PRP makes explicit rather than leaving implicit:

- **Terrain has a finite resolution floor**, `C / 2**octaves`. "Infinite zoom" was always an
  overstatement. The layer must report the floor and must refuse to invent flatness below it — a
  viewer that zooms past the ground's detail should say so, not show smooth invention.
- **Terrain statistics are abstracted, not derived.** Nothing in the axioms predicts a roughness
  exponent; that would need tectonics and erosion. Roughness and amplitude are world constants and
  now have an entry in the `docs/AXIOMS.md` §4 ledger, so no result about mountains or slopes can be
  reported as a finding about two-dimensional physics.

Scope is terrain only. Basins, water, drainage and the anoxic depth are the next layer and are
substantial on their own; erosion and craters are what the residual exists for, in a later PRP.

### FILES CREATED OR MODIFIED

    PRPs/surface-layer.md   — NEW. Awaits approval
    DECISIONS.md            — 017 resolved, with the cost table
    docs/AXIOMS.md          — §4 ledger gains terrain statistics
    MEMORY.md               — decision 19
    CONTEXT.md              — this entry

### TESTS WRITTEN

None — not approved. The test list is the substance of the PRP. Two of its tests are the ones worth
noting: exact periodicity, which the lattice modulo exists to guarantee and which must be shown to
fail when the modulo is removed; and a **power-spectrum slope** check, which is what distinguishes
fractal terrain from a field that is merely random.

### DECISIONS MADE

- DECISION-017 resolved: procedural base plus sampled residual, explicitly not spectral.
- Two new free parameters — roughness and amplitude — declared as world constants and sent for
  approval with the PRP rather than smuggled in as implementation detail.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- `PRPs/surface-layer.md` awaits approval. Branch `sim/surface-layer` unmerged, unpushed.
- DECISION-012 (habitability, blocks the scan), -013 (chemistry), -014 (grey vs spectral transfer).
- The planet layer and the debris/impact layer still have no PRPs.

---

## SESSION 13 — 2026-09-05 — Surface layer implementation — closed

Branch: sim/surface-layer

### WHAT WAS DONE

Implemented the surface layer test-first. **284 tests**, all passing headless, `mypy --strict` and
`ruff` clean. Vellum has ground, and it is visible in the viewer from the whole disc down to a
stretch of terrain.

`sim/surface/noise.py` is one octave of periodic gradient noise: a splitmix64 hash on a lattice
index taken **modulo the octave's cell count**, which is what makes the field exactly periodic
rather than stitched. `sim/surface/terrain.py` sums octaves, normalises to a requested RMS, and adds
an optional sampled residual. `TerrainTrace` draws it through `camera.surface_to_screen`, so ground
detail is composed from the planet centre and never quantised by the planet's distance from Kell.

**One measured correction, and it is the kind that is invisible by inspection.** The octave decay
needed to deliver a spectral slope is off by one from the obvious derivation. Power at octave `n`
goes as `A_n²`, so `A_n ∝ 2^(-βn/2)` should give `P(k) ~ k^-β` — and measured, it gives `-(β+1)`.
The missing factor is **mode density**: in one dimension the band `[2^n, 2^(n+1))` holds about `2^n`
Fourier modes, so power *per mode* carries an extra `k^-1`. Measured across decay exponents:

    p = 0.5   slope -1.976
    p = 1.0   slope -2.961
    p = 1.5   slope -3.924        => slope = -(2p + 1), exactly

So the decay is `2^(-(β-1)n/2)`. After the fix, requested roughness 1.5, 2.0, 2.5 and 3.0 measure
-1.49, -1.98, -2.48 and -2.96. The terrain looked entirely plausible at the wrong exponent; only an
FFT of the field distinguishes fractal ground from ground that is merely rough.

**The resolution floor is real and is reported.** With 22 octaves on the demo world the floor is
`C / 2**22`, and the viewer's readout says *below terrain detail* once the zoom passes it. "Evaluable
at any resolution" was always an overstatement; the layer states the limit instead of returning
convincing smoothness.

**Terrain statistics are abstracted.** Amplitude and roughness are world constants with an entry in
the `docs/AXIOMS.md` §4 ledger, and the module carries an `Abstracts:` line. No result about
mountains, slopes or basin shapes is a finding about two-dimensional physics.

### MUTATION RESULTS

    remove the lattice modulo         6 failed   caught (periodicity)
    uniform octave amplitudes         4 failed   caught (spectral slope)
    drop the residual seam wrap       1 failed   caught

### FILES CREATED OR MODIFIED

    sim/surface/noise.py      — NEW. Periodic gradient noise, splitmix64 hash
    sim/surface/terrain.py    — NEW. Octave sum, RMS normalisation, residual, floor reporting
    sim/surface/__init__.py   — NEW
    sim/tests/surface/*.py    — NEW, two files
    sim/view/render.py        — TerrainTrace; ScaleBar reports the terrain floor
    sim/view/app.py           — terrain wired into the demo world
    sim/tests/view/test_render.py — TerrainTrace tests
    MEMORY.md (decision 20), CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

284 total, 56 new. Exact periodicity at every octave count and after seven circumferences; seam
continuity; determinism; resolution consistency between a lone point and a dense array; RMS matching
the configured amplitude; **power-spectrum slope matching the configured roughness**, which is the
test that separates fractal terrain from noise; residual arithmetic and its periodic interpolation;
the resolution floor and its clamping report; and an AST check that the noise module never calls
Python's `hash()`, which is randomised per process and would break determinism between runs.

### DECISIONS MADE

- Octave decay is `2^(-(β-1)n/2)`; see MEMORY.md decision 20.
- Normalisation measures the field's RMS once at construction over a fixed deterministic sweep,
  rather than baking in a magic constant for unit-noise variance.
- The demo world's amplitude and roughness are tagged `WORLD CONSTANT` in `app.py`, not left as
  bare numbers.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `sim/surface-layer` is unmerged and unpushed.
- No water, no basins. That is the next layer.
- DECISION-012, -013, -014 still open.
- The terrain residual exists and is exercised by tests, but nothing writes to it yet — erosion and
  craters are what it is for, and both need their own PRP.

---

## NEXT SESSION START POINT

Open a new session entry in this file first, with state `open` and the branch name, and commit it.

Then read CLAUDE.md, MEMORY.md, DECISIONS.md, this file, and `docs/AXIOMS.md`.

The surface layer is complete and green on branch `sim/surface-layer`, unmerged. Merge it first.

**The next PRP is water** — the layer where two dimensions bite hardest, and where almost everything
follows from T0.1 with no new physics. A basin is a local minimum of `h`; filling it is a
one-dimensional problem, not a watershed. **A river cannot branch**, because a tributary would have
to arrive from a side that does not exist, so there are no confluences and no deltas — only single
unbranched runs. And a basin has no drainage network at all: what is sealed in one is sealed for
good.

Scope it as basin detection and filling. Leave stratification and the anoxic depth to a
climate-facing layer, and leave erosion — which writes to the terrain residual — to its own PRP.

Carry the Session 13 lesson: **measure a normalisation against the thing it is supposed to produce.**
The octave decay was off by exactly the one-dimensional mode-density factor, the terrain looked
perfectly plausible either way, and only an FFT of the field caught it.

Environment: `.venv/`. Run `.venv/bin/pytest`, `.venv/bin/mypy`, `.venv/bin/ruff check sim/`.

Do not edit `vellum-monograph.html`. It is frozen; it gets regenerated, not corrected.