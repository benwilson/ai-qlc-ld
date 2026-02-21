# Show Notes: Blooom & Wolfy Lights - Born Again

Status: `complete`
BPM: 174 | Duration: 2:42 (~160s / 116 bars) | Venue: home-studio
Genre: Drum & Bass

**Note on BPM**: Analysis pipeline detected 87 BPM (half-time artifact). Actual BPM is 174.
Each 1-bar step in drops = 1.38s (tight DnB pacing). Atmospheric sections use 4-bar steps (5.52s).

---

## Creative Thesis

> Stage an emergence from void — deep violet darkness building through rose and magenta into a blazing white catharsis of rebirth, then letting the violet reclaim what the light revealed.

---

## Color Palette

| Name | Purpose | RGB | Notes |
|------|---------|-----|-------|
| VOID | Verse darkness | 8, 2, 20 | Near-black violet tint |
| VIOLET | Primary colour world | 30, 5, 80 | Deep violet throughout |
| PURPLE | Drop 1 bloom | 60, 10, 120 | Richer purple at peak |
| ROSE | Break transition | 120, 30, 80 | Emotional warmth arriving |
| MAGENTA | Break peak | 160, 20, 100 | Rose-magenta |
| WHITE | Catharsis ONLY (step 12+) | 255, 230, 240 | Warm white — the only time |

Sharpy wheel: `50=purple (SH_PURPLE)`, `60=pink (SH_PINK)`, `0=white (SH_WHITE)`
BSW wheel: `50=magenta`, `62=pink`, `0=white`

**Rule: White appears only at the catharsis moment (DROP_2 steps 12–23). Never before.**

---

## DnB Design Principles

**Chase pattern**: Sharpy leads, BSW follows with 3-step lag.
At 1-bar steps, BSW is ~4 seconds behind Sharpy — two independent beams chasing each other.

**Timing**: `hold(bpm, 1)` at drops = instant snaps, 1-bar holds. No crossfade — DnB stabs.
Atmospheric sections (VERSE/BREAK/BRIDGE) use `smooth(bpm, 4)` = slow crossfades.

**Strobe accents**: Every 8th bar during DROP_1 (bars 7,15,23,31,39).
Every bar during DROP_2 catharsis (steps 12–23 = white blast).

**NI3K**: Heads in rotation mode (t1=t2=t3=160) during all drops — spinning during chaos.
H_PNK halo active from DROP_1 bar 0. Lasers arm at DROP_1 step 20 (bar 20).
H_RGB + all lasers from DROP_2 step 12 (the born-again moment).

---

## Fixture Roles

| Fixture | Role |
|---------|------|
| Sharpy (ID 8) | Lead beam — drives the chase, calls position changes |
| BSW (ID 1) | Chase follower — mirrors Sharpy 3 steps behind |
| Profile (ID 4) | Vocal fill at DSC, dim 5–90 tracking energy |
| 4BAR (ID 2) | Colour world foundation — violet base, rose/white arc |
| Missyees (ID 5, 6) | Ambient colour fill matching palette |
| NI3K (ID 3) | Halo active from DROP_1, lasers from bar 20, H_RGB at catharsis |

---

## Section-by-Section Breakdown

### VERSE — 0:00–0:24 (16 bars, 4 steps × 4 bars)
- Near-black void. Dim arc 20→60.
- Positions: DSC→DSC→C→DSC (nearly still — the void before birth)
- SH_PURPLE, heavy frost (235/210), Profile 5–15 dim
- NI3K dark, halos off, lasers off
- soul() helper — unified movement, smooth(174,4) crossfades

### DROP_1 — 0:24–1:19 (40 bars, 40 steps × 1 bar)
- Chase blast. Dim arc 160→209. Instant 1-bar snaps.
- Sharpy sweeps full room: DSC→C→SL→USR→SR→**DJ**→USL→C→DSR→DSC→SL→SR→USC→**DANCE**→...
- BSW lags 3 steps behind Sharpy — two beams chasing each other across the stage
- DJ at steps 5, 25 — performer focus moments at energy peaks
- DANCE at steps 13, 33 — audience floor hits when energy pushes outward
- Frost tightens 175→125 (beams sharpen as drop builds)
- Strobe on bars 7,15,23,31,39 (every 8 steps)
- NI3K: heads spinning (t=160), H_PNK halo, lasers arm at step 20 (bars 20–39)
- stab() helper, hold(174,1) timing

