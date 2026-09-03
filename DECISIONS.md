# DECISIONS.md — Vellum (2d_world)

Tracks architectural and design questions that are open, deferred, or resolved.

Rules:
- Every open decision blocks implementation of the code it affects.
- The AI must not implement anything that depends on an open decision.
- When a decision is resolved, move it to the RESOLVED section and record the outcome.
- Once resolved, copy the outcome to MEMORY.md as an architectural decision.

---

## OPEN — Requires human input before implementation

### DECISION-001 — Runtime and language for simulation code

**Status:** open
**Raised:** 2026-09-03 — Session 1
**Resolved by:** human
**Blocks:** All code. The TESTING RULE and ERROR HANDLING sections of CLAUDE.md are inert until
this resolves. No `package.json`, bundler, or dependency may be added before it.

**Question:** When Vellum grows past documents into a running simulation, what does it run on?

**Options:**
- A) **TypeScript, browser-first, no framework.** Continues the current constraint that everything
  opens from `file://`. The Result-type error handling in CLAUDE.md applies as written. Costs a
  build step the moment TypeScript appears, which contradicts the "no build" property the monograph
  currently has.
- B) **Vanilla JavaScript, no build, ever.** Preserves the self-contained property absolutely. Loses
  compiler-checked error paths — the ERROR HANDLING section would need rewriting, since its whole
  rationale is that TypeScript has no checked exceptions.
- C) **Python.** Better fit if the goal is offline simulation and generating plates from model
  output rather than an interactive artefact. Splits the project into two runtimes: docs in the
  browser, simulation in Python.

**Notes:** This is genuinely open — the monograph is a finished-feeling artefact and nothing in it
implies a simulation. Do not resolve this by drifting into it. The answer depends on whether the
next thing built is *about* Vellum or *runs* Vellum. See DECISION-006.

---

### DECISION-002 — Test framework and what gets tested

**Status:** open
**Raised:** 2026-09-03 — Session 1
**Resolved by:** human
**Blocks:** The TESTING RULE in CLAUDE.md. Writing any testable code.

**Question:** What runs the tests, and does the existing slide navigator get retrofitted with them?

**Options:**
- A) Defer entirely until DECISION-001 resolves — a test framework choice follows from a runtime.
- B) Adopt a zero-install browser test page now (a plain HTML file that asserts against the
  navigator) so the one piece of existing logic is covered without a package manager.
- C) Adopt a standard runner (Vitest, pytest, per DECISION-001) and accept the dependency.

**Notes:** The navigator is ~35 lines with four behaviours worth asserting: bounds clamping at both
ends, button disabled states, TOC index mapping, and the roman-numeral array running out past 18
slides (see ARCHITECTURE RULE 4 — that one is a live bug risk, not a hypothetical).

---

### DECISION-003 — File size limit

**Status:** open
**Raised:** 2026-09-03 — Session 1
**Resolved by:** human
**Blocks:** Nothing immediately; governs every future split.

**Question:** What is the maximum line count for a file in this project?

**Options:**
- A) **300 lines**, the guide's default, with `vellum-monograph.html` exempt (see DECISION-005).
- B) **No limit for documents, 300 for code.** A monograph is prose and diagrams; splitting it by
  line count would fragment it arbitrarily. Code has no such excuse.

**Notes:** Recommend B. `vellum-monograph.html` is ~900 lines and is one coherent document; a
300-line rule applied to it produces three meaningless fragments. CLAUDE.md currently instructs a
300-line working ceiling for *new* files until this resolves.

---

### DECISION-004 — Tokenising the typography and spacing scales

**Status:** open
**Raised:** 2026-09-03 — Session 1
**Resolved by:** human
**Blocks:** Any change that introduces a new font size or spacing value.

**Question:** `docs/DESIGN.md` requires every visual value to come from a token, but only the eight
colours are tokenised today. Font sizes are 14 hardcoded px values and spacing is ad hoc. Do we
tokenise them retroactively?

