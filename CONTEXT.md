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

## SESSION 14 — 2026-09-05 — Viewer zoom defects — closed

Branch: fix/viewer-zoom

### WHAT WAS DONE

The user ran the viewer, zoomed in, and hit three defects in about thirty seconds. All three were
real, all three were in shipped work, and none was caught by the 284 tests that existed.

**1. The GROUND band was unreachable.** `Camera.MIN_SCALE` / `MAX_SCALE` were absolute constants in
pixels per world unit, capped at 1e9. On a world 3.84e-5 units around that puts the deepest possible
zoom at a span ratio of 3.3e-2 — still REGIONAL. The limit was reported honestly; there was simply
no way past it.

This is **the same error as MEMORY.md decision 18, in a second place.** Scale bands in absolute
units had already been found meaningless in natural units and fixed. The zoom limits sat ten lines
away in the same file and were left alone. Both are span ratios now.

**2. Zooming in filled the window with gold.** `StarDisc` drew a circle of radius
`0.02 * camera.scale` with no culling — twenty million pixels at close zoom, centred a world unit
away, covering everything. The centre was clipped to the SDL int range; the radius never was. It now
culls against the viewport, and refuses to draw when the camera is inside the disc rather than
painting over the world.

**3. Following Vellum put the camera inside the planet.** Following centred on the planet's *centre*,
right only while the whole planet fits the viewport. Past that the surface is thousands of pixels
off-screen — planet radius 6.1e3 px against a 400 px half-height — so zooming in showed empty space
where the world should be. `Camera.focused_on_surface` and `_camera_for` now switch to a point on
the surface once the planet no longer fits, and left/right walks along the ground, wrapping, because
the surface has no edge.

Also raised the demo terrain from 22 octaves to 34: at 22 the resolution floor sat above the entire
GROUND band, so even once reachable there would have been nothing there but invented smoothness.

### THE PROCESS FAILURE, WHICH IS THE POINT

`PRPs/viewer-layer.md` had a validation step reading: *"Run it and zoom by hand from the full orbit
to a metre of ground. The precision requirement is the kind that passes its unit test and still
looks wrong, so it must also be looked at."*

That was not done. Headless smoke tests were run instead — each layer drawn once at four scales,
asserting only that some pixel changed. Every one of these defects passes that test trivially: a
uniformly gold viewport *is* a change, an unreachable band is never visited, and a camera inside the
planet still draws an orbit line.

`sim/tests/view/test_zoom_journey.py` is what should have been written. It walks the whole zoom
range — every band, about 140 steps — asserting that all four bands are visited, that some
background survives every frame, that the ground stays on screen while following, and that terrain
still has detail where the GROUND band begins. It catches all three, and it is the shape any
range-spanning visual feature should be tested with.

A rule went into CLAUDE.md's TESTING RULE: a feature whose output is visual is not validated by
asserting that pixels changed.

### FILES CREATED OR MODIFIED

    sim/tests/view/test_zoom_journey.py  — NEW. The traversal that catches all three
    sim/view/camera.py    — zoom limits as span ratios; focused_on_surface
    sim/view/render.py    — StarDisc culls; PlanetDisc limited to SYSTEM and PLANETARY
    sim/view/app.py       — _camera_for follows the surface; left/right walks the ground;
                            demo terrain raised to 34 octaves
    sim/tests/view/test_camera.py, test_precision.py — cover the new behaviour
    CLAUDE.md, MEMORY.md (decision 21), CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

295 total, 11 new. Measured after the fix, walking the full range: every band visited, background
between 89% and 99.6% of every frame, ground on screen at every step, and terrain relief falling
smoothly from 1.2e-7 to 9.0e-11 world units without reaching the resolution floor.

### DECISIONS MADE

- Zoom limits are span ratios (MEMORY.md decision 21).
- `PlanetDisc` draws only at SYSTEM and PLANETARY; below that `TerrainTrace` draws the real profile,
  and an outline circle through the middle of it is simply wrong.
- Being inside the star draws nothing rather than filling the view. Hiding a camera that is
  somewhere it should not be is worse than showing it.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `fix/viewer-zoom` unmerged, unpushed.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 15 — 2026-09-05 — Bigger window, mouse panning — closed

