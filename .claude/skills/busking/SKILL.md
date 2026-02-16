---
name: busking
description: >
  Busking workspace generator for QLC+ Virtual Console. Creates venue-specific busking
  workspaces with color palettes, position presets, movement effects, strobes, and
  special moment buttons — all organized for real-time improvised lighting control during
  live DJ sets. Use this skill whenever the user mentions busking, live lighting, improvised
  lighting, DJ lighting, live console, or wants to create a workspace for controlling
  lights on the fly without pre-programmed cues.
---

# Busking

Generate a complete QLC+ busking workspace for live, improvised lighting control during
DJ sets. The workspace provides layered control over colors, positions, effects, intensity,
strobes, and special moments — all accessible through the Virtual Console for real-time
operation.

## When to Use

- User says "busking," "busk," "live lighting," or "improvised lighting"
- User wants to control lights live during a DJ set (no pre-programmed cues)
- User asks for a "busking page," "busking layout," or "busking workspace"
- User wants buttons/faders for on-the-fly lighting control

## Philosophy

Busking is the art of creating live lightshows in real time, reacting to the music without
pre-programmed cues. The key principles from professional lighting designers:

1. **Layered control**: Independently mix colors, positions, effects, and intensity — don't
   trigger "whole looks." This gives maximum flexibility with minimum buttons.
2. **Two-color technique**: Most busking colors are two-color pairs (movers one color, pars
   another, then swap on tap). This creates variety from a small set of buttons.
3. **Home state**: Always have a good-looking base state you can snap back to instantly.
4. **Restraint = impact**: The drops hit hardest when breakdowns are dark. Save the biggest
   effects for the biggest moments.
5. **Contrast over complexity**: A sudden blackout → strobe is more dramatic than having
   everything on at once.

## Prerequisites

Before generating a busking workspace, you need:

1. **Venue**: Ask which venue. Read `venue/<name>/plot.md` for fixtures and layout.
2. **Patch**: Read `venue/<name>/patch.md` for fixture IDs, addresses, and channel counts.
3. **Focus positions**: Read `venue/<name>/focus-positions.md` for named mover positions.
4. **Genre**: Ask which genre(s). Read `genres/<genre>.md` for color palettes, timing, and conventions.
5. **Mood** (optional): Ask if the user wants a mood applied. Read `moods/<mood>.md` for
   abstract modifiers that shape how the genre's values get applied.

If focus-positions.md doesn't exist, trigger the **focus-positions** skill first.
If patch.md doesn't exist, trigger the **patch** skill first.

## Moods

Moods are abstract modifiers that shape how a genre's concrete values get applied. They
define **what feeling** to create, while genres define **what rules** to follow. The busking
skill combines them: genre provides the raw palette and timing, mood filters and adjusts.

There are two categories of moods:

**Emotional states**: Dark, Ethereal, Aggressive, Hypnotic, Euphoric, Melancholic, Chaotic, Intimate
**Energy levels**: Chill, Building, Peak, Comedown

Moods are optional. If no mood is specified, the genre's default conventions apply unmodified.

### How to Apply a Mood

Each mood file defines modifiers in these categories:

1. **Visual References** — 3 evocative reference images for creative alignment
2. **Color Scheme** — formal scheme type (monochromatic, complementary, analogous, triadic,
   split-complementary) that guides color pair selection
3. **Color Filtering** — temperature bias, saturation preference, palette selection rules,
   max simultaneous colors, par behavior override
4. **Intensity Modifiers** — base brightness scaling, contrast ratio, blackout frequency,
   fixture count, dimmer range
5. **Movement Modifiers** — speed multiplier, width preference, movement style, hold time
   scaling, preferred positions
6. **Effect Density** — strobe/laser/gobo/prism/frost usage levels
7. **Timing Modifiers** — fade speed scaling, hold duration scaling, chase speed scaling
8. **Energy Curve** — baseline energy, peak scaling, rise/fall time, sustain behavior
9. **Phases** *(optional)* — 2–4 internal progression stages for moods that evolve over time

When generating a busking workspace with a mood:

1. Read the genre file first — extract concrete values (RGB colors, timing ms, BSW/Sharpy
   wheel values).
