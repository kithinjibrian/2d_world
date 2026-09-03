# CLAUDE.md — Vellum (2d_world)

Behavioral instructions for AI coding assistants. Each rule exists to prevent a specific mistake.

Vellum is a simulation of a world with two spatial dimensions — one extended coordinate and one
vertical, no third direction. The project derives that world's physics from first principles rather
than importing it. `vellum-monograph.html` is a prior hypothesis document, not a specification.

Read `docs/AXIOMS.md` before writing any physics. Its axioms are tiered, it works in natural units
rather than SI, and its §4 ledger records everything the project posits rather than derives.

---

## SESSION HANDOFF RULE — NON-NEGOTIABLE

Every session in `CONTEXT.md` must have:
- A **name** — short descriptive title of what the session accomplished
- A **state** — `open` while work is in progress, `closed` once handoff is done
- A **branch** — the git branch this session's work lives on

Format:

    ## SESSION {n} — {YYYY-MM-DD} — {Name} — {state}
    Branch: {branch-name}

Rules:
- **Step 1 of every session, no exceptions:** append a new session entry to `CONTEXT.md` with state
  `open` and the current branch name. Do this before reading any other file, before planning, before
  writing any code. The entry must exist and be committed before any other work begins.
- Mark it `closed` only after CONTEXT.md is updated and committed and pushed.
- Never leave a session `open` at the end of a turn.
- Never start a new session without closing the previous one first.
- The NEXT SESSION START POINT block is always rewritten at the end of every session.
- Sessions are never deleted — the full history stays in this file.

---

## DERIVATION RULE — NON-NEGOTIABLE

The simulation is the authority on what is true about Vellum. Nothing enters the world by fiat.

Every quantity in the codebase is exactly one of three things:

1. **An axiom** — a free choice, listed in `docs/AXIOMS.md` §1. Axioms are tiered: Tier 0 is
   geometry and mechanics, Tier 1 the fundamental interactions, Tier 2 the effective theories.
   Adding one requires human approval and a DECISIONS.md entry.
2. **A world constant** — an initial condition for a particular world instance: the seed, Kell's
   mass, total angular momentum, initial composition.
3. **A derived result** — computed from the above, carrying a comment naming what derived it.

A number that fits none of those three is a bug. Before writing any constant, decide which of the
three it is. If you cannot, stop and open a DECISIONS.md entry.

**Never do these:**

- **Never tune a parameter to reproduce a number from the monograph.** This is the single most
  important rule in the file. The monograph was written before anything was checked; it is a guess.
  Fitting the simulation to it destroys the only thing that makes the result worth having. If the
  simulation disagrees with the monograph, the monograph is wrong.
- **Never import a constant or scaling law from a 3D reference without re-deriving it in 2D.**
  `G = 6.674e-11` is not `G₂` — it is not even the same kind of quantity. Density is kg·m⁻²,
  pressure is N·m⁻¹, radiated flux goes as `T³`. See `docs/AXIOMS.md` §2. Nothing will crash if
  this is wrong; the numbers will simply be meaningless.
- **Never express a constant in SI.** The project works in natural units: `G₂ = 1`, `σ₂ = 1`, and a
  chosen reference mass and length fix the rest. There is no correct SI value for a constant of
  another universe. Physics lives in dimensionless ratios; SI conversion happens only at the display
  layer. See `docs/AXIOMS.md` §2.
- **Never present a result that rests on an abstracted layer as a discovery.** Electromagnetism,
  matter microstructure and chemistry are posited, not derived — `docs/AXIOMS.md` §4 is the ledger.
  A result depending on one of those is a consequence of a choice, and must be reported that way. A
  module standing in for an abstracted layer raises where it cannot honestly answer; it never
  returns a plausible default.
- **Never hand-place a phenomenon that should emerge.** Do not place storms, seed basins at chosen
  positions, or script a behaviour that the physics is supposed to produce. If it does not emerge,
  that is a finding to report, not a gap to fill.
- **Never adjust a result to match `docs/AXIOMS.md` §3.** Those are theorems. If the simulation
  contradicts one, the derivation has a bug — find it.
- **Never write a number without a derivation reference.** See the CODE DOCUMENTATION RULE.

**What the monograph is still good for:** the topological prohibitions it describes are real
theorems (see `docs/AXIOMS.md` §3), and it is the long-term output target — the goal is to
regenerate it from simulation results. It is never an input.

---

## PRP RULE — NON-NEGOTIABLE

Never write code without a PRP file in `PRPs/`.

If a request arrives without a PRP:
1. Do not write any code.
2. Run the discovery interview in `PRPs/DISCOVERY.md` — one question at a time.
3. Cover: what it does, what it derives, what it must not touch, which axioms and which tier it
   depends on, whether it leans on anything in the abstraction ledger, and what the invariant tests
   are.
