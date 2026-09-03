# Vellum (2d_world)

A simulation of a world with two spatial dimensions — one extended coordinate and one vertical,
and no third direction.

The physics is derived, not imported. In two dimensions gravity spreads over a circle rather than a
sphere, so it falls as `1/r`, the potential is logarithmic, and **nothing can ever leave the
system** — including its atmosphere, which therefore never thins. Blackbody emission scales as `T³`
rather than `T⁴`, making climate a twitchier thing than it is here. Turbulence cascades backwards,
so storms merge and persist instead of shredding. Huygens' principle fails in even dimensions, so no
sound anywhere ever arrives without a tail. And any closed curve disconnects the plane, which turns
a lot of ordinary anatomy — a through-gut, a circulatory loop, a lens, a wheel — into theorems about
what cannot exist.

The point is to find out what such a world actually does, rather than to decide.

## The two artefacts

**`vellum-monograph.html`** — a natural history of Vellum: its star, its deep time, and seven kinds
of life. Open it in a browser; no server, no build, nothing to install. Arrow keys navigate.

It was written *before* any of the physics was checked, so it is a **hypothesis, not a
specification**. Some of it is already known to be wrong — its ~900-year seasonal precession should
be about 3.4 years under a `1/r` force. It is frozen, and no simulation parameter may be tuned to
reproduce anything in it. The long-term goal is to regenerate it from simulation output, with real
numbers and plates the simulation drew.

**`sim/`** — the simulation. Python, numpy, no framework. Does not exist yet; it is being built one
derived layer at a time: star → orbit → planet → surface → water → air → life.

---

## Working on this repo

This project uses a context engineering system so AI coding sessions stay consistent and do not
drift. If you are an AI assistant, read these in order before doing anything:

| File | What it is |
|------|------------|
| `CLAUDE.md` | Behavioral rules. Each one prevents a specific mistake. Start here. |
| `docs/AXIOMS.md` | The axioms, the 2D dimensions, and the established consequences |
| `MEMORY.md` | Resolved decisions, with reasoning and what they rule out |
| `DECISIONS.md` | Open questions. An open decision blocks the code it affects |
| `CONTEXT.md` | Session handoff log — what happened last session and where to pick up |
| `CHANGELOG.md` | What shipped, for humans |
| `docs/CODE_STYLE.md` | Documentation rules. Read before writing any function |
| `docs/DESIGN.md` | Design tokens. Read before writing markup or plate-generating code |
| `PRPs/` | One brief per module, written and approved *before* any code |
| `docs/source/` | Raw human context — meetings, research, direction, constraints |
| `reports/` | End-of-day summaries |

Three rules matter more than the rest:

1. **Open a session before you do anything.** Append an entry to `CONTEXT.md` with state `open` and
   the branch name, and commit it, before reading anything else or writing a line.
2. **Every number is an axiom, a world constant, or a derived result** — and carries a reference
   saying which. Anything else is a bug.
3. **Never tune anything to match the monograph.** It is a guess. Fitting the simulation to it
   destroys the only thing that makes the result worth having.

`setup.md` is the external guide this system was built from. Reference material, never edited.

## Licence

GPL-3.0. See `LICENSE`.
