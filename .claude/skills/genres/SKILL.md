---
name: genres
description: >
  Create and manage EDM genre lighting definitions. Each genre file defines color palettes,
  timing presets, movement conventions, strobe/laser/gobo rules, and par behavior for a
  specific genre. Use this skill when the user wants to create a new genre, edit an existing
  genre, or when a busking/show workflow needs a genre that doesn't exist yet. Triggers:
  "genre," "add a genre," "new genre," "edit genre," "create genre," or naming a specific
  EDM subgenre that doesn't have a file yet.
---

# Genres

Create and manage EDM genre lighting definitions for the `genres/` directory. Each genre
file provides the concrete lighting values (specific colors, DMX values, timing in ms,
section behaviors) that the busking skill and show generators consume. Moods modify these
values; genres provide the raw material.

## When to Use

- User says "genre," "add a genre," "new genre," "edit genre," or "create genre"
- User mentions a specific EDM subgenre that doesn't have a file in `genres/`
- A busking/show workflow needs a genre that doesn't exist yet
- User wants to adjust colors, timing, or conventions for an existing genre
- User asks to browse or list available genres

## Knowledge vs Research

When creating a new genre, **always ask the user first**:

> "I can create the [genre] lighting profile two ways:
>
> 1. **From my existing knowledge** — I have solid understanding of EDM subgenres, their
>    typical BPM ranges, energy structures, and lighting conventions. This is faster and
>    works well for mainstream genres.
> 2. **With web research first** — I'll research current lighting conventions, notable
>    artists/shows, and visual trends specific to this genre. This is better for niche
>    subgenres or if you want the most current scene-specific conventions.
>
> Which would you prefer?"

For **well-known genres** (deep house, progressive house, melodic techno, hard techno, liquid
DnB, neurofunk, riddim, future bass, psytrance, etc.), existing knowledge is usually sufficient.
Offer research as an option but recommend knowledge-first.

For **niche or emerging genres** (wave, deconstructed club, UK garage revival, amapiano,
hardwave, etc.), recommend research first to ensure accuracy.

If the user chooses research, search for:
- "[Genre] live show lighting" and "[Genre] stage design"
- Notable artists/festivals associated with the genre
- Visual aesthetics and color conventions of the scene
- Typical BPM range and song structure

## Creating a New Genre

### Step 1: Gather Requirements

Ask the user:
- What genre? (specific subgenre name)
- Should Claude use existing knowledge or do web research?
- Any specific artists or shows that exemplify the look they want?
- Any colors they want to emphasize or avoid?

### Step 2: Establish Core Parameters

Whether from knowledge or research, determine these core parameters:

1. **BPM range** — typical tempo range and common default BPM
2. **Energy profile** — how sections map to energy levels (table format)
3. **Color palette** — primary colors (3), accent colors (3), and why each fits
4. **Two-color pairs** — 6-8 busking-ready pairs with Color A, Color B, and usage context
5. **Movement conventions** — per-section movement behavior
6. **Timing presets** — BPM-calibrated fade/hold values (use `bpm_to_ms()` formula)
7. **Strobe/laser/gobo/prism conventions** — per-section usage rules
8. **Par behavior** — wash/gradient/chase patterns per section
9. **Key philosophy** — the one-paragraph essence of the genre's lighting approach

### Step 3: Calculate Timing Presets

Timing presets must be calculated from the genre's BPM. Use these formulas:

```
1 beat = 60000 / BPM (ms)
1 bar = 4 beats
```

Every genre file needs at minimum these timing presets:

| Preset | Formula | Purpose |
|--------|---------|---------|
| [Genre] Snap | FadeIn=50, Hold=1bar-50 | Sharp color change (1 bar) |
| [Genre] Fast Snap | FadeIn=50, Hold=1beat-50 | Beat-synced accent |
| [Genre] Strobe | FadeIn=0, Hold=1/4beat | Strobe timing |
| [Genre] Smooth 2bar | FadeIn=2bars, Hold=0 | Smooth crossfade |
| [Genre] Smooth 4bar | FadeIn=4bars, Hold=0 | Extended smooth sweep |
| [Genre] Breathe | FadeIn=8bars, Hold=0 | Slow ambient fade |
| [Genre] Beat Step | FadeIn=0, Hold=1beat | Beat-synced chase |
| [Genre] Half Beat | FadeIn=0, Hold=0.5beat | Double-time chase |

### Step 4: Map Colors to Fixture Values

Every color in the palette must include mappings for all fixture types:

