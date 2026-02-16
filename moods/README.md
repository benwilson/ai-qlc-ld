# Mood Definitions

Each `.md` file in this directory defines a lighting mood — an abstract set of modifiers
that shape how a genre's concrete values get applied. Moods define **what feeling** to
create; genres define **what rules** to follow. The busking skill combines them:
genre provides the raw palette and timing, mood filters and adjusts them toward a feeling.

## How Moods Modify Genres

A mood never defines exact DMX values or specific colors. Instead it defines:

- **Color filtering** — which temperature/saturation range to prefer from the genre palette
- **Intensity modifiers** — brightness levels, contrast ratios, blackout usage
- **Movement modifiers** — speed scaling, sweep width, movement style
- **Effect density** — how much strobe, laser, gobo, prism to use
- **Timing modifiers** — fade speed scaling, hold duration preference
- **Energy curve** — how the mood shapes energy over time

The busking skill reads both files, then applies the mood's modifiers to the genre's
concrete values. For example, "Ethereal" mood + DnB genre = DnB's blue/cyan palette
with slower movements, longer fades, no strobes. Same "Ethereal" + House = house's
teal/blue palette with even smoother fades and minimal effects.

## File Format

Every mood file follows a consistent structure:

- **Overview** — What this mood feels like, when to use it
- **Category** — `emotional` or `energy`
- **Visual References** — 3 evocative reference images that capture the mood's feeling (e.g., "Berghain at 4am — a single red beam cutting through industrial haze"). Used for creative alignment when designing and as translation anchors for the moods skill.
- **Color Scheme** — Formal color scheme type (monochromatic, complementary, analogous, triadic, split-complementary) with rationale. Guides the busking skill's color pair selection from the genre palette.
- **Color Filtering** — Temperature bias, saturation preference, palette selection rules
- **Intensity Modifiers** — Base level, contrast ratio, blackout behavior
- **Movement Modifiers** — Speed multiplier, width preference, style
- **Effect Density** — Strobe/laser/gobo/prism usage levels
- **Timing Modifiers** — Fade and hold scaling
- **Energy Curve** — How energy flows over time in this mood
- **Phases** *(optional)* — 2–4 internal progression stages for moods that evolve over time. Each phase defines duration, character, and modifier adjustments. Most sustained-state moods (chill, intimate, hypnotic) omit this section. Moods with natural arcs (building, dark, aggressive) use phases to define their progression.
- **Genre Interaction Notes** — How this mood plays with specific genres

## Available Moods

### Emotional States

| File | Mood | Color Scheme | Character |
|------|------|-------------|-----------|
| dark.md | Dark | monochromatic | Menacing, oppressive, shadow-heavy, minimal light |
| ethereal.md | Ethereal | analogous | Dreamy, floating, otherworldly, delicate |
| aggressive.md | Aggressive | complementary | Angry, intense, in-your-face, high contrast |
| hypnotic.md | Hypnotic | monochromatic | Repetitive, trance-inducing, mesmerizing patterns |
| euphoric.md | Euphoric | triadic | Joyful, uplifting, bright, celebratory |
| melancholic.md | Melancholic | analogous | Sad, reflective, muted, intimate |
| chaotic.md | Chaotic | split-complementary | Unpredictable, wild, sensory overload, everything at once |
| intimate.md | Intimate | monochromatic | Close, personal, warm, small-feeling |

### Energy Levels

| File | Mood | Color Scheme | Character |
|------|------|-------------|-----------|
| chill.md | Chill | monochromatic | Low energy sustained, ambient, background lighting |
| building.md | Building | analogous → complementary | Rising tension, progressive layering, anticipation |
| peak.md | Peak | complementary | Maximum energy, everything unleashed, climax |
| comedown.md | Comedown | analogous (narrowing) | Gradually reducing, cooling off, winding down |

## Usage

The busking skill asks the user for a genre and optionally a mood. If no mood is specified,
the genre's default conventions apply unmodified. If a mood is specified, the skill reads
both files and applies the mood's modifiers to the genre's values.

Multiple moods can potentially stack (e.g., "Dark + Building") but this is advanced usage.
The primary use case is a single mood applied to a single genre.

Use the **moods** skill to create new moods or edit existing ones.
