## FEATURE: [one sentence]

## OBJECTIVE
[2–3 sentences describing what "done" looks like. For a physics module, say what it derives and
what the result is used for downstream.]

## CONTEXT

- Starting state: [which files currently exist and are relevant]
- Ending state: [which files will be created or modified]
- Related existing code: [specific file paths to read before starting]
- Axioms this depends on: [which entries in docs/AXIOMS.md §1 this rests on, and which
  established consequences in §3 it must not contradict]
- New free parameters introduced: [each one is an axiom and needs approval — or "none"]
- Open decisions that must be resolved first: [list DECISIONS.md entries that block this]
- Related source files: [docs/source/... if this was shaped by a meeting, research, or constraint]

## IMPLEMENTATION REQUIREMENTS

### Must Do
- [specific requirement]
- [specific requirement]

### Must NOT Do
- [explicit exclusion — be specific about why]
- [explicit exclusion]

## DERIVATION CHECK

Confirm before implementation. Every box must be ticked or the PRP is not ready:
- [ ] Every quantity is classified as an axiom, a world constant, or a derived result
- [ ] No constant or scaling law is imported from a 3D reference without being re-derived in 2D
- [ ] All dimensions match docs/AXIOMS.md §2 (density kg·m⁻², pressure N·m⁻¹, G₂ m²·kg⁻¹·s⁻²,
      emission ∝ T³, flux ∝ 1/r)
- [ ] Nothing is tuned, fitted, or calibrated to reproduce a number from the monograph
- [ ] Nothing that should emerge is hand-placed
- [ ] Every new free parameter is listed above and approved
- [ ] Any random source is an explicitly seeded Generator threaded from the world constructor

New free parameters requiring human approval: [list them, or "none"]

## ERROR HANDLING REQUIREMENTS

- [Which failures this must surface and how]
- [Which it can ignore and why]
- [What the caller receives on each failure path]
- For documents: what happens when a fact is missing — the answer is always "stop and open a
  DECISIONS.md entry", never "write something plausible"

## SECURITY CONSIDERATIONS

- [Input validation — what must be validated before processing]
- [Auth requirements, if any]
- [Data exposure risks]
- [If any restricted category applies — auth, crypto, payments, secrets — note that human review is
  required before merging]
- If this introduces any content into the DOM that is not author-written, say so explicitly. See the
  SECURITY RULE in CLAUDE.md about `innerHTML` in the navigator.

## TESTS TO WRITE

Written before any implementation. Three kinds, in order — see the TESTING RULE in CLAUDE.md.

**Dimensional** — every quantity carries its 2D dimensions:
- [ ] [describe]

**Invariant** — true for every world and every seed, not just this run:
- [ ] Conservation: [which quantity, over what interval, within what tolerance and why]
- [ ] Boundedness / topology / ordering: [whichever apply]
- [ ] Finiteness: no NaN or infinity in any state array

**Regression** — determinism:
- [ ] A fixed seed reproduces byte-identical output

**Error paths:**
- [ ] [each raise, and what triggers it]

No test may assert a number taken from the monograph.

## ROLLBACK PLAN

If this needs to be abandoned mid-implementation:
- Branch to return to: [branch name]
- State the codebase should be in: [describe]
- Anything irreversible: [migrations, published URLs, or "none"]

## ACCEPTANCE CRITERIA
- [ ] [testable criterion]
- [ ] [testable criterion]
- [ ] Derivation check above is fully ticked
- [ ] `pytest` passes
- [ ] `mypy --strict sim/` passes
- [ ] `ruff check sim/` passes
- [ ] Every physical quantity has a units-bearing docstring and a derivation reference
- [ ] Every physics module has an `Axioms used` line
- [ ] No new dependency
- [ ] No file over 300 lines
- [ ] CHANGELOG.md updated
- [ ] CONTEXT.md session entry closed

## VALIDATION
Run these to verify completion:
- `pytest`
- `mypy --strict sim/`
- `ruff check sim/`
- [any module-specific check — e.g. "energy drift under 1e-9 relative over 1e6 steps"]