- **RGB value** — for 4BAR, Missyee pars, NI3K
- **BSW color wheel** — closest match from BSW_WHITE, BSW_RED, BSW_ORANGE, BSW_YELLOW,
  BSW_GREEN, BSW_BLUE, BSW_MAG, BSW_TEAL, BSW_PINK
- **Sharpy color macro** — closest match from value 0-120 (White=0, Red=10, Yellow=20,
  Blue=30, Green=40, Purple=50, Pink=60, Teal=70, Amber=80, Orange=90)
- **Profile color wheel** — closest match from value 0-35 (White=0, Red=5, Yellow=10,
  Blue=15, Green=20, Orange=25, Pink=30, Teal=35)

Include these mappings in the color palette section so the busking skill can generate
scenes without guessing at fixture-specific values.

### Step 5: Present and Iterate

Show the user the draft genre definition in plain language before writing the file:

> "Here's what I've got for [Genre]:
>
> **BPM**: [range], default [N]
> **Primary colors**: [list with rationale]
> **Character**: [1-2 sentences]
> **Key conventions**: [notable lighting behaviors]
>
> Want me to adjust anything before I write the file?"

Iterate until the user is satisfied.

### Step 6: Write the Genre File

Write to `genres/[genre-name].md` using the exact format below. Update `genres/README.md`
to include the new genre in the table.

## Genre File Format

Every genre file must follow this structure exactly. The busking skill parses these files,
so format consistency is critical.

```markdown
# Genre: [Full Name]

## Overview

[2-4 sentences describing the genre's character and how lighting should reflect it.
Include the key sonic features that drive lighting decisions.]

## BPM Range

- Typical: [N]–[N] BPM
- Common: [N] BPM
- Time signature: [e.g., 4/4, or "4/4 with half-time feel"]

## Energy Profile

[1-2 sentences about the genre's overall dynamic range and contrast level.]

| Section | Energy | Duration | Lighting Character |
|---------|--------|----------|--------------------|
| [Section name] | [Low/Medium/High/Peak] | [N–N bars] | [Brief description] |
| ... | ... | ... | ... |

## Color Palette

### Primary Colors (use most often)
- **[Color Name]** ([R], [G], [B]) / BSW [name] / Sharpy [name] — [why this color fits]
- **[Color Name]** ([R], [G], [B]) / BSW [name] / Sharpy [name] — [why]
- **[Color Name]** ([R], [G], [B]) / BSW [name] / Sharpy [name] — [why]

### Accent Colors (use for contrast and variety)
- **[Color Name]** ([R], [G], [B]) / Sharpy [name] — [usage context]
- **[Color Name]** ([R], [G], [B]) / Sharpy [name] — [usage context]
- **[Color Name]** ([R], [G], [B]) / Sharpy [name] — [usage context]

### Two-Color Pairs (primary busking combos)
| Combo Name | Color A | Color B | Best For |
|------------|---------|---------|----------|
| [Evocative name] | [Color A] | [Color B] | [When to use] |
| ... | ... | ... | ... |

[6-8 pairs minimum. Each pair should have a distinct character and usage context.]

### Avoid
- [Colors or combinations that don't fit this genre, with brief explanation]

## Movement Conventions

### [Section 1] Movement
- [Movement behaviors for this section]

### [Section 2] Movement
- [Movement behaviors]

[One subsection per major section type in the energy profile.]

## Timing Presets

| Preset | FadeIn (ms) | Hold (ms) | Use |
|--------|-------------|-----------|-----|
| [Genre] Snap | [N] | [N] | [Purpose] |
| [Genre] Fast Snap | [N] | [N] | [Purpose] |
| [Genre] Strobe | [N] | [N] | [Purpose] |
| [Genre] Smooth 2bar | [N] | [N] | [Purpose] |
| [Genre] Smooth 4bar | [N] | [N] | [Purpose] |
| [Genre] Breathe | [N] | [N] | [Purpose] |
| [Genre] Beat Step | [N] | [N] | [Purpose] |
| [Genre] Half Beat | [N] | [N] | [Purpose] |

[All timing values calculated from the genre's common BPM using 60000/BPM formulas.]

## Strobe Conventions

- **On drops**: [When, speed, duration]
- **On builds**: [Behavior]
- **Signature move**: [Any genre-specific strobe technique]
- **Never**: [What to avoid]
- **Fixture strobes**: [Per-fixture strobe channel notes]

## Laser Conventions

- **When**: [Which sections use lasers]
- **Color**: [How laser color relates to palette]
- **Signature**: [Any genre-specific laser technique]

## Gobo & Prism Conventions

- **[Section]**: [Gobo/prism behavior]
- [One entry per major section type]

## Par Behavior

- **[Section]**: [par_wash/par_gradient/par_chase/par_pairs usage]
- [One entry per major section type]

## Fixture Layering

[Define the fixture hierarchy for each major section. Which fixture type is the PRIMARY
visual element, which provides SECONDARY texture, and which is the ACCENT layer?]

### [Section 1] Layer Stack
1. **Foundation (N% of visual)**: [Fixture type] — [Role and behavior]
2. **Texture layer (N% of visual)**: [Fixture type] — [Role and behavior]
3. **Accent layer (N% of visual)**: [Fixture type] — [Role and behavior]

### [Section 2] Layer Stack
[Same structure]

[One subsection per major section type. Every genre has a different fixture hierarchy —
e.g., house is par-led (60-70% pars), techno is mover-led, dubstep is effect-led.]

## Haze & Atmosphere

[Define haze density requirements per section. Haze is a performance tool, not decoration.]

| Section | Density | Purpose |
|---------|---------|---------|
| [Section] | [None/Light/Medium/Heavy/Maximum] ([N-N%]) | [Why this level] |
| ... | ... | ... |

### Haze + Lighting Interaction
- [How beams look in haze for this genre]
- [How strobes interact with haze]
- [Any genre-specific haze techniques]

## Venue Scale Notes

[How the genre's conventions change between club and festival scale.]

### Club Scale ([capacity])
- **Fixture count**: [typical range]
- **Key adaptation**: [what changes at this scale]

### Festival Scale ([capacity])
- **Fixture count**: [typical range]
- **Key adaptation**: [what changes at this scale]

### Scaling Philosophy
[1-2 sentences on the core scaling principle for this genre]

## Notable References

### LDs / Productions
- **[Name]** — [What they're known for, what to study]

### Venues / Festivals
- **[Name]** — [Why it exemplifies this genre's lighting]

### Techniques to Study
- **[Technique name]**: [What it is, when to use it]

## Key Philosophy

[One paragraph capturing the essence of this genre's lighting approach. What's the single
most important principle? What separates this genre's lighting from others?]
```

