# Genre Definitions

Each `.md` file in this directory defines the lighting conventions for an EDM subgenre.
These files are read by the **busking** skill when generating busking workspaces, and
can be created/modified by the **genres** skill.

## File Format

Every genre file follows a consistent structure:

- **Overview** — Genre description and character
- **BPM Range** — Typical tempo range with timing reference calculations
- **Energy Profile** — Table mapping song sections to energy levels and lighting behavior
- **Color Palette** — Primary colors, accent colors, and two-color pairs with specific RGB/BSW/Sharpy/Profile values
- **Movement Conventions** — How movers behave in each section
- **Timing Presets** — Named timing values (FadeIn/Hold in ms) calibrated to the genre's BPM
- **Strobe Conventions** — When and how to use strobes
- **Laser Conventions** — When and how to use NI3K lasers
- **Gobo & Prism Conventions** — Beam effect usage per section
- **Par Behavior** — Par wash/gradient/chase patterns per section
- **Fixture Layering** — How different fixture types (beams, washes, spots, pars) work together per section
- **Haze & Atmosphere** — Haze density requirements per section and beam interaction notes
- **Venue Scale Notes** — How conventions change between club and festival scale
- **Notable References** — Real LDs, shows, venues, and techniques that exemplify the genre
- **Key Philosophy** — The one-paragraph summary of the genre's lighting approach

## Available Genres

| File | Genre | BPM | Character |
|------|-------|-----|-----------|
| drum-and-bass.md | Drum & Bass | 170–180 | Aggressive contrast, dark breakdowns, explosive drops, snare-synced accents |
| dubstep.md | Dubstep | 140–150 | Maximum drama, darkness, wobble-synced chaos, half-time feel |
| future-bass.md | Future Bass | 140–160 | Neon bright, emotional builds, vivid RGB, kawaii-meets-festival |
| hardstyle.md | Hardstyle | 150–160 | Theatrical drama, synchronized impact, kick-synced, pyro-equivalent moments |
| house.md | House | 120–130 | Warm, flowing, groove-based, disco heritage, par-led, sidechain breathing |
| liquid-dnb.md | Liquid DnB | 170–178 | Warm, atmospheric, emotional, smooth movements, blue-amber palette |
| melodic-techno.md | Melodic Techno | 120–128 | Emotional storytelling, Afterlife aesthetic, warm-cool gradients, restrained beauty |
| psytrance.md | Psytrance | 138–150 | UV-reactive, sacred geometry, fractals, hypnotic repetition, psychedelic colors |
| techno.md | Techno | 125–145 | Minimal, geometric, stark, darkness as design, beam architecture, restraint |
| trance.md | Trance | 130–150 | Emotional journey, euphoric releases, laser cathedral, sweeping movements |

## Usage

The busking skill reads the genre file to determine:
1. Which two-color pairs to generate as busking buttons
2. Default timing values for chaser speed presets
3. Strobe/laser conventions for effect buttons
4. Par wash patterns for color scenes
5. Fixture layering hierarchy for scene design
6. Haze density targets per section

Use the **genres** skill to create new genres or edit existing ones.