2. Read the mood file — extract abstract modifiers.
3. Apply modifiers to genre values:
   - **Color scheme type**: Use the mood's Color Scheme type to determine which genre pairs
     to include. Monochromatic moods → single-color washes only (filter out two-color pairs).
     Complementary → prefer high-contrast opposing pairs. Analogous → prefer adjacent-hue
     pairs. Triadic → include the widest variety of pairs. Split-complementary → one anchor
     color with two near-opposite accents.
   - **Color filtering**: From the filtered pairs, further narrow by the mood's temperature
     bias and preferred colors. If the mood says "prefer cool," drop any pair that uses
     warm colors.
   - **Intensity**: Multiply the genre's default dimmer values by the mood's base brightness
     percentage. Apply the mood's dimmer range (e.g., mood says 30–60% = cap dimmers at 153).
   - **Movement**: Multiply the genre's timing preset fade/hold values by the mood's speed
     multiplier. Select sweep paths that match the mood's width preference.
   - **Effects**: Include/exclude strobe, laser, gobo, prism buttons based on mood's density
     levels (none/rare/moderate/heavy).
   - **Timing**: Multiply all fade/hold timing by the mood's scaling factors.

4. The mood's Genre Interaction Notes section may have specific overrides for the chosen
   genre combination. Always check and apply these.
5. If the mood has **Phases**, generate phase-specific "look" buttons (e.g., for a Building
   mood: "GATHERING", "RISING", "CRESTING") that apply the phase's modifier adjustments on
   top of the base mood settings.

### Mood Buttons in the VC

If a mood is specified, add a "Mood" section to the VC with buttons for the mood's
typical energy levels. For example, if the mood is "Dark":

- **DARK LOW**: Apply mood at minimum energy (single fixture, minimal color)
- **DARK MID**: Apply mood at medium energy (2–3 fixtures, moderate)
- **DARK HIGH**: Apply mood at the mood's peak scaling (full dark treatment)

These are essentially pre-built "looks" that combine the genre palette with the mood's
modifiers at different intensity levels, giving the operator quick access to mood-appropriate
looks without having to manually combine layers.

## Workflow

### 1. Gather Requirements

Ask the user:
- Which venue?
- Which genre(s)? (determines color palettes, timing presets, conventions)
- Which mood? (optional — modifies how genre values are applied)
- Target BPM? (or use genre default)
- Any additional fixtures or custom requirements?

### 2. Read Source Files

Read all of these:
- `venue/<name>/plot.md` — fixture positions and layout
- `venue/<name>/patch.md` — DMX addressing
- `venue/<name>/focus-positions.md` — named positions with per-mover pan/tilt values
- `genres/<genre>.md` — color palette, timing presets, conventions
- `moods/<mood>.md` — mood modifiers (if mood specified)
- `showlib.py` — available fixture helpers and constants

### 3. Plan the Button Layout

A busking workspace is organized into these **layers** (each layer is independent):

#### Layer 1: Color Palette (Solo Frame)
Two-color scenes from the genre file. Each button sets ALL fixtures to a two-color combo
(movers get color A, pars get color B). Tapping a second time swaps A and B.

Implementation: For each two-color pair from the genre, create TWO scenes:
- Scene A: Movers in color A, pars in color B
- Scene B: Movers in color B, pars in color A

Put each pair as a 2-step chaser (Loop, instant snap) on a button. Place all color buttons
in a Solo Frame so only one color combo is active at a time.

**Fixture color mapping for two-color scenes:**
- BSW: Use BSW color wheel value (ch8) — find closest match from BSW_WHITE/RED/ORANGE/etc.
- Sharpy: Use Sharpy color macro (ch8) — find closest match from SHARPY_WHITE/RED/etc.
- Profile: Use Profile color wheel (ch5) — find closest match from PROF_WHITE/RED/etc.
- 4BAR: Use RGB values directly (ch3-14)
- Missyee pars: Use RGB values directly (ch1-3)
- NI3K: Use RGBW channels (ch7-10) + halo LED color (ch17, H_RED/GRN/BLU/etc.)

For "Color A = movers, Color B = pars":
- Sharpy, BSW, Profile → Color A (wheel values)
- 4BAR, Missyee 1, Missyee 2 → Color B (RGB values)
- NI3K → Color A (RGB) + matching halo

