# Tvboo - Fixin's — Show Design Notes

## Overview
- **BPM**: 144
- **Duration**: ~3:25 (116 bars)
- **Genre**: Dirty bass / riddim
- **Generator**: `generators/Tvboo - Fixin's.py`
- **Output**: `shows/Tvboo - Fixin's.qxw`
- **Run Order**: SingleShot
- **Analysis**: `songs-data/Tvboo - Fixin's.json` (BPM corrected from 72 half-time to 144)

## Creative Brief
- **FIRE & ICE** palette: red/orange/amber vs blue/cyan/white
- Every beat gets a par change — flashing constantly
- Full send strobes on ALL fixtures during drops
- Lasers: strobe during builds, solid ON during drops
- NI3K tilts: full chaos (auto-rotating) whenever beat is going, positioned on breakdowns
- Back wall movers (Sharpy + BSW) aimed towards front/audience
- Front mover (Profile) aimed towards back wall
- Sweeping movements on breakdowns, fast repositioning on drops
- Go BIG on drops — prisms, gobos, strobes, lasers, everything

## User Creative Choices
- Palette: **Fire & ice** (from 4 options)
- Strobe level: **Full send** — strobes on every drop beat
- Lasers: **Strobe on builds / solid on drops**
- NI3K tilts: **Full chaos** — auto-rotating tilts in 130-180 DMX range

## Color Palette

### Fire Colors (RGB for pars)
| Name | RGB | Usage |
|------|-----|-------|
| Fire Red | (255, 0, 0) | Primary fire |
| Fire Orange | (255, 80, 0) | Fire accent |
| Fire Amber | (255, 140, 0) | Fire warm |
| Fire White | (255, 200, 120) | Warm white |

### Ice Colors (RGB for pars)
| Name | RGB | Usage |
|------|-----|-------|
| Ice Blue | (0, 40, 255) | Primary ice |
| Ice Cyan | (0, 255, 200) | Ice accent |
| Ice White | (180, 220, 255) | Cool white |
| Ice Teal | (0, 200, 180) | Ice secondary |

### Combined Rotation
- **ALL_COLORS**: Fire Red → Ice Blue → Fire Orange → Ice Cyan → Fire Amber → Ice White (6-color alternating)

### Mover Color Mapping
| Palette | BSW Wheel | Sharpy Macro | Profile Wheel | NI3K Halo |
|---------|-----------|--------------|---------------|-----------|
| Fire[0] | BSW_RED | SHARPY_RED | PROF_RED | H_RED |
| Fire[1] | BSW_ORANGE | SHARPY_ORANGE | PROF_ORANGE | H_RED |
| Fire[2] | BSW_YELLOW | SHARPY_YELLOW | PROF_YELLOW | H_YEL |
| Fire[3] | BSW_WHITE | SHARPY_WHITE | PROF_WHITE | H_RGB |
| Ice[0] | BSW_BLUE | SHARPY_BLUE | PROF_BLUE | H_BLU |
| Ice[1] | BSW_TEAL | SHARPY_TEAL | PROF_TEAL | H_CYN |
| Ice[2] | BSW_WHITE | SHARPY_WHITE | PROF_WHITE | H_RGB |
| Ice[3] | BSW_TEAL | SHARPY_TEAL | PROF_TEAL | H_CYN |

## Fixture Roles
- **Sharpy + BSW**: Back wall movers aimed FORWARD toward audience. Fast repositioning on drops.
- **Profile**: Front center aimed BACKWARD toward back wall. Counter-direction to back movers.
- **4BAR (ID 2)**: Fire/ice flashing. chase, pairs, solid, alternating, and gradient patterns.
- **Missyee 1+2**: Extend 4BAR — alternate on even/odd beats, or split fire/ice.
- **NI3K (ID 3)**: Tilts auto-rotating on drops (130-180 range). Positioned (64) on breakdowns. Halo matches palette. Lasers strobe during builds, solid ON during drops.

## Movement Positions (8 named positions)
All positions designed so back movers face forward and Profile faces backward.

| Key | Sharpy | BSW | Profile | Description |
|-----|--------|-----|---------|-------------|
| C | 153, 0 | 7, 19 | 0, 123 | All center |
| FL | 120, 15 | 40, 25 | 30, 140 | Front left area |
| FR | 190, 15 | 200, 10 | 220, 140 | Front right area |
| W | 100, 20 | 210, 10 | 40, 100 | Wide spread |
| AUD | 153, 40 | 7, 45 | 0, 150 | Audience (fwd+down / back+up) |
| X | 100, 10 | 200, 10 | 200, 130 | Crossed beams |
| FAN | 80, 25 | 220, 25 | 0, 90 | Fanned out wide |
| UP | 153, 230 | 7, 0 | 0, 170 | Aimed up/back at ceiling |

### Position Sequences
- **POS_DROP** (8): C, FL, FR, W, X, AUD, FAN, C — standard drop movement
- **POS_SWEEP** (4): FL, C, FR, C — smooth breakdown sweeps
- **POS_BIG** (16): Full cycle — maximum variety for biggest drops

## Section-by-Section Breakdown