4. Write the PRP to `PRPs/[feature-name].md`.
5. Present it to the user for approval.
6. Only build after explicit approval.

A vague prompt is not a starting point. It is the beginning of a discovery.

Exempt: fixing a typo, and the maintenance writes to CONTEXT.md / CHANGELOG.md / DECISIONS.md that
every session performs.

---

## SCOPE RULE — NON-NEGOTIABLE

One PRP at a time. Never implement more than one module's scope in a single session.

This project is deliberately being built slowly, one derived layer at a time. Each layer is only
trustworthy if the layer beneath it was finished and verified first.

If mid-implementation you discover the scope is larger than the PRP described:
1. Stop immediately. Do not continue implementing.
2. Document what was discovered.
3. Update or create a new PRP for the expanded scope.
4. Get approval before continuing.

The model does not decide that something is "small enough to add." The human decides.

---

## PENDING DECISIONS RULE — NON-NEGOTIABLE

Before writing anything that depends on an unresolved question, check `DECISIONS.md`.

- If the decision is `open`, stop. Do not implement. Ask the user to resolve it first.
- If the decision is `resolved`, follow the outcome recorded there — do not re-litigate it.
- If you encounter a new unresolved question mid-implementation, add it to `DECISIONS.md` as `open`
  and stop. Do not guess.

Never make an architectural or physical choice silently. If you are guessing, you are making a
decision that belongs in DECISIONS.md.

---

## TESTING RULE — NON-NEGOTIABLE

Write the failing test before writing the implementation. No exceptions.

Tests live in `sim/tests/` and mirror the source tree: `sim/orbit/integrator.py` →
`sim/tests/orbit/test_integrator.py`. Run with `pytest`.

There are three kinds of test in this project, and the order matters:

**1. Dimensional tests — write these first for any new module.** Assert that every quantity carries
the 2D dimensions in `docs/AXIOMS.md` §2. These catch the failure mode that produces plausible
wrong numbers instead of crashes. Assert that dimensionless results really are dimensionless — in
natural units a dimensional slip is easy to miss, because the offending constant is 1.

**2. Invariant tests — the core of the suite.** Assert what must hold for *every* world and *every*
seed, not what happened in one run:
- Conservation: energy, momentum, angular momentum, mass. Assert bounded drift over a long run,
  with an explicit tolerance justified in a comment.
- Boundedness: no trajectory is ever unbound (a direct consequence of the log potential — if one
  escapes, the integrator is broken).
- Topological: no tissue loop closes; a barrier partitions the surface.
- Ordering: the sort order of surface bodies never changes except by birth and death.
- Finiteness: no NaN or infinity anywhere in any state array, ever.

**3. Regression tests.** A seeded world produces byte-identical output across runs. These pin
determinism, and they are the only tests allowed to assert a specific number — the number is
whatever the sim produced, recorded as a golden value, and a change to it is a change to be
explained, not a failure to be silenced.

**Never write a test that asserts a number from the monograph.** Outcomes are results to be read.
Invariants are what gets tested. A test that encodes a guessed number is worse than no test — it
locks the simulation to a hypothesis and disguises the lock as verification.

After any non-trivial change, run the full suite before considering the task done.

---

## ERROR HANDLING — NON-NEGOTIABLE

This project uses **exceptions**, in the ordinary Python way. Do not build Result/Either types —
Python has no checked exceptions to route around and no compiler to enforce the discipline, so the
ceremony costs the readability and returns nothing.

    Invalid input, impossible state, broken invariant  →  raise
    Recoverable, expected, part of normal operation    →  return a value

### Rules

- **Validate at module boundaries.** A public function checks its arguments and raises immediately.
  Internal helpers may assume their inputs are already valid; say so in the docstring.
- **Raise a specific exception type.** All project exceptions subclass `VellumError`. Never raise
  bare `Exception`, and never raise a string.
- **Never catch bare `except:` or `except Exception:`** unless you re-raise. Swallowing an exception
  in a numerical kernel converts a wrong answer into a silent wrong answer.
- **Fail fast on non-finite values.** Any numerical kernel checks its output for NaN and infinity
  and raises on encountering one. A NaN that propagates for a thousand steps costs an afternoon to
  trace; the check costs a microsecond.
- **Assert invariants in the code, not only in the tests.** Physical invariants — conservation,
  boundedness, ordering — are cheap to check at step boundaries and are the fastest way to localise
  a bug to a single tick. Use a debug flag if the cost matters in a long run.
- **Never silently clamp.** If a value leaves its physical range, raise. Clamping hides the bug that
  produced it and yields a result that looks fine.

### Typing

Type hints are required on every public function. `mypy --strict` must pass on `sim/`. This is where
the compile-time checking comes from; it is not optional decoration.

---

## SECURITY RULE — NON-NEGOTIABLE

