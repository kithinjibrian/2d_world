# AXIOMS — Vellum (2d_world)

**Status: DRAFT.** The axiom list in section 1 is not settled — that is DECISION-009, the most
important open question in the project. Sections 2 and 3 are settled: they are consequences of
choosing two spatial dimensions, and they do not depend on how DECISION-009 resolves.

This file is the anchor for the DERIVATION RULE in `CLAUDE.md`. Every quantity in the simulation is
exactly one of three things:

1. **An axiom** — a free choice, listed in section 1. Adding one requires human approval.
2. **A world constant** — an initial condition for a particular Vellum: the seed, Kell's mass, total
   angular momentum, initial composition. Varies per world; the physics does not.
3. **A derived result** — computed from 1 and 2, carrying a reference to what derived it.

A number that fits none of these three is a bug. This is the discipline that replaces the canon rule:
it is what stops "we derive our own physics" from becoming "we type in whatever looks right."

---

## 1. Axioms — DRAFT, pending DECISION-009

The free choices. Everything else must be derived from these.

**A1. Space has two dimensions.** One extended coordinate and one vertical. The universe is a plane;
Vellum is a disc within it; its surface is a closed curve.

**A2. Gravity follows from Gauss's law in 2D.** Flux spreads over a circle of circumference `2πr`,
so `F = G₂·m₁·m₂/r`. `G₂` is a free constant with units m²·s⁻²·kg⁻¹.

**A3. Newtonian mechanics.** `F = ma`, momentum and energy conserved, no relativity, no quantum
mechanics at simulation scale.

**A4. Blackbody radiation in 2D.** Emitted flux per unit length of radiating curve scales as `T³`.
`σ₂` is a free constant.

**A5. Classical thermodynamics and ideal-gas behaviour**, with 2D dimensions throughout.

**A6. Fluids obey Navier–Stokes in two dimensions.** Nothing about turbulence is imposed; the
inverse cascade is a consequence, not an axiom.

Candidates not yet decided: whether chemistry is modelled at all or abstracted; whether radiative
transfer is grey or spectral; whether `G₂` and `σ₂` are tuned to make a habitable world exist, or
held fixed with habitability left as a discovered outcome. That last one is the substance of
DECISION-009 and it is a real fork — one direction makes Vellum designed, the other makes it found.

---

## 2. Dimensions — settled, and the most common source of silent error

In 2D, physical quantities do not have their 3D dimensions. Nothing will crash if this is wrong;
the numbers will simply be meaningless. The units layer enforces these.

| Quantity | 3D | **2D (this project)** |
|---|---|---|
| Density | kg·m⁻³ | **kg·m⁻²** |
| Pressure | N·m⁻² (Pa) | **N·m⁻¹** — force per unit *length* |
| Gravitational constant | m³·kg⁻¹·s⁻² | **m²·kg⁻¹·s⁻²** |
| Mass distribution | volume integral | **area integral** |
| Radiating boundary | surface, m² | **curve, m** |
| Luminosity | W | **W** (but `L = 2πR·σ₂·T³`) |
| Flux | W·m⁻² | **W·m⁻¹** |
| Moment of inertia | kg·m² | kg·m² (unchanged) |

**Never import a numerical constant from a 3D reference.** `G = 6.674e-11` is not `G₂`; it is not
even the same kind of quantity. Any constant entering the codebase is either derived here or flagged
as an axiom.

---

## 3. Established consequences — derived, not chosen

These follow from section 1 and are recorded so sessions do not re-derive them incorrectly. Each is
a theorem, not a preference. Where the simulation contradicts one of these, the derivation is wrong
and must be found — do not adjust the result.

### Gravitation and orbits

- **The potential is logarithmic** (`Φ ∝ ln r`) and therefore unbounded above. **There is no escape
  velocity.** Nothing ever leaves the system, at any speed.
- **No orbit closes.** By Bertrand's theorem only inverse-square and harmonic force laws give closed
  orbits; `1/r` is neither. Every orbit is a rosette.
- **Apsidal precession is fast, not slow.** For near-circular orbits the apsidal angle is `π/√2 ≈
  127.3°`, so successive perihelia are `254.6°` apart and the apsis line regresses about **105° per
  orbit**. A season works its way round the calendar in roughly **3.4 orbits**.
  *The monograph's "~900 years" is wrong by a factor of ~300 and is not binding.* This is the
  worked example of why the monograph is not canon.
- **Seasons can only come from eccentricity.** A disc has no obliquity — there is no axis to tilt in
  a plane — so orbital distance is the sole driver.

### Radiation and climate

- **Flux dilutes as `1/r`, not `1/r²`** — light spreads over a circle. Insolation falls off far more
  slowly with distance, and the habitable zone is correspondingly wide.
- **Emission scales as `T³`.** A cubic law is a weaker stabilising feedback than the 3D quartic, so
  a 2D world's climate is more excitable than Earth's for the same forcing.
- **Wien's displacement still holds** in form (`λ_peak·T = const`), with a different constant.

### Atmosphere

- **There is no atmospheric escape.** This follows directly from the unbounded potential: no Jeans
  escape, no hydrodynamic blowoff. A 2D planet retains every gas it has ever acquired, hydrogen
  included, forever. Atmospheric composition is therefore cumulative and never thins.
- **Turbulence cascades inversely.** In 2D, enstrophy goes to small scales and energy to large ones,
  so eddies merge rather than shred. Large coherent vortices form and persist. This is a result of
  A6, not an imposed behaviour — do not hand-place storms.

### Waves and sound

- **Huygens' principle fails in even spatial dimensions.** The 2D wave equation's Green's function
  has support *inside* the light cone, not only on it, so a sharp pulse develops a decaying tail.
  No clean echo is possible, anywhere, ever.
- **Intensity falls as `1/r`** — cylindrical spreading. Signals carry much further than in 3D.

### Topology — the strongest constraints in the world

- **Any closed curve disconnects the plane** (Jordan curve theorem). A loop of tissue severs its
  interior from everything outside it. This forbids, as theorems and not as design choices: a
  through-gut, a closed circulatory circuit, a lens sealed across an aperture, and any hub inside a
  housing — so no wheel, no axle, no rotating joint. Every mechanism must oscillate.
- **A tunnel cannot be propped.** A support pillar spanning a tunnel seals it in two. Burrows are
  possible; connected networks are not.
- **On the surface, nothing passes anything.** Two bodies on a line are in a fixed order and stay in
  it. This has a direct computational consequence — see ARCHITECTURE RULES in `CLAUDE.md`.
- **A barrier across the line partitions the world**, not a landscape. There is no route around.

### Statistics

- **Random walks in 2D are recurrent** — a diffusing particle returns to its origin with probability
  1, where in 3D it may never return. Diffusion-limited processes behave qualitatively differently.

---

## 4. Relationship to the monograph

`vellum-monograph.html` is a **prior hypothesis**, written before any of this was checked. It is
reference material and a target artefact — the long-term goal is to regenerate it from simulation
output, with real numbers and plates the simulation drew.

It is not a source of truth, it is not canon, and **no parameter may be tuned to reproduce a number
in it.** Where it agrees with derivation (no escape velocity, wave tails, the inverse cascade,
the topological prohibitions) it guessed well. Where it disagrees (apsidal precession), it is simply
wrong, and the sim is right.