### Intro/Build (16 bars, 48 steps)
- **Bars 1-8** (16 steps, 2-beat each): Ice establishing. Pairs pattern building from dim (master 80→224). Movers sweeping slowly through POS_SWEEP with heavy frost (200→80). Fire starts creeping in at bars 7-8.
- **Bars 9-16** (32 steps, 1-beat each): Pars every beat, fire/ice chase. Movers de-frosting. NI3K tilts start rotating (bars 13+). Laser strobe teasing (bars 15-16, blue laser first, then red joins).

### DROP 1 (16 bars, 64 steps)
- **FULL SEND**. Fire & ice alternating every beat.
- Par chase pattern, full brightness (master 255).
- All movers: SHARPY_STROBE_FAST + BSW_SHUT_STROBE_FAST. Prisms on (Sharpy 128, BSW 80, Profile 60).
- NI3K: full chaos tilts (140-185 range), ALL 3 lasers ON, jump_fast halo.
- Positions cycle POS_DROP every bar.
- Palette alternates fire/ice every beat.

### DROP 1 Continued (8 bars, 32 steps)
- Same energy, switch to **alternating solid hits** (whole par wall fire then ice).
- **Double prism** on Sharpy (prism1 + prism2 both 128). BSW gobo G1_3.
- Different position offset for variety.
- Lasers remain ON.

### Breakdown 1 (8 bars, 16 steps)
- **Ice only**. Pars every 2 beats (pairs pattern).
- Movers frosted (180), slow sweep through POS_SWEEP. Smooth crossfades.
- Kill lasers. NI3K tilts positioned (64). Soft sync halo.
- Par master building (140→220).

### DROP 2 (8 bars, 32 steps)
- **Fire dominant**: 3 fire beats to 1 ice.
- Positions from POS_BIG. Different from Drop 1.
- Full strobes + prisms. All lasers ON.
- NI3K tilts chaos (135-195 range).

### Breakdown 2 (16 bars, 48 steps)
- **First 8 bars** (16 steps, 2-beat each): Slow ice wash. Gradient pars. Smooth crossfades. Movers frosted. Laser strobe tease starts bar 5 (blue first, red joins bar 7).
- **Last 8 bars** (32 steps, 1-beat each): Building tension. Fire creeps back in. Pars accelerate to every beat. Movers de-frost. Strobe buildup (bars 7-8 get SHARPY_STROBE_SLOW). NI3K tilts start rotating again (bar 5+). Laser strobe accelerating.

### DROP 3 (8 bars, 32 steps)
- **BIGGEST DROP**. Position changes EVERY BEAT (POS_BIG[beat]).
- Solid par walls alternating fire/ice.
- **Double prism** on Sharpy. BSW prism=128. Profile prism=120. BSW gobo G1_4.
- All strobes fast. All lasers ON. NI3K chaos tilts + jump_fast halo.

### DROP 3 Continued (8 bars, 32 steps)
- Sustained mayhem. Different gobo (G1_5).
- par_alternating (Fire Red vs Ice Blue solid walls).
- Position offset by 8 from Drop 3 for fresh movement.

### FINAL DROP (8 bars, 32 steps)
- **MAXIMUM EVERYTHING**.
- **White blast** on every downbeat (beat 1 of each bar): all movers go white with double prism + BSW gobo G1_3. Other beats alternate fire/ice.
- BSW gobo G1_6. All prisms maxed.
- NI3K tilts highest chaos (160-210 range). All lasers ON.

### Outro (8 bars, 16 steps)
- Cool down to ice. Pars every 2 beats, fading (master 180→20).
- Movers converging to center: W→FR→FL→C→C→C→C→C.
- Re-frosting (80→200). Kill lasers. NI3K settling (dim fading).
- Smooth crossfades.

### Fade Out (12 bars + blackout, 13 steps)
- Very slow fade. 4-beat smooth crossfades.
- Bars 1-8: Everything dimming to near-zero. Blue tinge.
- Bars 9-12: Only NI3K halo fading (blue). All other fixtures dark.
- Final blackout.

## Key Techniques
- **Scene deduplication**: 365 unique scenes, 0 reuses (every beat is unique due to varied positions + colors + tilt values).
- **Directional movers**: Back wall fixtures (Sharpy, BSW) always face forward. Profile always faces backward. Creates crossing beams.
- **Fire/ice palette system**: `mk_movers(palette="fire"/"ice", color_idx=N)` automatically picks correct BSW/Sharpy/Profile color from parallel arrays.
- **Smooth vs snap steps**: `smooth_step()` for breakdowns (FadeIn=duration), `beat_step()` for drops (FadeIn=0, instant snap).
- **Laser escalation**: OFF → strobe slow → strobe fast → solid ON across build sections.
- **NI3K tilt chaos**: Values in 130-180 DMX range trigger auto-rotation. Per-beat variation in t1/t2/t3 creates unpredictable multi-axis rotation.
- **White downbeat blast**: Final drop beats with bib==0 bypass mk_movers() to manually set BSW_WHITE + SHARPY_WHITE + PROF_WHITE for maximum impact.

## Custom VC Layout
- ▶ FIXIN'S (toggle, fire orange #FF4400, 470×100)
- BLACKOUT (toggle, red, 470×80)

## Stats
- 365 unique scenes (0 reuses), 365 chaser steps + 1 blackout
- Total: 193.8s (116.3 bars), target ~205s (3:25)
