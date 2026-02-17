---
name: moods
description: >
  Create and manage lighting mood definitions. Moods are abstract modifiers that shape how
  a genre's concrete lighting values get applied — color filtering, intensity scaling, movement
  speed, effect density, and timing adjustments. Use this skill when the user wants to create
  a new mood, edit an existing mood, or when a show/busking workflow needs a mood that doesn't
  exist yet. Triggers: "mood," "vibe," "feeling," "atmosphere," "theme," "aesthetic,"
  "create a mood," "new mood," "edit mood," or visual references like "I want it to feel like..."
---

# Moods

Create and manage lighting mood definitions for the `moods/` directory. Moods are abstract
modifiers that shape how a genre's concrete values get applied. They define **what feeling**
to create — genres define **what rules** to follow.

## When to Use

- User says "mood," "vibe," "feeling," "atmosphere," "theme," or "aesthetic"
- User describes a visual reference ("I want it to feel like Blade Runner")
- User wants to create a new mood for a show or busking workspace
- User wants to edit an existing mood
- A show/busking workflow needs a mood that doesn't exist in `moods/`
- User asks to browse or list available moods

## Mood Architecture

Moods combine with genres using a modifier pattern:

```
Genre (concrete values) + Mood (abstract modifiers) = Final lighting parameters
```

The genre provides raw material (specific colors, timing ms, DMX values). The mood filters
and adjusts that material toward a feeling. The same mood applied to different genres produces
different concrete results but the same emotional character.

There are two categories:

- **Emotional states**: Define a feeling (Dark, Ethereal, Aggressive, etc.)
- **Energy levels**: Define an intensity progression (Chill, Building, Peak, Comedown)

Users can combine one emotional state + one energy level (e.g., "Dark + Building" = ominous
tension rising). This is advanced usage — single moods are the default.

## Creating a New Mood

### Entry Points

The skill supports two entry points for mood creation. Always offer both, but lead with
the reference-based approach — it's more creative and produces more specific, evocative results.

#### Path A: Reference-Based (Recommended)

The user provides a visual reference, and you translate it into lighting parameters.

**Step 1: Gather the reference**

Ask the user to describe what they want the lighting to feel like. Good prompts:

- "Describe a scene, image, or place that captures the feeling you want."
- "Is there a movie, game, or photo that has the vibe you're after?"
- "If this mood were a place, where would it be?"

Reference examples and what they translate to:

| Reference | Temperature | Scheme | Intensity | Movement | Key Trait |
|-----------|-------------|--------|-----------|----------|-----------|
| "Blade Runner neon alleyway" | Cool + neon accents | Complementary (cyan/magenta) | Medium, high contrast | Slow, angular | Neon against darkness |
| "Underwater bioluminescence" | Cold | Analogous (blue/cyan/teal) | Low, gentle glow | Very slow, drifting | Organic, pulsing light |
| "Forest fire at night" | Hot | Monochromatic (red/orange) | High, flickering | Medium, erratic | Ember glow, smoke |
| "Cathedral stained glass" | Warm-cool mix | Triadic (rich jewel tones) | Medium, reverent | Static to very slow | Colored shafts of light |
| "Arctic aurora" | Cold | Analogous (green/cyan/purple) | Medium, flowing | Slow, sweeping | Color bands drifting |
| "Cyberpunk Tokyo street" | Cool + hot accents | Complementary (blue/pink) | High, busy | Medium, rhythmic | Dense, layered |
| "Abandoned hospital" | Cold/desaturated | Monochromatic (grey-green) | Very low | Static | Unease, decay |

**Step 2: Translate reference to lighting parameters**

Use your knowledge of visual aesthetics to identify:

1. **Dominant colors** — What colors define this visual? Map to stage lighting equivalents.
2. **Color scheme type** — Is it monochromatic, complementary, analogous, or triadic?
3. **Light quality** — Hard/soft? Focused/diffuse? Bright/dim?
4. **Movement quality** — Static/flowing/erratic? Fast/slow?
5. **Contrast level** — High contrast (dramatic shadows) or low contrast (even/soft)?
6. **Density** — Sparse (few light sources) or dense (many overlapping)?
7. **Key emotional triggers** — What makes this reference feel the way it does?

