# Show Notes: Mind Against - OnlyL ft. TSHA & NIMMO

Status: `complete`
BPM: 128 | Duration: 6:03 (363s) | Venue: home-studio

---

## Creative Thesis

> Chart a yearning emotional arc from restrained indigo longing through a near-silent void of pure vocals into a desaturated rose-white catharsis — love stripped to its last syllable.

---

## Color Palette

| Name | Purpose | RGB (approx) | Sharpy Wheel |
|------|---------|-------------|-------------|
| DEEP_INDIGO | Base / open / outro | 20, 20, 80 | Ch8=30 (blue) |
| DUST_ROSE | Vocal warmth (muted, adult) | 120, 70, 70 | Ch8=60 (pink) |
| PALE_ROSE | Building tension | 150, 90, 90 | Ch8=60 |
| CREAM_WHITE | Cathartic peak | 255, 240, 200 | Ch8=80 (amber) |
| PALE_SILVER | Rebuild phase | 180, 180, 200 | Ch8=0 (white) |

Desaturated throughout — no saturated colors. Everything feels cinematic, slightly washed-out.

---

## Fixture Roles

| Fixture | Role |
|---------|------|
| Sharpy (ID 8) | Primary beam organism — leads indigo sweeps |
| BSW (ID 1) | Secondary organism — follows Sharpy, activates in REBUILD |
| Profile (ID 4) | Vocal spotlight — the only fixture in the VOID |
| 4BAR (ID 2) | Color wash — indigo→rose gradient, dims in VOID |
| Missyee x2 (ID 5,6) | Ambient fill — matches section palette |
| NI3K (ID 3) | Lasers only from PEAK (4:32+), halos off until then |

---

## Section-by-Section Breakdown

### OPENING — 0:00–0:30 (16 bars, e=0.81)
- 4-bar steps, Sharpy solo entering from dark
- Pure DEEP_INDIGO, no pars, slow convergence toward DSC
- BSW, 4BAR, Missyees all dim — mover "organism" begins alone
- `vocal_spotlight()` dark at start, BSW parked at CEIL

### VERSE_1 — 0:30–1:15 (24 bars, e=0.82)
- First NIMMO vocal. Sharpy + BSW unified at DUST_ROSE
- 2-bar steps, `pairs` PAR mode (P1+P3 vs P2+P4)
- Profile tracks vocals at DSC, dims slightly on instrumental bars
- Color shifts: indigo base → rose on vocal emphasis

### BREATHE — 1:15–2:16 (32 bars, e=0.55)
- Sustained mid-energy vocal section, lower energy
- PALE_ROSE palette, `pairs` PAR mode, 2-bar steps
- BSW adds slight gobo (G1_2) for texture without busyness
- Profile as vocal spotlight, movers at lower intensity

### SURGE — 2:16–2:46 (16 bars, e=0.86)
- Converging positions (SL→DSC→SR), PALE_ROSE rising
- 2-bar steps, wider fixture activation, `pairs` PAR mode
- Feels like tension accumulating toward the coming void

### DIMMING — 2:46–3:09 (12 bars, e=0.49)
- Rose drains back toward indigo — deliberate 4-bar dissolve steps
- Movers dimming from 180 to ~80, positions parking at DSC
- Anticipates the void — world getting smaller

### VOID — 3:09–4:01 (28 bars, e=0.15)
**The emotional heart of the show — the 'OnlyL' moment.**
- `vocal_spotlight()` ONLY: Profile at DSC, dimmer 140, white
- Everything else completely dark: Sharpy/BSW at `dark_*()`, 4BAR off, Missyees off
- 4-bar steps throughout — the breath has nowhere to go
- NI3K lasers off
- This section must NOT be touched without explicit intent

### REBUILD — 4:01–4:32 (16 bars, e=0.22)
- Sharpy reappears first (PALE_SILVER), then BSW (DUST_ROSE)
- 4-bar steps, returning from void — quiet, tentative
- 4BAR fades back in with rose wash at half intensity
- No lasers yet, no prism, building toward peak

### PEAK — 4:32–5:21 (26 bars, e=0.89)
**Cathartic release — the only moment of near-full brightness.**
- CREAM_WHITE palette, full rig, wide sweeps (USL/USR/DSL/DSR)
- Prism active on Sharpy (both prism slots)
- NI3K lasers ON (all 3 colors)
- After 60% into section: amber accents emerge (WARM_AMBER tier)
- NI3K halo at H_RGB for color richness

### FADE — 5:21–6:07 (23 bars, e=0.85)
- Phase 1 (first ~60%): cream holds, lasers persist, movers wide
- Phase 2 (final 40%): return to DEEP_INDIGO, laser strobe softens, dimmer drops
- Ends at ~30 dimmer — love fades, indigo returns

---

## Key Design Rules (from research brief)

**Must preserve:**
- VOID section (3:09–4:01): Profile only, everything else dark
- Desaturated dusty rose for vocal moments — never saturated pink
- NI3K lasers activate ONLY from 4:32 onward
- All mover movement in 2–4 bar slow sweeps — no fast position changes

**Avoid:**
- Strobe at any point — this is emotional, not rave
- Saturated colors — always slightly desaturated and cinematic
- Independent mover divergence except in the void (park at DSC)

---

## Technical Notes

- Generator: `venue/home-studio/generators/Mind Against - OnlyL ft. TSHA & NIMMO.py`
- 113 scenes, 1 chaser (113 steps)
- Lint warnings: SOLO_MOVER on OPENING (intentional — Sharpy enters alone) and VOID (intentional — Profile only); LONG_STEP (intentional — 4-bar steps throughout void/rebuild); PAR_OFF in VOID (intentional)
- All 22 lint warnings are intentional design choices
- Brand alignment score: 4.4 (Afterlife-adjacent restraint)
