# docs/specs — Technical specifications

Written on demand only. The AI never writes a document unless told to, and never adds a section
beyond the approved structure.

## Structure — approve before any content is written, then lock it

1. Executive Summary — what this is and why it exists (max 150 words; **write it last**)
2. Background — context and motivation
3. Goals — numbered, and testable
4. Non-Goals — what this explicitly does not cover
5. Design / Architecture — how it works
6. Implementation Plan — steps, in order, with owners if known
7. Open Questions — numbered; each maps to a DECISIONS.md entry
8. References — related docs, PRPs, tickets

## Rules

- Goals must be testable. "Improve performance" is not a goal. "First slide interactive in under
  200 ms on a cold load" is.
- Non-Goals must exist. A spec without them is incomplete.
- Open Questions map to DECISIONS.md entries. Do not resolve them in the spec — let DECISIONS.md
  track the outcome.
- Superseded specs are marked `[SUPERSEDED by docs/specs/{filename}]` at the top, never deleted.

Filename: `[slug].md`
