# Genre: Trance

## Overview

Trance is built on euphoric melodies, long emotional builds, and cathartic releases. It's the
most "emotional journey" genre of EDM — a single track can take the listener from delicate
beauty through intense tension to overwhelming release. Lighting should follow this emotional
arc with sweeping movements, rich color evolution, and dramatic reveals.

## BPM Range

- Typical: 130–150 BPM
- Common: 138–142 BPM
- Time signature: 4/4

## Energy Profile

Trance has the longest build-release cycles of any EDM genre. Breakdowns are the emotional
peak (not the drops), and the release after a breakdown is cathartic rather than aggressive.

| Section | Energy | Duration | Lighting Character |
|---------|--------|----------|--------------------|
| Intro | Low | 16–32 bars | Ethereal wash, stars/gobo texture, gentle |
| Build 1 | Low–Medium | 16–32 bars | Slow color evolution, movers gradually widening |
| First Release | High | 16–32 bars | Full rig, sweeping movements, joyful colors |
| Extended Breakdown | Low–Medium | 16–32 bars | THE emotional peak — single color, intimate, beautiful |
| Main Build | Medium–High | 8–16 bars | Rising intensity, all elements layering in |
| Main Release | Peak | 16–32 bars | Full euphoria — maximum color, movement, lasers |
| Outro | Low | 8–16 bars | Gentle fade, return to ethereal |

## Color Palette

### Primary Colors
- **Blue** (0, 0, 255) / BSW Blue / Sharpy Blue — the signature trance color, sky and ocean
- **White** (255, 255, 255) — euphoria, release, transcendence
- **Cyan** (0, 255, 255) / Sharpy Teal — clean, celestial, uplifting

### Accent Colors
- **Purple** (128, 0, 255) / Sharpy Purple — emotional depth, mystical
- **Magenta** (255, 0, 255) / BSW Magenta — passionate, uplifting moments
- **Green** (0, 255, 0) / BSW Green / Sharpy Green — nature, outdoors, festival trance
- **Pink** (255, 64, 128) / Sharpy Pink — emotional, beautiful breakdowns

### Two-Color Pairs
| Combo Name | Color A | Color B | Best For |
|------------|---------|---------|----------|
| Sky | Blue | Cyan | Classic trance, euphoric release |
| Ethereal | Blue | White | Clean, uplifting peaks |
| Mystic | Purple | Blue | Deep breakdowns, emotional builds |
| Aurora | Cyan | Green | Festival trance, outdoors |
| Passion | Magenta | Pink | Emotional breakdowns |
| Celestial | White | Cyan | Maximum euphoria moments |
| Sunset | Magenta | Amber | Warm emotional peaks |

### Avoid
- Dark, aggressive colors as primaries (red, dark purple — wrong mood)
- Black/darkness as a primary tool (trance is about light, not shadow)
- Harsh, angular color changes (trance is flowing)

## Movement Conventions

### Release/Peak Movement
- Wide, sweeping arcs — the biggest, most dramatic mover movements
- All movers synchronized in large-scale sweeps (L→R over 4–8 bars)
- Figure-8 and circular patterns at medium speed
- Movements should feel "soaring" — matching the melodic euphoria
- NI3K slow rotation with full RGBW for ambient texture

### Breakdown Movement
- Movers converge slowly to center or DJ booth position
- Extremely slow, deliberate movement (16+ bar sweeps)
- The movement should feel intimate, like the room is shrinking
- Ceiling hit with single color for "starfield" effect in haze

### Build Movement
- Movers gradually spreading from center to wide (over 8–16 bars)
- Speed increasing from very slow to moderate
- Color shifting from cool to warm (blue → purple → magenta) over the build
- Add sweep width as build progresses

### Intro/Outro
- Minimal movement, movers at center or ceiling
- Gentle drift, barely perceptible
- Focus on color atmosphere, not position

## Timing Presets

| Preset | FadeIn (ms) | Hold (ms) | Use |
|--------|-------------|-----------|-----|
| Trance Sweep 4bar | 6857 | 0 | Smooth 4-bar sweep at 140 |
| Trance Sweep 8bar | 13714 | 0 | Extended 8-bar sweep for breakdowns |
| Trance Sweep 16bar | 27429 | 0 | Ultra-slow breakdown evolution |
| Trance Bar | 1714 | 0 | 1-bar smooth transition |
| Trance Beat | 0 | 429 | Beat-synced for peaks (1 beat at 140) |
| Trance 2Beat | 0 | 857 | 2-beat hold for accents |
| Trance Breathe | 6857 | 6857 | 8-bar pulse (4 bar fade + 4 bar hold) |
| Trance Strobe | 0 | 107 | 1/4 beat strobe (rare) |

## Strobe Conventions

- **Rare**: Trance uses less strobe than most EDM genres
- **Release moments only**: Brief strobe burst (2–4 beats) at the top of a release
- **White or cyan**: Color strobes if needed, matching the palette
- **Par strobe preferred**: Pars flashing rhythmically feels more "trance" than moving head strobe
- **Never during breakdowns**: Breakdowns are sacred — no strobe, no flash

## Laser Conventions

- **Release sections**: Lasers during the main release for maximum euphoria
- **All colors**: Trance is one of the few genres where full RGB laser spread works well
- **Sweeping**: NI3K pan sweep with lasers creates dramatic room-filling effects
- **Not for breakdowns**: Lasers off during emotional sections
- **Festival trance**: More laser-heavy than club trance

## Gobo & Prism Conventions

- **Breakdowns**: Soft gobo for texture (not harsh patterns), slow or no rotation
- **Releases**: Open gobo for clean beams, optional prism for multi-beam spread
- **Builds**: Add gobo texture partway through, then clear to open at release
- **Preferred gobos**: Organic/flowing patterns rather than sharp geometric ones

## Par Behavior

- **Releases**: `par_wash()` in bright, unified color — maximum euphoria
- **Grooves**: `par_gradient()` flowing through cool color families
- **Breakdowns**: `par_wash()` single intimate color at medium-low intensity
- **Builds**: `par_gradient()` evolving from cool to warm over the build

## Key Philosophy

Trance lighting is about **emotional journey and euphoria**. Every lighting choice should
serve the emotional arc — from delicate beauty through tension to cathartic release. The
breakdown is the most important section (not the drop) — treat it with care. Use long,
sweeping movements, rich color evolution, and dramatic reveals. The goal is to make the
audience FEEL something, not just SEE something. Trance is the genre where "less is more"
for effects but "more is more" for emotion.
