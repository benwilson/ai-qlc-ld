# BPM Timing Reference

## Conversion Formula

```
beat_ms = 60000 / BPM
bar_ms = beat_ms * 4       (for 4/4 time)
```

## Common BPM Timing Tables

### 120 BPM (House, Pop, EDM)

| Division | ms |
|----------|-----|
| 1/4 beat (1/16th note) | 125 |
| 1/2 beat (1/8th note) | 250 |
| 1 beat | 500 |
| 2 beats | 1000 |
| 1 bar | 2000 |
| 2 bars | 4000 |
| 4 bars | 8000 |
| 8 bars | 16000 |

### 140 BPM (Trance, Techno)

| Division | ms |
|----------|-----|
| 1/4 beat | 107 |
| 1/2 beat | 214 |
| 1 beat | 429 |
| 2 beats | 857 |
| 1 bar | 1714 |
| 2 bars | 3429 |
| 4 bars | 6857 |
| 8 bars | 13714 |

### 174 BPM (Drum & Bass, Jungle)

| Division | ms |
|----------|-----|
| 1/4 beat | 86 |
| 1/2 beat | 172 |
| 1 beat | 345 |
| 2 beats | 690 |
| 1 bar | 1379 |
| 2 bars | 2759 |
| 4 bars | 5517 |
| 8 bars | 11034 |

### 90 BPM (Hip-Hop, Downtempo)

| Division | ms |
|----------|-----|
| 1/4 beat | 167 |
| 1/2 beat | 333 |
| 1 beat | 667 |
| 2 beats | 1333 |
| 1 bar | 2667 |
| 2 bars | 5333 |
| 4 bars | 10667 |
| 8 bars | 21333 |

## Genre-Specific Chaser Patterns

### Drum & Bass (170-180 BPM)

DnB has distinct sections: drops, rolling bass, breakdowns, and builds. Lighting should match the energy.

**High energy (drops)**: Use 1/8th or 1/16th note timing with Loop or PingPong. Simple, high-contrast color pairs (red/black, white/black). Strobe-like effects work well — alternate between a bright scene and blackout.

**Rolling bass**: Use 1-bar or 2-bar PingPong timing. Deep blues, purples, and cyans. Smooth color transitions create the "rolling" feel. Consider lighting individual pars in sequence for movement.

**Color shifts**: 2-4 bar Loop timing. Full spectrum transitions. Work well during melodic sections or intros. Rainbow cascades and warm-to-cool shifts.

**Breakdowns/quiet moments**: 4-8 bar PingPong for gentle breathing. Warm ambers, soft whites, muted tones. Single-color fades give a meditative feel.

**Builds**: SingleShot run order. Progressively add pars (1 → 2 → 3 → 4), increase brightness, or accelerate timing. Strobe acceleration (PerStep timing from 1 bar down to 1/4 beat) is classic for DnB builds.

### House/Techno (120-140 BPM)

**Drops**: 1/4 or 1/2 beat strobes. Bold primary colors.

**Grooves**: 1-beat or 2-beat timing. Warm colors for deep house, cold neon for tech house.

**Breakdowns**: 2-4 bar slow transitions. Moody, atmospheric colors.

**Builds**: 4-bar to 8-bar SingleShot sequences building intensity.

### Hip-Hop/R&B (80-100 BPM)

**Verses**: 2-bar to 4-bar slow color shifts. Rich purples, deep reds, golds.

**Choruses**: 1-bar timing, brighter colors, more movement between pars.

**Drops/hits**: Short flash effects on accents. SingleShot bursts.

## Chaser Design Templates

### Strobe Snap (high energy)
- Timing: 1/16th note (shortest subdivision)
- RunOrder: Loop
- Steps: Bright scene → Blackout → repeat
- Effect: Rapid strobe-like flashing

### Color Bounce (medium energy)
- Timing: 1/2 beat
- RunOrder: PingPong
- Steps: Color A → Color B → (reverses)
- Effect: Smooth bouncing between two colors

### Par Chase (movement)
- Timing: 1 beat
- RunOrder: Loop
- Steps: P1 only → P2 only → P3 only → P4 only
- Effect: Light appears to move across the stage

### Slow Breathe (ambient)
- Timing: 4 bars
- RunOrder: PingPong
- FadeIn: 50% of duration
- Steps: Dim warm → Bright warm → (reverses)
- Effect: Gentle pulsing glow

### Build Up (SingleShot)
- RunOrder: SingleShot
- Steps: 1 par dim → 2 pars medium → 3 pars bright → all pars full → strobe
- Effect: Progressive intensity build, play once

### Accelerating Strobe (PerStep build)
- SpeedModes Duration: PerStep
- RunOrder: SingleShot
- Step holds: 1 bar → 2 beats → 1 beat → 1/2 beat → 1/4 beat
- Effect: Strobe speeds up, great for builds before drops
