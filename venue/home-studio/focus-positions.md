# Focus Positions: Home Studio

Source: venue/home-studio/plot.md
Generated: 2026-02-15

## Movers

Fixtures with pan/tilt control in this venue:

| Name | ID | Type | Mount Position | Safe Pan | Safe Tilt |
|------|----|------|----------------|----------|-----------|
| Back Left Sharpy | 8 | Sharpy Knockoff | (0.5, 1.5, 0.3) | 90–220 | 0–40 |
| Back Right BSW | 1 | BSW 3-in-1 | (3.8, 1.5, 0.3) | 0–200 | 5–40 |
| Front Center Profile | 4 | Profile Knockoff | (2.1, 4.0, 6.5) | 0–230 | 85–155 |
| Back Wall NI3K | 3 | Nausea Inducer 3000 | (1.3, 0.9, 0.3) | 0–255 | (per-head) |

Note: NI3K has pan control but tilts are per-head with rotation modes (0-127 position,
128-191 forward rotation, 192-255 reverse rotation). NI3K pan is included in area
positions but tilt values are omitted — use tilt as an effect parameter instead.

## Performance Area

The home studio is a 4.3m x 6.7m rectangular room. The DJ booth sits against the back
wall (Z=0). The performance/dance area spans roughly X=0.5–3.8, Z=1.5–5.5. Audience
perspective is from the front (Z=6.7). All three movers are mounted high and can cover
the full performance area.

