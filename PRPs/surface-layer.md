## FEATURE: Vellum's ground — a height field on the closed surface, evaluable at any resolution.

## OBJECTIVE

`sim/surface/` gives Vellum a shape: `h(s)`, the height of the ground at any position along the
closed surface curve, queryable at any resolution from the whole world down to the layer's stated
floor. Done means the viewer can zoom from the disc's outline to a stretch of ground a few metres
across and see real, consistent terrain at every step, with the same profile every time from the
same seed.

This is what the viewer was built to show.

## CONTEXT

- Starting state: `sim/units/`, `sim/star/`, `sim/orbit/`, `sim/view/` complete. Vellum is a bare
  circle.
- Ending state: `sim/surface/`, `sim/tests/surface/`, and a `TerrainTrace` drawable in
  `sim/view/render.py` replacing the bare `PlanetDisc` outline.
- Related existing code: `sim/view/geometry.py` for `Disc` and the periodic `mod`;
  `sim/view/camera.py` for `surface_to_screen`, which is how terrain reaches the screen.
- Axioms this depends on: **T0.1** (two dimensions — the surface is a closed curve, so `h` is a
  function of one periodic coordinate). Nothing else. Terrain shape is not derived from physics.
- Abstracted layers this leans on: **terrain statistics** — a new entry for `docs/AXIOMS.md` §4.
  Roughness and amplitude are world constants, not consequences. Deriving them would need tectonics
  and erosion, which are not modelled. **Any result depending on the shape of the ground is a
  consequence of a choice**, and the module must say so.
- New free parameters introduced: **roughness exponent** and **amplitude**, both world constants,
  both requiring approval as part of this PRP.
- Open decisions that block this: **none.** DECISION-017 resolved to a procedural base plus a
  sampled residual.

## IMPLEMENTATION REQUIREMENTS

### Must Do

- **Base field: periodic multi-octave gradient noise (fBm).** Each octave places a lattice over the
  surface, takes the cell index **modulo that octave's cell count**, and hashes it with the seed and
  the octave number. The modulo is what makes periodicity exact — `h(s) == h(s + C)` by
  construction, not by stitching. Amplitude falls by a fixed persistence per octave; that
  persistence is the roughness parameter.

  Not a Fourier sum. Resolving metre detail on a 38,400 km surface needs 38 million coefficients and
  costs `O(k)` per sample; fBm needs 26 octaves and costs `O(octaves)`. See DECISION-017.

- **Evaluate at the resolution asked for.** `height(s, resolution=...)` sums only the octaves that
  matter at that scale. Querying a whole-world profile must not pay for metre detail, and querying a
  metre of ground must get it.

- **Report the resolution floor, and refuse to fake anything below it.** The floor is
  `C / 2**max_octaves`. Asking for finer detail returns the finest available *and says so* — via an
  explicit, inspectable property, never a silent smoothing. A viewer that zooms past the floor must
  be able to tell the user the ground has run out of detail rather than showing invented flatness.

- **Sampled residual, added on top.** An optional array over the surface, linearly interpolated,
  periodic across the seam, `None` by default and costing nothing when absent. This is where a
  crater or an eroded channel will live — modifications that cannot be expressed by changing a noise
  parameter.

- **Determinism.** Same seed, same terrain, byte-identical, across runs and across processes. The
  hash must not use Python's `hash()` for strings or anything else the interpreter randomises per
  run. Use an explicit integer mix.

- **Consistency across resolutions.** The value of `h` at a point must not depend on whether it was
  evaluated alone, inside a dense array, or as part of a coarse sweep — up to the octaves included.
  A coarse evaluation must be the low-passed version of a fine one, not a different field.

- **A `TerrainTrace` drawable** for the viewer: sample the visible arc at roughly screen resolution,
  draw through `camera.surface_to_screen`. Bands GROUND, REGIONAL and PLANETARY. It replaces the
  bare outline currently drawn by `PlanetDisc`.

- **State the abstraction in the module docstring**, with an `Abstracts:` line naming terrain
  statistics, as `sim/star/` does for luminosity.

### Must NOT Do

- **No basins, no water, no sea level, no drainage.** That is the next layer, and it is substantial:
  basin detection, filling, the unbranched runs, the anoxic depth. Including it here doubles the
  module and breaks the SCOPE RULE.
- **No erosion, no tectonics, no craters.** The residual is the *mechanism* for those; using it is a
  later PRP.
- **No 2D heightmap.** The surface is a closed curve, so `h` is a function of one coordinate. Any
  API taking two surface coordinates is a misunderstanding of the world.
- **Do not tune terrain to the monograph.** It describes mountains and a 31 cm plant ceiling; none of
  that is a target, and the plant ceiling belongs to a life layer that does not exist.
- **Do not present terrain statistics as derived.** They are chosen. Say so wherever they appear.
- **Do not cache silently.** If evaluation is memoised, the cache must be explicit and must not
  change results — a cache that changes what `h(s)` returns is a bug that will be blamed on the
  noise for a week.

## DERIVATION CHECK