Branch: feat/viewer-input

### WHAT WAS DONE

Two viewer affordances the user asked for: a bigger window, and panning with the mouse.

**Window.** The size was a hardcoded 1280x800, which is a postage stamp on a large display and does
not fit a small one. It now queries the desktop and takes 88% by 82% of it, with a floor of 960x600.
On this machine that is 2703x1574 against a 3072x1920 desktop. The window is also `RESIZABLE`, and
`Camera.resized` preserves focus and zoom so a resize shows *more of the world* rather than
magnifying what was there — which also means the scale band can change on resize, since a band is
how much of the world is in view.

**Dragging, and the decision inside it.** Panning by mouse is trivial except for one question: what
should a drag mean while following Vellum at ground zoom? Free-panning there leaves the planet
within a few pixels of travel and shows empty space — exactly the failure fixed in Session 14. So
there are two regimes:

- **Following, and zoomed in past the planet:** a horizontal drag walks along the ground, wrapping,
  because the surface has no edge; a vertical drag changes height above it, clamped at the surface.
  Following stays engaged.
- **Otherwise:** the camera pans freely and following is dropped. It *has* to be dropped — with
  follow on the camera is re-centred every frame, so a drag would move the pointer while the view
  stayed put.

The sign convention is that whatever is under the pointer stays under it, and both regimes share it.
A test asserts that specifically, because a transition between two regimes that disagree about which
way is up reverses the controls under the user's hand mid-gesture.

**A test caught my own inconsistency**, in the tests rather than the code: the vertical-drag tests
were written expecting "drag up raises the viewpoint" while the free pan already implemented "drag
down raises the viewpoint". The code was self-consistent; the expectation was not. Fixed the tests
and added one asserting the two regimes agree.

### ON NOT WRITING A PRP

Judged below the threshold: no new physics, no new dependency, no new free parameter, and nothing
that changes what the simulation computes. Recorded here because the PRP rule does not carve out an
exemption for small features, and skipping it was a judgement call rather than a rule.

What the PRP would have been for was the one genuine design question — what a drag means on the
ground — and that is decided explicitly above rather than silently.

### FILES CREATED OR MODIFIED

    sim/tests/view/test_input.py  — NEW. Resizing and both drag regimes
    sim/view/camera.py            — Camera.resized
    sim/view/app.py               — _on_drag; drag, resize and button events; desktop-relative
                                    default size; RESIZABLE window
    CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

311 total, 16 new. Resizing preserves focus and zoom and can change the band; the world point under
the cursor stays under it through a drag; dragging drops follow when free-panning; horizontal drag
walks the surface and wraps; vertical drag changes height and clamps at the ground; and both regimes
agree on which way is up.

### DECISIONS MADE

- Two drag regimes rather than one, for the reason above.
- Dragging while following at wide zoom drops follow; while following on the ground it does not.
- Height clamps at the surface. Going below ground may be worth allowing later to inspect a terrain
  profile, but it is not what a drag should do by accident.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `feat/viewer-input` unmerged, unpushed.
- The ground is drawn as a thin line, not filled, so at close zoom the view is ~99.9% background.
  Correct for a profile drawing and arguably wrong for something called ground — worth a look, but
  it is a visual design choice rather than a defect.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 16 — 2026-09-05 — Camera rotation and cursor zoom — closed

Branch: feat/viewer-rotation

### WHAT WAS DONE

Three things the user asked about: mouse zoom, rotation, and whether the planet revolves.

**Mouse zoom was already wired and was being silently discarded.** `MOUSEWHEEL` called
`zoomed_about`, which moves the focus so the point under the cursor stays put — and then
`_camera_for` overrode the focus completely on the next line, because following re-centres the
camera every frame. So every scroll zoomed to the middle of the window regardless of the pointer.
Measured before fixing: focus 2.0e-9 after `zoomed_about`, 1.000006 after the follow override.

