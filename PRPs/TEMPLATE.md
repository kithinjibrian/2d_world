## FEATURE: [one sentence]

## OBJECTIVE
[2–3 sentences describing what "done" looks like from a reader's or user's perspective]

## CONTEXT

- Starting state: [which files currently exist and are relevant]
- Ending state: [which files will be created or modified]
- Related existing code: [specific file paths to read before starting]
- Canon this depends on: [which plates in vellum-monograph.html establish the facts this uses —
  quote the numbers you will rely on, so a mismatch is caught before implementation, not after]
- Open decisions that must be resolved first: [list DECISIONS.md entries that block this]
- Related source files: [docs/source/... if this was shaped by a meeting, research, or constraint]

## IMPLEMENTATION REQUIREMENTS

### Must Do
- [specific requirement]
- [specific requirement]

### Must NOT Do
- [explicit exclusion — be specific about why]
- [explicit exclusion]

## CANON CHECK

Confirm before implementation. Every box must be ticked or the PRP is not ready:
- [ ] Every fact used appears in `vellum-monograph.html`, or is listed below as a new fact requiring
      approval
- [ ] Nothing introduced requires a third direction — no sideways, lateral, yaw, roll, around, beside
- [ ] Nothing introduced sees, or is coloured, patterned, or displayed for an observer
- [ ] Nothing introduced closes a ring of tissue — no through-gut, closed circulation, lens, wheel,
      axle, or rotating joint
- [ ] Everything introduced passes the profile test: it can be drawn as a single closed outline
- [ ] The species count is unchanged at seven (Springhopper and Driftbladder are one animal)

New facts requiring human approval: [list them, or "none"]

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

List the specific test cases before any implementation begins:
- [ ] Happy path: [describe]
- [ ] Error path: [describe each failure variant]
- [ ] Edge case: [describe]

For document work, the equivalent is a verification list — what a reader can check to confirm the
change is correct:
- [ ] [e.g. the new plate's caption number follows the previous plate's]
- [ ] [e.g. every number in the new prose matches its plate]

## ROLLBACK PLAN

If this needs to be abandoned mid-implementation:
- Branch to return to: [branch name]
- State the codebase should be in: [describe]
- Anything irreversible: [migrations, published URLs, or "none"]

## ACCEPTANCE CRITERIA
- [ ] [testable criterion]
- [ ] [testable criterion]
- [ ] Canon check above is fully ticked
- [ ] The monograph still opens correctly from `file://` with no server
- [ ] No new hardcoded colour — every colour references a token in `:root`
- [ ] No new dependency, build step, or external file
- [ ] CHANGELOG.md updated
- [ ] CONTEXT.md session entry closed

## VALIDATION
Run these to verify completion:
- `xdg-open vellum-monograph.html` — step through every slide with arrow keys, confirm the TOC,
  position counter, and masthead all update and the first/last buttons disable correctly
- [any feature-specific check]