- [ ] Every quantity is an axiom, a world constant, or a derived result
- [ ] No constant or scaling law imported from a 3D reference
- [ ] Heights and positions carry the dimensions in `docs/AXIOMS.md` §2
- [ ] Nothing tuned to reproduce a monograph number
- [ ] Nothing that should emerge is hand-placed — no mountain is positioned by hand
- [ ] The two new free parameters (roughness, amplitude) are listed above and approved
- [ ] The abstraction ledger gains a terrain-statistics entry, and the module carries `Abstracts:`
- [ ] All computation in natural units; no SI outside display
- [ ] Every random source is an explicitly seeded generator or an explicit integer hash — never
      Python's randomised `hash()`

New free parameters requiring human approval: **roughness exponent** and **amplitude**, both world
constants.

## ERROR HANDLING REQUIREMENTS

- A non-positive circumference, amplitude, octave count or resolution raises `ValueError`.
- A residual whose length does not divide the surface sensibly, or which contains non-finite values,
  raises at construction rather than at first evaluation.
- `height()` raises `InvariantError` if it ever produces a non-finite value — the noise is bounded by
  construction, so a NaN means the hash or the interpolation is broken.
- **Never silently extrapolate below the resolution floor.** Return the finest available and expose
  the floor; do not invent detail and do not pretend the request was met.

## SECURITY CONSIDERATIONS

- No file read or written, no network, no deserialisation, no `pickle`, no `eval`.
- The seed is the only external input; it is an integer and is validated.
- No restricted category applies.

## TESTS TO WRITE

**Dimensional:**
- [ ] Height carries LENGTH; surface position carries LENGTH; roughness is dimensionless

**Invariant — true for every seed and every world:**
- [ ] **Exact periodicity:** `h(s) == h(s + C)` to float tolerance, for many `s`, at every octave
      count. This is the property the lattice modulo exists to guarantee, and the acceptance
      criteria require demonstrating it fails when the modulo is removed
- [ ] Continuity across the seam: `h` just before `C` and just after `0` differ by no more than the
      local slope times the step — no discontinuity at the wrap
- [ ] Determinism: identical seed gives byte-identical output; different seeds differ
- [ ] Resolution consistency: `h(s)` evaluated alone equals `h(s)` inside a dense array
- [ ] Coarse is a low-pass of fine: adding octaves adds detail without moving the coarse structure
      by more than the added octaves' amplitude
- [ ] Finiteness everywhere, over a dense sweep
- [ ] Bounded: `|h|` never exceeds the sum of octave amplitudes

**Statistical — the field must actually be what it claims:**
- [ ] RMS height matches the configured amplitude within a stated tolerance
- [ ] The power spectrum's slope matches the configured roughness within tolerance. This is the test
      that catches a noise function that is merely *random* rather than *fractal*
- [ ] The mean is near zero and does not drift with sample count

**Residual:**
- [ ] Adding a residual shifts `h` by exactly the interpolated residual
- [ ] The residual interpolates periodically across the seam
- [ ] A `None` residual costs nothing and changes nothing

**Resolution floor:**
- [ ] The floor is reported and equals `C / 2**max_octaves`
- [ ] Requesting finer detail returns the finest available and reports that it was clamped

**Viewer integration:**
- [ ] `TerrainTrace` declares its bands and draws without error at each of them
- [ ] At ground zoom the drawn profile visibly differs from a circle — the point of the layer

**Error paths:**
- [ ] Each raise above has a test

## ROLLBACK PLAN

- Branch to return to: `main` at the viewer commit.
- State the codebase should be in: `rm -rf sim/surface sim/tests/surface`, and restore
  `PlanetDisc` as the drawable for Vellum's outline.
- Anything irreversible: none.

## ACCEPTANCE CRITERIA

- [ ] **Removing the lattice modulo breaks the periodicity test — verified, not assumed**, as the
      units, orbit and viewer layers were mutation-checked
- [ ] The power-spectrum test fails if octave amplitudes are made uniform rather than decaying —
      also verified, since it is what distinguishes fractal terrain from noise
- [ ] Zooming in the viewer from the whole disc to a few metres of ground shows consistent terrain
      at every scale, with no popping and no seam
- [ ] The resolution floor is reported in the viewer's readout when the zoom passes it
- [ ] Derivation check fully ticked
- [ ] `pytest`, `SDL_VIDEODRIVER=dummy pytest`, `mypy --strict sim/`, `ruff check sim/` all pass
- [ ] `docs/AXIOMS.md` §4 gains the terrain-statistics entry
- [ ] Every module has `Axioms used`, and `sim/surface/` has `Abstracts: terrain statistics`
- [ ] No new dependency
- [ ] No file over 300 lines
- [ ] CHANGELOG.md updated; CONTEXT.md session closed

## VALIDATION

- `.venv/bin/pytest` and the headless run
- `.venv/bin/mypy` and `.venv/bin/ruff check sim/`
- `.venv/bin/python -m sim.view.app` — zoom from the whole disc to metres of ground. Terrain is the
  kind of thing that passes every statistical test and still looks wrong, so it must be looked at.
- Report the measured RMS height and spectral slope against the configured values.
