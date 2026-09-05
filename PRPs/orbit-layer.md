## FEATURE: The two-body Kell–Vellum orbit under 2D gravity, and the insolation it produces.

## OBJECTIVE

`sim/orbit/` integrates Vellum's motion around Kell under `F = G₂Mm/r` and reports the orbit's
geometry and the flux arriving at the planet over time. Done means the layer reproduces five
predictions that follow from the force law, each asserted as a test, and supplies an insolation time
series the climate layers can consume.

This is the project's first physics. Everything before it was apparatus.

## CONTEXT

- Starting state: `sim/units/` complete — `Dimension`, `Quantity`, `UnitSystem`, `G2`, `SIGMA_2`.
  No physics module exists.
- Ending state: `sim/orbit/` and `sim/tests/orbit/`, plus a minimal `sim/star/` stub (see below).
- Related existing code: read `sim/units/__init__.py` for the public surface, and
  `sim/units/quantity.py` for the boundary convention resolved in DECISION-015.
- Axioms this depends on: **T0.2** (Newtonian mechanics), **T0.3** (non-relativistic — and this is
  the layer that first makes that assumption checkable, see Must Do), **T1.1** (gravity as a direct
  attractive force), **T2.2** (radiation, for insolation only).
- Must not contradict `docs/AXIOMS.md` §3: no orbit closes, no trajectory is unbound, seasons come
  from eccentricity alone.
- Abstracted layers this leans on: **Kell's luminosity** (`docs/AXIOMS.md` §4, DECISION-010). Every
  insolation result is therefore a consequence of a chosen parameter, not a finding about stellar
  physics, and must be reported that way.
- New free parameters introduced: **none.** Kell's mass and the initial state are world constants;
  luminosity is a swept parameter already declared in the ledger.
- Open decisions that block this: **none.** DECISION-012 blocks the scan, not this layer.

### Predictions this layer must reproduce

All five follow from `F ∝ 1/r` and were **confirmed numerically in a scratch integration while
drafting this PRP**, so they are targets rather than hopes. They are not monograph numbers and must
not be treated as such — they are consequences of T1.1.

1. **Circular orbital speed is independent of radius.** `v_c = √(G₂M)`, the same at every distance,
   because a logarithmic potential gives `r·dΦ/dr = G₂M` regardless of `r`. Checked at radii from
   0.5 to 50 with a relative radius spread of ~2.5e-9.
2. **Kepler's third law is replaced by `T ∝ r`.** Period is `2πr/√(G₂M)`, linear in radius, not
   `r^(3/2)`.
3. **The apsidal angle is `π/√2 ≈ 127.2792°`**, so the sweep from one pericentre to the next is
   `254.5584°` and the apsis line **regresses ≈105.4416° per orbit**. Measured `254.5500°` at
   `v/v_c = 1.02`. The near-circular limit is what the analytic value describes; the measured angle
   drifts with eccentricity (`254.3529°` at `v/v_c = 1.10`), so the test must be written in the
   near-circular regime and the drift asserted as a trend, not a fixed number.
4. **A season works round the calendar in exactly `2 + √2 ≈ 3.414214` orbits.** Closed form:
   `360/(360 − 180√2) = 2 + √2`. The monograph's ~900 years is wrong by a factor of ~300 and is not
   a target.
5. **Nothing escapes, at any speed.** Launched at 100× circular speed the trajectory still turns
   around. An integrator that ever produces an unbound orbit is broken.

## IMPLEMENTATION REQUIREMENTS

### Must Do

- **Integrate with velocity-Verlet at a fixed timestep.** Symplectic, so energy error is bounded
  rather than secular.

  This is not a preference. **A non-symplectic integrator manufactures apsidal precession**, and
  apsidal precession is the headline quantity this layer measures. A dissipative scheme would return
  a number that looks plausible, is partly numerical, and cannot be distinguished from the physical
  answer by inspection. Adaptive stepping is excluded for the same reason: it breaks symplecticity.