## Editing an Existing Genre

When the user wants to modify an existing genre:

1. Read the genre file from `genres/<name>.md`
2. Show the user the current settings in plain language
3. Ask what they want to change
4. If changing BPM range, **recalculate all timing presets** automatically
5. If changing colors, update all fixture-specific values (BSW wheel, Sharpy macro, etc.)
6. If adding/removing color pairs, ensure the pair count stays at 6-8
7. Preserve unchanged sections exactly
8. Update `genres/README.md` if the genre's character summary changed

## Browsing Genres

When the user asks to see available genres or pick one:

1. List all files in `genres/` (excluding README.md)
2. For each, show: name, BPM range, primary colors, and key philosophy (first sentence)
3. Offer to show full details of any genre
4. Offer to create a new one if nothing fits

## Subgenre Relationships

Some subgenres share a parent genre's conventions with tweaks. When creating a subgenre:

1. Read the parent genre file first
2. Identify what's different (usually color palette, energy profile, and timing)
3. The subgenre file should be complete and standalone — don't reference the parent file.
   The busking skill reads one genre file; it can't merge parent + child.

Common parent → subgenre relationships:

| Parent | Subgenres | Key Differences |
|--------|-----------|-----------------|
| House | Deep House, Tech House, Progressive House, Melodic House | Tempo, energy range, color warmth |
| Techno | Melodic Techno, Hard Techno, Minimal Techno, Industrial Techno | Intensity, color palette, strobe aggression |
| DnB | Liquid DnB, Neurofunk, Jump-Up, Jungle | Contrast level, color warmth, breakdown character |
| Dubstep | Riddim, Melodic Dubstep, Brostep, Future Bass | Wobble behavior, color intensity, drop character |
| Trance | Psytrance, Progressive Trance, Uplifting Trance, Tech Trance | Build length, color evolution, euphoria level |

## Validation

After creating or editing a genre file:

1. Verify all required sections are present (Overview through Key Philosophy, including Fixture Layering, Haze & Atmosphere, Venue Scale Notes, and Notable References)
2. Verify BPM range includes typical, common, and time signature
3. Verify energy profile table has at least 5 sections
4. Verify color palette has 3 primary + 3 accent colors with RGB values and fixture mappings
5. Verify 6-8 two-color pairs exist with names and usage context
6. Verify timing presets are mathematically correct for the stated BPM
7. Verify movement conventions cover all sections from the energy profile
8. Verify strobe, laser, gobo, and par sections exist with per-section guidance
9. Verify fixture layering defines primary/secondary/accent layers per section
10. Verify haze section includes density table and interaction notes
11. Verify venue scale notes cover at least club and festival scale
12. Verify notable references include at least one LD/production and one venue/festival
13. Update `genres/README.md` table to include the new/modified genre

