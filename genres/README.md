# Genre Definitions

Each `.md` file in this directory defines the lighting conventions for an EDM subgenre.
These files are read by the **busking** skill when generating busking workspaces, and
can be created/modified by the **genres** skill.

## File Format

Every genre file follows a consistent structure:

- **Overview** — Genre description and character
- **BPM Range** — Typical tempo range
- **Energy Profile** — Table mapping song sections to energy levels and lighting behavior
- **Color Palette** — Primary colors, accent colors, and two-color pairs with specific RGB/BSW/Sharpy values
- **Movement Conventions** — How movers behave in each section
- **Timing Presets** — Named timing values (FadeIn/Hold in ms) calibrated to the genre's BPM
- **Strobe Conventions** — When and how to use strobes
- **Laser Conventions** — When and how to use NI3K lasers
- **Gobo & Prism Conventions** — Beam effect usage per section
- **Par Behavior** — Par wash/gradient/chase patterns per section
- **Key Philosophy** — The one-paragraph summary of the genre's lighting approach

## Available Genres

| File | Genre | BPM | Character |
|------|-------|-----|-----------|
| drum-and-bass.md | Drum & Bass | 170–180 | Aggressive contrast, dark breakdowns, explosive drops |
| dubstep.md | Dubstep | 140–150 | Maximum drama, darkness, wobble-synced chaos |
| house.md | House | 120–130 | Warm, flowing, groove-based, smooth transitions |
| techno.md | Techno | 125–145 | Minimal, geometric, stark, darkness as design |
| trance.md | Trance | 130–150 | Emotional journey, euphoric, sweeping, color evolution |

## Usage

The busking skill reads the genre file to determine:
1. Which two-color pairs to generate as busking buttons
2. Default timing values for chaser speed presets
3. Strobe/laser conventions for effect buttons
4. Par wash patterns for color scenes

Use the **genres** skill to create new genres or edit existing ones.