- **Include a timestep-convergence test.** Measure the precession at several timesteps and assert the
  result converges and is timestep-independent within a stated tolerance. Without it, prediction 3 is
  unverified no matter how good the number looks.
- **Report the apsidal angle by locating pericentres**, not by assuming any analytic form. Beware the
  distinction the drafting script got wrong: the *apsidal angle* is pericentre-to-apocentre
  (`π/√2`), while the pericentre-to-pericentre sweep is twice that. Name the function for what it
  returns.
- **Supply a screening path** (architecture rule 8) using the closed forms in predictions 1–4. It is
  nearly free here, and it independently cross-checks the integrator — a disagreement between the
  analytic and integrated apsidal angle in the near-circular limit is a bug in one of them.
- **Consume Kell through a stub** in `sim/star/`, exposing mass (a world constant) and luminosity (a
  swept parameter). It **raises `NotImplementedError`** for spectrum, radius, lifetime and evolution.
  Never a default. See anti-pattern 5 in CLAUDE.md.
- **Compute insolation as `L/(2πr)`** — flux dilutes as `1/r`, not `1/r²`, because light spreads over
  a circle. Return a time series over an orbit.
- **Check the non-relativistic assumption (T0.3).** Report the peak speed reached as a fraction of
  whatever signal speed the world is given, or, if none is defined yet, record the peak speed in
  natural units so the assumption can be checked the moment one is. T0.3 is the one axiom flagged as
  unvalidated, and this is the first layer able to say anything about it.
- Accept and return `Quantity` at the module boundary; work on raw arrays inside.

### Must NOT Do

- **No debris population and no impact cycle.** They are the obvious next thing and they are a
  separate PRP. Including them doubles the module and violates the SCOPE RULE.
- **No N-body.** Two bodies. Kell is fixed at the origin; Vellum is a test particle. If the mass
  ratio ever matters, that is a new PRP.
- **No planetary rotation, no day length, no tides, no obliquity.** A disc has no axis to tilt, so
  obliquity does not exist — do not add a parameter for it.
- **No adaptive timestep, and no `scipy.integrate.solve_ivp`.** See the symplectic requirement above.
- **Do not tune anything to the monograph's 611-day year or ~900-year precession.** Both are prior
  guesses; the second is known wrong.
- **Do not present insolation results as findings about stellar physics.** Luminosity is a stubbed
  parameter.

## DERIVATION CHECK

- [ ] Every quantity is an axiom, a world constant, or a derived result
- [ ] No constant or scaling law imported from a 3D reference — specifically not `1/r²` gravity,
      not `T ∝ r^(3/2)`, not `1/r²` flux
- [ ] All dimensions match `docs/AXIOMS.md` §2
- [ ] Nothing tuned or fitted to reproduce a monograph number
- [ ] Nothing that should emerge is hand-placed — precession is *measured*, never imposed
- [ ] Every new free parameter listed above and approved — **none are introduced**
- [ ] Abstracted layers listed above — **Kell's luminosity**, and every insolation result labelled
      as resting on it
- [ ] All computation in natural units; no SI outside the display layer
- [ ] Any random source is an explicitly seeded Generator — **none are used**

New free parameters requiring human approval: **none.**

## ERROR HANDLING REQUIREMENTS

- Non-positive or non-finite mass, radius, or timestep raises `ValueError` at the boundary.
- The integrator raises `InvariantError` if energy drift exceeds its stated bound, or if any state
  value becomes non-finite. A NaN propagating through a long integration costs an afternoon to trace.
- Requesting an apsidal angle from a trajectory containing fewer than two pericentres raises rather
  than returning a guess — too short an integration is a caller error, not a degenerate result.
- The Kell stub raises `NotImplementedError` for everything beyond mass and luminosity.
- **Never clamp a diverging trajectory.** Under this force law nothing escapes, so a trajectory
  running away is a bug in the integrator and must surface as one.

