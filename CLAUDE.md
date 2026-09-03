# CLAUDE.md — Vellum (2d_world)

Behavioral instructions for AI coding assistants. Each rule exists to prevent a specific mistake.

Vellum is a constructed world with two spatial dimensions — length and height, no sideways —
documented in `vellum-monograph.html`. The project is currently a **documents project**; code is
expected later. Rules marked `[CODE — BLOCKED]` do not apply until the stack decision in
`DECISIONS.md` is resolved.

---

## SESSION HANDOFF RULE — NON-NEGOTIABLE

Every session in `CONTEXT.md` must have:
- A **name** — short descriptive title of what the session accomplished
- A **state** — `open` while work is in progress, `closed` once handoff is done
- A **branch** — the git branch this session's work lives on

Format:

    ## SESSION {n} — {YYYY-MM-DD} — {Name} — {state}
    Branch: {branch-name}

Rules:
- **Step 1 of every session, no exceptions:** append a new session entry to `CONTEXT.md` with state
  `open` and the current branch name. Do this before reading any other file, before planning, before
  writing any code. The entry must exist and be committed before any other work begins.
- Mark it `closed` only after CONTEXT.md is updated and committed and pushed.
- Never leave a session `open` at the end of a turn.
- Never start a new session without closing the previous one first.
- The NEXT SESSION START POINT block is always rewritten at the end of every session.
- Sessions are never deleted — the full history stays in this file.

---

## CANON RULE — NON-NEGOTIABLE

`vellum-monograph.html` is the canon. Every fact about Vellum — physical, biological, historical,
numeric — either already appears there or does not exist yet.

Before writing any prose, diagram, spec, or simulation about Vellum:
1. Read the relevant plate in `vellum-monograph.html`.
2. If the fact you need is present, use it verbatim. Do not paraphrase a number.
3. If the fact is absent, **stop**. Do not invent it. Open a `DECISIONS.md` entry.

Never do these:
- **Never invent a species.** Vellum has exactly seven kinds of life: Spreadturf, Ridgeworm,
  Furrowsnake, Sillfish, Skimmer, Springhopper, Driftbladder. The Springhopper is the juvenile
  stage of the Driftbladder — they are one animal, not two. An eighth kind requires human approval.
- **Never contradict a stated number.** Day 19.4 h. Year 611 days. Surface 38,400 km, closed, no
  edge. Seasons precess over ~900 years. Impact cycle ~40 Ma. Six eras. 1,106 Sillfish species.
  Spreadturf max 31 cm. If you need a number not on this list, it is a decision, not a detail.
- **Never introduce a third direction.** No sideways, no lateral, no yaw, no roll, no "around",
  no "beside", no "abreast", no flanking, no encirclement, no branching river, no delta.
- **Never give anything sight or colour.** Nothing on Vellum sees. No camouflage, no warning
  colours, no display, no flowers. Signalling is acoustic or seismic, always.
- **Never draw a closed ring of tissue.** No through-gut, no closed circulation, no lens, no wheel,
  no axle, no rotating joint. Every mechanism oscillates.
- **Never build a tunnel network.** A burrow cannot be propped without being sealed in two. Vellum
  has burrows; it has never had a warren.

**The profile test.** Everything on Vellum is a profile. If a thing cannot be drawn as a single
closed outline — if any part of it must be seen from the front — it has never existed. Apply this
test to every asset, diagram, and description before writing it.

---

## PRP RULE — NON-NEGOTIABLE

Never write code, and never write a new document about Vellum, without a PRP file in `PRPs/`.

If a request arrives without a PRP:
1. Do not write any code or prose.
2. Run the discovery interview in `PRPs/DISCOVERY.md` — one question at a time.
3. Cover: what it does, who it affects, edge cases, error states, what files it touches, what it
   must not touch, which canon it depends on.
4. Write the PRP to `PRPs/[feature-name].md`.
5. Present it to the user for approval.
6. Only build after explicit approval.

A vague prompt is not a starting point. It is the beginning of a discovery.

Exempt from this rule: fixing a typo, correcting a fact already recorded in canon, and the
maintenance writes to CONTEXT.md / CHANGELOG.md / DECISIONS.md that every session performs.

---

## SCOPE RULE — NON-NEGOTIABLE

One PRP at a time. Never implement more than one feature's scope in a single session.

If mid-implementation you discover the scope is larger than the PRP described:
1. Stop immediately. Do not continue implementing.
2. Document what was discovered.
3. Update or create a new PRP for the expanded scope.
4. Get approval before continuing.

