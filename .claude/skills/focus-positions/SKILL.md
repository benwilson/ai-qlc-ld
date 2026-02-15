---
name: focus-positions
description: >
  Focus position management for QLC+ venues. Creates and updates venue focus position
  files (venue/<name>/focus-positions.md) that define named pan/tilt targets for every
  moving fixture in a venue. Use this skill whenever the user mentions focus positions,
  focusing fixtures, aiming movers, creating position presets, stage positions, or
  wants to define where fixtures should point. Also trigger when building a show and
  no focus-positions.md exists yet — focus positions are essential for creating
  musically coherent shows with intentional movement. If a show generator references
  positions like "front left" or "audience wash" and there's no focus-positions.md,
  trigger this skill first.
---

# Focus Positions

Create and manage focus position files for QLC+ venues. A focus position is a named
pan/tilt target that tells each moving fixture where to aim for a specific stage look.

Focus positions are the backbone of intentional lighting design. Without them, show
generators guess at pan/tilt values and movements feel random. With them, every mover
sweep traces a deliberate path between meaningful locations.

## Why Focus Positions Matter

In professional lighting, designers "focus" each fixture before the show — aiming it
at a specific spot on the stage and recording those values. Moving lights store these
as **palettes** or **presets** that get reused across hundreds of cues. The same idea
applies here: define the positions once, reference them everywhere.

Benefits for show generation:
- **Consistent movement**: Sweeps go between real locations, not arbitrary DMX values
- **Fixture coordination**: All movers aim at the same spot when "center" is called
- **Meaningful choreography**: "Slow sweep from DSL to DSR" maps to actual geometry
- **Easier iteration**: Change a position once, every show that references it updates

## When to Use

- User says "focus," "positions," "aim," "point at," "presets," or similar
- Building a new show and no `focus-positions.md` exists for the venue
- User wants to add new positions (e.g., a "DJ booth special" or "back wall wash")
- User asks to recalibrate or verify existing focus positions
- A show generator needs position data beyond the basic center/spread/cross

## Concepts

### Position Categories

Focus positions are organized into categories that reflect how lighting designers think:

**Areas** — The stage grid. Standard 9-point grid adapted to the venue's geometry.
These are your bread and butter for general coverage.
- Downstage (DS), Center (C), Upstage (US) combined with Left (L), Center (C), Right (R)
- Adapted from theatrical convention: "Stage Left" = performer's left facing audience
- Small venues may only need 4-6 areas; large stages might use 12+

**Specials** — Purpose-driven focus points for specific moments or objects.
- DJ booth, mic stand, prop table, entrance, feature wall
- Named by their purpose, not their grid position
- The most creative category — these define the venue's personality

**Effects** — Positions chosen for visual impact rather than illumination.
- Audience blinder, ceiling hit, floor sweep start/end, back wall wash
- Often used in pairs (sweep from A to B) or as momentary reveals
- Include extreme angles that wouldn't work for general lighting

**Safety** — Positions that should never be used (audience eye level, camera positions).
Document these to prevent accidental blinding during programming.

### Position Data

Each position stores the pan/tilt values that make every moving fixture aim at the
same physical point. Because fixtures are mounted at different locations and angles,
the same "floor center" position requires different DMX values for each fixture.

**Required per position:**
- Name (human-readable, used in show generators)
- Category (area / special / effect / safety)
- Description (what it looks like, when to use it)
- Pan/Tilt for each mover (DMX values, 0-255)

**Optional:**
- Floor coordinates (X, Z in meters — where the beam hits the floor)
- Verified flag (tested on hardware vs. calculated)
- Notes (e.g., "BSW gobo looks great here", "avoid with frost on")

## Workflow

### 1. Identify the Venue

Ask the user which venue to work with if not obvious. Read these files:
- `venue/<name>/plot.md` — fixture positions, room dimensions
- `venue/<name>/patch.md` — which fixtures are movers, their IDs and channel counts

### 2. Identify the Movers

From the patch and the channel maps in CLAUDE.md, identify which fixtures have
pan/tilt control. These are the only fixtures that get focus position entries.
Static fixtures (pars, 4BAR) don't need focus positions since they can't move.

### 3. Load or Create focus-positions.md

Check if `venue/<name>/focus-positions.md` exists.

- **Exists**: Read it, show the current positions, ask what the user wants to change.
- **Doesn't exist**: Start the focusing workflow from scratch (step 4).

### 4. Define Area Positions

Start with the standard stage grid, adapted to the venue's room dimensions:

1. **Map the performance area.** Using `plot.md` dimensions, identify the usable floor
   space. For a small studio, this might be a 3m x 4m rectangle. For a club, it could
   be the whole dance floor.

2. **Choose grid density.** Small rooms need fewer positions — a 3x2 grid (6 areas)
   often works better than a full 3x3. Ask the user or suggest based on room size:
   - Under 20 sqm: 4 positions (DS-L, DS-R, US-L, US-R) + center
   - 20-50 sqm: 6-9 positions (standard grid)
   - Over 50 sqm: 9-12 positions (expanded grid with mid-points)