## Professional Techniques Reference

These techniques were distilled from research into professional EDM lighting designers and
landmark productions. Use them as building blocks when creating or editing genre files.

### Core Principles

**Negative Space / Darkness as Design Element**
Darkness is not the absence of lighting — it's an active design choice. The deeper the darkness
in quiet sections, the more devastating the bright moments. Every genre has a different
relationship with darkness: techno treats it as the primary canvas, dubstep uses it to
maximize drop contrast, house avoids it in favor of warm ambient glow. When defining a genre,
explicitly state how darkness functions.

**Restraint Earns Impact**
Every effect gains power through scarcity. A strobe that fires once per track hits harder than
one that runs every 8 bars. A laser reveal on the second drop is more dramatic than lasers
running from bar 1. When writing genre conventions, define what's held back and when it's
released — the restraint/release cycle is the fundamental unit of lighting dramaturgy.

**Fixture Introduction Order**
During builds, introduce fixtures one at a time, every 4–8 bars. The order of introduction
creates a narrative: pars first (ambient foundation) → movers (spatial definition) → gobos
(texture) → prisms (complexity) → lasers (spectacle) → strobe (climax). This layering
principle applies to every genre — only the timing and density changes.

### Movement Techniques

**Ballyhoo (Figure-8)**
The fundamental mover movement pattern. Pan and tilt trace a figure-8 in the air, creating
smooth continuous motion. Works at any speed — slow ballyhoo for atmospheric sections, fast
for energy. Particularly effective in haze where the beam path becomes visible. Best for:
rolling bass sections, grooves, sustained energy without chaos.

**Mover Convergence**
All movers gradually moving toward a single point (center, DJ booth, ceiling hit). Creates
intimacy and focus. The inverse — movers spreading from center to wide — creates opening
and release. The convergence/spread cycle maps directly to breakdown/release energy arcs.

**Synchronized Parallel Sweeps**
All movers executing the same movement in the same direction simultaneously. Creates geometric
precision and visual unity. More "architectural" than individual random movements. Signature
technique for techno (geometric precision) and trance (soaring euphoria). The direction and
speed communicate genre: slow L→R = hypnotic/flowing, sharp angular snaps = aggressive/industrial.

**Beam Geometry in Haze**
Parallel beams, fan patterns, grid intersections, and crossing patterns are only visible in haze.
These geometric shapes are the primary design vocabulary for beam-heavy genres (techno, DnB,
trance). When defining movement conventions, think in terms of the shapes beams create in space,
not just where fixtures point.

### Color Techniques

**Color Temperature as Energy Indicator**
Cool colors (blue, cyan, teal) = low energy, introspection, depth. Warm colors (amber, magenta,
red, white) = high energy, excitement, release. This mapping is nearly universal across EDM
genres. Builds should shift from cool → warm. Breakdowns should return to cool. Define each
genre's specific temperature journey in the Color Palette section.

**Color Evolution Journey**
A track-length color arc that mirrors the emotional narrative. Example (trance): deep blue →
blue/purple → bright cyan → single pure blue → purple/magenta → white/magenta explosion.
Every genre should define its characteristic evolution journey in the Color Palette section.
This gives the busking operator a roadmap for live color decisions.

**Two-Color Pair Philosophy**
Each pair needs a distinct emotional character and usage context. The operator selects a pair
and assigns Color A to movers and Color B to pars (or vice versa). Both assignments should
look good — design pairs that work in either direction. Include at least one pair that uses
black/off as a color (for dark/minimal moments) and one all-warm pair (for peak energy).

### Par Techniques

**Sidechain Breathing**
Pars oscillate brightness on the beat, mimicking the sidechain compression that's fundamental
to electronic music production. The kick "ducks" everything — lighting mirrors this with subtle
brightness pulses. Implementation: dimmer oscillates ±10–20% on downbeats. Most effective in
house (where the four-on-the-floor pulse defines everything) and DnB (where the breakbeat
drives energy). Define the breathing intensity and timing per genre.

**Par-Led vs Mover-Led**
Some genres are par-led (house: 60-70% of visual from pars), others are mover-led (techno:
beams are the primary element). This distinction fundamentally shapes the fixture layering.
When creating a genre, decide which fixture type carries the visual foundation and state it
explicitly in the Fixture Layering section.

### Effect Techniques

