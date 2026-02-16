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

1. Verify all required sections are present (Overview through Key Philosophy)
2. Verify BPM range includes typical, common, and time signature
3. Verify energy profile table has at least 5 sections
4. Verify color palette has 3 primary + 3 accent colors with RGB values and fixture mappings
5. Verify 6-8 two-color pairs exist with names and usage context
6. Verify timing presets are mathematically correct for the stated BPM
7. Verify movement conventions cover all sections from the energy profile
8. Verify strobe, laser, gobo, and par sections exist with per-section guidance
9. Update `genres/README.md` table to include the new/modified genre

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
