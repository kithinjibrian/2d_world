## FEATURE: Standing water on a closed curve — basins, filling, and where a drop goes.

## OBJECTIVE

`sim/water/` finds Vellum's basins, works out which hold water and how deep, and says which stretch
of ground drains into each. Done means the viewer shows lakes and an ocean sitting in real terrain,
and the simulation can report how many basins there are, how many are sealed, and what fraction of
the world is wet — none of which is an input.

This is the first layer that produces a result the monograph only guessed at. What it produces is
not the guess.

## CONTEXT

- Starting state: `sim/units/`, `sim/star/`, `sim/orbit/`, `sim/surface/`, `sim/rotation/`,
  `sim/view/` complete. `h(s)` exists; nothing sits on it.
- Ending state: `sim/water/`, `sim/tests/water/`, and water drawn in the viewer.
- Related existing code: `sim/surface/terrain.py` for `h(s)`; `sim/periodic.py` for `wrap` and
  `distance` — **every comparison of surface positions goes through those**, never subtraction.
- Axioms this depends on: **T0.1** (two dimensions — a closed surface curve, so `h` is a function of
  one periodic coordinate), **T1.1** (gravity gives the downhill direction).
- Abstracted layers this leans on: **terrain statistics**, since the shape of the ground is chosen
  (`docs/AXIOMS.md` §4). Every count and fraction this layer reports therefore depends on a chosen
  roughness, and must be reported as such.
- New free parameters introduced: **total water area**, a world constant. Requires approval.
- Open decisions that block this: **none.** DECISION-013 (chemistry) would matter for ice and
  salinity; neither is in scope.

### What follows from two dimensions, and was checked before writing this

1. **A basin is a local minimum of `h`.** Filling it is a one-dimensional problem, not a watershed.
2. **A basin's catchment is a contiguous arc**, bounded by the two maxima either side. In three
   dimensions a drainage basin can be any shape; here it is an interval, and that is a theorem.
3. **Rivers cannot branch.** A tributary would have to arrive from a side that does not exist, so
   there are no confluences and no deltas. Discharge still accumulates *along* a channel — but there
   is only ever one channel between any two points, so nothing ever joins anything.
4. **A basin has exactly one outlet**: the lower of its two enclosing maxima. Not a network, not a
   choice — one point.
5. **A basin that never fills to its lip has no outlet at all.** What is sealed in one is sealed
   permanently: no flood route, no drainage web, no chance passage.
6. **Water quantity is an area, not a volume.** The world is two-dimensional, so a body of water is
   a region of the plane and `∫(level − h) ds` has dimensions `L²`. Mass is `density × area` with
   density in kg·m⁻², consistent with `docs/AXIOMS.md` §2.
7. **The basin structure is a merge tree.** Flooding upward, basins merge at the saddle between
   them; the shallower one dies there. In one dimension this is a sort plus union-find over
   neighbours.

### The finding that changes what this layer should report

**"How many basins are there" is not a well-defined question.** Terrain is fractal, so the number of
local minima is a function of how finely you sample it:

    samples     resolution     local minima
      1,024      3.75e-08              207
      4,096      9.38e-09              830
     16,384      2.34e-09            3,313
     65,536      5.86e-10           12,980
    262,144      1.46e-10           52,101

Counting minima means choosing the answer. The scale-free alternative is **topological persistence**
— a basin's depth below the point where it merges into a deeper one — which does not depend on
sampling. Measured on the current demo terrain:

    depth greater than      basins
      0.01 × RMS height      7,158
      0.05 × RMS               1,677
      0.10 × RMS                 582
      0.25 × RMS                 116
      0.50 × RMS                  36
      1.00 × RMS                   8

**So the monograph's 1,106 sealed basins is not a number this project can confirm or refute.** It
corresponds to *some* persistence threshold and not to any property of the world. The honest output
is the **curve**, not a count — and any single number must state the threshold that produced it.
Do not go looking for a threshold that yields 1,106.

## IMPLEMENTATION REQUIREMENTS

### Must Do

- **Build the merge tree by flooding upward**: sort samples by height, union with already-flooded
  neighbours, and record the merge height when two basins meet. The shallower basin dies there and
  its persistence is `merge height − its minimum`. Sort plus union-find; nothing cleverer is needed
  in one dimension.
- **Report basins by persistence, with the threshold as an explicit argument.** There is no default.
  A caller that does not state a depth has not asked a well-posed question.
- **Compute the catchment map**: which basin each surface position drains to. Assert it is a
  contiguous arc per basin — that is the one-dimensional form of "rivers cannot branch" and it is a
  theorem, so a violation is a bug.
- **Fill by cascade.** Water arrives in proportion to catchment length, each basin fills to the level
  its share supports, and any excess spills through the single outlet into the neighbour, repeating
  until stable. Basins that merge share one level thereafter.
- **Classify each basin as sealed or spilling** — sealed meaning its water never reaches its lip.
  That distinction is the whole reason the monograph's fish never meet, and it is an output.
- **Conserve water area exactly.** Total area in must equal total area held, to a stated tolerance,
  through every cascade. This is the headline invariant.
- **Work in areas, and say so.** Water quantity carries `LENGTH**2`. A quantity named "volume" in
  this layer is a bug.
- **Use `sim.periodic`** for every position comparison and every wrap.
- **Draw water in the viewer**, filled between the terrain and the level. Fill the ground below the
  profile at the same time — water sitting against an unfilled outline reads as a line drawing, not
  a world, and the ground fill has been outstanding since the surface layer.

