# CONTEXT.md — Vellum (2d_world)

Session handoff file. Updated at the end of every session.
Read at the start of the next session alongside CLAUDE.md, MEMORY.md, and DECISIONS.md.

Every session has a name and a state: open | closed.
A session is closed only after CONTEXT.md is committed and pushed.

---

## SESSION 1 — 2026-09-03 — Context system setup — closed

Branch: setup/context-system

### WHAT WAS DONE

Built the full context engineering system described in `setup.md` and tailored it to this repo
rather than leaving the guide's placeholders in place.

The repo held only a GPL licence, a one-line README, and an untracked `vellum-monograph.html` — an
18-slide, 17-plate natural history of Vellum, self-contained, no build step. There was no source
code, no package manager, and no tests, so the guide's TypeScript-shaped rules (Result types,
service/controller layers, npm commands) had nothing to attach to.

The user chose "documents now, code later" with unknowables recorded as open decisions rather than
guessed. So the code-specific rules are present but explicitly marked `[CODE — BLOCKED]` and inert
until DECISION-001 resolves, and every value that could not be read from the repo became a numbered
open decision instead of an invented default.

The substantive work was reading the monograph in full and deriving real project rules from it. The
result is a **CANON RULE** — the seven kinds of life, the fixed numbers, and six structural
prohibitions (no third direction, no sight or colour, no closed ring of tissue, no tunnel networks,
the profile test) — plus a design system documenting the eight colour tokens that genuinely exist
and, honestly, the two places where the document does not follow its own rules.

Three real defects were found while reading and recorded rather than fixed, since fixing them was
outside this session's scope:
- The navigator's `roman` array is hardcoded to 18 entries; a 19th slide gets an `undefined` label
  with no error.
- The SVG plate classes hardcode hex values instead of referencing the colour tokens.
- TOC buttons are built with `innerHTML`; safe only while every `data-t` is author-written.

