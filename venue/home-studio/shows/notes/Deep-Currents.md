# Deep Currents — Show Design Notes

## Overview
- **BPM**: 128
- **Duration**: ~2:00 (64 bars), looping
- **Genre**: Ambient / deep electronic
- **Generator**: `generators/gen_deep_currents.py`
- **Output**: `shows/Deep-Currents.qxw`
- **Run Order**: Loop (seamless — scene 32 matches scene 0)

## Creative Brief
- Cool & deep palette: blues, teals, cyans, purples
- Multiple energy waves (2 peaks with valleys between)
- Leader/follower mover relationship (BSW leads, Sharpy follows one position behind)
- NI3K: 2 dramatic reveals at surprising moments (NOT at peaks)
- Snap types: position snaps, white flash bursts, gobo/color punches
- Static fixtures (4BAR, Missyees): unified wash throughout
- Gobos/prisms: sparingly, only at peak energy

## Color Palette
| Name | RGB | Usage |
|------|-----|-------|
| Deep Blue | (0, 0, 180) | Primary wash, emergence |
| Dim Blue | (0, 0, 80) | Low-energy sections |
| Wash Teal | (0, 180, 128) | Swell sections, energy building |
| Wash Cyan | (0, 220, 255) | Peak moments, flash accent |
| Wash Purple | (80, 0, 180) | Valley/retreat, gobo punch |
| Build Cyan | (0, 80, 120) | Second build ramp |

### Mover Color Mapping
- BSW: Blue → Teal → Magenta → White (follows palette shifts)
- Sharpy: SHARPY_BLUE → SHARPY_TEAL → SHARPY_PURPLE → SHARPY_WHITE
- Profile: PROF_BLUE → PROF_TEAL → PROF_PINK → PROF_WHITE

## Fixture Roles
- **BSW (ID 1)**: Leader mover. Enters first, sets movement direction. Sweeps R→L across 5 named positions.
- **Sharpy (ID 8)**: Follower mover. Enters one step behind BSW. Mirrors BSW's sweep one position delayed.
- **Profile (ID 4)**: Independent. Subtle movement from front center. First appearance delayed to Valley section for dramatic reveal.
- **4BAR (ID 2)**: Unified wash. Mostly solid colors matching palette. Inner-par-only for emergence.
- **Missyee 1+2 (ID 5, 6)**: Extend 4BAR wash. Sometimes split (one on, one off) for directional feel.
- **NI3K (ID 3)**: Two surprise reveals — atmospheric during build (Reveal #1), explosive during breakdown (Reveal #2).

## Movement Positions
### BSW (back right, center pan=7)
- BSW_R (240, 25) → BSW_CR (250, 22) → BSW_C (7, 19) → BSW_CL (25, 15) → BSW_L (45, 10)

### Sharpy (back left, center pan=153)
- SH_R (100, 5) → SH_CR (125, 3) → SH_C (153, 0) → SH_CL (180, 253) → SH_L (210, 250)

### Profile (front center, center pan=0)
- PR_SL (245, 125) → PR_C (0, 123) → PR_SR (10, 121)

## Section-by-Section Breakdown

### Section 1: Emergence (bars 1-8, 4 scenes)
- Fixtures fade in one by one over 8 bars
- S0: Single missyee, dim blue. All movers pre-positioned but dark.
- S1: Both missyees + 4BAR inner pars
- S2: Full wash blue. BSW enters from right (dim 180).
- S3: BSW at center-right. Sharpy enters from right (dim 120), following BSW.
- Timing: 4 steps × smooth 2-bar crossfades

### Section 2: First Swell (bars 9-16, 4 scenes)
- Rising energy. Wash shifts blue → teal.
- S4-S5: BSW sweeps center→left, Sharpy follows center-right→center
- S6: **POSITION SNAP** — movers jump to opposite sides, cyan flash on all pars
- S7: Post-snap flow, resume sweep from new positions
- Profile dark throughout (first appearance reserved for Valley)
- Timing: smooth 2-bar, smooth 1.5-bar, SNAP 0.5-bar, smooth 4-bar

### Section 3: Valley (bars 17-24, 4 scenes)
- Energy drops. Fixtures peel away one by one.
- S8: Wash dims to purple, Sharpy fading. Profile enters at dim 80.
- S9: BSW alone + dim purple pars. Profile gone.
- S10: BSW fades out, **Profile appears** as solo — first real profile moment.
- S11: Near darkness — just Profile thin beam + one dim missyee.
- Timing: 4 steps × smooth 2-bar crossfades

### Section 4: Second Build (bars 25-34, 5 scenes)
- Fixtures rejoin in leader/follower chain.
- S12: Pars back in cyan, Profile sweeping.
- S13: BSW follows Profile.
- S14: All 3 movers in leader/follower chain.
- S15: **NI3K REVEAL #1** — fades in with blue/purple glow and cyan halo. No lasers. Other fixtures continue sweep. Atmospheric, not explosive.
- S16: NI3K intensifies. All movers building.
- Timing: 5 steps × smooth 2-bar crossfades

### Section 5: Second Peak (bars 35-42, 5 scenes)
- Biggest moment. Everything bright.
- S17: Full bloom — everything bright cyan.
- S18: **WHITE FLASH** — all fixtures blast white via color, not strobe channels. Snap timing creates burst feel without strobe crossfade artifacts.
- S19: **Prism fracture** — BSW prism on, movers crossing.
- S20: **GOBO PUNCH** — gobo + purple shift, movers snap to new positions.
- S21: Riding out — back to flowing teal.
- Timing: smooth 1.5, SNAP 0.5, smooth 2, SNAP 1, smooth 3

### Section 6: Breakdown (bars 43-52, 5 scenes)
- Energy drains to near darkness.
- S22-S23: Pulling back, NI3K fading.
- S24: Near dark — one dim missyee only.
- S25: Total silence — single 4BAR par, dim purple.
- S26: **NI3K REVEAL #2** — everything dark, NI3K takes over completely. All 3 lasers ON, halo RGB cycling, bright blue-white RGBW. Tilts spread (80, 40, 100) for maximum room coverage.
- Timing: 4 × smooth 2-bar, SNAP 2-bar for NI3K takeover

### Section 7: Return & Loop (bars 53-64, 6 scenes)
- Rebuild from blackout back to opening state.
- S27: Blackout breath — total darkness after NI3K cuts.
- S28: Pars fade back in blue.
- S29: BSW returns, slow sweep from right.
- S30: All movers rejoin, leader/follower rebuilding.
- S31: Settling — dimming, movers centering.
- S32: **Loop point** — matches S0 exactly for seamless loop.
- Timing: hold 1-bar, then smooth 2-3 bar crossfades

## Key Techniques
- **Dark helpers**: `dark_sharpy()`, `dark_bsw()`, `dark_profile()` keep shutter/strobe at "open" so crossfades don't pass through strobe ranges.
- **White flash via color**: S18 uses BSW_WHITE + full RGB instead of strobe channels to avoid crossfade artifacts.
- **NI3K reveal timing**: Both reveals happen at unexpected moments (mid-build and breakdown) rather than at obvious peaks.
- **Leader/follower**: BSW always arrives at a position first, Sharpy follows 1 step behind.
- **Seamless loop**: S32 values match S0 exactly. Chaser run_order=Loop.

## Stats
- 34 scenes, 33 chaser steps
- Total: 120.0s (64.0 bars)
