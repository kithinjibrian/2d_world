# AXIOMS — Vellum (2d_world)

The anchor for the DERIVATION RULE in `CLAUDE.md`. Every quantity in the simulation is exactly one
of three things:

1. **An axiom** — a free choice, listed in §1. Adding one requires human approval.
2. **A world constant** — an initial condition for a particular world: the seed, Kell's mass, total
   angular momentum, composition. Varies per world; the axioms do not.
3. **A derived result** — computed from the above, carrying a reference to what derived it.

A number fitting none of the three is a bug.

**Status.** The tier structure and §2–§5 are settled. The dimensionless ratios that characterise a
world are **scanned** rather than chosen (DECISION-009): habitability is an output of a parameter
sweep, not an assumption built into it. What remains open is the predicate deciding which grid points
count as habitable — DECISION-012.

---

## 1. The axioms, in tiers

Axioms are layered. Each tier takes the tier below as given, and each declares what it **cannot**
derive. The declarations matter as much as the axioms: they are the record of where this project
posits rather than derives, and §4 collects them into a single ledger.

The chain from fundamental forces to a climate is not computable — not here, not in three
dimensions, not by anyone. Nobody derives Navier–Stokes by simulating molecules. So the honest
structure is not one fundamental layer generating everything, but a stack of effective theories
whose *form* is constrained by the geometry and whose *parameters* are declared.

---

### Tier 0 — Geometry and mechanics

Nearly free. Almost everything else hangs off these.

**T0.1 — Space has two dimensions.** One extended coordinate and one vertical. The universe is a
plane; Vellum is a disc within it; its surface is a closed curve. This is the only axiom the project
exists to explore; everything interesting is a consequence of it.

**T0.2 — Mechanics is Newtonian.** `F = ma`. Energy, linear momentum and angular momentum are
conserved. Time is absolute.

**T0.3 — Dynamics is non-relativistic.** Orbital and fluid speeds are assumed far below any signal
speed, so no Lorentz structure is needed.
*Cannot derive:* its own validity. This is an assumption about the regime, and it must be checked
once orbital speeds are known rather than assumed forever. If a derived speed ever approaches a
meaningful fraction of a signal speed, this axiom has failed and the layer above it is invalid.

---

### Tier 1 — Fundamental interactions

**T1.1 — Gravity is a direct attractive force**, not spacetime curvature:

    F = G₂ · m₁ · m₂ / r          (attractive, always)

The `1/r` follows from Gauss's law in a plane — flux spreads over a circle of circumference `2πr`,
not a sphere of area `4πr²`.

