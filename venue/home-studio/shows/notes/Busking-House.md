# Show Notes: Busking-House

## Overview
- **Type**: Busking / looping show
- **Venue**: Home Studio
- **Genre**: House (128 BPM)
- **Duration**: 5 minutes (160 bars), loops continuously
- **Generator**: `venue/home-studio/generators/Busking-House.py`

## VC Layout

### Controls
| Button | Function | Color |
|--------|----------|-------|
| FULL SHOW | Plays all 8 sections in order, loops | Green |
| BLACKOUT | All fixtures off | Red |

### Section Triggers (all loop independently)
| Button | Bars | Duration | Color Pair | Character |
|--------|------|----------|------------|-----------|
| INTRO | 16 | 30s | Golden Hour (Warm White + Amber) | Warm wash, center/DJ drift |
| GROOVE BUILD | 16 | 30s | Deep Ocean (Deep Blue + Teal) | Gentle side-to-side, building layers |
| MELODIC RISE | 16 | 30s | Neon Rose (Pink + Magenta) | Wider movement, colors deepening |
| PEAK | 32 | 60s | Sunset + Club Classic | Full sweep SL→SR, prisms, bright |
| EMOTIONAL BREAK | 16 | 30s | Night Sky (Deep Blue + Purple) | Intimate, frost on movers, DJ focus |
| FINAL BUILD | 16 | 30s | Cool Dawn (Cyan + Blue) | Spreading from center, rising intensity |
| PEAK 2 | 32 | 60s | Sunset + Club Classic + Lasers | Widest sweeps, all NI3K lasers, full prism |
| OUTRO | 16 | 30s | Golden Hour (Warm White + Amber) | Return to opening, dimming down |

## Color Palette
Following house genre conventions — warm, flowing, groove-enhancing:
- **Warm White** (255, 180, 100) — foundation, bookends
- **Deep Blue** / BSW Blue — groove sections, breakdowns
- **Magenta** / BSW Magenta — peaks, disco heritage
- **Amber** / Sharpy Amber — warmth, peaks
- **Teal** / BSW Teal — depth, groove
- **Pink** / BSW Pink — melodic moments
- **Cyan** — builds, tech energy
- **Purple** — emotional break

## Movement
All crossfades are 4-bar smooth (7500ms at 128 BPM) — no snaps. House is about flow.
- Intro/Outro: Center ↔ DJ drift
- Groove: Center ↔ SL ↔ SR gentle sway
- Melodic: SL → C → SR → DSC widening
- Peak: Full SL ↔ SR sweep with prisms
- Emotional Break: DJ ↔ C ↔ USC intimate convergence with frost
- Final Build: C → SL → SR → DSC spreading out
- Peak 2: FAR_L ↔ FAR_R widest possible sweep + lasers

## Fixture Roles
- **Sharpy + BSW**: Lead movers, color wheel matching, sweep the room
- **Profile**: Front-facing accent, follows mover positions from audience perspective
- **4BAR + Missyees**: Par wash in the secondary color of each pair
- **NI3K**: Atmospheric fill — halo colors match mood, lasers reserved for Peak 2 only

## Usage Tips
- Start with FULL SHOW for set-and-forget operation
- Tap individual section triggers to jump to a specific vibe
- Section triggers all loop — stay in GROOVE BUILD as long as you want
- BLACKOUT kills everything instantly
- Lasers only fire during PEAK 2 — per house genre convention (peaks only, brief)