3. **Calculate pan/tilt values.** For each area position and each mover:
   - Use the fixture's physical position from `plot.md`
   - Use the known center reference values from CLAUDE.md as anchor points
   - Extrapolate pan/tilt for other positions based on relative geometry
   - Mark calculated values as `(calc)` — they need hardware verification

4. **Present the grid visually.** Show the user an ASCII representation of the
   positions overlaid on the room, so they can verify the layout makes sense.

### 5. Define Specials

Generate sensible default specials based on what's in the venue's `plot.md`. Every
venue gets these if the geometry supports them:

- **DJ Booth / Performer position** — infer from plot.md (usually near the back wall
  or wherever the booth/desk is noted). If plot.md mentions a DJ booth, use its
  coordinates. Otherwise place it at center-upstage (X=center, Z near back wall).
- **Par Wall / Wash Wall** — if static fixtures (pars, 4BAR) are mounted on a wall,
  create a special that aims movers at that wall for layered looks.

Additional specials to include if the venue layout suggests them:
- **Entrance** — if plot.md mentions a door or entry point
- **Feature wall / backdrop** — any wall called out in plot.md as visually significant

After generating defaults, offer the user the chance to add, remove, or adjust:
"I've included these specials based on your venue layout. Want to add any others
or adjust these?"

### 6. Define Effects

Generate a standard set of effect positions for every venue. These are universal —
every venue benefits from having them available, so include all of them by default:

- **Audience blinder** — movers aimed at audience eye level (use sparingly in shows)
- **Ceiling hit** — beams as close to vertical as safe tilt ranges allow
- **Back wall wash** — movers aimed at the rear wall for color wash backdrop
- **Sweep Far Left / Sweep Far Right** — extreme pan endpoints for wide sweeping
  movements, beyond the normal performance area

Additional effects to include if venue geometry supports them:
- **Side wall wash** — if movers can reach side walls at reasonable angles
- **Floor pool** — tight downward angle for dramatic pools (mainly useful for
  front-mounted fixtures with steep throw angles)

After generating, offer the user the option to adjust: "I've included these standard
effect positions. Want to modify any or add venue-specific ones?"

### 7. Document Fixture Coverage & Blind Spots

Generate this section automatically by analyzing each mover's mount position relative
to the performance area. For each mover, write:

- **Strongest coverage**: Which area positions are closest / best angle (home territory)
- **Good coverage**: Positions it can reach well
- **Weakest coverage**: Farthest positions, longest throws, widest beam spread
- **Behind the fixture**: What pan/tilt ranges aim away from the performance area
  (at walls, ceiling, behind the mount). Express as DMX ranges to avoid. Derive these
  from the safe pan/tilt ranges in the Movers table — anything outside the safe range
  is "behind."
- **Key advantage**: What this fixture does better than the others (cross-room beams,
  front-face lighting, texture effects, etc.)

This analysis is critical for show generators — it tells them which fixture should
"lead" at each position and which ranges produce wasted or dangerous light.

No user input needed — this is purely derived from geometry.

### 8. Define Safety Zones

Generate automatically from the fixture coverage analysis. For each mover, the
pan/tilt ranges that fall outside the safe forward-facing range become a safety zone
row. Always include:

- One row per fixture for "behind the fixture" ranges (derived from safe pan/tilt bounds)
- One row for "Audience eye level (sustained)" covering all movers, noting the 4-beat
  max duration rule
- Note which fixture is most dangerous for audience blinding based on mount position
  (front-mounted fixtures are worse than back-mounted ones)

After generating, offer the user the option to add venue-specific zones: "I've
generated safety zones from fixture geometry. Any additional zones to avoid? (cameras,
projector screens, mirrors, etc.)"

### 9. Write focus-positions.md

Save to `venue/<name>/focus-positions.md` using the format below.

## focus-positions.md Format