If the reference is obscure or highly specific, offer to do web research to get more precise
visual details. For well-known references (films, common nature scenes, famous artworks),
Claude's built-in knowledge is sufficient.

**Step 3: Present the translation and iterate**

Show the user how you've interpreted their reference as lighting parameters. Use plain
language, not technical jargon:

> "Based on 'underwater bioluminescence,' I'm thinking:
> - Color palette centered on deep blues, cyan, and teal — analogous color scheme
> - Very low intensity, like the glow is coming from within
> - Extremely slow, drifting movement — like currents
> - No hard beams — everything frosted/soft
> - Occasional gentle pulses of brighter cyan (the 'bioluminescent flash')
> - No strobe, no lasers — too artificial for this organic mood
>
> Does this capture what you're after, or should I adjust?"

Iterate until the user is happy, then generate the mood file.

#### Path B: Parameter-Based

For users who think in technical terms, offer direct parameter entry:

1. Ask: emotional state or energy level?
2. Walk through each modifier category:
   - Color filtering (temperature, saturation, scheme type)
   - Intensity (base level, contrast, blackout frequency)
   - Movement (speed, width, style)
   - Effect density (strobe, laser, gobo, prism, frost)
   - Timing (fade speed, hold duration)
3. Ask about genre interactions
4. Generate the mood file

### Naming Conventions

Mood names should be:
- **Evocative, not technical** — "Smoldering" not "Warm-Dim-Slow"
- **Single word or two-word phrase** — "Neon Abyss" not "Dark Cyberpunk Neon Alleyway"
- **Lowercase filename** with hyphens — `neon-abyss.md`
- **Not duplicating existing moods** — check `moods/` first

If the user struggles with naming, suggest 3 options based on the mood's character.

## Mood File Format

Every mood file must follow this structure exactly. The busking skill and show generators
parse these files, so the format must be consistent.

