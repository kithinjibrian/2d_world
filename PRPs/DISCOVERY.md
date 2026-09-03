# Discovery Interview Protocol

Use when a request arrives without a PRP.

## When to Run a Discovery Interview

Any time a feature or document is described in one or two sentences without specifying:
- What triggers it and what it produces
- Who is affected and how
- What the error and edge-case behavior should be
- Which existing files it touches
- What it must not touch
- Which axioms it rests on, and whether it needs a new free parameter
- Which open decisions in DECISIONS.md are relevant

## Question Sequence

Ask one question at a time. Do not batch questions. Wait for the answer before continuing.

Cover in order:
1. What does it do — input, processing, output
2. Who reads or uses it, and when
3. What happens when it fails — the user-facing result on each failure path
4. Edge cases — empty states, the first and last slide, invalid input, a fact that turns out to be
   missing
5. Which existing files it reads from or writes to
6. What it must never modify
7. **Which axioms does this rest on, and does it introduce any new free parameter?** Name them by
   tier identifier. A new free parameter is a new axiom — stop and get it approved before
   continuing. Also ask what it must *not* contradict in `docs/AXIOMS.md` §3 — those are theorems.
8. **Does it lean on anything in the abstraction ledger (§4)?** If so, any result it produces is a
   consequence of a choice rather than a finding about 2D physics, and both the PRP and the module
   must say so.
9. Are there open entries in DECISIONS.md this depends on?
10. What are the security implications — any file loaded, any format that executes on load
   (never pickle), any generated content entering the monograph's DOM?
11. What does rollback look like if this is abandoned?
12. How is success verified — what can be run or read to prove it works?

## After the Interview

Write the completed PRP to `PRPs/[feature-name].md` using `PRPs/TEMPLATE.md`.
Present it to the user.
Wait for explicit approval before writing anything.

## PRP Quality Check

Before approving one, verify:

- [ ] The work is described in terms of visible behavior or reader-visible content, not implementation
- [ ] Every existing file the implementation will touch is listed
- [ ] "Must NOT do" covers the most common wrong approaches for this type of work
- [ ] The derivation check is filled in and every new free parameter is flagged for approval
- [ ] The test list separates dimensional, invariant and regression tests, and asserts no monograph number
- [ ] Error handling describes what happens on every failure path
- [ ] Security considerations are filled in — not left blank
- [ ] Test cases or a verification list are written before implementation starts
- [ ] Rollback plan is specified
- [ ] Blocking DECISIONS.md entries are listed
- [ ] Acceptance criteria are testable — each can be verified with a command or a specific check
- [ ] The validation section has runnable commands, not just "test it"
