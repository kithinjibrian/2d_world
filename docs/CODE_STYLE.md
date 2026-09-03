# Code Style — Vellum (2d_world)

Documentation rules for all code in this project.
Read this before writing any function, class, or module.

Python 3.11+. Type hints on every public function; `mypy --strict` must pass on `sim/`.

---

## The Three Layers of Documentation

### Layer 1 — Docstrings (what this is)

Every public function, class, and module gets a docstring. Private helpers get one only if their
purpose is not immediately obvious.

**Format** — NumPy style, since this is numerical code and the convention is expected here:

    def orbital_period(a: float, m_star: float, g2: float) -> float:
        """Return the radial period of an orbit under 2D gravity.

        Note this is the *radial* period, not the time to return to the same
        angular position — no orbit closes under a 1/r force, so those differ.

        Parameters
        ----------
        a : float
            Semi-major axis, metres.
        m_star : float
            Stellar mass, kilograms.
        g2 : float
            The 2D gravitational constant, m^2 kg^-1 s^-2. Note the dimensions
            differ from 3D G — see docs/AXIOMS.md section 2.

        Returns
        -------
        float
            Radial period in seconds.

        Raises
        ------
        ValueError
            If `a` or `m_star` is non-positive.

        Examples
        --------
        >>> orbital_period(1.5e11, 2.0e30, G2)
        4.27e7
        """

Rules:
- The summary is one line, imperative or declarative, ending in a period. Start with the verb:
  "Return", "Compute", "Integrate", "Raise". Not "This function returns...".
- Parameters, Returns, and Raises are required on every public function. **Every physical parameter
  states its units.** A float without units in the docstring is a bug waiting to happen.
- One `Examples` block on every public API function.
- Document what a function assumes about its inputs when it does not validate them.

### Layer 2 — Inline comments (why this decision was made)

Comments explain decisions, not code.

**Good:** `# Integrate in the rotating frame — the apsis regresses ~105 deg/orbit, so the inertial frame needs a tiny timestep to resolve it`
**Bad:** `# Loop over particles`

Rules:
- Comment above the line, not trailing it.
- Use one when: a magic number appears, a numerical method was chosen over an obvious alternative, a
  tolerance was picked, a guard prevents a non-obvious failure, or a workaround exists.
- Never comment what the code does. If it needs that, rewrite the code.
- Every TODO carries a reference: `# TODO(DECISION-010): replace stub once Kell is derived`

### Layer 3 — Derivation references (mandatory, and the point of the whole file)

**Every physical quantity carries a reference to where it came from.** One of three forms, matching
the three categories in the DERIVATION RULE:

    # AXIOM (A2): Gauss's law in 2D — flux over a circle, so F ∝ 1/r
    G2_EXPONENT = -1.0

    # WORLD CONSTANT: set per world instance, see World.from_seed
    self.m_star = m_star

    # DERIVED: from A4 (T^3 emission) and the structure solve in sim/star/structure.py
    luminosity = 2 * np.pi * radius * SIGMA_2 * temperature**3

A number without one of these is indistinguishable from an invented number a session later, and
"was this derived or did someone type it?" is the question this project cannot afford to be unable
to answer. This is what makes the DERIVATION RULE enforceable rather than aspirational.

**Never** write a bare numeric literal in physics code. If it is not a mathematical constant like
`2` or `np.pi`, it is one of the three categories above and it gets a name and a reference.

---

## Module-Level Documentation

Every module opens with:

    """Two-dimensional stellar structure.

    Solves hydrostatic equilibrium for a disc star under Gauss-law gravity and
    T^3 radiative emission. Produces luminosity, radius and effective
    temperature. Does NOT handle orbits or insolation at the planet — see
    sim/orbit/.

    Axioms used: A1, A2, A4, A5.
    Depends on: sim.units, sim.constants
    Used by: sim.orbit, sim.climate
    """

The `Axioms used` line is required in any module that does physics. It is how a reader knows what
the module's results rest on without tracing every call.

---

## Numerical Code Rules

These are specific to this project and matter more than style:

- **Check for non-finite values at kernel boundaries.** Any function returning an array of physical
  state checks for NaN and infinity and raises. A NaN that propagates a thousand steps costs an
  afternoon; the check costs a microsecond.
- **Never silently clamp.** If a value leaves its physical range, raise. Clamping hides the bug and
  produces output that looks fine.
- **State the tolerance and justify it.** `atol=1e-9` with no comment is a guess. Say what it is
  relative to and why it is enough.
- **Assert invariants at step boundaries**, behind a debug flag if the cost matters. Conservation,
  boundedness and ordering checks localise a bug to a single tick — nothing else does that.
- **Seed explicitly.** Every random source is a `numpy.random.Generator` passed in. Never
  module-level `np.random.*`.
- **Vectorise, but not at the cost of legibility.** A readable loop that runs once at setup is
  better than an unreadable one-liner. A per-tick inner loop is a different matter — that one wants
  to be array code.

---

## Error Handling

Exceptions, in the ordinary Python way. Do not build Result/Either types — see MEMORY.md decision 7.

    Invalid input, impossible state, broken invariant  →  raise
    Recoverable, expected, part of normal operation    →  return a value

    class VellumError(Exception):
        """Base for every error raised by this project."""

    class DimensionError(VellumError):
        """A quantity was used with the wrong physical dimensions."""

    class InvariantError(VellumError):
        """A physical invariant was violated — conservation, boundedness, ordering."""

- Validate at module boundaries; public functions check arguments and raise immediately.
- Raise a specific subclass. Never `raise Exception`, never raise a string.
- Never `except:` or `except Exception:` without re-raising.
- Let genuine programmer errors surface. Do not wrap an `IndexError` into something friendlier —
  the traceback is the useful part.

---

## What Bad Code Looks Like Here — Do Not Write This

    # BAD: 3D gravitational constant in a 2D world. Will not crash. Will be wrong.
    G = 6.674e-11

    # BAD: unattributed magic number — axiom, world constant, or derived? Unknowable.
    def emission(t):
        return 5.67e-8 * t**4          # BAD: T^4 is the 3D law; 2D is T^3

    # BAD: no units, no reference, silent clamp, swallowed error
    def temp(flux):
        try:
            return max(0.0, (flux / 5.67e-8) ** 0.25)
        except Exception:
            return 0.0

Every line of that runs without complaint and every number it produces is meaningless.

---

## Documentation Anti-Patterns

1. **Describing the code.** The code is the description. Comments explain what it cannot.
2. **Stale comments.** A comment contradicting the code is worse than none. Change both in one edit.
3. **A physical quantity without units in its docstring.**
4. **A number without a derivation reference.** Non-negotiable — see Layer 3.
5. **`# TODO` with no decision or ticket reference.**
6. **A physics module without an `Axioms used` line.** The reader cannot tell what the result rests
   on, which is the only thing that makes a derived result meaningful.
