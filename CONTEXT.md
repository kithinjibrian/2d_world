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

## SESSION 8 — 2026-09-05 — Orbit layer PRP — open

Branch: sim/orbit-layer

---

## NEXT SESSION START POINT

Open a new session entry in this file first, with state `open` and the branch name, and commit it.

Then read CLAUDE.md, MEMORY.md, DECISIONS.md, and this file — in that order, then `docs/AXIOMS.md`.

The units layer is done and green. **The next artefact is the PRP for the orbit layer**, not code.

That PRP should carry two acceptance criteria that finally check hand derivations recorded in
`docs/AXIOMS.md` §3 and never confirmed numerically:
- **Apsidal regression of ~105° per orbit** for a near-circular orbit under `F ∝ 1/r`, so a season
  works round the calendar in ~3.4 orbits. Derived from `ω_r/ω_θ = √2`.
- **No trajectory is ever unbound**, at any launch speed — the logarithmic potential admits no
  escape velocity, so an integrator producing an escaping orbit is broken.

It is also the first layer to need architecture rule 8 (a screening path as well as a full solve),
and the first to consume the stubbed Kell, which must raise rather than default.

Environment: `.venv/` exists, created with `uv`; dependencies are declared in `pyproject.toml`.
Run `.venv/bin/pytest`, `.venv/bin/mypy`, `.venv/bin/ruff check sim/`.

Also worth putting to the user: **DECISION-012**, what counts as habitable. It blocks the scan.

Do not edit `vellum-monograph.html`. It is frozen; it gets regenerated, not corrected.
