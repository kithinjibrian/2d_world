## FEATURE: A dimensional bookkeeping layer for two-dimensional physics, in natural units.

## OBJECTIVE

`sim/units/` gives every physical quantity in the project a checkable dimension in 2D, and defines
the natural-unit system in which `G₂ = 1` and `σ₂ = 1`. Done means no constant can enter the
codebase without declaring its dimensions, a formula written with a 3D scaling law fails a test
rather than producing a plausible number, and the conversion to SI exists in exactly one place and
is used only for display.

Nothing downstream computes anything until this exists. It derives no physics itself; it is the
apparatus that keeps every later derivation honest.

## CONTEXT

- Starting state: no `sim/` tree exists. The repo holds only documents and the frozen monograph.
- Ending state: `sim/units/` and `sim/tests/units/`, plus `pyproject.toml` configuring pytest, mypy
  and ruff. First code in the project.
- Related existing code: none. This is module zero.
- Axioms this depends on: **T0.1** (two dimensions) and **T0.2** (Newtonian mechanics) for the base
  dimension set; **T1.1** for `G₂`'s dimensions; **T2.2** for `σ₂`'s. It must not contradict
  `docs/AXIOMS.md` §2, which is the authoritative dimension table.
- Abstracted layers this leans on: **none.** This is the only module in the project that will be
  able to say that.
- New free parameters introduced: **none.** `M_ref` and `L_ref` are display anchors, not physics —
  they set what a metre means for printing, and no result depends on them.
- Open decisions that must be resolved first: **DECISION-015** — where dimension checking happens.
  The PRP cannot be approved until it is answered, because the answer changes the public API.
- Architecture rule 8 (two fidelities) does **not** apply. This is not a physics layer; there is no
  screening approximation of a dimension.

## IMPLEMENTATION REQUIREMENTS

### Must Do

- Represent a dimension as exponents over four base dimensions — **mass, length, time,
  temperature** — using `Fraction`, not `int`. Fractional exponents arise: `σ₂ = 1` fixes the
  temperature scale through a cube root.
- Implement the algebra: multiply adds exponents, divide subtracts, power multiplies, equality is
  exponent-wise. Dimensionless is the zero vector.
- Name every dimension the project needs, with its 2D value. At minimum:

      FORCE      M L T⁻²        ENERGY     M L² T⁻²      POWER      M L² T⁻³
      DENSITY    M L⁻²          PRESSURE   M T⁻²         FLUX       M L T⁻³
      G2         M⁻¹ L² T⁻²     SIGMA2     M L T⁻³ Θ⁻³   VISCOSITY  M T⁻¹

  Note `PRESSURE` is force per unit *length* and `VISCOSITY` is `M T⁻¹`, both differing from their
  3D forms. Kinematic viscosity is `L² T⁻¹`, which does *not* differ — include it as a reminder that
  not everything changes.
- Implement `UnitSystem`: given display anchors `M_ref` and `L_ref`, derive `T_ref` from `G₂ ≡ 1`
  (which forces `T = L/√M`) and `Θ_ref` from `σ₂ ≡ 1` (which forces `Θ = (M L T⁻³)^⅓`). Expose
  `to_si` / `from_si` for display only.
- Define `G2 = 1.0` and `SIGMA_2 = 1.0` as named constants carrying `# AXIOM (T1.1)` and
  `# AXIOM (T2.2)` derivation references.
- Every public function gets a docstring stating units, and every module an `Axioms used` line.

### Must NOT Do

- **Do not define any 3D dimension.** No `DENSITY_3D`, no inverse-square gravity helper, nothing.
  A name that exists can be selected by accident; a name that does not exist cannot. This is the
  cheapest possible enforcement of the second anti-pattern in CLAUDE.md.
- **Do not add a dependency.** Not `pint`, not `astropy.units`. The STACK list in CLAUDE.md is
  closed, and adding to it is a decision, not an implementation detail. This module is small enough
  to own.
- **Do not build a general-purpose units library.** No unit parsing, no string formats like
  `"kg*m^-2"`, no prefix handling, no imperial anything. Only what Vellum needs.
- **Do not put SI values anywhere except the display path.** No SI constant is ever imported.
- **Do not make dimension objects mutable**, and do not let them carry a magnitude unless
  DECISION-015 resolves that way.

## DERIVATION CHECK

- [ ] Every quantity is classified as an axiom, a world constant, or a derived result
- [ ] No constant or scaling law is imported from a 3D reference without being re-derived in 2D
- [ ] All dimensions match `docs/AXIOMS.md` §2
- [ ] Nothing is tuned, fitted, or calibrated to reproduce a number from the monograph
- [ ] Nothing that should emerge is hand-placed
- [ ] Every new free parameter is listed above and approved — **none are introduced**
- [ ] Every abstracted layer leaned on is listed above — **none**
- [ ] All computation is in natural units; no SI value appears outside the display layer
- [ ] Any random source is an explicitly seeded Generator — **none are used**

New free parameters requiring human approval: **none.**