**Options:**
- A) **Tokenise now, in its own PRP.** Makes the DESIGN RULE enforceable as written. Touches nearly
  every rule in the stylesheet; risk of visual regression across 18 slides with no test to catch it.
- B) **Freeze the current scale and document it as-is.** `docs/DESIGN.md` records the 14 sizes that
  exist as the permitted set; adding a fifteenth requires approval. No code changes, and the rule
  becomes enforceable immediately by inspection.
- C) Leave it. The DESIGN RULE stays partially unenforceable.

**Notes:** Recommend B. It gets the constraint working today at zero regression risk, and A stays
available later. `docs/DESIGN.md` documents the existing sizes on this assumption and marks them
provisional.

---

### DECISION-005 — Does the monograph stay a single file?

**Status:** open
**Raised:** 2026-09-03 — Session 1
**Resolved by:** human
**Blocks:** Any restructuring of `vellum-monograph.html`; the exemption in the FILE SIZE RULE.

**Question:** `vellum-monograph.html` is ~68 KB and ~900 lines with 17 inline SVG plates. Does it
remain one self-contained file as it grows?

**Options:**
- A) **Yes, permanently.** The document opens from a filesystem with nothing installed, which is
  the property that makes it survive. Accept that it grows large.
- B) **Split plates into separate SVG files.** Smaller, more editable, but requires a server for
  `file://` fetches or an inlining build step — either one breaks the current property.

**Notes:** Recommend A. ARCHITECTURE RULE 1 in CLAUDE.md is written on that assumption and must be
revised if this resolves to B.

---

### DECISION-006 — What is the project actually for?

**Status:** open
**Raised:** 2026-09-03 — Session 1
**Resolved by:** human
**Blocks:** Prioritisation of everything. DECISION-001 largely follows from this.

**Question:** Is Vellum a finished monograph to be extended and polished, a worldbuilding corpus
that grows more documents, or the design substrate for a simulation or game?

**Options:**
- A) **The monograph is the product.** Future work is more plates, better typography, accessibility,
  publishing. No code beyond the navigator.
- B) **Worldbuilding corpus.** More documents in the same voice — a gazetteer, a field guide, an
  era-by-era history. Canon management becomes the central problem.
- C) **Simulation substrate.** The physics described (2D gravity with no escape velocity, inverse
  turbulence cascade, the first law) get implemented and run.

**Notes:** The session that opened this file set the project up as "documents now, code later",
which is compatible with all three. This decision is what makes the next session's work concrete.

---

## DEFERRED — Acknowledged, not yet needed

### DECISION-007 — Accessibility of the monograph

**Status:** deferred
**Raised:** 2026-09-03 — Session 1
**Revisit when:** The monograph is published anywhere with a real audience, or anyone needs to read
it with a screen reader.

**Question:** The slide navigator hides 17 of 18 sections with `display:none`, has no landmark
regions, no live region announcing slide changes, and the SVG plates have captions but no
`<title>`/`aria-label`. What is the accessibility target?

**Notes:** Safe to defer while this is a private artefact. Listed as KNOWN ISSUE 4 in CLAUDE.md so
it does not get fixed piecemeal in the middle of unrelated work. Needs its own PRP when it comes up.

---

### DECISION-008 — Publishing and hosting

**Status:** deferred
**Raised:** 2026-09-03 — Session 1
**Revisit when:** The monograph is ready to share outside this machine.

**Question:** Where does the monograph live for readers — GitHub Pages, a published Artifact, a
downloaded file, print/PDF?

**Notes:** Affects DECISION-005 (a hosted document could fetch separate SVGs safely) and the font
loading strategy (Google Fonts requires a network; a print or offline target needs them embedded or
a fallback that holds up). No urgency while `xdg-open` is the only reader.

---

## RESOLVED

*None yet. When a decision resolves, move it here with its outcome and rationale, then copy the
outcome to MEMORY.md.*
