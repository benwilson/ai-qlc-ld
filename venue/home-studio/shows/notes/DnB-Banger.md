# DnB Banger — Show Notes

## Creative Brief
High-energy generic DnB show at 174 BPM. Maximum visual impact with beat-level scene changes across every section. Not synced to a specific song — designed as a loopable or one-shot party piece that follows standard DnB structure.

## BPM & Timing
- **174 BPM** — 345ms per beat, 1379ms per bar
- Beat-level snaps in drops (every 345ms = new look)
- 2-beat steps in builds (~690ms)
- 1-bar smooth crossfades in breakdown/outro (~1379ms)

## Structure (72 bars, ~99s)

| Section | Bars | Beats | Energy | Palette | Key Technique |
|---------|------|-------|--------|---------|---------------|
| Intro | 8 | 32 | Low→Med | Dark red | A/B pulse on each beat, movers center |
| Build 1 | 8 | 16 (2-beat steps) | Rising | Red→Amber | Movers cycle positions, intensity ramps 80→255 |
| Drop 1 | 16 | 64 | Peak | Red/Amber/Orange | Beat snaps, prisms, red lasers, par chase |
| Breakdown | 8 | 8 (bar steps) | Low | Deep blue | Smooth crossfade sweep, frost on movers |
| Build 2 | 8 | 16 (2-beat steps) | Rising | Blue→Cyan→Purple | Color transition, prisms build in |
| Drop 2 | 16 | 64 | Peak+ | Blue/Cyan/Purple | All lasers, dual prisms, gobo rotation, BSW strobe hits |
| Outro | 8 | 8 (bar steps) | Falling | Blue fade | Converge to center, dim to black |

## Color Palettes

### Drop 1 — Fire
- Sharpy: Red, Amber, Orange, Yellow cycle
- BSW: Red, Orange, Yellow cycle
- Profile: Alternating Red/Orange
- 4BAR: Hot red-orange / amber / pure red / yellow-amber chase
- NI3K: Red LED, red laser only, halo red/yellow alternate
- Missyee: Red-orange / red split

### Drop 2 — Electric
- Sharpy: Blue, Purple, Teal, Pink cycle
- BSW: Blue, Magenta, Teal, Pink cycle
- Profile: Blue / Teal alternate
- 4BAR: Pure blue / cyan / purple / magenta chase
- NI3K: Blue LED, ALL lasers on, halo blue/pink alternate
- Missyee: Blue / purple split

### Breakdown — Deep
- All fixtures: Deep blue, dimmed (60-100), frosted movers

## Fixture Roles

| Fixture | Role |
|---------|------|
| Sharpy | Lead mover — position snaps, color changes, prism1 (drop1), prism1+2 (drop2) |
| BSW | Support mover — mirrors Sharpy positions, gobo accents every 4 beats, strobe hits in drop2 |
| Profile | Fill/spot — front-facing, alternating colors, steady open shutter |
| 4BAR | Color chase — 4 colors cycling 1 position per beat across the 4 pars |
| Missyee x2 | Accent — split colors alternating with par chase |
| NI3K | Chaos engine — tilts in rotation mode, lasers on in drops, halo color pulse |

## Movement Positions
All positions from verified focus-positions.md. Drops cycle through 16-position patterns per 16 beats:

**Drop 1**: DSC → SL → SR → C → DSL → DSR → CEIL → C → SWEEP_L → C → SWEEP_R → C → SL → SR → DSC → DJ

**Drop 2**: C → DSR → DSL → CEIL → SR → SL → DSC → C → SWEEP_R → C → SWEEP_L → DJ → DSC → CEIL → C → DSC

## Virtual Console Layout
- **FULL SHOW** (big green button) — runs entire 72-bar sequence
- **Section buttons** — each section individually triggerable
- **BLACKOUT** (red) — emergency kill

## Effects Detail

### Prisms
- Drop 1: Prism1 on for 4-beat blocks, off for 4 (50% duty cycle)
- Drop 2: Prism1 on 75% of beats. Prism2 added from beat 32 onward (second half escalation)

### NI3K Tilts
All three tilt heads use rotation mode (values 150-220) with different modulation rates per head, creating organic multi-arm spinning patterns. Each beat produces unique tilt combinations.

### Lasers
- Drop 1: Red laser only (NI3K)
- Drop 2: All three lasers (RGB) — maximum visual density
- Breakdown/Builds: Lasers off

### Strobes
- BSW gets strobe hits every 8th beat in the second half of Drop 2
- No sustained strobe — flashes only

## Generator
`venue/home-studio/generators/DnB-Banger.py`

179 scenes, 8 chasers (416 total steps). Beat-level dedup unlikely due to unique NI3K tilt modulation per beat.