**Strobe Discipline**
Professional LDs use strobe far less than amateurs expect. Rules of thumb: maximum 2–4 bars of
sustained strobe per section; always follow strobe with a contrasting moment (blackout or calm);
white strobe for maximum impact, color strobe for palette continuity; accelerating strobe
(slow → fast over 4–8 bars) is a build technique, not a drop technique.

**Laser as Architecture**
Lasers function as spatial architecture — beams cutting through haze define rooms and volumes
of light. Static laser beams are more "designed" than strobing lasers. In trance, lasers create
a "cathedral" effect with parallel vertical beams. In techno, a single red laser cutting through
haze is a Berghain signature. In dubstep, all lasers simultaneously create overwhelming assault.
Define each genre's laser philosophy in terms of architectural intent, not just on/off rules.

**Gobo Progression**
Gobos add visual complexity progressively through a build: open beam → static gobo → rotating
gobo → gobo + prism. This progression works as a secondary build technique alongside fixture
introduction. Different genres favor different gobo aesthetics: organic/flowing for trance,
sharp/geometric for techno, mechanical/repetitive for riddim dubstep.

### Haze Techniques

**Haze as Performance Tool**
Haze is not a static atmospheric effect — it's a dynamic performance tool with its own density
curve per section. Heavy haze reveals beam geometry but obscures the room. Light haze preserves
intimacy. No haze makes beams invisible. Every genre file should define a haze density table
that maps sections to density percentages, just like a dimmer curve.

**Haze + Beam Synergy**
Beam-heavy genres (techno, DnB, trance) REQUIRE haze for their fundamental aesthetic to work.
Without haze, geometric beam patterns are invisible — the audience only sees dots of light on
surfaces. With haze, they see sculpted volumes of light in space. When defining a genre, state
whether haze is essential, recommended, or optional.

**Haze + Color Interaction**
Warm colors (amber, gold) in haze create a "honeyed glow" (house signature). Cool colors
(blue, cyan) in heavy haze feel expansive and deep. White beams in heavy haze create the most
visible geometry. Red in haze creates industrial warmth. These interactions should inform color
palette choices — some colors only achieve their intended character in haze.

### Venue Scaling Principles

**Club vs Festival Adaptation**
When defining venue scale notes, apply these universal scaling rules:
- **Movement**: Double duration at festival scale (2-bar sweep → 4-bar sweep)
- **Strobe**: Halve density, extend duration at festival scale
- **Haze**: Increase density 20-25% at festival scale (larger volume dissipates faster)
- **Contrast**: Increase section contrast at festival scale (harder to perceive subtlety at distance)
- **Breakdowns**: Avoid total blackout at festival (back of crowd loses focus); use 20-30% dim instead
- **Fixture density**: More fixtures doesn't mean all-on — restraint at large scale is harder and more impactful

**The Constant Across Scales**
Every genre has one element that doesn't change with scale — identify and state it. For house,
it's warm amber/gold foundation. For techno, it's geometric precision. For dubstep, it's the
blackout-to-drop contrast ratio. This constant is the genre's identity regardless of venue.

### Notable Reference Patterns

When writing the Notable References section, include:
- **At least one LD or production team** with a named technique to study
- **At least one venue or festival** that exemplifies the genre's lighting DNA
- **Specific techniques** named and described concretely enough to recreate
- **A lesson** for each reference — what principle it teaches about the genre

Good references are specific: "Ed Warren's philosophy: hit the beat, the off beat, wait for the
last possible moment" is actionable. "DnB lighting is energetic" is not.

## Important Notes

- **Genre files define concrete values** — specific RGB colors, specific ms timing, specific
  fixture channel values. This is what separates genres from moods (which are abstract modifiers).
- **The busking skill is the primary consumer** — it reads the genre file to generate color
  buttons, timing presets, and effect conventions. Write with that parser in mind.
- **Timing precision matters** — always calculate from BPM, don't estimate. A timing preset
  that's 20ms off at 174 BPM will drift noticeably over a 32-bar chaser.
- **Two-color pairs are the core busking tool** — these become the color buttons in the
  Virtual Console. Each pair needs to look good as both "movers=A, pars=B" and "movers=B,
  pars=A" since the operator can swap.
- **Fixture color mappings prevent runtime guesswork** — including BSW/Sharpy/Profile wheel
  values in the color palette means the busking generator doesn't have to approximate at
  generation time.
- **Don't duplicate parent genre files** — if creating a subgenre, it must be standalone but
  shouldn't just copy the parent with minor tweaks. The differences should be meaningful
  enough to justify a separate file.
- **Ask about knowledge vs research** — this is the key workflow decision. Always give the
  user the choice, with a recommendation based on how mainstream/niche the genre is.