## ERROR HANDLING REQUIREMENTS

- Combining incompatible dimensions raises `DimensionError`, a subclass of `VellumError`. The
  message names both dimensions in readable exponent form — a mismatch reported as two opaque tuples
  costs more time than it saves.
- Constructing a `UnitSystem` with a non-positive or non-finite anchor raises `ValueError`.
- **Nothing is silently coerced.** No "close enough" comparison of exponents, no promotion of a
  dimensionless value into a dimensioned one. `Fraction` makes exponent equality exact, so there is
  no tolerance question and none should be invented.
- No failure here is recoverable. Every error is a programmer error, and every one raises.

## SECURITY CONSIDERATIONS

- No file is read or written. No network. No deserialisation, and specifically no `pickle`.
- No `eval` or `exec`, including for any convenience that parses a dimension from a string — which
  is one of the reasons string parsing is excluded above.
- No external input of any kind reaches this module.
- No restricted category (auth, crypto, payments, secrets) applies.

## TESTS TO WRITE

Written before any implementation. Three kinds, in order.

**Dimensional** — the point of the module:
- [ ] The algebra: multiply, divide, power, equality, dimensionless identity, `Fraction` exponents
      surviving a cube root
- [ ] Every named dimension matches `docs/AXIOMS.md` §2 exactly. This test is the executable copy
      of that table and must fail if either drifts from the other
- [ ] **`g = G₂M/r` has the dimensions of acceleration, and `G₂M/r²` does not.** Verified by hand:
      `M⁻¹L²T⁻² · M / L = L T⁻²` ✓, while the inverse-square form gives `T⁻²` ✗
- [ ] **`L = 2πR σ₂ T³` has the dimensions of power, and `4πR² σ₂ T⁴` does not.** Verified:
      `L · MLT⁻³Θ⁻³ · Θ³ = ML²T⁻³` ✓, while the 3D form gives `ML³T⁻³Θ` ✗
- [ ] **`P = ρ g h` gives 2D pressure using `ρ = M L⁻²`, and 3D pressure using `M L⁻³`.** Verified:
      `ML⁻² · LT⁻² · L = MT⁻²` ✓ versus `ML⁻¹T⁻²` ✗
- [ ] Flux at distance `r` from luminosity, `L/(2πr)`, matches the flux dimension `M L T⁻³`
- [ ] Kinematic viscosity `μ/ρ` is `L² T⁻¹` — the case that is *not* different in 2D

  These three discriminating tests are the module's whole purpose: each is a formula that a
  3D-trained reflex writes wrongly and that dimensional analysis catches immediately.

  **Do not add a Reynolds-number test.** `ρvL/μ` is dimensionless under both the 2D and the 3D
  forms, so it discriminates nothing. Checked during this PRP; recorded so nobody adds it later
  believing it is a real check.

**Invariant** — true for every unit system:
- [ ] Natural-unit closure: for any valid `M_ref`, `L_ref`, the constructed system evaluates `G₂` and
      `σ₂` to exactly 1.0
- [ ] Round trip: `from_si(to_si(x)) == x` to within floating tolerance, for a spread of magnitudes.
      State the tolerance and why
- [ ] No NaN or infinity is producible from finite inputs through any public function
- [ ] Dimension objects are immutable and hashable; algebra never mutates an operand

**Regression:**
- [ ] Not applicable — nothing here is stochastic and nothing is generated. Recorded explicitly so
      the omission reads as deliberate rather than forgotten.

**Error paths:**
- [ ] Incompatible-dimension combination raises `DimensionError` with both dimensions in the message
- [ ] Non-positive and non-finite `UnitSystem` anchors raise `ValueError`

## ROLLBACK PLAN

- Branch to return to: whatever precedes the units-layer branch.
- State the codebase should be in: documents only, no `sim/`. Nothing depends on this yet, so
  rollback is `rm -rf sim/ pyproject.toml`.
- Anything irreversible: none. No data is generated, nothing is published, no migration exists.

## ACCEPTANCE CRITERIA

- [ ] The three discriminating tests above pass, and each fails when the 3D form is substituted —
      **verify the failure, do not assume it.** A test that cannot fail proves nothing
- [ ] The named-dimension test agrees with `docs/AXIOMS.md` §2 line for line
- [ ] Derivation check above fully ticked
- [ ] `pytest` passes
- [ ] `mypy --strict sim/` passes
- [ ] `ruff check sim/` passes
- [ ] Every physical quantity has a units-bearing docstring and a derivation reference
- [ ] Every physics module has an `Axioms used` line — and this one records `Abstracts: nothing`
- [ ] No new dependency
- [ ] No file over 300 lines
- [ ] CHANGELOG.md updated
- [ ] CONTEXT.md session entry closed

## VALIDATION

- `pytest`
- `mypy --strict sim/`
- `ruff check sim/`
- Deliberately break one formula to an inverse-square form and confirm the suite goes red. The value
  of this module is entirely in what it refuses to accept, so the refusal is the thing to
  demonstrate.
