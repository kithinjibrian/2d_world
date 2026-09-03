# Code Style — Vellum (2d_world)

Documentation rules for all code in this project.
Read this before writing any function, class, or module.

The project has very little code today — the slide navigator in `vellum-monograph.html`. These
rules govern that, and every line written after DECISION-001 resolves.

---

## The Two Layers of Documentation

### Layer 1 — Block documentation (what this is)

Every exported function, class, interface, and type alias gets a documentation block.
Internal functions get one only if their purpose is not immediately obvious.

**Format:**

    /**
     * [One-sentence description of what this does from the caller's perspective.]
     *
     * [Optional second paragraph: when to use it, what to watch out for.]
     *
     * @param name - [What this param is. Include units, constraints, allowed values.]
     * @returns [What is returned. For Result types, describe both the ok and error paths.]
     * @throws [Only if this function is a deliberate exception to the Result rule]
     *
     * @example
     * const result = getSlide(3)
     * if (!result.ok) { ... }
     */

Rules:
- The first line is always a single sentence. No "This function...". Start with the verb: "Fetches",
  "Creates", "Returns", "Validates".
- `@param` and `@returns` are required on every exported function. No exceptions.
- One `@example` is required on every public API function. Not optional.
- `@throws` is used only for deliberate exceptions to the Result pattern. Do not use it on service
  functions.

### Layer 2 — Inline comments (why this decision was made)

Inline comments explain decisions, not code.

**Good:** `// Reset scroll — a slide is a page in a book, not a scroll position to preserve`
**Bad:** `// Set scroll to top`

Rules:
- Comment above the line it explains, not at the end of it.
- Use an inline comment when: a magic number appears, a library is used non-obviously, a performance
  trade-off was made, a guard clause prevents a non-obvious bug, or a workaround exists for a known
  issue.
- Never comment what the code does. If the code needs a comment to explain what it does, rewrite the
  code.
- Every TODO carries a ticket or a date: `// TODO(DECISION-004): remove once the type scale is
  tokenised`

### Layer 3 — Canon references (Vellum-specific, mandatory)

Any code, markup, or SVG that encodes a fact about Vellum carries a comment naming the plate it came
from.

**Good:** `// Plate XIII: 1,106 Sillfish species, one per sealed basin`
**Bad:** `const SPECIES_COUNT = 1106`

A number without a plate reference cannot be verified a session later, and an unverifiable number is
indistinguishable from an invented one. See the CANON RULE in CLAUDE.md.

---

## Module-Level Documentation

Every file gets a top-of-file comment block:

    /**
     * [Module name]
     *
     * [One paragraph: what this module is responsible for and what it is NOT responsible for.]
     *
     * Depends on: [what this imports from]
     * Used by: [what imports from this — omit if it is a leaf module]
     */

---

## Error Handling — the pattern, once DECISION-001 resolves to a typed runtime

This project uses **return-based error handling**. Do not throw for expected failures.

    Expected failure  →  return { ok: false, data: null, error: ... }
    Truly unexpected  →  let it throw (programmer error, unrecoverable state)

**Why:** TypeScript has no checked exceptions. A function that throws gives callers no type-level
signal that failure is possible. A function that returns a Result makes every failure path visible,
compiler-checked, and impossible to ignore silently.

### The Pattern

    // Define once in lib/result.ts
    type Result<T, E = AppError> =
      | { ok: true;  data: T; error: null }
      | { ok: false; data: null; error: E }

    function ok<T>(data: T): Result<T, never> {
      return { ok: true, data, error: null }
    }

    function err<E>(error: E): Result<never, E> {
      return { ok: false, data: null, error }
    }

    // Service layer — all try/catch lives here
    async function getBasin(id: string): Promise<Result<Basin, "NOT_FOUND" | "READ_ERROR">> {
      // Validate before the read — avoids a round-trip on obviously bad input
      if (!isValidId(id)) return err("NOT_FOUND")

      try {
        const basin = await store.basins.find(id)
        if (!basin) return err("NOT_FOUND")
        return ok(basin)
      } catch {
        return err("READ_ERROR")
      }
    }

    // Caller is forced to handle both paths
    const result = await getBasin(id)
    if (!result.ok) return handleError(result.error)   // result.error is typed
    render(result.data)                                 // result.data is typed Basin

### What Goes Where

| Layer | Rule |
|-------|------|
| Service / domain | Returns `Result<T, E>`. All try/catch lives here. |
| Controller / route handler | Calls the service, maps the Result to a response. No try/catch. |
| UI component | Calls the service, reads `result.ok` to decide what to render. |
| Third-party library calls | Wrapped in a thin adapter that converts throws into `err(...)`. |

### What Still Throws

- Programmer errors — accessing a property on null when it should never be null
- Process-level failures — missing configuration at startup
- Framework internals — do not catch exceptions that signal misconfiguration

### Anti-Patterns

- **Never** `throw new Error(...)` in a service function for a predictable failure.
- **Never** `try/catch` in a controller — service errors come back as typed Results.
- **Never** return `undefined` to signal failure — the caller cannot distinguish "not found" from
  "returned nothing on purpose."
- **Never** expose a raw library or database error message to the client.

**If DECISION-001 resolves to an untyped runtime, this section must be rewritten before any code is
written.** Its entire rationale is compiler-checked error paths; applying the ceremony without the
compiler gets the cost and none of the benefit.

---

## What Good Documentation Looks Like

    /**
     * Fetches a single basin by ID.
     *
     * Returns NOT_FOUND if the basin does not exist. Returns READ_ERROR if the underlying read
     * fails — the caller should not retry automatically, as READ_ERROR indicates a store-level
     * failure rather than a transient one.
     *
     * @param id - The basin's identifier. Must match /^basin-[0-9]{1,4}$/.
     * @returns Result<Basin, "NOT_FOUND" | "READ_ERROR">
     *
     * @example
     * const result = await getBasin("basin-0417")
     * if (!result.ok) return respondWithError(result.error)
     * return respond(result.data)
     */

## What Bad Documentation Looks Like — Do Not Write This

    // BAD: no block, no params, no example
    async function getBasin(id) {
      const basin = await store.basins.find(id)
      return basin  // BAD: throws on read failure, returns undefined on not-found
    }

    // BAD: describes what, not why
    // Find the basin in the store by its ID
    // If found, return the basin

---

## Documentation Anti-Patterns

1. **Describing the code.** The code is the description. Comments explain what the code cannot.
2. **Stale comments.** A comment that contradicts the code is worse than no comment. Change the code,
   change its comment, in the same edit.
3. **`// TODO` without a ticket or a date.** Untracked TODOs accumulate and rot.
4. **Over-documenting internals.** Not every helper needs a block. Obvious private helpers do not.
5. **Under-documenting the error contract.** Every exported function's `@returns` must describe its
   failure paths. For callers, this is the most important part of the block.
6. **A canon fact without its plate reference.** Vellum-specific and non-negotiable — see Layer 3.