Also include single-color washes:
- "ALL WHITE" — every fixture white, full intensity
- "ALL [primary color]" — every fixture in the genre's primary colors

#### Layer 2: Position Presets (Solo Frame)
One button per named focus position from `focus-positions.md`. Each button sets mover
pan/tilt values for that position (doesn't change color, intensity, or effects).

Read the focus-positions.md tables and create scenes with ONLY pan/tilt values for each
mover. Use the exact Pan and Tilt values from the tables.

**Position scenes should set:**
- Sharpy: ch0 (pan), ch1 (tilt) — and safe defaults for other channels
- BSW: ch0 (pan), ch2 (tilt) — and safe defaults for other channels
- Profile: ch2 (pan), ch3 (tilt) — and safe defaults for other channels
- NI3K: ch0 (pan) only (tilt is per-head, leave as effect parameter)

Include ALL area positions (C, DSC, USC, SL, SR, DSL, DSR, USL, USR), specials (DJ Booth,
Par Wall, etc.), and effects positions (Ceiling Hit, Back Wall Wash, Audience Blinder).

Place in a Solo Frame so only one position is active at a time.

#### Layer 3: Movement Effects
Chasers that cycle movers through positions from the Sweep Paths table. Each sweep path
becomes a chaser where each step is a scene with mover positions for that waypoint.

Read the Sweep Paths from focus-positions.md and create chasers for each path:
- Each step = scene with mover pan/tilt for that waypoint position
- Timing: Use smooth crossfade from the genre's timing presets (e.g., 2-bar or 4-bar smooth)
- RunOrder: PingPong for sweeps, Loop for circular paths

Include a Speed Dial widget (or multiple timing buttons) to adjust sweep speed live.

Also include "static" movement effects:
- **Slow Drift**: 16-bar PingPong between two nearby positions (e.g., SL ↔ SR)
- **Wide Sweep**: Full LR Sweep at 8-bar speed
- **Tight Sweep**: Narrow LR at 4-bar speed

#### Layer 4: Intensity Masters (Sliders)
Faders to control brightness of fixture groups independently:

| Fader | Controls | Purpose |
|-------|----------|---------|
| MOVERS | Sharpy + BSW + Profile dimmer channels | Bring movers in/out |
| PARS | 4BAR master + Missyee masters | Bring pars in/out |
| NI3K | NI3K dimmer | Bring NI3K in/out |
| MASTER | All dimmers | Overall intensity (Grand Master backup) |

Implementation: These are best done as QLC+ slider widgets controlling scene intensity or
as submaster-style controls. In QLC+ VC, use Slider widgets with Function type set to
control the appropriate scenes.

#### Layer 5: Strobe & Flash (Buttons)
Based on genre conventions:

| Button | Action | Implementation |
|--------|--------|----------------|
| STROBE ALL | All fixtures strobe at genre-appropriate speed | Scene with all strobe channels active |
| STROBE MOVERS | Only mover strobes (Sharpy ch6, BSW ch16) | Scene with mover strobe channels |
| STROBE PARS | Only par strobes (4BAR ch2, Missyee ch4) | Scene with par strobe channels |
| FLASH WHITE | Momentary bump to full white (all fixtures) | Flash button, momentary action |
| BUMP | Quick bump to current color at full (momentary) | Flash button |

Strobe scenes should set the strobe channels to the appropriate speed value:
- Sharpy: ch6 = SHARPY_STROBE_MED (64) for medium, SHARPY_STROBE_FAST (120) for fast
- BSW: ch16 = BSW_SHUT_STROBE_SLOW (20) for slow, BSW_SHUT_STROBE_FAST (128) for fast
- 4BAR: ch2 = 128 for medium strobe
- Missyee: ch4 = 128 for medium strobe
- NI3K: ch6 = 128 for medium strobe

#### Layer 6: Special Moments (Buttons)
These are "one-tap dramatic effect" buttons:

| Button | What it does | When to use |
|--------|-------------|-------------|
| BLACKOUT | All fixtures to zero | Between tracks, dramatic pauses |
| WHITEOUT | All fixtures full white, full intensity | Drop hits, maximum impact |
| LASERS ON | NI3K all lasers on (rl=250, gl=250, bl=250) | Drops, reveals |
| LASERS STROBE | NI3K lasers strobing | Peak moments |
| LASERS OFF | NI3K all lasers off | End of drops, transitions |
| PRISM CHAOS | All movers: prism on + rotation | Drop accents, brief chaos |
| GOBO TEXTURE | All movers: gobo on (genre-appropriate) | Builds, atmosphere |
| OPEN BEAM | All movers: gobo off, prism off, frost off | Clean looks, resets |
| AUDIENCE BLINDER | Movers to audience position + strobe | Briefest drop moments ONLY |

#### Layer 7: Genre Quick-Select (Optional, if multiple genres)
If the user selected multiple genres, include buttons to swap the active color palette.
Each genre button reconfigures the color Solo Frame to that genre's two-color pairs.

Implementation: This is complex in QLC+ — the simplest approach is to generate separate
color button sets in different Solo Frames and collapse the inactive ones.

### 4. Generate the Python Script

Create a generator script at `venue/<name>/generators/Busking-<Genre>.py` that uses
showlib.py to build the workspace. The script should:

1. Import from showlib
2. Parse focus-positions.md programmatically to extract position data
3. Build all scenes for each layer
4. Build chasers for sweep paths
5. Build VC layout with:
   - Solo Frames for colors and positions
   - Regular Frames for effects, strobes, specials
   - Sliders for intensity masters
   - Speed Dials for timing control
6. Write workspace to `venue/<name>/shows/Busking-<Genre>.qxw`

#### Generator Structure Template

```python
#!/usr/bin/env python3
"""
Busking workspace generator for [Venue] - [Genre]
Generated by busking skill

Run from project root:
    python3 "venue/<name>/generators/Busking-<Genre>.py"
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from showlib import *

# =============================================================================
# CONFIGURATION
# =============================================================================
VENUE = "venue/<name>"
GENRE = "<genre>"
BPM = <bpm>
OUTPUT = f"{VENUE}/shows/Busking-{GENRE}.qxw"

# =============================================================================
# PARSE FOCUS POSITIONS from focus-positions.md
# =============================================================================
def parse_focus_positions(venue_dir):
    """Parse focus-positions.md and return dict of position_name -> fixture_values."""
    fp_path = os.path.join(venue_dir, "focus-positions.md")
    with open(fp_path) as f:
        content = f.read()

    positions = {}
    current_position = None

    # Find each ### heading and its table
    for match in re.finditer(
        r'###\s+(.+?)\n.*?\n\|.*?\n\|.*?\n((?:\|.*?\n)*)',
        content, re.DOTALL
    ):
        pos_name = match.group(1).strip()
        table_rows = match.group(2).strip()

        fixture_vals = {}
        for row in table_rows.split('\n'):
            cells = [c.strip() for c in row.split('|')[1:-1]]
            if len(cells) >= 4:
                fixture_name = cells[0]
                pan_str = cells[1]
                tilt_str = cells[2]

                # Skip entries with — (NI3K tilt)
                pan = int(pan_str) if pan_str.isdigit() else None
                tilt = int(tilt_str) if tilt_str.isdigit() else None

                if 'Sharpy' in fixture_name:
                    fixture_vals['sharpy'] = {'pan': pan, 'tilt': tilt}
                elif 'BSW' in fixture_name:
                    fixture_vals['bsw'] = {'pan': pan, 'tilt': tilt}
                elif 'Profile' in fixture_name:
                    fixture_vals['profile'] = {'pan': pan, 'tilt': tilt}
                elif 'NI3K' in fixture_name:
                    fixture_vals['ni3k'] = {'pan': pan}

        positions[pos_name] = fixture_vals

    return positions

POSITIONS = parse_focus_positions(VENUE)

# =============================================================================
# HELPER: Create a position-only scene for movers
# =============================================================================
def position_scene(name, pos_name, path="Busking/Positions"):
    """Create a scene that only sets mover positions from focus-positions.md."""
    pos = POSITIONS.get(pos_name, POSITIONS.get("Center (C)", {}))
    fixtures = []

    s = pos.get('sharpy', {})
    if s.get('pan') is not None and s.get('tilt') is not None:
        fixtures.append(sharpy(pan=s['pan'], tilt=s['tilt']))
    elif s.get('pan') is not None:
        fixtures.append(sharpy(pan=s['pan']))

    b = pos.get('bsw', {})
    if b.get('pan') is not None and b.get('tilt') is not None:
        fixtures.append(bsw(pan=b['pan'], tilt=b['tilt']))

    p = pos.get('profile', {})
    if p.get('pan') is not None and p.get('tilt') is not None:
        fixtures.append(profile(pan=p['pan'], tilt=p['tilt']))

    n = pos.get('ni3k', {})
    if n.get('pan') is not None:
        fixtures.append(ni3k(pan=n['pan']))

    return scene(name, *fixtures, path=path)

# =============================================================================
# LAYER 1: COLOR PALETTE
# Build two-color scenes from genre definition
# =============================================================================
# ... [Insert genre-specific color scenes here] ...

# =============================================================================
# LAYER 2: POSITION PRESETS
# One scene per focus position
# =============================================================================
# ... [Insert position scenes here using position_scene()] ...

# =============================================================================
# LAYER 3: MOVEMENT EFFECTS
# Chasers cycling through sweep path positions
# =============================================================================
# ... [Insert sweep chasers here] ...

# =============================================================================
# LAYER 4: STROBE & FLASH
# =============================================================================
# ... [Insert strobe/flash scenes here] ...

# =============================================================================
# LAYER 5: SPECIAL MOMENTS
# =============================================================================
# ... [Insert blackout, whiteout, laser scenes here] ...

# =============================================================================
# VIRTUAL CONSOLE LAYOUT
# =============================================================================
# ... [Build vc_buttons list with Solo Frames, buttons, sliders] ...

# =============================================================================
# WRITE WORKSPACE
# =============================================================================
# write_workspace(OUTPUT, all_scenes, all_chasers, bpm=BPM, vc_buttons=vc_buttons)
```

### 5. VC Layout Guidelines

The Virtual Console layout should be organized for a touchscreen or mouse-driven workflow.
Use the full 1920x1080 space.

**Recommended layout (left to right):**

```
+------------------+------------------+------------------+------------------+
|                  |                  |                  |                  |
|  COLORS          |  POSITIONS       |  EFFECTS &       |  SPECIALS        |
|  (Solo Frame)    |  (Solo Frame)    |  STROBES         |  (Buttons)       |
|                  |                  |  (Buttons)       |                  |
|  Two-color pair  |  C, DSC, USC     |  Strobe All      |  BLACKOUT        |
|  buttons         |  SL, SR          |  Strobe Movers   |  WHITEOUT        |
|  (genre colors)  |  DSL, DSR        |  Strobe Pars     |  LASERS ON       |
|                  |  USL, USR        |  Flash White      |  LASERS OFF      |
|  ALL WHITE       |  DJ Booth        |                  |  LASERS STROBE   |
|  ALL [primary]   |  Ceiling Hit     |  Movement:       |  PRISM CHAOS     |
|                  |  Audience Blinder|  LR Sweep        |  GOBO TEXTURE    |
|                  |  Back Wall       |  RL Sweep        |  OPEN BEAM       |
|                  |                  |  Slow Drift      |  AUDIENCE BLINDER|
|                  |                  |                  |                  |
+------------------+------------------+------------------+------------------+
|  MASTER slider   |  MOVERS slider   |  PARS slider     |  NI3K slider     |
+------------------+------------------+------------------+------------------+
```

**Button sizing:**
- Color buttons: 120x60px (wide enough for two-color name)
- Position buttons: 100x50px
- Effect/strobe buttons: 100x50px
- Special buttons: 120x70px (bigger for emergency access)
- Sliders: Full width of their column, 30px wide

**Color coding (ARGB hex for QLC+ VC):**
- Color buttons: Match the primary color of the pair (e.g., red pair = red button)
- Position buttons: Neutral gray (#444444)
- Strobe buttons: Yellow (#FFFF00)
- BLACKOUT: Red (#FF0000)
- WHITEOUT: White (#FFFFFF) with dark text
- Laser buttons: Green (#00FF00)
- Other specials: Orange (#FF8800)

### 6. Write Show Notes

Create `venue/<name>/shows/notes/Busking-<Genre>.md` with:
- Genre and venue
- Color palette summary
- Position list
- Button layout description
- Usage tips for live operation

### 7. Validate

Run `xmllint --noout` on the generated .qxw file to verify valid XML.

## Important Notes

- **Every scene must set ALL channels** for the fixtures it controls. Don't set just
  color — set pan, tilt, dimmer, strobe, gobo, prism, focus, everything. Use safe defaults
  for channels you don't specifically need (from showlib.py fixture helpers).
- **Solo Frames** are the key QLC+ widget for busking — they ensure only one color or
  position is active at a time, with automatic release of the previous selection.
- **Button actions**: Color and position buttons should be "Toggle" action. Strobe and
  flash buttons should be "Flash" (momentary) action. Special buttons vary — BLACKOUT
  is Toggle, WHITEOUT is Flash.
- **showlib.py handles fixture channel maps** — use the helper functions (sharpy(), bsw(),
  profile(), etc.) rather than raw channel values. This prevents channel order mistakes.
- **NI3K tilt** is an effect parameter (0-127 position, 128-191 forward rotation, 192-255
  reverse rotation), not a focus position. Don't include NI3K tilt in position scenes.
  Instead, put NI3K tilt controls in the effects section.
- **The genre file is the source of truth** for color palettes, timing, and conventions.
  Don't invent colors or timing values — read them from `genres/<genre>.md`.

## showlib.py Extensions Needed

The current showlib.py `write_workspace()` function supports basic buttons but not Solo
Frames, Sliders, Speed Dials, or nested Frames. The busking generator will need to either:

1. **Extend showlib.py** to support these VC widget types, OR
2. **Generate the VC XML directly** in the generator script (using the XML format from
   `references/qxw-format.md`)

Option 2 is recommended for the first implementation — write the VC XML section directly
in the generator rather than trying to make showlib.py support every widget type. The
generator can use showlib.py for scenes/chasers and handle the VC layout itself.

### QLC+ Solo Frame XML Format

```xml
<SoloFrame Caption="Colors" ID="100">
 <WindowState Visible="True" X="10" Y="10" Width="400" Height="600"/>
 <Appearance>
  <BackgroundColor>Default</BackgroundColor>
 </Appearance>
 <AllowChildren>True</AllowChildren>
 <AllowResize>True</AllowResize>
 <ShowHeader>True</ShowHeader>
 <ShowEnableButton>True</ShowEnableButton>
 <Collapsed>False</Collapsed>
 <Disabled>False</Disabled>
 <Button Caption="Red/Blue" ID="101" Icon="">
  <WindowState Visible="True" X="10" Y="10" Width="120" Height="60"/>
  <Appearance>
   <BackgroundColor>#FF0000</BackgroundColor>
  </Appearance>
  <Function ID="0"/>
  <Action>Toggle</Action>
 </Button>
 <!-- more buttons... -->
</SoloFrame>
```

### QLC+ Slider XML Format

```xml
<Slider Caption="MOVERS" ID="200" WidgetStyle="Slider">
 <WindowState Visible="True" X="10" Y="700" Width="100" Height="300"/>
 <Appearance>
  <BackgroundColor>Default</BackgroundColor>
 </Appearance>
 <SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None">Level</SliderMode>
 <Level LowLimit="0" HighLimit="255">
  <Channel Fixture="8">7</Channel>   <!-- Sharpy dimmer -->
  <Channel Fixture="1">17</Channel>  <!-- BSW dimmer -->
  <Channel Fixture="4">0</Channel>   <!-- Profile dimmer -->
 </Level>
</Slider>
```

## Common Mistakes to Avoid

1. **Don't set strobe ON in color/position scenes** — strobe is its own layer. Color scenes
   should leave strobe at the "open" value (Sharpy: 252, BSW: 8, others: 0).
2. **Don't forget NI3K strobe is inverted** — ch6 value 0 = ON (shutter open), not off.
3. **Don't mix position and color in one scene** — they're separate layers so the operator
   can mix any color with any position independently.
4. **Don't create too many buttons** — a professional busking setup has ~10-15 color combos,
   ~10 positions, ~5-8 effects, and ~8-10 specials. More than that and it becomes unusable
   in a live situation.
5. **Don't forget the home state** — always include a "HOME" button that returns to a
   genre-appropriate base look (usually center position, primary color, full intensity).
