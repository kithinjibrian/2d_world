# Discovery Interview Protocol

Use when a request arrives without a PRP.

## When to Run a Discovery Interview

Any time a feature or document is described in one or two sentences without specifying:
- What triggers it and what it produces
- Who is affected and how
- What the error and edge-case behavior should be
- Which existing files it touches
- What it must not touch
- Which canon it depends on, and whether it needs any fact that does not yet exist
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
7. **Which plates establish the facts this depends on — and does it need any fact that is not yet
   in the monograph?** If yes, that fact is a decision. Stop and get it approved before continuing
   the interview.
8. Are there open entries in DECISIONS.md this depends on?
9. What are the security implications — does anything enter the DOM that is not author-written?
10. What does rollback look like if this is abandoned?
11. How is success verified — what can be run or read to prove it works?

## After the Interview

Write the completed PRP to `PRPs/[feature-name].md` using `PRPs/TEMPLATE.md`.
Present it to the user.
Wait for explicit approval before writing anything.

## PRP Quality Check

Before approving one, verify:

- [ ] The work is described in terms of visible behavior or reader-visible content, not implementation
- [ ] Every existing file the implementation will touch is listed
- [ ] "Must NOT do" covers the most common wrong approaches for this type of work
- [ ] The canon check is filled in and every new fact is flagged for approval
- [ ] Error handling describes what happens on every failure path
- [ ] Security considerations are filled in — not left blank
- [ ] Test cases or a verification list are written before implementation starts
- [ ] Rollback plan is specified
- [ ] Blocking DECISIONS.md entries are listed
- [ ] Acceptance criteria are testable — each can be verified with a command or a specific check
- [ ] The validation section has runnable commands, not just "test it"