The model does not decide that something is "small enough to add." The human decides.

---

## PENDING DECISIONS RULE — NON-NEGOTIABLE

Before writing anything that depends on an unresolved question, check `DECISIONS.md`.

- If the decision is listed as `open`, stop. Do not implement. Ask the user to resolve it first.
- If the decision is listed as `resolved`, follow the outcome recorded there — do not re-litigate it.
- If you encounter a new unresolved question mid-implementation, add it to `DECISIONS.md` as `open`
  and stop. Do not guess.

Never make an architectural or canonical choice silently. If you are guessing, you are making a
decision that belongs in DECISIONS.md.

---

## DESIGN RULE — NON-NEGOTIABLE

Read `docs/DESIGN.md` before writing any markup or styling.

Every colour must come from the tokens defined there. Never write a raw hex value outside the
`:root` block. The typography and spacing scales are **not yet tokenised** — see DECISION-004
before adding new type sizes; do not invent a new size to solve a one-off layout problem.

---

## TESTING RULE `[CODE — BLOCKED]`

Blocked by DECISION-001 (runtime and stack) and DECISION-002 (test framework). Do not write code
that would need tests until both are resolved.

Once resolved, this rule takes effect and this notice is deleted:
- Write the failing test before writing the implementation. No exceptions.
- Tests mirror the source tree.
- Test behavior visible to callers — inputs, outputs, and error paths. Do not test internals,
  private functions, or third-party library behavior.
- Every exported function gets one test for its happy path and one for each error path.
- Run the full suite after any non-trivial change.

There is one testable thing in the repo today: the slide navigator in `vellum-monograph.html`.
It has no tests, and adding a test runner for it is DECISION-002.

---

## ERROR HANDLING `[CODE — BLOCKED]`

Blocked by DECISION-001. The intended pattern is **return-based error handling** (Result/union
types) — expected failures return a value, only truly unexpected conditions throw:

    Expected failure  →  return { ok: false, data: null, error: ... }
    Truly unexpected  →  let it throw (programmer error, unrecoverable state)

The full pattern, layer table, and anti-patterns are specified in `docs/CODE_STYLE.md` and take
effect the moment DECISION-001 resolves to a typed runtime. If DECISION-001 resolves to an untyped
runtime, this section must be rewritten before any code is written — do not apply it half-way.

---

## SECURITY RULE — NON-NEGOTIABLE

Never implement the following without explicit human review and approval:
- Authentication or session management
- Authorization / permission checks
- Cryptographic operations (hashing, signing, encrypting)
- Payment processing
- Secrets or credential handling

For everything else:
- Never hardcode credentials, API keys, tokens, or secrets. Not even in comments or example values.
- Never construct queries by string concatenation.
- Never trust input from the user, URL params, or external APIs without validation first.
- Never log sensitive data.
- Never expose internal error details to the client.

Applies today: `vellum-monograph.html` builds table-of-contents entries with `innerHTML` from
`data-t` attributes. That is safe only while every slide's `data-t` is author-written. If slide
titles ever come from data, from a build step, or from user input, this becomes an injection point
and must be changed to `textContent` first.

If you are unsure whether something has a security implication, stop and ask before implementing.

---

## CODE DOCUMENTATION RULE — NON-NEGOTIABLE

Read `docs/CODE_STYLE.md` before writing any function, class, or module.

Every exported function, class, and type must have a documentation block. Every non-obvious
decision inside a function must have an inline comment explaining *why*, not what. The what is in
the code. The why is what degrades when context is lost.

For Vellum specifically: any code or markup that encodes a canon fact carries a comment naming the
plate it came from — e.g. `// Plate XIII: 1,106 species, one per basin`. A number without a plate
reference is unverifiable a session later.

---

## FILE SIZE RULE

No file exceeds the limit set in DECISION-003, which is **open**. Until it is resolved, treat 300
lines as the working ceiling for any new file, and note that `vellum-monograph.html` is already
~900 lines and is explicitly exempt pending DECISION-005.

When a file reaches the limit:
1. Stop before adding more code.
2. Propose a split to the user — show the proposed new file names and what moves where.
3. Wait for approval.
4. Split, then continue.

Do not ask "should I split this?" — propose the specific split.

---

## PROTECTED FILES — NON-NEGOTIABLE

Never read, modify, or delete the following under any circumstances:

