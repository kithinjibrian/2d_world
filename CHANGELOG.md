# CHANGELOG — Vellum (2d_world)

Follows [Keep a Changelog](https://keepachangelog.com) format.
Updated at the end of every session when something is completed and merged.
Never deleted. Older entries are never modified.

---

## [Unreleased]

### Added
- The orbit layer — Vellum's motion around Kell under two-dimensional gravity, with the insolation
  it produces. Establishes in code what had only been derived on paper: circular orbital speed is
  the same at every distance, orbital period is linear in radius rather than Kepler's three-halves
  power, the apsis regresses 105.44° every orbit so no orbit ever closes, a season works round the
  calendar in 2+√2 orbits, and no launch speed however large ever escapes.
- The units layer — the simulation's first module. Every physical quantity now carries checkable
  two-dimensional dimensions, the natural unit system fixes `G₂` and `σ₂` to 1, and formulas written
  with a three-dimensional scaling law fail a test rather than producing a plausible number.
- Context engineering system for AI sessions: behavioral rules, session handoff log, decision
  register, PRP templates, design system, and code style guide.
- `docs/AXIOMS.md` — the project's axioms in three tiers (geometry and mechanics, fundamental
  interactions, effective theories), the dimensions of physical quantities in two dimensions, and
  the consequences already derived from them: no escape velocity, no atmospheric escape, ~105° of
  apsidal regression per orbit, `T³` emission, `1/r` flux, inverse turbulent cascade, wave tails
  from the failure of Huygens' principle, and the topological prohibitions.
- An abstraction ledger recording everything the project posits rather than derives, so a result
  that reflects a choice can never be mistaken for a finding about two-dimensional physics.

### Changed
- Gravity is postulated as a direct attractive force rather than spacetime curvature, because
  general relativity in 2+1 dimensions has no propagating degrees of freedom and produces no
  gravitational attraction at all.
- Electromagnetism is abstracted rather than modelled; light and material response are supplied as
  effective theories with declared parameters.
- The project works in natural units rather than SI. A world is characterised by dimensionless
  ratios, which is the only thing that was ever physically meaningful.
- Those ratios are scanned rather than chosen: habitability is an output of a parameter sweep rather
  than an assumption built into it, so every layer needs a cheap screening path as well as a full
  solve.
- Kell is stubbed behind its real interface — stellar luminosity is a swept parameter for now, and
  deriving the star later collapses an axis of the scan rather than invalidating it.
- The project is now a simulation that derives its own physics. `vellum-monograph.html` is
  reclassified from specification to prior hypothesis, and frozen — no simulation parameter may be
  tuned to reproduce a number in it.

---

## [0.1.0] — 2026-09-03

### Added
- Vellum monograph — an 18-slide natural history of a two-dimensional world, with 17 hand-drawn
  plates, covering the system of Kell, the three laws of the plane, the four anatomical
  prohibitions, six eras of deep time, and the seven surviving kinds of life.
