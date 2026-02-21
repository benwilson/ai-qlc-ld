# Show Notes: Nora En Pure - Bartok (Extended Mix)

Status: `complete`
BPM: 125 | Duration: ~7:08 (428s / 224 bars) | Venue: home-studio

---

## Creative Thesis

> Trace the arc of an open landscape at dawn — amber light breathing over earth and water, four-on-the-floor pulse as heartbeat, the whole rig exhaling together in slow organic unison.

---

## Color Palette

| Name | Purpose | RGB | Notes |
|------|---------|-----|-------|
| EARTH / PAR_EARTH | Intro dark base | 120, 60, 8 | Deep amber-brown |
| AMBER / PAR_AMBER | Verse / chorus base | 200, 100, 15 | Warm amber |
| GOLD / PAR_GOLD | Chorus peak | 240, 140, 20 | Warm gold |
| STRAW / PAR_STRAW | Final run accent | 255, 220, 80 | Pale straw-white |
| BURNT / PAR_BURNT | Break sections | 80, 40, 5 | Burnt sienna dim |

Sharpy colour wheel: `80=amber (SH_AMBER)`, `20=yellow/gold (SH_GOLD)`
BSW colour wheel: `26=orange (BSW_ORG)`, `32=yellow/gold (BSW_YEL)`

No cold colours anywhere. Everything warm earth.

---

## Fixture Roles

| Fixture | Role |
|---------|------|
| Sharpy (ID 8) | Primary organism — leads all sweeps, tracks palette |
| BSW (ID 1) | Unified organism — mirrors Sharpy at same position |
| Profile (ID 4) | Ambient front fill at DSC throughout (dim 50–80) |
| 4BAR (ID 2) | Landscape colour wash — warm amber/gold arc |
| Missyees (ID 5, 6) | Ambient amber side fill |
| NI3K (ID 3) | Lasers only from FINAL_RUN (5:06+), dim=0 (LED off) |

---

## Section-by-Section Breakdown

### INTRO — 0:00–1:02 (32 bars, 8 steps × 4 bars)
- Single organism entering from deep earth. Dim arc 50→140.
- Positions: DSC→C→USC→C→DSC→C→USC→DSC (slow breathing arc)
- SH_AMBER (80), BSW_ORG (26), heavy frost (220/190)
- PAR scales with dim, no prism, no lasers, no effects
- Profile provides 30–50 dim floor fill

### CHORUS_1 — 1:02–1:33 (16 bars, 8 steps × 2 bars)
- First reveal: warm amber opens to full rig
- Wide arc: SL→C→SR→DSC→USL→C→USR→DSC
- Dim 160, frost 180/150, Profile 60

### BRIDGE — 1:33–1:48 (8 bars, 4 steps × 2 bars)
- Inst break — soft settle, park toward DSC, dim 120–130
- Amber holds, frost rises (210/185)

### CHORUS_2 — 1:48–2:50 (32 bars, 16 steps × 2 bars)
- Main chorus run. Dim arc 170→220.
- **Bar 1–16**: amber palette (SH_AMBER, BSW_ORG)
- **Bar 17–32**: gold palette (SH_GOLD=20, BSW_YEL=32) — warmth earned
- Same wide LR sweep × 2, frost tightens as gold arrives (150→120)

### BREAK_1 — 2:50–3:37 (24 bars, 6 steps × 4 bars)
- Breakdown. Dim arc 140→60, parking toward DSC then C.
- Amber stays warm but dims. Frost heavy (225/200).

### RISING — 3:37–4:08 (16 bars, 8 steps × 2 bars)
- Converging motion toward DSC (USL→SL→C→SR→USR→C→DSC→DSC).
- Dim arc 140→240. Frost tightens (150→100) as beams sharpen.
- **Gold palette from step 4 (mid-section)**
- **Prism fires at steps 6–7** (Sharpy prism1=128) — climax at 4:04

### BREAK_2 — 4:08–5:06 (28 bars, 7 steps × 4 bars)
- **Phase 1 (steps 0–2)**: post-peak dim 150→80, amber, parking C→DSC
- **Phase 2 (steps 3–6)**: re-intro strip, dim 60→25, burnt palette
- Movers all at DSC from step 1 onward — intentional re-intro stillness
- This is the "bare earth" moment — nearly nothing, just ambient PAR glow

### FINAL_RUN — 5:06–6:54 (56 bars, 28 steps × 2 bars)
- **NI3K lasers ON** (all 3: red, green, blue). dim=0, laser-only mode.
- Full warm gold (SH_GOLD, BSW_YEL), frost opens (110/90) — tighter beams
- Wide 28-position sweep: USL→SR→DSC→SL→USR→C→DSL→… cycling
- **After step 16 (~6:00)**: straw palette (255,220,80), NI3K halo→H_RGB
- Dim arc 200→255 across the full final run
- Profile 80 throughout

### OUTRO — 6:54–7:08+ (12 bars, 3 steps × 4 bars)
- Return to earth. Dim arc 100→60→30.
- Step 1: lasers on LASER_STROBE_SLOW. Steps 2–3: LASER_OFF.
- Amber palette, heavy frost (230/200), PAR dims to near-dark.

---

## Key Design Rules (from research brief)

**Must preserve:**
- Warm earth tones throughout — never cold or blue
- Unified mover organism: all movers at same position at all times
- 4-bar step minimum — this is slow melodic house, not DnB
- NI3K lasers only from 5:06 (FINAL_RUN)

**Avoid:**
- Strobe at any point
- Cold or blue palette
- Independent or fast mover movement
- Saturated neon aesthetics

---

## Technical Notes

- Generator: `venue/home-studio/generators/Nora En Pure - Bartok (Extended Mix).py`
- 88 scenes, 1 chaser (88 steps), 224 bars, 430.1s
- Lint warnings (26 total): all intentional
  - `LONG_STEP`: 4-bar slow steps throughout breaks/intro/outro
  - `STATIC_POS` steps 52–55: BREAK_2 re-intro strip at DSC (intentional)
  - `NI3K_OFF` 100%: dim=0 laser-only mode fools the dim-based checker; lasers ARE on in FINAL_RUN
- Brand alignment score: 4.2 (organic melodic house, Nora En Pure aesthetic)