Grid layout (performer's perspective facing audience):

```
         Stage Left        Center        Stage Right
         X=0.8             X=2.15        X=3.5
         |                 |             |
Z=1.7  --USL--------------USC-----------USR--   (near DJ booth)
         |                 |             |
Z=3.35 --SL---------------C-------------SR--    (mid-room)
         |                 |             |
Z=5.0  --DSL--------------DSC-----------DSR--   (near audience)
```

## Areas

### Center (C)
The default home position. All movers converge on floor center. Use as the "reset"
position between movements and as the anchor for intimate, focused moments.
Floor: X=2.15, Z=3.35

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 153 | 0 | Yes |
| BSW (ID 1) | 7 | 19 | Yes |
| Profile (ID 4) | 0 | 123 | Yes |
| NI3K (ID 3) | 128 | — | Yes |

### Downstage Center (DSC)
Near the audience, dead center. The strongest audience-engagement position — use for
climactic moments, drops, and direct visual impact.
Floor: X=2.15, Z=5.0

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 158 | 6 | Yes |
| BSW (ID 1) | 179 | 27 | Yes |
| Profile (ID 4) | 64 | 145 | Yes |
| NI3K (ID 3) | 128 | — | — |

### Upstage Center (USC)
Near the DJ booth/back wall. Points at the performer position. Good for back-lighting
the DJ and dramatic reveals from behind.
Floor: X=2.15, Z=1.7

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 157 | 0 | Yes |
| BSW (ID 1) | 181 | 21 | Yes |
| Profile (ID 4) | 52 | 136 | Yes |
| NI3K (ID 3) | 128 | — | — |

### Stage Left (SL)
Mid-depth, left side. Useful for side-washes and creating width in the room.
Floor: X=0.8, Z=3.35

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 170 | 0 | Yes |
| BSW (ID 1) | 189 | 29 | Yes |
| Profile (ID 4) | 50 | 165 | Yes |
| NI3K (ID 3) | 80 | — | No (calc) |

### Stage Right (SR)
Mid-depth, right side. Mirror of SL. Near the par wall — creates interesting layering
when pars and movers overlap on this side.
Floor: X=3.5, Z=3.35

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 149 | 5 | Yes |
| BSW (ID 1) | 170 | 23 | Yes |
| Profile (ID 4) | 110 | 145 | Yes |
| NI3K (ID 3) | 176 | — | No (calc) |

### Downstage Left (DSL)
Near audience, stage left. Good for solo spotlighting and entrance highlights.
The Sharpy hitting this from across the room creates a dramatic long-throw beam.
Floor: X=0.8, Z=5.0

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 170 | 0 | Yes |
| BSW (ID 1) | 189 | 29 | Yes |
| Profile (ID 4) | 50 | 165 | Yes |
| NI3K (ID 3) | 80 | — | No (calc) |

### Downstage Right (DSR)
Near audience, stage right. Mirror of DSL. BSW cross-beam from across the room
pairs well with the Sharpy at DSL for symmetrical looks.
Floor: X=3.5, Z=5.0

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 149 | 5 | Yes |
| BSW (ID 1) | 170 | 23 | Yes |
| Profile (ID 4) | 110 | 145 | Yes |
| NI3K (ID 3) | 176 | — | No (calc) |

### Upstage Left (USL)
Near back wall, left side. Sharpy home territory — shortest throw, tightest beam.
Good for punchy gobo projections on the wall behind the DJ.
Floor: X=0.8, Z=1.7

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 170 | 0 | Yes |
| BSW (ID 1) | 189 | 29 | Yes |
| Profile (ID 4) | 50 | 165 | Yes |
| NI3K (ID 3) | 80 | — | No (calc) |

### Upstage Right (USR)
Near back wall, right side. BSW home territory — shortest throw. Mirror of USL.
Floor: X=3.5, Z=1.7

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 149 | 5 | Yes |
| BSW (ID 1) | 170 | 23 | Yes |
| Profile (ID 4) | 110 | 145 | Yes |
| NI3K (ID 3) | 176 | — | No (calc) |

## Specials

### DJ Booth
Tight spot on the DJ position behind the decks. All movers converge on the back
wall where the performer stands. Use for "look at me" moments during builds and
transitions.
Floor: X=2.15, Z=0.5

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 142 | 3 | Yes |
| BSW (ID 1) | 196 | 25 | Yes |
| Profile (ID 4) | 95 | 107 | Yes |
| NI3K (ID 3) | 128 | — | — |

### Par Wall
Highlighting the right wall where the two Missyee pars are mounted. Movers converge
on the wall to layer beam effects with par wash. Creates depth when the pars and movers
are in contrasting colors.
Floor: X=4.2, Z=2.2

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 220 | 0 | No (calc) |
| BSW (ID 1) | 0 | 25 | No (calc) |
| Profile (ID 4) | 0 | 115 | No (calc) |

### Dance Floor
Center of the open dance area, slightly downstage of room center. All movers converge
on the heart of the dance space. Use for audience-facing wash looks and dance-centric
shows where the action is further from the DJ.
Floor: X=2.15, Z=4.2

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 158 | 6 | Yes |
| BSW (ID 1) | 179 | 27 | Yes |
| Profile (ID 4) | 64 | 145 | Yes |
| NI3K (ID 3) | 128 | — | — |

Notes: Very close to DSC values. All back movers tilt slightly forward from center;
Profile tilts more toward the audience. Good default position for dance-floor-centric
shows or when the energy should feel like it's "in the crowd."

### Disco Ball
All beams converge upward on a ceiling-mounted disco ball at room center. Creates
classic reflected light scatter when beams hit the ball. Use with tight beam (no frost,
no gobo) and saturated single colors for cleanest reflections.
Target: X=2.15, Y=4.5, Z=3.35

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 144 | 34 | Yes |
| BSW (ID 1) | 170 | 56 | Yes |
| Profile (ID 4) | 154 | 168 | Yes |
| NI3K (ID 3) | 128 | — | — |

Notes: Assumes a disco ball is mounted at ceiling center (X=2.15, Y=4.5, Z=3.35).
Pan values stay centered since the ball is directly above room center. Tilt values
push well outside normal forward-facing ranges — all movers aim significantly upward.
Verify ball position before use. Best with Sharpy beam mode (no frost) for tight
reflections. NI3K tilt heads should use position mode (low values, 0-30) for upward aim.

### Center Ceiling
All beams aimed at the ceiling above room center. Dramatic in haze — creates visible
shafts of light converging overhead. Best with tight gobos and saturated colors. The
three beams from different positions create a tent/pyramid effect.
Target: X=2.15, Y=4.9, Z=3.35

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 158 | 73 | Yes |
| BSW (ID 1) | 180 | 86 | Yes |
| Profile (ID 4) | 91 | 30 | Yes |
| NI3K (ID 3) | 128 | — | — |

Notes: Tilt values are well outside normal forward-facing ranges — all movers aim
significantly upward. Profile tilt=30 is far below its normal floor-facing range
(85-155), meaning it's aimed nearly straight up from its high front mount. Pair with
haze for maximum beam visibility.

## Effects

### Ceiling Hit
Same target as Center Ceiling special — all beams aimed at the ceiling above room
center. Listed here as an effect for sweep path reference.

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 158 | 73 | Yes |
| BSW (ID 1) | 180 | 86 | Yes |
| Profile (ID 4) | 91 | 30 | Yes |

### Back Wall Wash
All movers aimed at the back wall behind the DJ booth. Creates a color wash
backdrop. Works well with wide zoom/frost and no gobo. Especially effective when
the 4BAR is also washing the back wall in a contrasting color.

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 153 | 0 | No (calc) |
| BSW (ID 1) | 7 | 35 | No (calc) |
| Profile (ID 4) | 0 | 95 | No (calc) |

### Audience Blinder
All movers aimed at the audience area at eye level. USE SPARINGLY — brief
strobes during drops only. Never sustained. The Profile has the best angle for
this since it's front-mounted; the Sharpy and BSW shoot over heads from the back.

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 153 | 15 | No (calc) |
| BSW (ID 1) | 7 | 5 | No (calc) |
| Profile (ID 4) | 0 | 155 | No (calc) |

### Sweep Far Left
Extreme stage left for sweep endpoints. Beyond the normal performance area.
Use as the start or end of a sweep, never as a sustained position.

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 90 | 5 | No (calc) |
| BSW (ID 1) | 100 | 15 | No (calc) |
| Profile (ID 4) | 45 | 120 | No (calc) |

### Sweep Far Right
Extreme stage right. Mirror of Sweep Far Left.

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 220 | 5 | No (calc) |
| BSW (ID 1) | 0 | 15 | No (calc) |
| Profile (ID 4) | 0 | 120 | No (calc) |

## Sweep Paths

Pre-defined movement paths for chasers. Each path is a sequence of area/effect
positions that creates a specific visual movement.

| Path Name | Positions (in order) | Description | Best For |
|-----------|---------------------|-------------|----------|
| LR Sweep | Sweep Far Left → SL → C → SR → Sweep Far Right | Wide left-to-right sweep | Builds, breakdowns |
| RL Sweep | Sweep Far Right → SR → C → SL → Sweep Far Left | Wide right-to-left sweep | Builds, breakdowns |
| Narrow LR | SL → C → SR | Tight center sweep | Verses, low energy |
| Cross | USL → DSR then USR → DSL | X-pattern crossing beams | Drops, high energy |
| Front-Back | DSC → C → USC | Pull from audience toward DJ | Transitions, reveals |
| Back-Front | USC → C → DSC | Push toward audience | Builds before drop |
| Diamond | DSC → SR → USC → SL → DSC | Diamond shape sweep | Extended breakdowns |
| Spread | C → SL + SR (split) | Movers fan out from center | Drop hits |
| Converge | SL + SR → C (merge) | Movers pull into center | Build climax |
| Diagonal L | USR → C → DSL | Diagonal left sweep | Verse movement |
| Diagonal R | USL → C → DSR | Diagonal right sweep | Verse movement |

## Fixture Coverage & Blind Spots

Each mover has strengths and limitations based on where it's mounted. Use this to
choose which fixtures carry the lead for each position.

### Sharpy (ID 8) — Back Left, (0.5, 1.5, 0.3)
- **Strongest coverage**: USL (home territory, shortest throw, tightest beam)
- **Good coverage**: USC, SL, C, USR — anything upstage or center
- **Weakest coverage**: DSR (longest throw, widest beam spread, across entire room)
- **Behind the fixture**: Pan below 90 or above 220 aims at the back/left walls — not
  useful for audience-facing looks. Use only for deliberate wall wash effects.
- **Key advantage**: Long cross-room throws to DSR create dramatic diagonal beams in haze

### BSW (ID 1) — Back Right, (3.8, 1.5, 0.3)
- **Strongest coverage**: USR (home territory, shortest throw)
- **Good coverage**: USC, SR, C, USL — anything upstage or center
- **Weakest coverage**: DSL (longest throw, across entire room)
- **Behind the fixture**: Pan above 200 aims at the back/right walls.
- **Key advantage**: Mirrors the Sharpy — together they create symmetrical cross-beams

### Profile (ID 4) — Front Center, (2.1, 4.0, 6.5)
- **Strongest coverage**: DSC, DSL, DSR (closest positions, steepest downlight angle)
- **Good coverage**: C, SL, SR — mid-room positions
- **Weakest coverage**: USC, USL, USR (long throw backward, shallow angle)
- **Can't reach**: Tilt below 85 aims behind/above the fixture — never useful. Tilt
  above 155 aims too far past the audience area.
- **Key advantage**: Only front-facing fixture — the only mover that can light faces
  from the front. Essential for "spotlight" and "reveal" moments.

### NI3K (ID 3) — Back Wall, (1.3, 0.9, 0.3)
- **Coverage**: Pan sweeps are wide and dramatic. Best used for effects, not precision.
- **Limitation**: Tilts are per-head with rotation modes, not position presets. Don't
  try to focus NI3K tilt on specific floor positions — use LED effects and laser
  patterns instead.
- **Key advantage**: Lasers and multi-head LED effects fill the room with texture that
  the movers can't replicate.

## Safety Zones

| Zone | Why Avoid | Affected Fixtures | Pan Range | Tilt Range |
|------|-----------|-------------------|-----------|------------|
| Sharpy rear wall | Beam fires into back wall, not visible to audience | Sharpy (ID 8) | 0–89, 221–255 | any |
| BSW rear wall | Beam fires into back/right wall | BSW (ID 1) | 201–255 | any |
| Profile behind | Beam fires upward/behind, wasted light | Profile (ID 4) | any | 0–84 |
| Audience eye level (sustained) | Painful for audience, never hold more than 4 beats | All movers | (varies) | (varies) |

General guidance: brief audience blinder strobes (2-4 beats) during drops are fine.
Never sustain audience-aimed positions through an entire section. The Profile is the
most dangerous for blinding because it's front-mounted at eye level — its Audience
Blinder position (tilt=155) should only ever appear with strobe, never open shutter.

## Notes

- Values marked `(calc)` are calculated from geometry using known center reference
  values as anchors and linear interpolation from the spread/cross calibration
  points in showlib.py. They need hardware verification.
- When verified on the rig, update the Verified column to `Yes` and adjust values.
- Pan/Tilt values are DMX 0-255 as used in .qxw files.
- Stage Left/Right follow theatrical convention (performer's perspective facing audience).
- NI3K pan values are estimated proportionally. NI3K tilt is per-head and typically
  used as an effect parameter (rotation modes) rather than a static focus position.
- The Profile's safe tilt range (85-155) means it can't aim straight up or backward.
  Its best coverage is center-to-downstage.
- The Sharpy and BSW are both mounted at the back, so their downstage coverage
  requires longer throws. They're most precise at upstage positions.
- The Disco Ball special assumes a ball is mounted at ceiling center — verify
  physical location and update target coordinates if different. Best results with
  tight beams (no frost/gobo) and single saturated colors for clean reflections.