```markdown
# Mood: [Name]

## Overview

[2-4 sentences describing the feeling. What does it look like? When to use it?
Include the visual reference that inspired it, if applicable.]

## Category

[emotional | energy]

## Visual References

[1-3 visual references that capture this mood's essence. These help future users
understand the intent and help Claude recreate the feeling in different contexts.]

- [Reference 1 — e.g., "Blade Runner 2049 — the orange dust storm scene"]
- [Reference 2 — e.g., "Neon signs reflected in wet Tokyo streets"]
- [Reference 3 — optional]

## Color Scheme

- **Type**: [monochromatic | complementary | analogous | triadic | split-complementary]
- **Rationale**: [1 sentence on why this scheme fits the mood]

## Color Filtering

- **Temperature bias**: [Cold | Cool | Neutral | Warm | Hot — or a transition like "Cool→Warm"]
- **Saturation preference**: [Low | Medium-low | Medium | Medium-high | High | Maximum]
- **Palette selection**: [How to choose from the genre's color pairs — what to prefer/avoid]
- **Preferred colors**: [Specific color descriptions or names]
- **Max simultaneous colors**: [Number or range]
- **Par behavior override**: [How pars should behave in this mood]

## Intensity Modifiers

- **Base brightness**: [N% of genre default]
- **Contrast ratio**: [Minimal | Low | Medium | High | Maximum | Extreme]
- **Blackout frequency**: [None | Rare | Strategic | Medium | High]
- **Number of fixtures active**: [Description of fixture count behavior]
- **Fixture density**: [Sparse | Minimal | Moderate | Dense | Maximum — describes how many
  fixtures are active simultaneously and how that affects the spatial feel]
- **Dimmer behavior**: [Dimmer range, e.g., "30–60% range"]
- **Key-to-fill ratio**: [N:1 — ratio of key (directional) to fill (ambient) light.
  2:1 = bright and open, 8:1 = dramatic with deep shadows, 10:1+ = stark isolation]

## Movement Modifiers

- **Speed multiplier**: [Nx genre default — e.g., 0.4x, 1.5x]
- **Width preference**: [Narrow | Medium | Wide | Maximum — or progressive]
- **Movement style**: [Smooth curves | Angular/deliberate | Erratic | Near-static | etc.]
- **Position hold time**: [Nx genre default]
- **Preferred positions**: [List preferred focus positions from venue]

## Effect Density

- **Strobe**: [None | Rare | Moderate | Heavy — with notes on style]
- **Lasers**: [None | Minimal | Moderate | Full — with notes]
- **Gobos**: [None | Optional static | Rotating | Heavy — with notes]
- **Prism**: [None | Optional | Yes — with notes]
- **Frost**: [Avoid | Optional | Yes | Heavy — with notes]
- **Haze**: [Minimal | Light | Medium | Medium-heavy | Heavy]

## Timing Modifiers

- **Fade speed**: [Nx genre default — higher = slower fades]
- **Hold duration**: [Nx genre default — higher = longer holds]
- **Chase speed**: [Nx genre default]
- **Special timing notes**: [Any exceptions or additional timing behavior]

## Energy Curve

- **Baseline**: [Very low | Low | Medium-low | Medium | High | Maximum]
- **Peak scaling**: [N% of genre peak]
- **Rise time**: [Instant | Fast | Medium | Slow | Very slow | Extremely slow]
- **Fall time**: [Instant | Fast | Medium | Slow | Very slow]
- **Sustain**: [None | Short | Medium | Long | Maximum]

## Phases (Optional)

[If this mood has internal narrative phases, define 2-4 phases here. Each phase
describes how the mood's modifiers shift over time. If the mood is a static state
with no internal progression, omit this section entirely.]

### Phase 1: [Phase Name]
- **Duration**: [N bars or "until operator transitions"]
- **Character**: [1 sentence description]
- **Modifier adjustments**: [How specific modifiers differ from the base mood in this phase]

### Phase 2: [Phase Name]
- **Duration**: [N bars or "until operator transitions"]
- **Character**: [1 sentence description]
- **Modifier adjustments**: [How modifiers shift]

[Additional phases as needed, maximum 4]

## Genre Interaction Notes

- **DnB**: [How this mood plays with DnB conventions]
- **Dubstep**: [How this mood plays with dubstep]
- **Future Bass**: [How this mood plays with future bass]
- **Hardstyle**: [How this mood plays with hardstyle]
- **House**: [How this mood plays with house]
- **Liquid DnB**: [How this mood plays with liquid DnB]
- **Melodic Techno**: [How this mood plays with melodic techno]
- **Psytrance**: [How this mood plays with psytrance]
- **Techno**: [How this mood plays with techno]
- **Trance**: [How this mood plays with trance]
```

## Editing an Existing Mood

When the user wants to modify an existing mood:

1. Read the mood file from `moods/<name>.md`
2. Show the user the current settings in plain language (not the raw markdown)
3. Ask what they want to change
4. Make the changes, preserving unchanged sections
5. If the change affects genre interactions, update those notes too

## Browsing Moods

When the user asks to see available moods or pick one:

1. List all files in `moods/` (excluding README.md)
2. For each, show: name, category (emotional/energy), and the Overview's first sentence
3. Offer to show full details of any mood
4. Offer to create a new one if nothing fits

## Validation

After creating or editing a mood file:

1. Verify all required sections are present
2. Verify modifier values are reasonable (e.g., speed multiplier between 0.1x and 3x,
   brightness between 10% and 120%)
3. Verify genre interaction notes exist for all 10 genres (DnB, Dubstep, Future Bass,
   Hardstyle, House, Liquid DnB, Melodic Techno, Psytrance, Techno, Trance)
4. Verify the color scheme type is one of: monochromatic, complementary, analogous,
   triadic, split-complementary
5. Verify the category is either "emotional" or "energy"
6. If phases are included, verify each has duration, character, and modifier adjustments
7. Verify fixture density and key-to-fill ratio are present in Intensity Modifiers
8. Verify haze density is specified in Effect Density

## Professional Techniques Reference

These techniques were distilled from research into professional lighting designers and apply
to how moods shape a genre's concrete values. Use them when creating or editing mood files.