### Must NOT Do

- **No precipitation, evaporation, or hydrological cycle.** Water is placed, not rained. A cycle
  needs climate, which does not exist.
- **No erosion.** It writes to the terrain residual and is its own PRP.
- **No stratification and no anoxic depth.** The monograph's dead basin floors follow from the
  inverse turbulent cascade, which is a fluids-and-climate question.
- **No tides, no currents, no waves.**
- **No ice and no salinity.** Both need DECISION-013.
- **Do not tune anything toward 1,106 basins**, or toward any monograph number. See above: the count
  is a function of a threshold, so matching it would mean choosing the threshold that matches — which
  is fitting, dressed as a result.
- **Do not report a basin count without its threshold.** A bare number is not a finding here.
- **Do not assume a global sea level.** Disconnected basins hold different levels; that is the point.

## DERIVATION CHECK

- [ ] Every quantity is an axiom, a world constant, or a derived result
- [ ] No 3D constant or scaling law; water is an **area**, not a volume
- [ ] Dimensions match `docs/AXIOMS.md` §2
- [ ] Nothing tuned to a monograph number, and the basin count is reported with its threshold
- [ ] Nothing hand-placed: no basin is positioned, no lake is put anywhere
- [ ] The one new free parameter (total water area) is listed above and approved
- [ ] Results are reported as resting on chosen terrain statistics (§4 ledger)
- [ ] All computation in natural units
- [ ] No random source beyond the terrain's own seed

New free parameters requiring human approval: **total water area**, a world constant.

## ERROR HANDLING REQUIREMENTS

- Negative or non-finite water area raises `ValueError`. Zero is legal and means a dry world.
- A non-positive persistence threshold raises — "all basins" is the fractal answer and is not a
  question with an answer.
- The cascade raises `InvariantError` if water area is not conserved to tolerance, or if it fails to
  reach a stable state within a bounded number of rounds. A cascade that will not settle is a bug in
  the merge tree, not a result to return.
- Non-finite levels raise.

## SECURITY CONSIDERATIONS

- No file read or written, no network, no deserialisation, no `eval`.
- No external input beyond parameters from calling code.
- No restricted category applies.

## TESTS TO WRITE

**Dimensional:**
- [ ] Water quantity carries `LENGTH**2`; level and depth carry `LENGTH`

**Invariant — theorems, so a failure is a bug:**
- [ ] **Water area is conserved exactly** through filling and every cascade
- [ ] **Every catchment is a contiguous arc** — the one-dimensional form of "rivers cannot branch",
      checked against a brute-force downhill walk from every sample
- [ ] Every surface position drains to exactly one basin
- [ ] Each basin has exactly one outlet, and it is the lower of its two enclosing maxima
- [ ] Basins that have merged share a level; basins that have not, do not
- [ ] Water never sits above its basin's lip
- [ ] Water level is never below the basin floor, and depth is never negative
- [ ] Merge-tree events number one fewer than the basins, since everything eventually joins
- [ ] Determinism: the same seed and water area give the same lakes

**Physical results — outputs, not targets:**
- [ ] Persistence is stable under sampling: refining the grid must not materially change the count
      of basins above a fixed depth, whereas counting raw minima must change it a lot. **Both halves
      asserted** — the second is what shows why persistence is used at all
- [ ] More water means a greater wet fraction, monotonically
- [ ] Enough water submerges the whole world, and the wet fraction reaches one
- [ ] With little water, some basins are sealed and hold different levels
- [ ] Sealed basins exist at plausible water amounts — the property the monograph's fish depend on

**Error paths:**
- [ ] Each raise above has a test

**Viewer:**
- [ ] The water drawable declares its bands and draws at each
- [ ] A lake is visible at ground zoom, and its surface is level
- [ ] Drawing does not raise for a dry world, a fully submerged world, or a single-sample lake —
      the degenerate shapes, tested directly rather than by rendering frames and hoping

## ROLLBACK PLAN

- Branch to return to: `main` at the polyline-crash fix.
- State: `rm -rf sim/water sim/tests/water`, remove the water drawable and the ground fill.
- Anything irreversible: none.

## ACCEPTANCE CRITERIA

- [ ] Water-area conservation fails if the cascade drops the overflow rather than passing it on —
      **verified by mutation**, as every layer so far
- [ ] The contiguous-catchment test fails if the catchment map is built by nearest-minimum rather
      than by descent — also verified
- [ ] Reported: the basin count at several persistence thresholds, the number sealed, and the wet
      fraction, each stated with the threshold and water area that produced it
- [ ] Derivation check fully ticked
- [ ] `pytest`, headless `pytest`, `mypy --strict sim/`, `ruff check sim/` all pass
- [ ] `docs/AXIOMS.md` §3 gains: catchments are arcs, one outlet per basin, water is an area, and
      that basin counts are threshold-dependent
- [ ] No new dependency; no file over 300 lines
- [ ] CHANGELOG.md updated; CONTEXT.md session closed

## VALIDATION

- `.venv/bin/pytest`, headless run, `mypy`, `ruff`
- `.venv/bin/python -m sim.view.app` — select Vellum, zoom to the ground, and **look at the water**.
  Session 14 established that a visual feature is not validated by asserting pixels changed, and
  Session 21 that rendering frames is not coverage of a rendering edge case. Both apply here.
- Report the basin-count curve against persistence, and say plainly that it is a curve rather than
  the number the monograph gives.