**This is not a simplification of general relativity. It is a replacement for it, because in two
spatial dimensions GR is empty.** In `d` spacetime dimensions the graviton carries `d(d−3)/2`
propagating degrees of freedom: two in 3+1D, and **exactly zero in 2+1D**. The mechanism is that in
three dimensions the Riemann tensor has the same six independent components as the Ricci tensor and
is algebraically determined by it — there is no Weyl tensor. In vacuum, Einstein's equations force
Ricci to vanish, which now forces Riemann to vanish too, so **spacetime is flat everywhere there is
no matter.** A point mass produces no field, only a conical defect: a deficit angle in an otherwise
flat plane (Deser, Jackiw & 't Hooft, 1984). Masses in that geometry feel nothing. Nothing orbits.
There are no gravitational waves and no black holes without a cosmological constant bolted on.

So geometric gravity in 2D does not give a weak force; it gives *no* force. Gravity here must be
postulated as an interaction. It is an axiom in the strongest sense — nothing derives it.

*Cannot derive:* why gravity is attractive, or the value of `G₂` (see §2 — it is set to 1 by choice
of units, which makes the real question a dimensionless one).

**T1.2 — Electromagnetism is abstracted, not modelled.** *(DECISION-011, resolved)*

There is no Maxwell solver. Light, radiative transport and material cohesion are supplied at Tier 2
as effective theories with declared parameters.

*Cannot derive:* light as a phenomenon, material strength, refraction, plasma behaviour, chemistry,
or anything requiring charge dynamics. Every one of these is either posited at Tier 2 or absent.

If EM is ever added, 2D changes it substantially and the interface must not assume otherwise: the
magnetic field is a **scalar**, not a vector, because there is no cross product in a plane — so no
vector dipole moment, no compass, no magnetosphere in the familiar sense. The photon has **one
polarization state** rather than two, so polarization phenomena do not exist. The electric force
falls as `1/r`, by the same Gauss argument as gravity.

**T1.3 — Matter has no microstructure.** No nuclear, atomic or molecular model. Matter is a
continuum characterised by bulk parameters at Tier 2.

*Cannot derive:* chemistry, phase transitions from first principles, material strength, opacity,
composition-dependent behaviour of any kind. Phases and material properties are posited.

---

### Tier 2 — Effective theories

Each entry has a **form** constrained by Tier 0 geometry, and **parameters** that are world
constants rather than derived quantities. The form is not free; the parameters are.

**T2.1 — Thermodynamics is classical.** Ideal-gas behaviour, with 2D dimensions throughout (see §2).
*Parameters:* specific heats, molecular mass of each bulk species.

**T2.2 — Radiation is a field with 2D geometry.** Blackbody flux per unit length of radiating curve
scales as `T³`; flux dilutes as `1/r`.

The `T³` is not a choice — it follows from counting modes in two dimensions, where the mode density
goes as `k^(d−1)` and the energy density therefore as `T^(d+1)`. The photon's single polarization
state changes the constant `σ₂`, not the exponent. Wien's displacement law survives in form
(`λ_peak · T = const`) with a different constant.
*Parameters:* `σ₂` (set to 1 by units, see §2); opacity. Whether transfer is grey or spectral is
DECISION-014.

**Kell's output is an input, not a result** (DECISION-010). The star is stubbed behind its real
interface: luminosity is supplied as a swept parameter rather than solved from stellar structure.
Under a scan this is not a placeholder but an extra axis — and deriving the star later *collapses*
that axis by predicting luminosity from stellar mass, rather than invalidating anything. The stub
raises rather than answering for spectrum, radius, lifetime or evolution.

**T2.3 — Fluids obey the Navier–Stokes equations in two dimensions.**
Nothing about turbulence is imposed. The inverse cascade — energy to large scales, enstrophy to
small, eddies merging rather than shredding — is a **consequence** of 2D Navier–Stokes and must
emerge. Do not hand-place storms.
*Parameters:* viscosity, equation of state.

**T2.4 — Solids are a continuum with bulk material response.**
*Parameters:* density, stiffness, yield strength, friction — per material, all world constants.
*Cannot derive:* any of those parameters. They come from T1.3 being abstracted.

---

## 2. Units and scales

**Choose natural units. Do not attempt to express anything in SI.**

SI is calibrated to our universe; there is no correct value of `G₂` in it, and looking for one is a
category error. Instead the constants define the scales:

1. Choose a **reference mass** `M_ref` ≡ 1.
2. Choose a **reference length** `L_ref` ≡ 1.
3. **Set `G₂` ≡ 1.** Since `[G₂] = L²·M⁻¹·T⁻²`, this fixes the time unit: `T_ref = L_ref / √M_ref`.
4. **Set `σ₂` ≡ 1.** Since `[σ₂] = M·L·T⁻³·Θ⁻³`, this fixes the temperature unit.

Two reference choices and two normalisations fix all four base units. Conversion to metres and
seconds happens only at the display layer, where it is cosmetic.

**What survives this, and is therefore the only thing physically meaningful, is dimensionless
ratios.** In our own universe the questions that matter are the fine-structure constant and the
proton–electron mass ratio, not the numeric value of `G`. The same holds here: a world is
characterised by ratios such as Kell's mass to Vellum's, orbital radius to planetary radius,
atmospheric scale height to radius, thermal to gravitational binding energy, and the Reynolds number
of the atmosphere. **Those are the free parameters of a world, and they are swept, not chosen** —
see DECISION-009. Habitability is read off the sweep, never assumed into it.

### Dimensions in two dimensions

Dimensional bookkeeping is mechanical once the base dimensions are fixed — mass, length, time,
temperature — and every other quantity is a product of powers. Its job is narrow but real: catching
the moment a density is written as `kg·m⁻³` in a world where it is `kg·m⁻²`. Nothing will crash if
that is wrong; the number will simply be meaningless, and it will surface several modules later as
an untraceable result.

| Quantity | 3D | **2D (this project)** |
|---|---|---|
| Density | kg·m⁻³ | **kg·m⁻²** |
| Pressure | N·m⁻² (Pa) | **N·m⁻¹** — force per unit *length* |
| Gravitational constant | m³·kg⁻¹·s⁻² | **m²·kg⁻¹·s⁻²** |
| Mass distribution | volume integral | **area integral** |
| Radiating boundary | surface, m² | **curve, m** |
| Flux | W·m⁻² | **W·m⁻¹** |
| Luminosity | W | W, but `L = 2πR·σ₂·T³` |
| Moment of inertia | kg·m² | kg·m² (unchanged) |

**Never import a numerical constant from a 3D reference.** `G = 6.674e-11` is not `G₂`; it is not
even the same kind of quantity.

---

## 3. Established consequences — derived, not chosen

Theorems, not preferences. Where the simulation contradicts one of these, the derivation is wrong
and must be found — do not adjust the result.

### Gravitation and orbits *(from T1.1)*

- **The potential is logarithmic** (`Φ ∝ ln r`) and unbounded above. **There is no escape velocity.**
  Nothing ever leaves the system, at any speed.
- **No orbit closes.** By Bertrand's theorem only inverse-square and harmonic force laws give closed
  orbits; `1/r` is neither. Every orbit is a rosette.
- **Apsidal precession is fast.** For near-circular orbits the radial and angular frequencies stand
  in the ratio `√2`, so the apsidal angle is `π/√2 ≈ 127.2792°`, successive perihelia are
  `254.5584°` apart, and the apsis line regresses **105.4416° per orbit**. *The monograph's "~900
  years" is wrong by a factor of ~300.* **Confirmed numerically** by `sim/orbit/` in Session 9;
  measured `254.5563°` at `v/v_c = 1.01` with timestep convergence.
- **A season works round the calendar in exactly `2 + √2 ≈ 3.414214` orbits.** Closed form:
  `2π / (2π − 2·π/√2) = 2 + √2`. Confirmed numerically.
- **Circular orbital speed is independent of radius:** `v_c = √(G₂M)`, identical at every distance,
  because `r·dΦ/dr = G₂M` leaves no `r`. Every circular orbit around Kell moves at the same speed,
  however far out — the two-dimensional analogue of a flat galactic rotation curve. Verified from
  `r = 0.5` to `r = 1000`.
- **Kepler's third law is replaced by `T ∝ r`.** Period is `2πr/√(G₂M)`, linear in radius rather
  than `r^(3/2)`. Verified: fitted exponent 1.0 to 1e-12.
- **The orbital equation of motion is scale-invariant.** `r → kr` with `t → kt` leaves it unchanged,
  so orbit *shape* — and therefore the apsidal angle — is independent of scale. A practical
  consequence found while testing: an integrator leaking energy inflates an orbit without changing
  its measured precession, so precession is a poor diagnostic of integration quality here and the
  orbit's radius is a good one.
- **The turning radius for a radial launch is `r₀·exp(v²/(2G₂M))`** — finite for every launch speed,
  which is what "no escape velocity" means concretely. It grows so fast that above roughly `37.7×`
  the circular speed it exceeds double precision, even though the trajectory is still bound.
- **Seasons can only come from eccentricity.** A disc has no obliquity — there is no axis to tilt in
  a plane — so orbital distance is the sole driver.

### Radiation and climate *(from T2.2)*

- **Flux dilutes as `1/r`**, not `1/r²`. Insolation falls off far more slowly with distance, and the
  habitable zone is correspondingly wide.
- **Emission scales as `T³`.** A cubic law is a weaker stabilising feedback than the 3D quartic, so
  a 2D world's climate is more excitable than Earth's under the same forcing.

### Atmosphere *(from T1.1 and T2.3)*

- **There is no atmospheric escape**, ever. This follows directly from the unbounded potential: no
  Jeans escape, no hydrodynamic blowoff. A 2D planet retains every gas it has ever acquired,
  hydrogen included, forever. Atmospheric composition is cumulative and never thins.
- **Turbulence cascades inversely.** Energy to large scales, enstrophy to small; eddies merge rather
  than shred, so large coherent vortices form and persist. A result of T2.3, not an imposed
  behaviour.

### Waves and sound *(from T0.1)*

- **Huygens' principle fails in even spatial dimensions.** The 2D wave equation's Green's function
  has support *inside* the light cone, not only on it, so a sharp pulse develops a decaying tail.
  No clean echo is possible, anywhere, ever.
- **Intensity falls as `1/r`** — cylindrical spreading. Signals carry much further than in 3D.

### Topology — the strongest constraints in the world *(from T0.1)*

- **Any closed curve disconnects the plane** (Jordan curve theorem). A loop of tissue severs its
  interior from everything outside. This forbids — as theorems, not design choices — a through-gut,
  a closed circulatory circuit, a lens sealed across an aperture, and any hub inside a housing. So
  no wheel, no axle, no rotating joint. Every mechanism must oscillate.
- **A tunnel cannot be propped.** A support pillar spanning a tunnel seals it in two. Burrows are
  possible; connected networks are not.
- **Nothing passes anything on the surface.** Two bodies on a line hold their order permanently.
  This has a direct computational consequence — see ARCHITECTURE RULES in `CLAUDE.md`.
- **A barrier across the line partitions the world**, not a landscape. There is no route around.

### Statistics *(from T0.1)*

- **Random walks in 2D are recurrent** — a diffusing particle returns to its origin with probability
  1, where in 3D it may never return. Diffusion-limited processes behave qualitatively differently.

---

## 4. The abstraction ledger

Everything this project posits rather than derives, in one place. **A result that depends on an
entry here is not a discovery about two-dimensional physics — it is a consequence of a choice.**
Any module standing in for an abstracted layer must say so in its docstring and raise loudly where
it is asked for something it cannot honestly supply, rather than returning a plausible default.

| Abstracted | Because | What it costs | Revisit when |
|---|---|---|---|
| Electromagnetism (T1.2) | DECISION-011 — a Maxwell solver is a project in itself and still yields no chemistry | Light is posited, not derived. No refraction, plasma, or charge dynamics | Radiation behaviour becomes a research question rather than an input |
| Matter microstructure (T1.3) | Not computable from forces | All material parameters are inputs: density, strength, opacity, phase behaviour | Never, realistically |
| Chemistry | Follows from T1.3 | Composition is a small set of bulk species with assumed properties | DECISION-009b |
| Constitutive relations (T2.1, T2.3, T2.4) | Effective theories require them by construction | Viscosity, specific heats, stiffness are chosen | Only if a value turns out to matter qualitatively |
| Non-relativistic regime (T0.3) | Assumed, not checked | Invalid if any derived speed approaches a signal speed | Once orbital speeds are known |
| Kell's luminosity (T2.2) | DECISION-010 — stubbed to reach the surface layers sooner | Stellar output is a swept parameter, so no climate result is a finding about stellar physics | Once the scan shows which luminosities matter — the map makes the derivation better targeted |

---

## 5. Relationship to the monograph

`vellum-monograph.html` is a **prior hypothesis**, written before any of this was checked. It is
reference material and a target artefact — the long-term goal is to regenerate it from simulation
output, with real numbers and plates the simulation drew.

It is not a source of truth, it is not canon, and **no parameter may be tuned to reproduce a number
in it.** Where it agrees with derivation — no escape velocity, wave tails, the inverse cascade, the
topological prohibitions — it guessed well. Where it disagrees, as with apsidal precession, it is
simply wrong.
