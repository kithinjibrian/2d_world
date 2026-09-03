# docs/source — Raw human context

The input layer. This folder holds the actual conversations, findings, direction, and constraints
that eventually produce entries in `MEMORY.md` and `DECISIONS.md`. Those two files are the output
layer; this is the raw material.

**The AI does not read this folder automatically.** Files are brought in explicitly:

- **At PRP creation** — reference the relevant file under `CONTEXT` → `Related source files`.
- **At session start** — "read `docs/source/[file]` before planning; it affects today's work."
- **When opening a DECISIONS.md entry** — cite it in the entry's `Notes`.
- **When updating MEMORY.md** — cite it in the decision's `Why`.

## Rules

- Every conversation that produces a decision, constraint, or open question gets a note. Not every
  conversation — only ones that change what gets built or how.
- Notes are written the same day. A note written a week later is a reconstruction, not a record.
- The **Impact on the Project** section is mandatory. A note without it is just an archive.
- If a note introduces something that conflicts with a decision in `MEMORY.md`, open a
  `DECISIONS.md` entry immediately. Never silently override a recorded decision.
- **Source files are never deleted.** If direction reverses or a constraint lifts, add a dated
  header to the original: `[SUPERSEDED — see docs/source/stakeholder/[new-file].md]`

## Layout

    meetings/      YYYY-MM-DD-[slug].md      — any meeting that affects the project
    research/      [topic].md                — user research, comparables, desk research
    stakeholder/   [topic]-YYYY-MM-DD.md     — direction from clients, founders, owners
    constraints/   [topic].md                — legal, compliance, platform, budget limits

Each subfolder has a `TEMPLATE.md`. Copy it; do not add sections it does not have.

## Where information goes

| Information | Goes in |
|-------------|---------|
| "No new species — seven is the point" | `stakeholder/` → then MEMORY.md once settled |
| "We chose inline SVG over a chart library" | MEMORY.md directly — already resolved |
| "Should the monograph become a simulation?" | DECISIONS.md directly — a pending question |
| "Readers got lost at the deep-time slide" | `research/` |
| "It must stay openable offline, forever" | `constraints/` |
| "We decided to delay the accessibility pass" | `meetings/` → then update the relevant PRP |