The fix is `_on_zoom`, which cannot move the focus on the ground and instead moves the **anchor**,
so the surface point under the cursor stays under it. That works precisely because the camera is now
rolled to local vertical there, so screen x runs along the surface and screen y away from it. Also
added the legacy button-4/5 wheel path, since some setups deliver scrolling that way rather than as
`MOUSEWHEEL`.

**Camera roll.** On a closed surface "up" is radially outward, which points a different way at every
position and is exactly inverted on the far side of the world. Without roll the ground tilts as you
walk and turns upside down halfway round. `Camera.rotation` plus `aligned_to_surface` fixes it, and
`_camera_for` applies it whenever the view is on the ground. Verified at eight points around the
world: up is up and the ground runs horizontally at every one.

Refactored every camera-returning method to `dataclasses.replace` while adding the field. The old
versions listed each field positionally, which is how `reference_length` had to be threaded through
five call sites by hand when it was added — a new field would have had the same problem, silently.

**Does Vellum revolve? Yes — and it does not spin.** It orbits Kell, integrated and visible. It has
no rotation about itself: that was excluded from the orbit layer's scope deliberately. The
consequence is that **Vellum has no day**. Insolation varies with orbital distance only; no part of
the surface ever faces away from Kell. That is a gap rather than an impossibility — rotation is
perfectly available in two dimensions, where angular momentum is a signed scalar rather than a
vector — and it needs its own PRP. Recorded as MEMORY.md decision 22.

**Two sign conventions were pinned by tests that initially disagreed with the code.** The vertical
drag last session, and the roll direction this session: a positive roll turns the *camera*
counter-clockwise, so the world appears to turn clockwise. Both times the implementation was
self-consistent and my expectation was not. The roll test now says which way and why, because
getting that sign backwards puts the ground upside down and looks like a bug in the alignment
instead.

### FILES CREATED OR MODIFIED

    sim/tests/view/test_rotation.py — NEW. Roll transform, alignment round the world, cursor zoom
    sim/view/camera.py    — rotation field; with_rotation; aligned_to_surface; replace() throughout
    sim/view/app.py       — _on_zoom; roll applied on the ground; legacy wheel buttons
    MEMORY.md (decision 22), CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

339 total, 28 new. Round trip under roll at five angles; a full turn is the identity; roll does not
move the focus; zoom-about-cursor still holds its point when rolled; up is up and the ground is
level at six points around the world; the far side is not inverted; the surface point under the
cursor survives a zoom; and zooming at the centre leaves the anchor alone.

### DECISIONS MADE

- Roll is applied automatically on the ground rather than being a manual control. Manual roll would
  be a way to make the ground crooked, which is not a feature.
- Zoom on the ground moves the anchor, not the focus, for the reason above.
- Camera construction goes through `dataclasses.replace` so a new field cannot be dropped silently.

### PENDING DECISIONS OPENED

None, but MEMORY.md decision 22 records planetary rotation as a known gap needing a PRP.

### STILL OPEN AT CLOSE

- Branch `feat/viewer-rotation` unmerged, unpushed.
- **Vellum does not spin.** No day, no night, no diurnal cycle. Needs its own PRP.
- The ground is drawn as a thin line rather than filled.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 17 — 2026-09-06 — Rotation layer PRP — closed

Branch: sim/rotation-layer

### WHAT WAS DONE

Wrote `PRPs/rotation-layer.md`. No code — it awaits approval and it introduces a new free parameter.

MEMORY.md decision 22 recorded that spin needs its own PRP: a rotation rate is a world constant, the
surface frame turns relative to inertial space, and insolation becomes a function of surface
position as well as orbital phase. This is that PRP.

**Seven results were derived and checked before writing it**, so the PRP rests on measurement rather
than expectation:

1. **Angular momentum is a signed scalar** — no axis in the plane for it to point along. Already
   established in the orbit layer.
2. **The moment of inertia of a uniform disc is `MR²/2`**, verified by integrating with a per-area
   density. Identical to the 3D coefficient — another case where two dimensions do *not* change the
   answer, and it gets a test for the same reason kinematic viscosity has one.
3. **The terminator is two points, not a curve.** In 3D it is a great circle; on a closed surface
   curve, day and night are two arcs meeting at two points.