### How Moods Actually Work in Practice

**Moods Are Multipliers, Not Replacements**
A mood never overrides a genre's DNA — it scales, filters, and reshapes it. "Dark + House"
shouldn't feel like dark techno with house timing; it should feel like house music performed
in a shadowy basement. The genre's warm amber palette gets filtered to deep blues/teals, but
the par-led foundation and groove-driven timing remain. Always preserve the genre's structural
identity while transforming its emotional character.

**The Two Levers: What and How Much**
Every mood modifier operates on two dimensions: (1) what subset of the genre's values to use,
and (2) how intensely to apply them. "Dark" selects the coolest/darkest colors and reduces
intensity. "Euphoric" selects the brightest/warmest colors and increases intensity. "Building"
progressively widens both selection and intensity over time. Make both dimensions explicit in
every modifier.

### Atmosphere Shaping Techniques

**Key-to-Fill Ratio as Mood Indicator**
The ratio of directional (key) light to ambient (fill) light is the single most powerful mood
tool. Low ratios (2:1) feel open, inviting, celebratory — good for euphoric, intimate, peak
moods. High ratios (8:1+) feel dramatic, isolated, tense — good for dark, aggressive, hypnotic
moods. When defining a mood, the key-to-fill ratio communicates more about the feeling than
any other single parameter. Always include it with a concrete number and explanation.

**Fixture Density as Spatial Psychology**
How many fixtures are active simultaneously changes how the room feels:
- **Sparse** (1–2 fixtures): Isolation, focus, tension, intimacy. The audience's attention
  narrows to a single point. Best for dark, intimate, hypnotic moods.
- **Moderate** (3–5 fixtures): Balanced, comfortable, engaged. Multiple visual elements
  without overwhelm. Best for chill, building, melancholic moods.
- **Dense** (most/all fixtures): Immersive, overwhelming, euphoric. Light comes from
  everywhere. Best for peak, euphoric, chaotic moods.
State fixture density explicitly and explain the spatial psychology it creates.

**Haze as Mood Amplifier**
Haze doesn't just make beams visible — it transforms the room's character:
- Heavy haze + sparse fixtures = oppressive, claustrophobic (dark mood)
- Heavy haze + dense fixtures = immersive, enveloping (euphoric mood)
- Light haze + warm colors = honeyed, intimate (intimate mood)
- No haze + cold colors = clinical, exposed (aggressive mood in a specific context)
Define haze density as a mood modifier, not just a genre convention.

### Movement as Emotion

**Movement Vocabulary**
Different movement styles communicate different emotions. Use these descriptors in mood files
and be specific about what they mean for fixture behavior:

| Movement Style | Emotion | Fixture Behavior |
|----------------|---------|------------------|
| Stalking | Menace, dread | Slow angular changes with long holds, deliberate |
| Soaring | Euphoria, release | Wide sweeping arcs, figure-8s, synchronized |
| Breathing | Calm, organic | Slow continuous drift, barely perceptible |
| Drifting | Detachment, trance | Very slow random movement, unfocused |
| Pounding | Aggression, impact | Sharp snaps synced to beat, minimal transition |
| Flowering | Beauty, opening | Gradual spread from center, unfurling |
| Collapsing | Sadness, withdrawal | Convergence to center, narrowing, dimming |
| Stuttering | Chaos, disorientation | Erratic, unpredictable position changes |

When defining a mood's movement style, reference these archetypes and describe how they
modify the genre's default movement conventions.

**Movement Speed × Width = Energy**
Speed and width multiply to create perceived energy. A mood can maintain the same perceived
energy while changing character by adjusting the ratio:
- Fast + narrow = nervous, tense, contained (aggressive, building)
- Fast + wide = explosive, chaotic, overwhelming (peak, chaotic)
- Slow + narrow = intimate, focused, oppressive (dark, intimate, hypnotic)
- Slow + wide = epic, soaring, transcendent (euphoric, ethereal)

### Build and Transition Techniques

**The Layering Principle for Building Mood**
Add ONE new element every 4–8 bars: color → fixture → movement → gobo → laser → release.
The build is a patience game — the longer you hold back, the more powerful the release. This
principle extends beyond the "building" energy mood to any transition between low and high
energy states. Even within a static emotional mood, energy transitions should layer progressively.

