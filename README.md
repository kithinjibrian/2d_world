# Vellum (2d_world)

A natural history of a world with two dimensions — length and height, and nothing else.

Vellum has no sideways. No creature has ever gone around another; no root has ever spread beneath a
rival; no eye has ever been worth the trouble of growing. Everything in the monograph follows from
that one fact: a star nothing can escape, rivers that cannot branch, animals with one aperture doing
two jobs, a world that is blind and extremely loud, and seven kinds of life that hold it.

**Read it:** open `vellum-monograph.html` in a browser. No server, no build, nothing to install.
Arrow keys navigate; slide I lists the contents.

---

## Working on this repo

This project uses a context engineering system so that AI coding sessions stay consistent and do not
drift. If you are an AI assistant, read these in order before doing anything:

| File | What it is |
|------|------------|
| `CLAUDE.md` | Behavioral rules. Each one prevents a specific mistake. Start here. |
| `MEMORY.md` | Resolved architectural decisions, with the reasoning and what they rule out |
| `DECISIONS.md` | Open questions. An open decision blocks the code it affects |
| `CONTEXT.md` | Session handoff log — what happened last session and where to pick up |
| `CHANGELOG.md` | What shipped, for humans |
| `docs/DESIGN.md` | Design tokens and component rules. Read before touching any markup |
| `docs/CODE_STYLE.md` | Documentation rules. Read before writing any function |
| `PRPs/` | One brief per feature, written and approved *before* any code |
| `docs/source/` | Raw human context — meetings, research, direction, constraints |
| `reports/` | End-of-day summaries |

Two rules matter more than the rest:

1. **Open a session before you do anything.** Append an entry to `CONTEXT.md` with state `open` and
   the branch name, and commit it, before reading anything else or writing a line.
2. **The monograph is the canon.** Every fact about Vellum either already appears in
   `vellum-monograph.html` or does not exist. Do not invent one — open a `DECISIONS.md` entry.

`setup.md` is the external guide this system was built from. It is reference material, not a
project document, and is not edited.

## Licence

GPL-3.0. See `LICENSE`.