- `.env` and `.env.*` (any environment file)
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` (lockfiles — managed by the package manager)
- `migrations/` and `*.migration.*` (database migration history)
- `LICENSE` (GPL-3.0 — legal text, never edited)
- `.git/` (repository internals)

Append-only — read freely, add to the end, never rewrite or delete existing entries:
- `CHANGELOG.md` — past entries are never modified
- `CONTEXT.md` — past sessions are never deleted
- `reports/` — EOD reports are never deleted
- `docs/decisions/` — ADRs are never renumbered or removed
- `docs/source/` — source notes are never deleted; supersede them with a dated header instead

If a task seems to require touching a protected file, stop and ask the user how to proceed.

See also: `.llmignore` at the project root, which must stay in sync with this section.

---

## COMMANDS

There is no build, no test, and no dev server. The project is a single self-contained HTML file.

    # View the monograph
    xdg-open vellum-monograph.html

    # Optional local server (only if a future change needs a real origin)
    python3 -m http.server 8000

Every other command is blocked by DECISION-001. **Do not add a `package.json`, a bundler, a
framework, or a dependency to make something work.** Introducing tooling is a decision, not an
implementation detail.

---

## STACK

- HTML5 + CSS + vanilla ES5-style JavaScript, single file, no build step
- Two webfonts from Google Fonts: Fraunces (display) and Spectral (body)
- Inline SVG for every plate — no image files, no icon library
- No package manager, no dependencies, no framework
- Runtime for future simulation work: **undecided — DECISION-001**

---

## ARCHITECTURE RULES

1. **`vellum-monograph.html` is self-contained.** Everything except the two Google Fonts is inline:
   styles, scripts, and every plate as SVG. Do not extract CSS or JS to a separate file, and do not
   add an image file. The document must render correctly from `file://` with no server.
2. **Plates are inline SVG, authored by hand.** No canvas, no chart library, no raster export. A
   plate is a diagram of a two-dimensional world, so it is a section view by definition — see the
   profile test in the CANON RULE.
3. **Slides are `<section class="slide">` with a `data-t` title.** The navigator derives the table
   of contents, the position counter, and the masthead from the slide list. Adding a slide means
   adding one section with a `data-t` — never touch the navigator to add content.
4. **Roman numerals are hardcoded in the navigator** (`roman` array, currently 18 entries). Adding
   a slide beyond that length breaks the TOC label silently. Extend the array in the same edit.
5. **Colour lives in `:root` only.** See `docs/DESIGN.md`.

---

## ANTI-PATTERNS

1. **Never add a build step or a dependency to solve a styling or layout problem.** The document's
   value is that it opens from a filesystem in ten years with nothing installed.
2. **Never replace a hand-drawn SVG plate with a generated chart.** The plates are illustrations
   with captions, not data visualisations; a library cannot draw a Driftbladder.
3. **Never write "left" or "right" as absolute directions in prose.** On a closed line they are
   relative to a traveller. The monograph uses "along the line", "the eastern arc", "either side".
4. **Never describe a Vellum animal turning around casually.** Pitching a body through half a
   circle takes two seconds, and two seconds is usually the whole hunt. The Springhopper is
   end-to-end symmetrical precisely so it never has to.
5. **Never treat the Springhopper and the Driftbladder as separate animals in a count.** Seven
   kinds of life, eight names.
6. **Never soften the physics into a metaphor.** Every rule on Vellum is absolute: a shadow takes
   all the light, an obstruction stops everything, a wall makes two worlds. "Mostly" and "usually"
   are the wrong register for this world.
7. **Never edit `setup.md`.** It is the external guide this system was built from, not a project
   document. It is superseded by the files it told us to create.

---

## KNOWN ISSUES — DO NOT FIX

1. **Font sizes in `vellum-monograph.html` are hardcoded px values, not tokens.** This is a real
   gap, tracked as DECISION-004. Do not tokenise the type scale opportunistically mid-task — it
   touches every rule in the stylesheet and needs its own PRP.
2. **The navigator uses `innerHTML` for TOC buttons.** Safe today because all input is
   author-written. Do not "fix" it in passing; see the SECURITY RULE for the condition that makes
   it a real defect.
3. **`window.scrollTo(0, 0)` on every slide change.** Intentional — a slide is a page in a book,
   not a scroll position to preserve.
4. **The monograph has no `<h1>` on most slides and no landmark regions.** Accessibility work is
   deliberately deferred, not overlooked. It needs a PRP; do not add ARIA attributes ad hoc.
