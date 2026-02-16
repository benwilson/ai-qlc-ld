---
name: plot
description: "Venue fixture plot manager for placing, moving, and removing lighting fixtures in 3D space. Saves venue layouts as markdown to venue/<name>/plot.md. Use this skill whenever the user mentions: venue plot, fixture placement, fixture positions, room layout, adding/removing fixtures from a venue, stage plot, lighting plot, switching venues, or wants to visualize or document where fixtures are physically located in a space. Also trigger when the user says things like 'put the Sharpy on the back truss' or 'move the par cans to the front wall.'"
---

# Plot — Venue Fixture Plot Manager

Manage lighting fixture placement in 3D venue space. Each venue gets a `venue/<name>/plot.md` file that documents every fixture's physical location, orientation, and identity. The format is pure markdown — human-readable but structured enough that an AI can parse it into JSON for feeding into `showlib.py` or QLC+ workspace generation.

## When This Skill Activates

Any time the user wants to work with the physical layout of fixtures in a venue:

- "Add the Sharpy to back left truss at 3 meters"
- "Remove the Missyees from the plot"
- "Show me what's in the venue"
- "Create a new venue called basement"
- "Move the BSW to the other side of the room"
- "Switch to the main stage venue"

## Core Concepts

**Venue**: A named physical space (room, stage, club). Each venue has exactly one plot file at `venue/<name>/plot.md` relative to the project root. Multiple venues can exist simultaneously — the user picks which one they're working on.

**Fixture Entry**: A single fixture placed in the venue. Every entry has:

- **Name** (unique within the venue) — a human-friendly label like "Back Left Sharpy" or "DJ Booth Par 1"
- **Type** — the fixture model. Should match a known fixture from the rig when possible, but custom types are allowed for rentals, borrowed gear, or non-DMX items (see Fixture Types below).
- **Position** — XYZ coordinates in meters (X = left/right, Y = up/down, Z = front/back from DJ booth)
- **Orientation** — where the fixture is aimed or facing (free text, e.g. "aimed at floor center", "facing audience", "tilted 45° down")

**Coordinate System** (from DJ booth perspective, looking out at the room):

- **X**: 0 = left wall, positive = rightward
- **Y**: 0 = floor, positive = upward
- **Z**: 0 = back wall (where DJ is), positive = toward audience/front

## Plot File Format

The plot file at `venue/<name>/plot.md` uses this exact structure:

```markdown
# Venue: <Name>

<Optional 1-2 sentence description of the space.>

## Dimensions

| | Meters |
|---|--------|
| Width (X) | 5.0 |
| Depth (Z) | 5.0 |
| Height (Y) | 3.0 |

## Fixtures

| Name | Type | X (m) | Y (m) | Z (m) | Orientation |
|------|------|--------|--------|--------|-------------|
| Back Left Sharpy | Generic Sharpy Knockoff | 0.5 | 2.8 | 0.3 | Aimed at floor center |
| Back Right BSW | Generic Beam Spot Wash 3-in-1 | 4.2 | 2.8 | 0.3 | Aimed at floor center |
| Front Profile | Generic Profile Knockoff | 2.5 | 2.5 | 4.5 | Aimed backward at floor center |
| 4BAR | Chauvet 4BAR | 2.5 | 2.0 | 0.2 | Facing audience |
| Right Par 1 | Missyee 36 RGB LED | 0.2 | 1.5 | 2.5 | Facing center |
| Right Par 2 | Missyee 36 RGB LED | 0.2 | 1.5 | 3.0 | Facing center |
| Nausea Inducer | Generic Nausea Inducer 3000 | 2.5 | 2.8 | 2.5 | Centered |
```

The Dimensions section is optional — omit it if the user doesn't know or doesn't care about exact room size. When present, use it to sanity-check fixture coordinates (a fixture at X=6.0 in a 5m-wide room is probably wrong).

## Fixture Types

**Read known types from `showlib.py`** by checking the `FIXTURE_DEFS` list. This keeps the plot in sync with the actual rig without hardcoding a fixture list in this skill. The current rig's `FIXTURE_DEFS` contains manufacturer, model, and name fields — use the model name as the Type string in the plot.