## SECURITY CONSIDERATIONS

- No file read or written, no network, no deserialisation, no `pickle`, no `eval`.
- No external input; all parameters arrive from calling code.
- No restricted category applies.

## TESTS TO WRITE

Written before implementation.

**Dimensional:**
- [ ] `G₂M/r` is an acceleration; the inverse-square form is rejected
- [ ] Insolation `L/(2πr)` carries `FLUX`; `L/(2πr²)` does not
- [ ] Specific orbital energy and angular momentum carry the right dimensions

**Invariant** — true for every orbit and every seed:
- [ ] **Nothing escapes.** Over a spread of launch speeds up to at least 100× circular, the
      trajectory turns around. Confirmed in drafting at v = 2, 5, 20, 100
- [ ] Energy drift is bounded, not secular, over a long run — the property velocity-Verlet is chosen
      for. State the bound and justify it
- [ ] Angular momentum is conserved to integrator tolerance
- [ ] No NaN or infinity in any state array
- [ ] Radial distance is always strictly positive — the log potential is singular at the origin, so
      a trajectory reaching `r = 0` is a setup error and must raise

**Physical predictions** — the substance of this layer:
- [ ] `v_c = √(G₂M)` at radii spanning at least two decades, to a stated tolerance
- [ ] Period is linear in radius: fitted `d(log T)/d(log r) = 1` to tolerance, **and demonstrably
      not 1.5**
- [ ] Near-circular apsidal angle is `π/√2` within the timestep-convergence tolerance
- [ ] Apsidal angle drifts away from `π/√2` as eccentricity rises — asserted as a monotone trend
- [ ] Season cycle is `2 + √2` orbits
- [ ] Timestep convergence: precession is timestep-independent as `dt → 0`

**Screening path:**
- [ ] Analytic and integrated results agree in the near-circular limit, to a stated tolerance
- [ ] The screening path is materially cheaper — assert it, so it cannot silently become as
      expensive as the full solve

**Regression:**
- [ ] A fixed initial state and timestep reproduce byte-identical output

**Error paths:**
- [ ] Each raise above has a test

## ROLLBACK PLAN

- Branch to return to: `main` at the units-layer commit.
- State the codebase should be in: `sim/units/` only; `rm -rf sim/orbit sim/star sim/tests/orbit`.
- Anything irreversible: none. No data generated, nothing published.

## ACCEPTANCE CRITERIA

- [ ] All five predictions pass as tests
- [ ] The timestep-convergence test passes — without it prediction 3 is unverified
- [ ] Substituting an inverse-square force makes the suite go red. **Verify the failure, do not
      assume it**, exactly as the units layer was mutation-checked
- [ ] Substituting a non-symplectic integrator (forward Euler) visibly corrupts the precession
      measurement — demonstrate it once and record the number, since it is the justification for the
      symplectic requirement
- [ ] Derivation check fully ticked
- [ ] `pytest`, `mypy --strict sim/`, `ruff check sim/` all pass
- [ ] Every physical quantity has a units-bearing docstring and a derivation reference
- [ ] Every module has `Axioms used`, and `sim/star/` has `Abstracts: Kell's luminosity`
- [ ] No new dependency beyond `scipy` if it is genuinely needed — prefer not
- [ ] No file over 300 lines
- [ ] CHANGELOG.md updated; CONTEXT.md session closed
- [ ] `docs/AXIOMS.md` §3 updated: the apsidal-precession entry loses its "to be re-confirmed
      numerically" caveat, and predictions 1, 2 and 4 are added as established consequences

## VALIDATION

- `.venv/bin/pytest`
- `.venv/bin/mypy`
- `.venv/bin/ruff check sim/`
- Break the force law to `1/r²` and confirm the suite goes red.
- Report the measured apsidal regression against the predicted `105.4416°/orbit`, and the season
  cycle against `2 + √2 = 3.414214` orbits.