Never implement the following without explicit human review and approval:
- Authentication or session management
- Authorization / permission checks
- Cryptographic operations
- Payment processing
- Secrets or credential handling

For everything else:
- Never hardcode credentials, API keys, tokens, or secrets. Not even in comments or example values.
- Never trust input from a file, a URL, or an external API without validation first.
- **Never `pickle` simulation state, and never load a pickle.** Unpickling executes arbitrary code.
  World files use `.npz`, HDF5, or another data-only format.
- Never `eval` or `exec` a configuration value or an expression from a file.

Applies to the monograph: `vellum-monograph.html` builds TOC entries with `innerHTML` from `data-t`
attributes. Safe only while every title is author-written. If titles ever come from generated data —
which becomes likely once the sim regenerates the document — this becomes an injection point and
must be changed to `textContent` first.

---

## DESIGN RULE

Read `docs/DESIGN.md` before writing any markup, styling, or plate-generating code.

This applies to the monograph and to any SVG the simulation generates for it. Generated plates use
the same colour tokens and the same plate classes as the hand-drawn ones — a generated figure must
be indistinguishable in style from `Plate IV`. Never write a raw hex value outside the `:root`
block. The typography scale is frozen at the fourteen existing sizes; see DECISION-004.

---

## CODE DOCUMENTATION RULE — NON-NEGOTIABLE

Read `docs/CODE_STYLE.md` before writing any function, class, or module.

Every public function, class, and type gets a docstring. Every non-obvious decision inside a
function gets an inline comment explaining *why*, not what.

**Vellum-specific and non-negotiable:** every physical quantity carries a derivation reference —
the tiered axiom it comes from, the module that computed it, or the abstracted layer it stands in
for.

    # AXIOM (T1.1): gravity is postulated, not geometric — 2+1D GR has zero
    # propagating degrees of freedom. Gauss's law in a plane gives F ∝ 1/r.
    # WORLD CONSTANT: set per world instance, see World.from_seed
    # DERIVED: from T2.2 (T^3 emission) and the solve in sim/star/structure.py
    # ABSTRACTED (T1.2): stands in for electromagnetism — see AXIOMS.md §4

A number without a derivation reference is indistinguishable from an invented one a session later.
This is the mechanism that makes the DERIVATION RULE enforceable rather than aspirational.

---

## FILE SIZE RULE

**300 lines maximum for code** (resolved, DECISION-003). Documents have no limit — prose and
derivations are split by argument, not by line count.

When a file reaches the limit:
1. Stop before adding more code.
2. Propose a split to the user — show the proposed new file names and what moves where.
3. Wait for approval.
4. Split, then continue.

Do not ask "should I split this?" — propose the specific split.

---

## PROTECTED FILES — NON-NEGOTIABLE

Never read, modify, or delete the following under any circumstances:

- `.env` and `.env.*` (any environment file)
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `uv.lock` (lockfiles)
- `migrations/` and `*.migration.*`
- `LICENSE` (GPL-3.0 — legal text, never edited)
- `.git/` (repository internals)
- `setup.md` (external guide; reference only, superseded by the files it produced)

Append-only — read freely, add to the end, never rewrite or delete existing entries:
- `CHANGELOG.md` — past entries are never modified
- `CONTEXT.md` — past sessions are never deleted or edited, only superseded by later ones
- `reports/` — EOD reports are never deleted
- `docs/decisions/` — ADRs are never renumbered or removed
- `docs/source/` — source notes are superseded with a dated header, never deleted

Frozen — do not modify without an approved PRP:
- `vellum-monograph.html` — the prior hypothesis document. It is reference material and an output
  target. Do not correct its physics by hand; it gets regenerated from simulation results.

If a task seems to require touching a protected file, stop and ask the user how to proceed.

See also `.llmignore`, which must stay in sync with this section.

---

## COMMANDS

The simulation tree does not exist yet — it arrives with the first approved PRP. These are the
commands it will be set up to support, and every one of them must work before that PRP is done:

    pytest                        # full suite
    pytest sim/tests/orbit -x     # one module, stop on first failure
    mypy --strict sim/            # required to pass
    ruff check sim/               # lint

Working today:

    xdg-open vellum-monograph.html    # read the monograph

Run `pytest` and `mypy --strict` after every non-trivial change. A task is not done until both pass.

**Do not add a dependency to make something work.** The dependency list under STACK is closed;
adding to it is a decision, not an implementation detail.

---

## STACK

**Simulation** — resolved, DECISION-001:
- Python 3.11+
- `numpy` — the world is arrays; this is the workhorse
- `scipy` — integrators, FFT, optimisation
- `matplotlib` — plate generation, SVG output
- `pytest`, `mypy`, `ruff`

No game engine, no ECS library, no simulation framework, no notebook-driven development. The
computation is array math on periodic domains; a framework would add indirection and no capability.