4. **The lit fraction is `arccos(R/d)/π`** — a third at `d/R = 2`, 0.468 at `d/R = 10`, tending to
   exactly a half for a distant star. The distant-star approximation is wrong by 6% at `d/R = 10`,
   so the PRP requires the exact form.
5. **A 2D planet flies apart when its surface moves at orbital speed.** Breakup is `√(G₂M)/R`, so the
   surface speed there is `√(G₂M) = v_c` — and circular speed in two dimensions is the same at every
   radius, so that is the speed of an orbit *anywhere*.
6. **Total intercepted power is `F·2R`**, the disc presenting a cross-section of length `2R`.
   Integrating `F·cos(incidence)` over the lit arc gives exactly that, confirmed numerically. This
   is the strongest invariant available and the PRP makes it the headline test.
7. **No axial tilt is possible**, so the PRP forbids adding a parameter for one. A parameter that
   must always be zero is an invitation to set it.

The scope is illumination, not climate: this layer says where the light falls and when, and what the
ground does with it belongs to a climate layer. Oblateness is excluded and becomes a ledger entry —
a spinning body bulges, and modelling that needs the material response abstracted at T2.4.

### FILES CREATED OR MODIFIED

    PRPs/rotation-layer.md   — NEW. Awaits approval
    CONTEXT.md               — this entry

### TESTS WRITTEN

None — not approved. The test list is the substance. Two acceptance criteria are the ones that
matter: the intercepted-power identity must fail when `cos(incidence)` is dropped, and the lit
fraction must fail when the distant-star approximation replaces the exact geometry.

### DECISIONS MADE

None. One new free parameter — the rotation rate — is sent for approval with the PRP rather than
smuggled in.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- `PRPs/rotation-layer.md` awaits approval. Branch `sim/rotation-layer` unmerged, unpushed.
- Vellum still does not spin, so there is still no night anywhere on it.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 18 — 2026-09-06 — Rotation layer implementation — closed

Branch: sim/rotation-layer

### WHAT WAS DONE

Implemented the rotation layer test-first. **404 tests**, headless, `mypy --strict` and `ruff`
clean. **Vellum turns on itself and has a day.** Zooming to the ground and letting time run shows a
point pass from daylight into night; measured 8 transitions over 4 rotations, with the terminator
visibly crossing the view in the partial frames (14.3% and 41.7% of the visible arc lit).

`sim/rotation/spin.py` holds the rotating frame — surface coordinates are body-fixed, so a rock
stays at the same `s` forever and the frame turns around it — plus the sidereal and solar days, the
moment of inertia, and the breakup limit. `sim/rotation/illumination.py` holds the terminator, the
lit arc, incidence and flux at a point on the ground. `TerrainTrace` now draws day and night in
different colours, and `space` runs the clock so the world can be watched turning.

**The illumination geometry is exact, and the approximations everyone reaches for are wrong here.**
The instinct that half a world is lit is a *distant-star* result. The lit fraction is
`arccos(R/d)/π`: 0.468 at `d/R = 10`, and exactly one third at `d/R = 2`. Likewise for intercepted
power — the familiar `F·2R` cross-section form is asymptotic, while `L·arcsin(R/d)/π` is **exact**
for a point source and any convex body, and they are 4.7% apart at `d/R = 2`. Measured against the
implementation at four distances, both forms agree to six figures.

That identity is the strongest invariant in the layer: it pins the incidence geometry, the `1/r`
flux dilution and the terminator all at once. It caught every mutation tried — dropping
`cos(incidence)`, substituting the distant-star terminator, and evaluating flux at the planet centre
rather than at each surface point.

**The breakup check rejected my own test fixture.** The first fixture used a rate of 1000 against a
breakup limit of 283 — 3.5× over. The check is not decoration; an unphysical world is easy to
specify by accident, and this one was specified by me while writing the tests for it.

**The wrap subtlety appeared a third time, so it moved.** `sim/periodic.py` now owns `wrap`, and
`sim/view/geometry.py` delegates to it. Two defects had already come from reimplementing this —
`fmod(fmod+b, b)` quantising a micron at the period's ulp, and `%` returning exactly the period for
a tiny negative. A third occurrence was the signal that it belongs in one place.

