# docs/decisions — Architecture Decision Records

An ADR is the permanent record of one decision. Numbered sequentially, never renumbered, never
deleted.

## Structure

1. Title — `ADR-{n}: [Decision in one sentence]`
2. Status — Proposed | Accepted | Deprecated | Superseded by ADR-{n}
3. Context — the situation that forced a decision
4. Decision — what was decided, in one paragraph
5. Consequences — what this makes easier, harder, or impossible
6. Alternatives Considered — what was rejected and why

## Relationship to DECISIONS.md and MEMORY.md

- `DECISIONS.md` tracks the question while it is open.
- An ADR is written when a decision is significant enough to need its full reasoning preserved.
- When an ADR is created, mark the DECISIONS.md entry resolved and point it at the ADR file.
- `MEMORY.md` carries the short form the next session reads; the ADR carries the long form.

Not every resolved decision needs an ADR. Most only need a MEMORY.md entry. Write an ADR when the
alternatives were genuinely close, or when a future session will otherwise try to reverse it.

Filename: `ADR-{n}-{slug}.md`
