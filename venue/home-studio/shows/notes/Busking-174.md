# Busking-174 Show Notes

## Creative Brief

High-energy party DnB busking file at 174 BPM. Designed for live triggering — no song sync, just hit buttons to match whatever's playing. Bright neon palette, big movements, crowd energy.

## Color Palette

- **Neon Pink** (255, 20, 100) — party energy, drops
- **Neon Green** (0, 255, 80) — contrast with pink
- **Neon Blue** (0, 80, 255) — rolling bass sections
- **Neon Purple** (180, 0, 255) — breakdowns, atmosphere
- **Hot Orange** (255, 80, 0) — fire looks, aggression
- **Ice White** (200, 220, 255) — clean full-send moments

## VC Layout (18 buttons, 4 columns)

### Column 0 — Looks (warm/bright)
| Button | What It Does |
|--------|-------------|
| Full White | All fixtures white, movers center. Clean reset look. |
| Neon Pink | Pink everywhere. Party starter. |
| Deep Blue | Blue room + all lasers on. Rolling vibe. |
| Green Machine | Green wash + green laser. |
| Fire | Red/orange gradient, movers spread wide. Aggressive. |

### Column 1 — Looks (effects/special)
| Button | What It Does |
|--------|-------------|
| Purple Haze | Crossed movers with prisms spinning. Psychedelic. |
| Ceiling Hit | Beams straight up with gobos. Haze required. |
| Pars Only | Movers off, just par gradient. Low energy. |
| Lasers Only | Everything dark except NI3K lasers. Dark room moment. |
| BLINDER | All fixtures strobe at audience. USE SPARINGLY — 2-4 beats max on drops. |

### Column 2 — Chasers
| Button | Speed | What It Does |
|--------|-------|-------------|
| LR Sweep | 1 bar/pos | Smooth left-right-left mover sweep in cyan/blue. |
| Color Cycle | 1 bar/color | Snap through red→blue→green→pink. Whole room changes. |
| Drop Strobe | 2 beats | Alternating full white / blackout. Medium intensity. |
| Fast Strobe | 1/8 note | Rapid fire strobe. For the heaviest drops only. |
| Cross Beams | 2 bar | Movers swap sides with red/blue split. Dramatic. |

### Column 3 — Chasers + Control
| Button | Speed | What It Does |
|--------|-------|-------------|
| Rolling Bass | 2 bar | Deep blue/purple slow sweep. Movers drift SL→C→SR→C. |
| Par Chase | 1 beat | 4BAR sequential chase with alternating missyees. |
| BLACKOUT | — | Kill everything. |

## Fixture Roles

- **Sharpy + BSW**: Primary movers. Carry color and position for all looks. Cross-beam and sweep duties.
- **Profile**: Front-fill and audience-facing color. Always matches or complements the rear movers.
- **4BAR**: Background color wash. Solid colors for looks, gradients for atmosphere, chase patterns for energy.
- **Missyees**: Accent pars. Often split colors for depth, or matched to 4BAR for unity.
- **NI3K**: Atmosphere and effects. Halo color matches the room mood. Lasers reserved for drops and dark moments.

## Busking Strategy

### Verse / Rolling
Start with **Rolling Bass** or **Pars Only**. Keep it chill, let the music breathe. Add **Deep Blue Lasers** for more intensity without going full send.

### Build
Switch to **LR Sweep** or **Color Cycle** as energy rises. The sweep creates visual momentum. Trigger **Ceiling Hit** for a dramatic pre-drop moment.

### Drop
Hit **Full White** or **Fire** on the 1. Layer **Fast Strobe** or **Drop Strobe** over it. Use **BLINDER** for a 2-beat flash on the biggest hits. **Cross Beams** is great for sustained drops.

### Breakdown
Pull back to **Pars Only** or **Lasers Only**. Dark room moment. Let ears and eyes reset.

### Second Drop
Different color — if first drop was Fire, go **Neon Pink** or **Purple Haze**. Layer **Par Chase** for movement.

## Key Timings (174 BPM)

- 1 beat = 345ms
- 1 bar = 1379ms
- 2 bars = 2759ms
- 1/8 note = 172ms (fast strobe speed)

## Generator

`venue/home-studio/generators/Busking-174.py`
