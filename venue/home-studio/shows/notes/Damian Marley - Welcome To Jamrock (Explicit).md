# Show Notes: Damian Marley - Welcome To Jamrock (Explicit)

## Creative Brief

Reggae/dancehall track with a menacing, heavy energy. Iconic siren intro. The lighting
leans into Rastafarian culture with a red/gold/green palette. Movers PULSE to the bass —
snap bright on each bass onset, then smooth-fade back to dim over the next beat. Between
pulses, movers drift slowly between positions with smooth crossfades. Pars provide constant
rhythmic energy with a crisp beat-synced chase pattern.

**Architecture**: Split-chaser design. Movers and pars run as two parallel chasers bundled
in a QLC+ Collection (one-button playback). This allows independent FadeIn timing: movers
use smooth crossfades (FadeIn=779ms) for pulse decay and position drift, while pars use
instant snaps (FadeIn=0) for crisp chase patterns.

## Color Palette

- **Rasta Red** (255, 0, 0) — fire, intensity
- **Rasta Gold** (255, 200, 0) — warmth, sunshine
- **Rasta Green** (0, 255, 0) — nature, life
- Colors cycle through all fixtures on a 3-beat rotation

### Mover Color Wheel Mapping

| RGB Color | Sharpy (Ch8) | BSW (Ch8) | Profile (Ch5) |
|-----------|-------------|-----------|---------------|
| Red | 10 | 20 | 5 |
| Gold | 20 (yellow) | 32 (yellow) | 10 (yellow) |
| Green | 40 | 38 | 20 |

## Fixture Roles

- **Sharpy + BSW + Profile (movers)**: Bass-reactive PULSE. On bass beats, snap bright
  (FadeIn=0). On non-bass beats, smooth crossfade back to dim base level (FadeIn=779ms),
  creating a visible pulse decay. Position drift happens via the same smooth crossfades —
  positions change every 8 beats (~2 bars). Gobos and prisms added in choruses.
  Runs in its own dedicated chaser for independent fade timing.
- **4BAR + Missyees (pars)**: Constant beat-synced chase with instant snaps (FadeIn=0).
  One par lit per beat, cycling through Rasta colors. Missyees alternate on even/odd beats.
  Intensity builds per section. Runs in its own dedicated chaser for crisp timing.
- **NI3K**: OFF for entire show. Clean mover + par aesthetic.

## Movement & Positions

Movers drift slowly between positions, changing every 8 beats (~2 bars):

- **Intro**: C → SL → C → SR → C (conservative, centered)
- **Verses**: C → SL → SR → DSC → C → USL → USR → C (wider exploration)
- **Choruses**: DSC → SL → SR → DSL → DSR → C → DSC → SL (audience-facing, energetic)
- **Outro**: C → SL → C → SR → C → USC → C (return to center, winding down)

## Section Breakdown

### Intro (0:00 - 0:29, 38 beats)
- Siren intro + first verse establishing
- Pars build from dim (master 80) up to moderate (200)
- Movers start dark (dim=0), flash dim on bass hits (building from 80 to 200)
- Heavy frost (200) for diffuse atmosphere
- 15 bass hits — scattered, building

### Verse 2 (0:29 - 0:45, 19 beats)
- Groove established, consistent vibe
- Movers have subtle base glow (dim=40), flash to 220 on bass
- Frost reduced to 150
- Pars at master 200

### Verse 3 (0:45 - 1:08, 31 beats)
- Building toward first chorus
- Movers brighter base (dim=60), flash to 240
- Frost 100, sharper beams emerging
- Pars at master 220

### Chorus 1 (1:08 - 1:22, 18 beats)
- "WELCOME TO JAMROCK" — first energy peak
- Movers base dim=80, flash to full 255
- No frost, sharp beams
- BSW gobo 3 added for texture
- Pars at full master 255

### Verse 4 (1:22 - 2:00, 47 beats)
- Longest section, pull back from chorus energy
- Movers dim=50, flash to 220
- Frost back to 120 for softer feel
- Pars at 180

### Verse 5 (2:00 - 2:25, 33 beats)
- Rebuilding toward second chorus
- Movers dim=70, flash to 240
- Frost 60, getting sharp again
- Pars at 220

### Chorus 2 (2:25 - 2:49, 30 beats)
- Big chorus — gobos AND prisms on all movers
- Sharpy prism 1 on (128) + spinning (200)
- BSW prism on (80) + spinning (180)
- Profile prism (60)
- Movers dim=100, flash to 255
- Pars full blast 255

### Chorus 3 (2:49 - 3:03, 17 beats)
- PEAK energy — everything maxed
- Wider prisms (BSW 128/200, Profile 80)
- BSW gobo 5 for aggressive pattern
- Movers dim=120 base, flash to 255
- Pars full 255

### Outro (3:03 - 3:28, 33 beats)
- Progressive decay — all values dim over time
- Par master fades from 220 down to 60
- Mover flash dims from 200 down to 80
- Frost increases back to heavy (200+)
- Returns to atmospheric, diffuse feel

### End (3:28 - 3:33)
- Snap to full blackout
- 4-beat hold on black

## Key Techniques

- **Split-chaser pulse architecture**: Two parallel chasers (movers + pars) in a Collection.
  Movers use smooth FadeIn (779ms) for pulse decay and drift. Pars use instant FadeIn (0ms)
  for crisp chase. This solves the QLC+ limitation of one FadeIn per step affecting all fixtures.
- **Bass-reactive mover pulse**: 109 bass onsets quantized to nearest beat. On bass beats,
  movers snap to flash brightness (FadeIn=0). On the next non-bass beat, smooth crossfade
  (FadeIn=779ms) fades the dimmer back down — creating a visible pulse that decays over ~0.8s.
  Consecutive bass hits stay bright (no decay between them).
- **Smooth position drift**: Non-bass beats use FadeIn=779ms, which also smoothly crossfades
  pan/tilt values between positions. Movers glide between focus points rather than snapping.
- **3-color cycling**: All fixtures cycle R/G/Y on a 3-beat rotation, creating a constantly
  shifting tricolor pattern that never repeats the same way.
- **Progressive frost**: Intro uses heavy frost (200) for atmosphere, gradually sharpens
  through sections, choruses have no frost for maximum beam punch.
- **Energy envelope**: Intro builds from near-dark, choruses peak, outro decays — the
  show breathes with the song structure.
- **Par chase as heartbeat**: 4BAR one-par-at-a-time chase provides constant rhythmic pulse
  even when movers are dark between bass hits.

## Stats

- 289 unique scenes (246 dedup reuses)
- 274 steps per chaser (2 chasers + 1 Collection)
- 117 snap beats (bass pulses + blackouts), 157 smooth beats (pulse decay + drift)
- 109 bass-triggered mover pulses across 270 beats (40% hit rate)
- Duration: 213.4s matching song length
- BPM: 77 (reggae half-time feel)