When the user refers to fixtures casually ("the sharpy", "a par can", "the flower thing"), match to the closest fixture in `FIXTURE_DEFS`. If ambiguous, ask.

**Custom fixture types are allowed.** If the user places a fixture that isn't in `FIXTURE_DEFS` (rental gear, borrowed equipment, non-DMX items like a hazer or strobe), accept whatever type string they give. Note it with a brief mention so it's clear it's not part of the standard rig — for example, just use the type string as-is: "Rental - Martin Rush MH6" or "ADJ Fog Fury 3000". No need for special markup, the non-standard name makes it obvious.

## Operations

### Creating a New Venue

When the user wants a new venue:

1. Ask for the venue name (if not provided). Sanitize it for use as a directory name (lowercase, hyphens for spaces).
2. Ask about the room — rough dimensions and shape are helpful but not required. If provided, add the Dimensions table.
3. Create the full venue directory structure:
   - `venue/<name>/plot.md` — the fixture plot
   - `venue/<name>/shows/` — workspace files for this venue
   - `venue/<name>/shows/notes/` — show design notes
   - `venue/<name>/generators/` — generator scripts for this venue
4. After adding fixtures, run `generate_venue_template(venue_dir)` from showlib.py to create a `Template-Base.qxw` with the venue's fixtures.

If the user gives fixture placements in the same breath, add them immediately.

### Adding a Fixture

When the user wants to place a fixture:

1. **Name**: If not provided, suggest one based on position + type (e.g. "Back Left Sharpy"). Names must be unique within the venue.
2. **Type**: Match to a known fixture from `FIXTURE_DEFS` when possible. Accept custom types for non-rig gear.
3. **Position**: If the user gives spatial descriptions ("back left corner, up high"), convert to XYZ coordinates using the venue dimensions as reference. If dimensions are known, sanity-check that the position falls within the room. Ask if the position is ambiguous.
4. **Orientation**: Default to "Aimed at floor center" for movers, "Facing audience" for static pars/bars. Accept whatever the user specifies.

Add the row to the fixtures table. Keep rows ordered by Z (back to front), then X (left to right) for readability.

### Removing a Fixture

Match by name (case-insensitive, partial match OK if unambiguous). Remove the row from the table. If the match is ambiguous ("remove the par" when there are multiple pars), list the options and ask.

### Moving a Fixture

Update the position and/or orientation of an existing fixture. This is just an edit to the table row — find by name, update the changed fields.

### Listing / Reviewing

When the user asks what's in the venue, read the plot file and present it. If they ask about a specific fixture, pull that row.

### Switching Venues

Multiple venues can coexist under `venue/`. There's no "active venue" state — just ask the user which venue they mean when it's ambiguous.

When the user says "add a par" without specifying a venue:
- If only one venue exists, use it.
- If multiple venues exist, ask which one.

To list available venues, check subdirectories under `venue/`.

## Interactive Placement Mode

When the user is placing fixtures without giving specific coordinates, walk through it conversationally:

1. "Where in the room?" — get a spatial description
2. Convert to approximate XYZ based on venue dimensions (if known) or reasonable defaults
3. State what you're setting: "I'll put that at X=0.5, Y=2.8, Z=0.3 — back left corner, near ceiling height. Sound right?"
4. "Where is it aimed?" — get orientation
5. Confirm and add

For direct instructions like "add the Sharpy at 0.5, 2.8, 0.3 aimed at center" — just do it, no need to walk through each field.

## Important Notes

- The `venue/` directory lives at the project root (same level as `fixtures/`, `showlib.py`).
- Each venue is a self-contained subdirectory with its own plot, shows, notes, and generators:
  ```
  venue/<name>/
  ├── plot.md          # Fixture positions
  ├── shows/           # .qxw workspace files
  │   └── notes/       # Show design notes
  └── generators/      # Python show generator scripts
  ```
- Always read the existing plot file before modifying it — don't clobber existing fixtures.
- When multiple fixtures of the same type exist, the unique name is what distinguishes them (not QLC+ IDs — those are a show concern, not a plot concern).
- The plot is about physical placement only. DMX addresses, channel modes, and QLC+ IDs are handled elsewhere (showlib.py, workspace files). Don't include them in the plot.