**Effect Removal Order for Comedown Mood**
The inverse of the layering principle. Remove elements in reverse order of impact:
1. Kill lasers first (biggest spectacle element)
2. Reduce strobe to nothing
3. Simplify gobos back to open
4. Narrow mover width
5. Reduce par intensity
6. Slow movement speed
7. Reduce fixture count to 1–2
This ordered de-escalation feels natural and prevents jarring transitions.

**Phase Design Patterns**
Moods with internal phases should follow one of these narrative arcs:
- **Linear escalation**: Phase 1 → 2 → 3, each more intense (building, peak)
- **Arc**: Phase 1 (calm) → 2 (peak) → 3 (return), classic dramatic structure (euphoric)
- **Cycle**: Phases repeat, each iteration slightly different (hypnotic, ethereal)
- **Strike pattern**: Phase 1 (sustained state) → 2 (brief violent burst) → 1 (return) (dark, aggressive)

### Genre Interaction Wisdom

**The Tension Test**
When writing genre interaction notes, ask: "Does this mood create productive tension with
the genre, or does it fight it?" Dark + DnB creates productive tension (neurofunk). Dark +
House creates a challenging but rewarding pairing (deep house at 4am). Dark + Future Bass
fights the genre's DNA — possible but requires significant modifier adjustments. State the
difficulty level and what adjustments are needed.

**Warm vs Cold Genre Foundations**
Genres have a temperature foundation that moods interact with:
- **Warm-foundation genres** (house, future bass, liquid DnB, trance): Cool moods create
  dramatic tension by fighting the natural warmth. Warm moods amplify the natural character.
- **Cold-foundation genres** (techno, DnB, dubstep): Warm moods soften and humanize.
  Cold moods push deeper into the genre's natural territory.
- **Neutral genres** (melodic techno, hardstyle, psytrance): Temperature shifts have maximum
  impact because there's no strong default to fight.

**The Identity Preservation Rule**
A mood should never make one genre's output indistinguishable from another genre. "Dark +
House" should still be recognizably house (par-led, groove-driven, four-on-the-floor). If
applying a mood makes house look like techno, the mood's modifiers are too aggressive. Test
this by asking: "Would a DJ recognize this as lighting for their genre?" If not, dial back.

## Important Notes

- **Moods never define exact DMX values** — they define abstract modifiers. The genre file
  provides the concrete values; the mood shapes how they're applied.
- **Every mood must have genre interaction notes** — the same mood plays differently with
  each genre. These notes prevent the busking skill from making bad combinations.
- **Visual references are important** — they're the quickest way for a future user (or Claude)
  to understand the mood's intent. Always include at least one.
- **The busking skill is the primary consumer** of mood files. When writing modifiers, think
  about how the busking skill will interpret them to select colors, adjust timing, and
  enable/disable effects.
- **Don't duplicate existing moods** — check the existing collection first. If a new mood
  is similar to an existing one, consider if it's different enough to warrant a new file
  or if the existing mood should be edited.
- **The color scheme type is key** — it's the most actionable new field. It tells the busking
  skill whether to generate monochromatic looks (variations of one hue), complementary pairs
  (contrasting colors), analogous blends (neighboring hues), or triadic combinations.

## Color Scheme Quick Reference

For translating visual references to scheme types:

| Scheme | When to Use | Visual Character | Example |
|--------|-------------|------------------|---------|
| Monochromatic | Focused emotion, intensity, unity | One color dominates everything | "All red" anger, "all blue" melancholy |
| Complementary | Tension, contrast, duality | Two opposing colors create drama | Red vs cyan, purple vs gold |
| Analogous | Harmony, flow, immersion | Colors blend smoothly into each other | Blue→cyan→teal ocean feel |
| Triadic | Richness, vibrancy, complexity | Three distinct colors in balance | Red/blue/yellow festival feel |
| Split-complementary | Contrast with more nuance | One base + two near-complements | Blue + orange-red + yellow-orange |
