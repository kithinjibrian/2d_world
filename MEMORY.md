# MEMORY.md — Vellum (2d_world)

Records resolved architectural decisions and current project state.
Read this at the start of every session before writing any code.

Open questions do not belong here — they live in `DECISIONS.md`.

---

## ARCHITECTURAL DECISIONS

### 1. The monograph is a single self-contained HTML file

**Decision:** `vellum-monograph.html` contains its own styles, scripts, and all 17 plates as inline
SVG. The only external resources are two Google Fonts. It renders correctly opened directly from
the filesystem, with no server and nothing installed.

**Why:** The document's durability is the point. A worldbuilding artefact that requires a build step,
a package manager, or a running server is one dependency bump away from being unopenable. This one
will open in ten years.

**Rules out:** External stylesheets and scripts. Image files. Icon libraries. Chart libraries. Any
bundler or build step. Anything that fetches at runtime, since `file://` blocks it.

**Still provisional:** Whether this holds as the document grows is DECISION-005.

---

### 2. Plates are hand-authored inline SVG, always in section view

**Decision:** Every diagram is drawn by hand as SVG in the document, with a caption in the
`Plate N.` form.

**Why:** Vellum has two dimensions, so any honest diagram of it is a section. There is no plan view,
no perspective, no three-quarter angle — those would depict a world that does not exist. A charting
library cannot draw a Driftbladder's tendril curtain, and a generated chart would import a visual
grammar (axes, legends, gridlines) that belongs to data, not to natural history illustration.

**Rules out:** Canvas rendering. Chart and diagram libraries. Raster images. Any view that is not a
profile.

---

### 3. Content and navigation are decoupled through `data-t`

**Decision:** Each slide is a `<section class="slide" data-t="Title">`. The navigator derives the
table of contents, the position counter, and the masthead title from the slide list at load.

**Why:** Adding a slide should be a content edit, not a code edit. Any scheme where the TOC is
written out by hand drifts out of sync with the slides on the first insertion.

**Rules out:** Hardcoded TOC markup. Per-slide navigation wiring.

**Known limit:** The roman-numeral array in the navigator is fixed at 18 entries. A 19th slide gets
an `undefined` label with no error. Extend the array in the same edit that adds the slide.

---

### 4. Colour is tokenised; typography and spacing are not

**Decision:** Eight colour tokens live in `:root` and every colour in the document references one.
Font sizes and spacing are currently hardcoded values.

**Why:** Recorded as fact, not as endorsement. The colour system is genuinely enforced; the type
scale is not. Writing this down prevents a future session from assuming `docs/DESIGN.md` describes
a fully tokenised system and "restoring" tokens that never existed.

**Rules out:** Nothing yet. Whether to tokenise the type scale retroactively is DECISION-004.

---

### 5. Vellum's canon is closed and lives in the monograph

**Decision:** `vellum-monograph.html` is the single source of truth for every fact about Vellum.
Facts are not invented in passing — an absent fact is a decision that requires human input.

**Why:** The world's coherence is its whole value. It is built as a chain of consequences from one
premise (two dimensions, no sideways), and every creature and event is an answer to a constraint
that premise creates. A single invented detail that does not descend from the premise breaks the
chain, and the break is invisible until someone traces it.

**Rules out:** New species. New numbers. Any mechanism requiring a third direction, a closed ring of
tissue, sight, or rotation. See the CANON RULE in CLAUDE.md for the full prohibition list.

---

### 6. The project is documents now, code later

**Decision:** Vellum is currently a documents project. The code-specific rules in CLAUDE.md
(testing, Result-type error handling, commands) are present but explicitly marked
`[CODE — BLOCKED]` and inert until DECISION-001 resolves.

**Why:** Writing the code rules now, blocked, is better than either omitting them (a future session
starts a simulation with no rules) or activating them (a future session invents a stack to satisfy
a rule that was never chosen). The block is the honest state.

**Rules out:** Adding a `package.json`, a bundler, a framework, or any dependency before DECISION-001
resolves.

---

## CURRENT PROJECT STATE

### Fully Working
- `vellum-monograph.html` — 18 slides, 17 inline SVG plates, keyboard and button navigation,
  derived table of contents. Opens from `file://` with no server.
- The context engineering system: CLAUDE.md, MEMORY.md, CONTEXT.md, DECISIONS.md, CHANGELOG.md,
  `.llmignore`, `PRPs/`, `docs/`, `reports/`.

### In Progress
- Nothing. Session 1 built the context system and wrote no project content.

### Not Started
- Everything downstream of DECISION-006 (what the project is for). No simulation, no additional
  documents, no publishing target, no tests.

---

## NEXT SESSION START POINT

Read CLAUDE.md, then this file, then DECISIONS.md, then CONTEXT.md — in that order.

Before planning any work, resolve **DECISION-006** with the user: is Vellum a monograph to finish, a
worldbuilding corpus to grow, or a simulation to build? Everything else waits on that answer, and
DECISION-001 (runtime) mostly follows from it. DECISION-003 and DECISION-004 both have a
recommendation recorded and can be resolved in the same pass in about five minutes each.

Do not open `vellum-monograph.html` for editing until a PRP exists. If the next task is content,
read the relevant plate first and quote its numbers exactly — the CANON RULE lists the fixed values
that must never be contradicted.