### FILES CREATED OR MODIFIED

    CLAUDE.md                        — behavioral rules; canon rule, architecture rules, anti-patterns,
                                       known issues; code rules present but marked [CODE — BLOCKED]
    MEMORY.md                        — six resolved decisions derived from the monograph as it stands
    CONTEXT.md                       — this file; session log
    DECISIONS.md                     — six open decisions, two deferred
    CHANGELOG.md                     — 0.1.0 records the monograph; Unreleased records this system
    README.md                        — rewritten from one line to a project and system orientation
    .llmignore                       — protected paths, in sync with CLAUDE.md
    PRPs/TEMPLATE.md                 — PRP template, extended with a mandatory canon check
    PRPs/DISCOVERY.md                — interview protocol; question 7 stops on any missing fact
    docs/DESIGN.md                   — real tokens, the 14 existing font sizes, plate SVG classes
    docs/CODE_STYLE.md               — documentation rules; adds Layer 3, canon references
    docs/source/README.md            — how the raw-context layer is used, and by whom
    docs/source/*/TEMPLATE.md        — meeting, research, stakeholder, constraint templates
    docs/specs|decisions|incidents|status/README.md — document structures, locked before writing
    reports/TEMPLATE.md              — EOD report template
    reports/2026-09-03.md            — this session's EOD report

`vellum-monograph.html` was read in full but not modified, and is now tracked.

### TESTS WRITTEN

None. There is no test runner and adding one is DECISION-002. The navigator is the only testable
code in the repo; four behaviours worth asserting are listed in that decision entry.

Verification performed instead: every colour token, font size, and SVG class documented in
`docs/DESIGN.md` was extracted from the stylesheet rather than recalled, and every canon fact in
CLAUDE.md was quoted from the monograph text.

### DECISIONS MADE

- The project is documents now, code later — code rules written but blocked, rather than omitted or
  activated against an unchosen stack (MEMORY.md #6).
- `vellum-monograph.html` is the canon, and an absent fact is a decision rather than a detail
  (MEMORY.md #5). This is the rule the rest of the system exists to enforce.
- Unknowable values were not defaulted. No file-size limit, test runner, or stack was invented.
- The guide's `CLAUDE.md` template was not copied verbatim. Rules that could not answer "what
  mistake does this prevent?" for this repo were replaced with ones derived from the monograph.
- `setup.md` is treated as external reference material, listed in `.llmignore` and never edited.

### PENDING DECISIONS OPENED

- DECISION-001 — Runtime and language for simulation code (blocks all code)
- DECISION-002 — Test framework, and whether the navigator is retrofitted with tests
- DECISION-003 — File size limit (recommendation recorded: no limit for documents, 300 for code)
- DECISION-004 — Whether to tokenise the type scale (recommendation recorded: freeze and document)
- DECISION-005 — Whether the monograph stays a single file (recommendation recorded: yes)
- DECISION-006 — What the project is actually for — blocks prioritisation of everything
- DECISION-007 — Accessibility target (deferred)
- DECISION-008 — Publishing and hosting (deferred)

### STILL OPEN AT CLOSE

- **Not pushed.** The branch `setup/context-system` is committed locally only. The remote is
  `git@github.com:kithinjibrian/2d_world.git`; pushing needs the user's go-ahead.
- Git identity was unset in this repo and was configured locally (not globally) as
  `kithinjibrian <brian.kithinji@massa-advisors.ai>`. Correct it if that is the wrong authorship.
- Six open decisions block essentially all downstream work. DECISION-006 is the one that matters.
- The three defects listed above are recorded, not fixed. Each needs a PRP.
- The DESIGN RULE is only partially enforceable until DECISION-004 resolves.

---

## SESSION 2 — 2026-09-03 — Git identity correction — closed

Branch: setup/context-system

### WHAT WAS DONE

Resolved the authorship item left open at the close of Session 1.

Git had no identity configured on this machine, so Session 1 set one repo-locally as a stopgap and
flagged it for correction. The user supplied the correct address. The identity is now set globally
in `~/.gitconfig` as `kithinjibrian <kithinjibrian369@gmail.com>`, and the repo-local override was
removed so the global value actually applies here rather than being shadowed.

Session 1's two commits were re-authored to match. Both were local and unpushed, so the rewrite was
safe; the initial commit `d535259` is the user's own and was left untouched. Commit hashes for the
two session commits changed as a result — `e86d716` → `ad71b42` and `54b08da` → `9e4087d`.

Session 1's entry above still records the old address. That is deliberate: past sessions are
append-only under the PROTECTED FILES rule in CLAUDE.md, so the record stands as written and this
entry supersedes it.

### FILES CREATED OR MODIFIED

    CONTEXT.md    — this entry
    ~/.gitconfig  — global user.name and user.email (outside the repo)

No project file changed. CHANGELOG.md was deliberately not updated: nothing observable shipped, and
the CHANGELOG rule excludes changes a reader cannot see or feel.

### TESTS WRITTEN

None. Verified directly instead: `git config --get user.email` resolves to the global value with no
local override, and `git log --format='%an <%ae> | %cn <%ce>'` shows both author and committer
corrected on both commits.

### DECISIONS MADE

- The identity is global, not repo-local, since the user asked for it to be permanent.
- Session 1's commits were rewritten rather than left with the wrong author, because they were
  unpushed and created in this session. Nothing that had left the machine was touched.

### PENDING DECISIONS OPENED

None.

### STILL OPEN AT CLOSE

- **Still not pushed.** The branch `setup/context-system` is local only. Remote is
  `git@github.com:kithinjibrian/2d_world.git`.
- Everything else carried over from Session 1: six open decisions, DECISION-006 the blocking one,
  and three recorded defects each needing a PRP.

---

## NEXT SESSION START POINT

Open a new session entry in this file first, with state `open` and the branch name, and commit it.

Then read CLAUDE.md, MEMORY.md, DECISIONS.md, and this file — in that order.

The first task is not code. **Resolve DECISION-006 with the user: is Vellum a monograph to finish, a
worldbuilding corpus to grow, or a simulation to build?** Nothing downstream can be prioritised
until that is answered, and DECISION-001 mostly follows from it. DECISION-003, -004 and -005 each
have a recommendation recorded and can be closed in the same conversation in a few minutes.

If the answer is "finish the monograph", the highest-value first PRP is the `roman` array bug — it
is the only recorded defect that will silently produce wrong output the next time a slide is added,
and a slide is the most likely next change.

Do not open `vellum-monograph.html` for editing until a PRP exists and is approved. When you do,
read the relevant plate first and quote its numbers exactly; the CANON RULE in CLAUDE.md lists the
fixed values that must never be contradicted.

The branch has never been pushed. Confirm with the user whether it should be before building on it.