### BREAK — 1:19–1:48 (20 bars, 5 steps × 4 bars)
- Energy pulls back post-drop. Dim 155→110.
- Positions: SL→C→SR→DSC→C (wide settling to intimate)
- SH_PINK (ch8=60), BSW transitions from magenta to pink
- NI3K H_PNK halo activates — first halo join
- Steps 0–1: PAR_ROSE. Steps 2–4: PAR_MAGENTA.
- soul() helper, smooth(174,4) crossfades

### BRIDGE — 1:48–2:03 (12 bars, 3 steps × 4 bars)
- Final void. Dim arc 80→40→20.
- All parked at DSC. Heavy frost (240/220).
- PAR dims with mover. NI3K halos off.
- Step 3 at dim 20 — last dark before the light.
- soul() helper, smooth(174,4) crossfades

### DROP_2 — 2:03–2:36 (24 bars, 24 steps × 1 bar)
- **Steps 0–11 (2:03–2:19) — Rise**: Void to near-full. Pink/rose/magenta rebuild.
  - Dim 80→253. Positions: DSC→C→SL→USL→SR→C→USR→DSC→SL→SR→C→DSC
  - Frost tightens (200→110). H_PNK halo. No lasers.
  - stab() with hold(174,1) timing — 1-bar chase snaps
- **Steps 12–23 (2:19–2:36) — BORN AGAIN MOMENT**:
  - SH_WHITE (ch8=0), BSW white, PAR_WHITE (255,230,240)
  - NI3K: all lasers ON (red+green+blue), halo H_RGB
  - Strobe EVERY bar — SHARPY_STROBE_MED + BSW_SHUT_STROBE_SLOW
  - Profile 90. Frost fully open (120/90).
  - Positions include DISCO_BALL (step 12, 20) — beams scatter off ball into room
  - Positions include CEIL (step 17, 21) — overhead dramatic shafts at peak
  - BSW lags 3 steps — two white beams chasing through the catharsis

### END — 2:36–2:42 (4 bars, 2 steps × 2 bars)
- White drains. Violet reclaims. Dim 120→60.
- Laser STROBE_SLOW on all 3 (step 1), then LASER_OFF (step 2). H_OFF.
- Return to deep violet on everything — the light fades.

---

## Key Design Rules (from research brief)

**Must preserve:**
- Near-black verse opening — 20 dim max
- White ONLY at catharsis (steps 12–23 of DROP_2, 2:19+)
- Bridge near-darkness: 20 dim at step 3
- NI3K lasers only from DROP_1 step 20 onward

**Avoid:**
- White before the catharsis moment
- Unified/slow movement in DROP sections — those need the chase
- Lasers before DROP_1 step 20

---

## Technical Notes

- Generator: `venue/home-studio/generators/Blooom & Wolfy Lights - Born Again.py`
- 78 scenes, 1 chaser (78 steps), 116 bars, 160.0s
- 13 lint warnings, all intentional:
  - `LONG_STEP` (12): 4-bar steps in VERSE, BREAK, BRIDGE — atmospheric breathing
  - `NI3K_OFF` (1): dim=0 laser-only mode fools the dim-based checker; NI3K IS active
    (halo H_PNK in DROP_1 + DROP_2 rise; H_RGB + all lasers in DROP_2 catharsis)
- BPM: 174 — analysis detected 87 (half-time). Actual is 174 DnB.
- Brand alignment score: 4.0 (void-to-light arc adapted for DnB energy)

## Chase Pattern Details

```
DROP_1 Sharpy cycle (40 steps):
  0:DSC  1:C    2:SL   3:USR  4:SR
  5:DJ   6:USL  7:C    8:DSR  9:DSC
 10:SL  11:SR  12:USC 13:DANCE 14:DSR
 15:C   16:USL 17:USR 18:DSL 19:DSC
 20:C   21:SL  22:DSC 23:SR  24:USL
 25:DJ  26:USR 27:C   28:DSL 29:DSC
 30:SL  31:SR  32:C   33:DANCE 34:DSC
 35:USL 36:USR 37:DSL 38:DSR 39:DSC

BSW = sh_cycle[3:] + sh_cycle[:3]  (lags by 3 positions = ~4.1 seconds)
```