```markdown
# Focus Positions: <Venue Name>

Source: venue/<name>/plot.md
Generated: <YYYY-MM-DD>

## Movers

Fixtures with pan/tilt control in this venue:

| Name | ID | Type | Mount Position |
|------|----|------|----------------|
| Back Left Sharpy | 8 | Sharpy Knockoff | (0.5, 1.5, 0.3) |
| Back Right BSW | 1 | BSW 3-in-1 | (3.8, 1.5, 0.3) |
| Front Center Profile | 4 | Profile Knockoff | (2.1, 4.0, 6.5) |

## Performance Area

Brief description of the usable stage/performance space and how positions are laid
out relative to the room.

## Areas

Standard stage grid positions.

### Center (C)
The default home position. All movers converge on floor center.
Floor: X=2.1, Z=3.3

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 153 | 0 | Yes |
| BSW (ID 1) | 7 | 19 | Yes |
| Profile (ID 4) | 0 | 123 | Yes |

### Downstage Left (DSL)
Near audience, stage left. Good for solo moments or entrance highlights.
Floor: X=0.8, Z=5.0

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| Sharpy (ID 8) | 180 | 10 | No (calc) |
| BSW (ID 1) | 40 | 25 | No (calc) |
| Profile (ID 4) | 30 | 110 | No (calc) |

(... more positions ...)

## Specials

### DJ Booth
Tight spot on the DJ position behind the decks.
Floor: X=2.1, Z=0.5

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| ... | ... | ... | ... |

(... more specials ...)

## Effects

### Ceiling Hit
All beams straight up — dramatic in haze.

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| ... | ... | ... | ... |

### Audience Blinder
All movers aimed at audience. Use sparingly and briefly.

| Fixture | Pan | Tilt | Verified |
|---------|-----|------|----------|
| ... | ... | ... | ... |

(... more effects ...)

## Sweep Paths

Pre-defined movement paths for chasers. Each path is a sequence of positions
that creates a specific visual movement when played as a chaser.

| Path Name | Positions (in order) | Description |
|-----------|---------------------|-------------|
| LR Sweep | DSL → C → DSR | Slow left-to-right audience sweep |
| Cross | USL → DSR, USR → DSL | Movers cross in an X pattern |
| Front-Back | DSC → C → USC | Pull from audience toward back wall |
| Circle CW | DSL → DSC → DSR → SR → USR → USC → USL → SL | Full clockwise sweep |
| Narrow Sweep | SL → C → SR | Tight center sweep |

## Fixture Coverage & Blind Spots

For each mover, document mount position strengths, weaknesses, blind spots, and
what pan/tilt ranges aim behind the fixture (wasted light). Include key advantages
that make each fixture unique.

### <Fixture Name> — <Mount Description>
- **Strongest coverage**: <positions>
- **Good coverage**: <positions>
- **Weakest coverage**: <positions>
- **Behind the fixture**: <pan/tilt ranges that aim away from performance area>
- **Key advantage**: <what this fixture does best>

(... repeat for each mover ...)

## Safety Zones

| Zone | Why Avoid | Affected Fixtures | Pan Range | Tilt Range |
|------|-----------|-------------------|-----------|------------|
| <name> | <reason> | <fixture> | <range> | <range> |

Include general guidance on audience-facing position duration limits and which
fixtures are most dangerous for blinding based on mount angle.

## Notes

- Values marked `(calc)` are calculated from geometry and need hardware verification.
  When verified on the rig, update the Verified column to `Yes`.
- Pan/Tilt values are DMX 0-255 as used in .qxw files (0-indexed).
- Stage Left/Right follow theatrical convention (performer's perspective facing audience).
- Sweep paths reference position names from the Areas and Effects sections.
```

## Calculating Pan/Tilt from Geometry

When you don't have hardware-verified values, estimate pan/tilt from fixture positions
and known reference points. The approach:

1. **Anchor on center.** Every venue's `Center` position should be verified first
   (these are the center reference values in CLAUDE.md). All other positions are
   calculated relative to center.

2. **Estimate proportionally.** If you know center and one extreme (e.g., from
   `movers_spread()` or `movers_cross()` in showlib.py), interpolate for positions
   between them. The relationship isn't perfectly linear (it depends on throw
   distance and mounting angle), but it's close enough for initial programming.

3. **Respect fixture limits.** Check CLAUDE.md for safe pan/tilt ranges that keep
   movers forward-facing. Stay within those bounds for area positions.

4. **Mark everything as unverified.** Calculated values are starting points. The
   user should verify on the actual rig and update the file.

## Modifying Existing Positions

When the user wants to change focus positions:

1. Read the current `focus-positions.md`.
2. Ask what they want to change (add position, adjust values, verify a calc, add a path).
3. For new positions, calculate pan/tilt for all movers and present for confirmation.
4. Rewrite `focus-positions.md` with the updated data.

## Integration with showlib.py

When focus positions exist, show generators should reference them by name rather than
hardcoding pan/tilt values. This is the recommended pattern in generators:

```python
# Instead of:
sharpy(pan=180, tilt=10)  # What is this position?

# Reference the focus positions doc:
# DSL position (from focus-positions.md): Sharpy pan=180, tilt=10
sharpy(pan=180, tilt=10)  # DSL — solo moment
```

The position names in comments make generators self-documenting and maintainable.
When positions get re-verified on hardware, you only update focus-positions.md and
then update the generator values to match.

## Notes

- Focus positions complement the patch — patch says what's connected, focus positions
  say where everything points.
- Always read `plot.md` first for room geometry. The physical layout determines what
  positions are reachable by each fixture.
- The NI3K has pan but its tilts are per-head with rotation modes (0-127 position,
  128-191 fwd rotation, 192-255 rev rotation). Document NI3K pan positions but note
  that tilt is typically handled as an effect rather than a focus position.
- For fixtures with Pan Fine / Tilt Fine channels, focus-positions.md stores only the
  coarse values (the main pan/tilt channels). Fine adjustment happens during hardware
  verification.