**Monograph** — unchanged:
- Single self-contained HTML file, no build step, opens from `file://`
- Two Google Fonts (Fraunces, Spectral); inline SVG for every plate

---

## ARCHITECTURE RULES

1. **Two trees, one bridge.** `vellum-monograph.html` stays a self-contained document with no build
   step. The simulation lives in `sim/`. The only connection between them is generated SVG plates
   written into the document. Neither tree imports from the other.
2. **Determinism is a hard requirement.** A seed reproduces a world byte-for-byte. Every random
   source is an explicitly seeded `numpy.random.Generator` passed down from the world constructor.
   Never call module-level `np.random.*`, never use `random`, never read the clock or the
   environment during generation, never depend on set or dict iteration order for numerical results.
   A world you cannot regenerate is a world you cannot study.
3. **Generation is separate from query.** Building a world is slow and happens once; reading it is
   fast and happens constantly. Generated worlds persist to disk as data-only files (`.npz`/HDF5 —
   never pickle) and are loaded read-only.
4. **The surface is one periodic 1D array.** Position is a scalar in `[0, L)`. Wraparound is
   implemented in exactly one place and used everywhere; never open-code a modulo against the
   circumference.
5. **The order of surface bodies is invariant.** Nothing passes anything on the line — a topological
   consequence, see `docs/AXIOMS.md` §3. So an array sorted by position stays sorted for the life of
   every body in it, and the array index *is* the spatial index. Neighbours are `i±1`. Do not build
   a spatial hash, a quadtree, or a broad phase; do not re-sort each tick. Births and deaths insert
   and delete — nothing else ever reorders.
6. **Natural units throughout; dimensions enforced by the units layer, not by comments.** `G₂ = 1`,
   `σ₂ = 1`, with a chosen reference mass and length fixing the rest. No physical constant enters
   the codebase except through the units layer, and no SI value appears outside the display layer.
   See `docs/AXIOMS.md` §2.
7. **Derived layers depend downward only.** Star → orbit → planet → surface → water → air → life.
   A lower layer never reads from a higher one. If it needs to, the layering is wrong — stop and
   open a decision.

---

## ANTI-PATTERNS

1. **Never tune anything to match the monograph.** Restated from the DERIVATION RULE because it is
   the failure this project is most likely to suffer: the monograph is vivid and specific, and
   matching it feels like progress. It is the opposite.
2. **Never import a 3D constant or scaling law, and never reach for an SI value.** In 2D, gravity
   goes as `1/r`, flux goes as `1/r`, emission goes as `T³`, density is per area, pressure is per
   length. A 3D value substituted here produces a plausible number that means nothing, and there is
   no correct SI value for a constant of another universe.
3. **Never treat a posited quantity as a derived one.** If it is in the abstraction ledger
   (`docs/AXIOMS.md` §4), any result depending on it is a consequence of a choice, not a finding
   about two-dimensional physics.
4. **Never introduce an unseeded random source.** It silently destroys reproducibility, and you will
   not notice until you try to regenerate a world you cared about.
5. **Never hand-place an emergent phenomenon.** Storms, basins, and species distributions are
   results. Placing them by hand and reporting them as findings is the deepest way to waste this
   project's time.
6. **Never let a non-finite value propagate.** Check and raise at the kernel boundary.
7. **Never add a framework, engine, or dependency to solve a structural problem.** The structure is
   arrays on periodic domains. If that feels insufficient, the design is wrong, not the tooling.
8. **Never let a fact live only in the conversation.** A derivation you worked out and did not write
   down evaporates at the end of the session. It goes in `docs/AXIOMS.md`, a docstring, or a
   DECISIONS.md entry before the session closes.
9. **Never edit `setup.md`.** External reference material.

---

## KNOWN ISSUES — DO NOT FIX

1. **The monograph's apsidal precession figure (~900 years) is wrong.** A `1/r` force gives roughly
   105° of regression per orbit, so seasons cycle in ~3.4 orbits — a factor of ~300 out. Recorded in
   `docs/AXIOMS.md` §3. **Do not edit the monograph to correct it.** It is a frozen hypothesis
   document and gets regenerated from simulation output once there is output to regenerate it from.
2. **The monograph's `roman` array is hardcoded to 18 entries.** A 19th slide gets an `undefined`
   TOC label with no error. Real, and it matters if the document is ever regenerated
   programmatically — but it needs a PRP, not a drive-by fix.
3. **The monograph's SVG plate classes hardcode hex values** instead of referencing the colour
   tokens. Values are currently identical to the tokens. Generated plates must use `var(--token)`;
   do not extend the deviation.
4. **The monograph has no landmark regions and no ARIA.** Deliberately deferred, DECISION-007. Do
   not add attributes ad hoc.