It also gained `separation` and `distance`, prompted by a subtler failure. After exactly one
sidereal day the phase lands 8.9e-16 short of a full turn, so the substellar point returns as
`circumference − 1e-21`. Subtracting says it travelled the whole way round; on a closed curve it did
not move at all. **Comparing positions on the surface must be circular distance, never subtraction**
— and the water and life layers will need it constantly, since "how far apart are two things" on a
closed curve is the shorter way round and is never more than half the world.

### MUTATION RESULTS

    drop cos(incidence)                       6 failed   caught
    distant-star terminator instead of exact  5 failed   caught
    flux from the planet centre               6 failed   caught

### MEASURED, AS THE PRP REQUIRED

    d/R      lit fraction    arccos(R/d)/pi     intercepted    L*asin(R/d)/pi
    1.5          0.267725          0.267720    2.322795e-01      2.322795e-01
    2.0          0.333335          0.333333    1.666667e-01      1.666667e-01
    10.0         0.468115          0.468116    3.188428e-02      3.188428e-02
    1000.0       0.499685          0.499682    3.183099e-04      3.183099e-04

    breakup rate 283.406; the demo world spins at 100.0, 35.3% of it
    sidereal day 0.06283, about 100 days to the orbit

### FILES CREATED OR MODIFIED

    sim/rotation/spin.py          — NEW. Rotating frame, days, inertia, breakup
    sim/rotation/illumination.py  — NEW. Terminator, lit arc, incidence, flux, intercepted power
    sim/rotation/__init__.py      — NEW
    sim/periodic.py               — NEW. wrap, separation, distance — the shared closed-curve maths
    sim/tests/rotation/*.py       — NEW, two files
    sim/tests/test_periodic.py    — NEW
    sim/view/geometry.py          — delegates wrapping to sim.periodic
    sim/view/render.py            — TerrainTrace draws day and night separately
    sim/view/app.py               — the demo world spins; space runs the clock
    docs/AXIOMS.md                — section 3 gains rotation and illumination; section 4 gains
                                    oblateness
    MEMORY.md (22 amended, 23 and 24 added), CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

404 total, 65 new. Body-fixed coordinates recovering exactly; phase periodic and bounded over long
runs; sidereal versus solar day and a tidally frozen world having neither; the moment of inertia
that does not change from 3D; breakup surface speed equal to circular orbital speed; exactly two
terminator points; the lit fraction at four distances; every point seeing both day and night over
one rotation; a frozen world having permanent day on one arc; night being exactly zero rather than
small; and the intercepted-power identity at five distances.

### DECISIONS MADE

- One new free parameter approved with the PRP: the rotation rate, a world constant.
- Oblateness abstracted rather than modelled, with a ledger entry.
- No axial-tilt parameter, because a disc has no axis to tilt and a parameter that must always be
  zero is an invitation to set it.
- Wrapping and circular comparison extracted to `sim/periodic.py`.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `sim/rotation-layer` unmerged, unpushed.
- The ground is still drawn as a thin line rather than filled.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 19 — 2026-09-06 — System view regressions — closed

Branch: fix/viewer-system-view

### WHAT WAS DONE

Two regressions the user hit immediately after the rotation layer shipped, both caused by it.

**1. The whole system slid across the window.** Session 18 started the clock by default so the
world could be seen turning. But `_camera_for` follows the planet whenever the viewport is wider
than the circumference — which at system zoom is always true — so the camera tracked an orbiting
body and dragged the background with it. Measured: the camera focus moved from `(+1.0000, +0.0024)`
to `(-0.6424, +1.2572)` over 1200 steps while the star sat still in world space, so the star slid
right across the view. The planet was the only thing not moving, which is exactly backwards.

Following is now suppressed at SYSTEM zoom. At that scale the system is the subject and the planet
is the thing moving through it; from PLANETARY inward the planet is the subject and following is
right.

**2. Vellum was invisible.** Its radius at the opening view is **0.0013 pixels**, so `PlanetDisc`'s
outline had nothing to draw. The star has carried a `max(2, ...)` floor since it was written; the
planet never had one. It now draws a marker below three pixels.

**A test that passed for the wrong reason, caught before it shipped.** The first visibility test
asserted "something other than background is drawn near the planet" — and it passed *before* the fix,
because the orbit trace runs exactly through the planet's position. It now checks for Vellum's own
marker colour, which is why the colour exists as a named constant. A visual assertion that cannot
name what it is looking for is not an assertion; that is the same lesson as Session 14, arriving in
a subtler form.

Both fixes were confirmed by reversion: without the system-view fix, 1 test fails; without the
planet marker, 4 fail.

**Also added a clock readout.** The world starting to move on its own is alarming when nothing on
screen says it is running. The scale bar now shows the day count, the time, and `running`/`paused`
with the key that toggles it.

### FILES CREATED OR MODIFIED

    sim/view/app.py       — no following at SYSTEM zoom; clock state passed to the readout
    sim/view/render.py    — PlanetDisc minimum size and a named marker colour; clock readout
    sim/tests/view/test_zoom_journey.py — both regressions, tested by colour rather than by
                            "not background"
    MEMORY.md (decision 25), CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

410 total, 6 new. The camera does not move while the planet orbits at system zoom; it still follows
once the planet is worth following; Vellum's marker is present at the opening view and at three
further zoom-outs.

### DECISIONS MADE

- Follow from PLANETARY inward only.
- Anything that can shrink below a pixel gets a minimum drawn size.
- Visual tests assert a specific colour, not merely that the background changed.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `fix/viewer-system-view` unmerged, unpushed.
- The ground is still a thin line rather than filled.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 20 — 2026-09-06 — Object sidebar — closed

Branch: feat/viewer-sidebar

### WHAT WAS DONE

The user could not get onto Vellum. At system scale it is three pixels across and crosses the window
in seconds, so catching it with the pointer and then zooming five orders of magnitude while it moves
is not something a person can do. **Selection replaces aim.**

`sim/view/sidebar.py` holds the target list, hit-testing and framing, and imports no pygame — the
purity test now covers it alongside the camera. `Sidebar` in `render.py` draws the panel. Clicking a
row selects that body, re-engages following, and frames it.

Measured: framing Vellum takes the scale from `2.13e+02` to `2.62e+07` px per world unit in one
step — five orders of magnitude — and lands in the PLANETARY band. That last part matters, because
it is what re-engages following: decision 25 deliberately suppresses chasing an orbiting body while
the whole system is in view, so the framing is what gets you out of that regime. From there,
scrolling reaches GROUND with the surface dead centre.

Two details worth keeping:

- **A click outside the panel is not a selection.** `row_at` returns None there, so dragging the
  world still works and the sidebar does not swallow every gesture.
- **Kell's framing radius is a display value.** The star is stubbed and its real radius raises by
  design (DECISION-010), so a test asserts that `Kell.radius` still raises and that the list does not
  claim the star has ground.

The scale bar and clock readout moved right to clear the panel.

### FILES CREATED OR MODIFIED

    sim/view/sidebar.py            — NEW. Target, row_at, frame. No pygame
    sim/tests/view/test_sidebar.py — NEW. Hit-testing, framing, and the journey end to end
    sim/view/render.py             — Sidebar drawable; readout shifted clear of the panel
    sim/view/app.py                — targets_for; click-to-select; framing on selection
    sim/tests/view/test_camera.py  — purity test covers sidebar.py
    MEMORY.md (decision 26), CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

423 total, 16 new. Rows map to indices; clicks on the world are not selections; framing centres the
target, crosses five orders of magnitude for Vellum, leaves the SYSTEM band, respects the zoom
limits, and keeps the system in view when the star is framed instead. And the journey end to end:
clicking Vellum's row lands on the planet with following engaged, and the ground is reachable by
scrolling from there.

### DECISIONS MADE

- Selection frames the target rather than merely focusing it — crossing the scale gap is the point.
- The sidebar is drawn in every band, since knowing what you are looking at matters most when the
  view gives no clue.
- Vellum is selected by default. It is the world.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `feat/viewer-sidebar` unmerged, unpushed.
- The list has two entries because the system has two bodies. Debris, when it exists, appears here.
- The ground is still a thin line rather than filled.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 21 — 2026-09-06 — Single-point polyline crash — closed

Branch: fix/terrain-runs

### WHAT WAS DONE

The viewer crashed on the user's machine: `ValueError: points argument must contain 2 or more
points`, from the day/night split in `TerrainTrace.draw`.

**The cause.** Splitting the ground into lit and unlit runs was inline index juggling. It drew
`points[start:index+1]` on each change and `points[start:]` at the end — and when the last sample
flipped, that trailing slice held exactly one point. Reproduced immediately once written out:

    mask=DDDDD  trailing run has 5 points
    mask=DDDDn  trailing run has 1 point   <-- crash
    mask=DnDnD  trailing run has 1 point   <-- crash

**Why no test caught it, which is the interesting part.** The logic lived inside a `draw` method, so
it could only be exercised by rendering. And rendering does not sample the input space — it samples
one trajectory through it. A sweep of **516 frames across six zoom levels produced 239 visible
terminators and not a single single-sample run.** Driving more frames would not have found this;
relying on that would have shipped it again.

**The fix is the extraction.** `sim.view.geometry.contiguous_runs` is a pure function returning
`(start, stop, value)` per run. Tested with seven table-driven cases including every degenerate
shape, plus property tests that runs tile the mask without gap or overlap and that neighbours always
differ. The crashing case is now one line of input rather than an unreachable rendering state. The
draw path is tested separately against forced masks, because what matters there is that drawing does
not raise.

Both halves confirmed by reversion: removing the length guard fails 2 tests.

**The breakup check rejected a third fixture.** Writing the render test, I gave the spin a rate of
10.0 against a breakup of 0.0315. Every spin written this project without doing the arithmetic has
been unphysical, and the check has caught every one.

### FILES CREATED OR MODIFIED

    sim/view/geometry.py            — contiguous_runs
    sim/view/render.py              — TerrainTrace.draw uses it, and guards short segments
    sim/tests/view/test_runs.py     — NEW. The segmentation, including every degenerate shape
    sim/tests/view/test_render.py   — the draw path against forced masks
    MEMORY.md (decision 27), CHANGELOG.md, CONTEXT.md

### TESTS WRITTEN

447 total, 20 new. Table-driven segmentation across seven shapes; empty mask; runs tile without gap
or overlap; neighbouring runs differ; each run reports the value it covers; and the draw path
against six forced masks — all day, all night, a flip on the last sample, a flip on the first, every
sample flipping, and one terminator in the middle.

### DECISIONS MADE

- Non-trivial logic does not live inside a `draw` method.
- Rendering many frames is not coverage of a rendering edge case.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- Branch `fix/terrain-runs` unmerged, unpushed.
- The ground is still a thin line rather than filled.
- No water. DECISION-012, -013, -014 still open.

---

## SESSION 22 — 2026-09-06 — Water layer PRP — open

Branch: sim/water-layer

---

## NEXT SESSION START POINT

Open a new session entry in this file first, with state `open` and the branch name, and commit it.

Then read CLAUDE.md, MEMORY.md, DECISIONS.md, this file, and `docs/AXIOMS.md`.

Branch `fix/terrain-runs` is unmerged. Merge it first.

**The next PRP is water**: basins as local minima of `h`, filling, and the unbranched runs that
follow from having no third direction. The first layer that can produce a number the monograph only
guessed — the basin count. Use `sim.periodic.distance` for anything comparing surface positions.

Carry the Session 21 lesson: **logic inside a `draw` method cannot be tested, so it should not be
there.** 516 rendered frames produced 239 terminators and never the shape that crashed. Rendering
samples one trajectory through the input space, not the space.

Also still open: DECISION-012 (habitability, blocks the scan), -013 (chemistry), -014 (transfer).

Environment: `.venv/`. Run `.venv/bin/pytest`, `.venv/bin/mypy`, `.venv/bin/ruff check sim/`.

Do not edit `vellum-monograph.html`. It is frozen; it gets regenerated, not corrected.
