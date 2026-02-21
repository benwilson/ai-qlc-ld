# Creativity Center: Music Stage Lighting (PAR + Moving Lights)

Last updated: 2026-02-19  
Primary use: inspiration bank for humans + AI show/cue generation

## 1) Purpose

This file is the central research + idea library for building music lighting looks.

Goals:
- Give general stage-lighting technique guidance that is stable and reusable.
- Focus on combining PAR-style wash fixtures with moving lights for depth and contrast.
- Provide many AI-friendly look recipes with consistent structure and tags.

### 1.1 Canonical Machine Data (For Parsing/Generation)

`references/creativity.md` is the human playbook.  
`references/data/*.json` is the canonical machine-readable global layer for generation and automation.
`venue/<name>/references/creative-profile.json` is the venue-specific machine layer.

Use these files first when building shows programmatically:
- `references/data/coordination-techniques.json`
- `references/data/palettes.json`
- `references/data/designers.json`
- `references/data/phrase-rules.json`
- `references/data/manifest.json`
- `venue/<name>/references/creative-profile.json`

Maintenance workflow:
1. Edit creative content in `references/creativity.md`.
2. Run `python3 references/data/sync_from_creativity.py`.
3. Run `python3 references/data/validate_data.py`.
4. Update venue adaptation files under `venue/<name>/references/`.
5. Run `python3 references/data/validate_venue_profiles.py`.
6. Run `python3 references/data/validate_generator_portability.py`.

---

## 2) Rig-Agnostic Role And Zone Abstraction

Use this abstraction when generating looks:

- `PAR_A`: primary PAR layer (main wash/chase role)
- `PAR_B`: secondary PAR layer (contrast/side/wall role)
- `M1_BEAM`: beam-led mover role
- `M2_HYBRID`: hybrid beam/spot/wash mover role
- `M3_PROFILE`: profile/key mover role
- `M4_FX`: effect fixture role

Focus zones available:
- `USL`, `USC`, `USR`, `SL`, `C`, `SR`, `DSL`, `DSC`, `DSR`
- Optional specials: `DJ_BOOTH`, `PAR_WALL`, `DANCE_FLOOR`, `DISCO_BALL`, `CENTER_CEILING`

Venue mapping source of truth:
- `venue/<name>/references/creative-profile.json`
- `venue/<name>/references/creativity-venue.md`

---

## 3) Research Foundations (Distilled)

### 3.1 Controllable Properties
All effective looks manipulate these four properties:
- `intensity`
- `color`
- `distribution/focus`
- `movement/time`

### 3.2 Core Lighting Objectives
Most musical looks should balance:
- `visibility` (what must be seen)
- `revelation_of_form` (shape, shadows, depth)
- `composition` (what the eye tracks first)
- `mood` (emotional color + motion)
- `information` (time, section, impact cues)

### 3.3 Angle Logic
Use angle contrast to create dimensionality:
- `front_45`: natural, readable faces, musical "clarity"
- `back`: separation, silhouettes, drama
- `side`: body shape, dance energy
- `top`: sculptural and controlled
- `up`: unnatural/tension effects (use sparingly)

### 3.4 PAR Strengths
PARs are best for:
- stable area coverage
- broad color environments
- room tone and continuity
- visual glue under moving effects

Limitations:
- less precise beam shaping than profiles/spots
- movement is usually from cue changes, not fixture mechanics

### 3.5 Moving-Light Strengths
Moving fixtures are best for:
- directed attention (where to look)
- dynamic accents and kinetic energy
- texture (gobos/prisms/focus effects)
- spatial punctuation (hits, sweeps, reveals)

### 3.6 Why PAR + Movers Works
Most strong modern looks use:
- `PAR layer = canvas` (base world)
- `moving layer = narrative` (lead voice)

This avoids thin, disconnected beam-only looks and avoids flat wash-only looks.

### 3.7 Color Strategy
Reliable color behavior:
- warm/cool split creates form
- saturation controls perceived intensity (high saturation often feels dimmer)
- limited palettes (2-3 dominant colors) read cleaner than full-rainbow all the time
- reserve white for emphasis, realism, and section boundaries

### 3.8 Movement Strategy
Treat movement as rhythm:
- low energy: long arcs, low speed variance
- medium energy: repeated motifs in 1-2 bar loops
- high energy: shorter cycles, snap changes, occasional strobe punctuation

### 3.9 Musical Phrasing
Section-aware timing works best:
- intro/breakdown: 4-16 bar visual phrases
- groove/verse: 1-4 bar motion loops
- build: density and speed ramp every 1-2 bars
- drop: strongest contrast in first 1-4 beats, then controlled sustain

### 3.10 Atmosphere/Haze Note
Aerial beam looks require particulate atmosphere to read clearly.
Without haze, shift emphasis to:
- floor/fan patterns
- silhouette geometry
- color and intensity contrast on surfaces/performers

---

## 4) AI Design System

### 4.1 Required Fields Per Look

Use this schema for generated cues:

```yaml
id: string
name: string
energy: 1-5
moods: [tags]
sections: [intro|verse|build|drop|breakdown|outro|transition]
tempo_range_bpm: "min-max"
par_strategy:
  base_groups: [PAR_A, PAR_B]
  role: "canvas|pulse|wall|silhouette|contrast"
  intensity_range: "x-y %"
  color_mode: "static|2-color alternate|gradient|slow morph|flash accents"
mover_strategy:
  lead_fixtures: [M1_BEAM, M2_HYBRID, M3_PROFILE, M4_FX]
  role: "accent|texture|key|aerial|hit|sweep"
  position_pattern: [zone list]
  movement_rate: "static|slow|medium|fast|aggressive"
timing:
  phrase: "bars"
  subdivisions: "beats or note divisions"
  transition_style: "crossfade|snap|bump|strobe burst|blackout cut"
color_palette: [main colors]
variation_knobs: [parameters to randomize safely]
```

### 4.2 Global Safety/Quality Constraints

- Keep one visual anchor at all times (a stable PAR tone or static key).
- Avoid all fixtures strobing together for long durations.
- Use full white as a contrast event, not constant baseline.
- At least one low-motion segment every 16-32 bars prevents fatigue.
- For heavy movement scenes, keep PAR layer simple.

---

## 5) PAR + Moving-Light Archetypes

Use these as high-level templates:

1. `Anchor + Spear`: PAR wash base + one tight moving beam focal line.
2. `Color Bed + White Cuts`: saturated PAR world + white mover accents on transients.
3. `Opposition`: warm PAR base vs cool moving beams (or inverse).
4. `Silhouette Driver`: back PAR glow + front movers minimal, preserving outlines.
5. `Texture Float`: static PAR color + slow gobo/prism movement.
6. `Ceiling Architecture`: PAR low-level room tone + movers drawing overhead geometry.
7. `Wall Narrative`: PAR side-wall color + movers narrating center-stage action.
8. `Pulse and Orbit`: PAR pulses on kick + movers orbit over 2-4 bars.
9. `Dead Air Reset`: brief low-light reset between dense phrases.
10. `Drop Detonation`: blackout or deep dim before first drop hit, then full contrast release.
11. `Chase Lattice`: PAR chase direction opposes moving pan direction.
12. `Two-Plane Look`: PAR on floor/surfaces, movers in air.
13. `Monochrome Discipline`: one hue family, movement provides variation.
14. `Prism Bloom`: PAR steady, movers prism-expand only on phrase boundaries.
15. `Key + Chaos`: profile key on subject while other movers run high-energy FX.

---

## 6) Look Recipe Bank (60 Ideas)

Format:
- `energy` uses 1 (lowest) to 5 (highest)
- all looks assume PAR + movers in combination

### A) Intro / Ambient / Low Energy

### CR-001 Warm Horizon
- `energy`: 1 | `sections`: intro, breakdown | `moods`: intimate, warm
- `par`: PAR_A amber fan at 20-35%; PAR_B dim lavender edge 10-18%.
- `movers`: M3_PROFILE soft pool at `C`; M2_HYBRID slow sweep `USC -> SL -> SR` over 16 bars; M1 off.
- `timing`: 8-bar breathe; 1-bar micro-rise at phrase ends.
- `palette`: amber, lavender, deep blue.
- `variation_knobs`: widen PAR fan, alternate profile focus soft/hard every 16 bars.

### CR-002 Cold Dawn Grid
- `energy`: 1 | `sections`: intro, outro | `moods`: spacious, minimal
- `par`: PAR_A steel-blue static 18-25%; PAR_B cyan vertical split.
- `movers`: M1_BEAM to `CENTER_CEILING` static; M2 tiny tilt drift.
- `timing`: 16-bar static with 4-bar crossfade color drift.
- `palette`: steel blue, cyan, white tint.
- `variation_knobs`: randomize ceiling target between center and slight left/right.

### CR-003 Candle and Halo
- `energy`: 1 | `sections`: verse, breakdown | `moods`: organic, tender
- `par`: warm low PAR bed (amber + peach) at 12-22%.
- `movers`: M3 key at `DJ_BOOTH`; M2 soft circular move around `C` very slow.
- `timing`: 4-bar pulse on kick ghost notes.
- `palette`: amber, peach, soft gold.
- `variation_knobs`: pulse depth 5-12%.

### CR-004 Static World, Moving Sky
- `energy`: 1 | `sections`: intro | `moods`: cinematic, suspended
- `par`: PAR_A + PAR_B fixed cool wash 20%.
- `movers`: M1/M2 on `CENTER_CEILING` with very slow crossing pans.
- `timing`: 32-bar macro movement.
- `palette`: indigo, cyan, low white.
- `variation_knobs`: change crossing point every 8 bars.

### CR-005 Sidewall Breathing
- `energy`: 1 | `sections`: intro, break | `moods`: hypnotic
- `par`: PAR_B dominant (side-wall glow), PAR_A very low fill.
- `movers`: M2 static center; M3 gentle iris pulse.
- `timing`: 2-bar inhale/exhale.
- `palette`: teal, navy.
- `variation_knobs`: offset PAR_B heads by 1/8 beat for subtle ripple.

### CR-006 Fog Memory
- `energy`: 1 | `sections`: breakdown | `moods`: ethereal, distant
- `par`: desaturated blue haze look 15-25%.
- `movers`: M1 thin beam at low dimmer sweeping `USL <-> USR`; M2 frost/wash mode if available.
- `timing`: 8-bar sweep loop.
- `palette`: ice blue, moon white.
- `variation_knobs`: increase beam sharpness only on final 2 bars before transition.

### CR-007 Mono Lavender Drift
- `energy`: 1 | `sections`: intro, verse | `moods`: dreamy
- `par`: all PAR groups one hue (lavender), different intensities per zone.
- `movers`: M3 slow positional morph between `C` and `DSC`.
- `timing`: 4-bar morph.
- `palette`: lavender family only.
- `variation_knobs`: occasional 1-beat white pin from M1 every 16 bars.

### CR-008 Ghosted Pulse
- `energy`: 1 | `sections`: intro | `moods`: mysterious
- `par`: PAR_A floor-only low pulses on offbeats.
- `movers`: M2 static gobo texture at `USC`; M4 very slow macro.
- `timing`: 1-bar offbeat pulse pattern.
- `palette`: dark blue, muted purple.
- `variation_knobs`: gobo rotation on/off every 8 bars.

### CR-009 Skyline Wash
- `energy`: 1 | `sections`: intro, outro | `moods`: open, reflective
- `par`: PAR_A top-heavy brightness gradient (outer heads dimmer than inner).
- `movers`: M1/M2 pointed above audience line for skyline silhouette.
- `timing`: 16-bar color fade.
- `palette`: cyan to magenta gradient.
- `variation_knobs`: reverse gradient direction each phrase.

### CR-010 Quiet Toplight
- `energy`: 1 | `sections`: spoken intro, breakdown | `moods`: focused, sparse
- `par`: PAR_B near-off; PAR_A low neutral fill.
- `movers`: M3 tight top key on `DJ_BOOTH`; M2 off except tiny phrase glints.
- `timing`: mostly static; accent hits 1/2 beat.
- `palette`: neutral white, dim steel blue.
- `variation_knobs`: drop to near-black for 1 beat before section change.

### B) Groove / Verse / Medium-Low Energy

### CR-011 Split Complement
- `energy`: 2 | `sections`: verse, groove | `moods`: clean, modern
- `par`: PAR_A in blue, PAR_B in amber (complement split).
- `movers`: M2 traces `SL -> C -> SR` in 2-bar loop.
- `timing`: 1-bar PAR pulse + 2-bar mover loop.
- `palette`: blue/amber.
- `variation_knobs`: swap warm/cool sides every 16 bars.

### CR-012 Kick-Locked Floor Chase
- `energy`: 2 | `sections`: groove | `moods`: rhythmic
- `par`: PAR_A four-head chase synced to kick.
- `movers`: M1 short diagonal sweeps only on bar starts.
- `timing`: 1 beat steps, 4-bar phrase reset.
- `palette`: red + white accents.
- `variation_knobs`: reverse chase direction each phrase.

### CR-013 Side-to-Center Conversation
- `energy`: 2 | `sections`: verse | `moods`: conversational
- `par`: PAR_B answers PAR_A with delayed 1/4 beat pulses.
- `movers`: M3 alternates `SL` and `SR`.
- `timing`: call/response every 2 beats.
- `palette`: teal, magenta.
- `variation_knobs`: random 10% probability of silence bar.

### CR-014 Rotating Color Bed
- `energy`: 2 | `sections`: verse, groove | `moods`: fluid
- `par`: slow 8-bar hue rotation across PAR groups.
- `movers`: M2 static position but gobo rotates slowly.
- `timing`: 8-bar color wheel; 1-bar micro intensity bumps.
- `palette`: cyan, violet, blue.
- `variation_knobs`: momentary white pop at bar 8.

### CR-015 Bounce Corridor
- `energy`: 2 | `sections`: groove | `moods`: bouncy
- `par`: PAR_A center heads stronger than outers (corridor look).
- `movers`: M1 bounce `DSL <-> DSR`; M2 holds `C`.
- `timing`: 1-bar ping-pong.
- `palette`: lime, cyan, white.
- `variation_knobs`: change bounce width every 4 bars.

### CR-016 Dimmer Swing
- `energy`: 2 | `sections`: groove, pre-build | `moods`: rolling
- `par`: sine-wave dimmer swing across PAR_A.
- `movers`: M3 medium pan arc over audience line.
- `timing`: 2-bar swing.
- `palette`: warm white + soft rose.
- `variation_knobs`: increase swing depth from 20% to 45% before build.

### CR-017 Mono Blue Engine
- `energy`: 2 | `sections`: verse | `moods`: disciplined, deep
- `par`: monochrome blue bed with subtle PAR_B shimmer.
- `movers`: M2 narrow beam scans in slow triangles.
- `timing`: 4-bar geometric cycle.
- `palette`: 3 shades of blue.
- `variation_knobs`: add occasional amber back-hit every 8 bars.

### CR-018 Prism Whisper
- `energy`: 2 | `sections`: groove, breakdown bridge | `moods`: airy
- `par`: static low saturation wash.
- `movers`: M2 prism at low speed only on phrase end; M1 static.
- `timing`: prism on bars 4 and 8 only.
- `palette`: cool white, cyan.
- `variation_knobs`: prism depth 0-35%.

### CR-019 Floor Fan Groove
- `energy`: 2 | `sections`: groove | `moods`: clubby, grounded
- `par`: PAR_A fan aimed low across dance floor with medium saturation.
- `movers`: M1/M2 cross from upstage toward `DANCE_FLOOR`.
- `timing`: 1-beat bumps + 4-bar sweeps.
- `palette`: purple, blue, white.
- `variation_knobs`: alternate crossed and parallel beams per phrase.

### CR-020 Drum Ghost Highlights
- `energy`: 2 | `sections`: verse | `moods`: detailed, syncopated
- `par`: base at 25%; ghost hits at +10% on percussion fills.
- `movers`: M3 punctuates snare ghosts with short iris snaps.
- `timing`: 1/8 beat accent map.
- `palette`: amber + cyan duality.
- `variation_knobs`: switch ghost map every 8 bars.

### C) Build / Tension / Acceleration

### CR-021 Ladder Build
- `energy`: 3 | `sections`: build | `moods`: rising tension
- `par`: PAR_A add heads progressively (1 -> 2 -> 3 -> 4).
- `movers`: M2 beam narrows while pan range shrinks toward center.
- `timing`: one step every bar for 8 bars.
- `palette`: deep blue to white.
- `variation_knobs`: optional final-bar blackout.

### CR-022 Compression Tunnel
- `energy`: 3 | `sections`: build | `moods`: claustrophobic
- `par`: start wide wash then reduce to narrow central strip.
- `movers`: M1/M2 converge on `C` from opposite sides.
- `timing`: 4-bar compression + 1-bar hold.
- `palette`: desaturated white then red accent.
- `variation_knobs`: freeze last frame for 1 beat before drop.

### CR-023 Tempo Illusion
- `energy`: 3 | `sections`: build | `moods`: urgent
- `par`: pulse rate doubles every 2 bars.
- `movers`: movement speed stays constant to create relative acceleration illusion.
- `timing`: 1/2 beat -> 1/4 beat -> 1/8 beat.
- `palette`: white + electric blue.
- `variation_knobs`: insert one silent bar after max speed.

### CR-024 Rising Diagonal
- `energy`: 3 | `sections`: build | `moods`: forward motion
- `par`: diagonal chase across PAR_A heads.
- `movers`: M3 tilt rises from floor to ceiling through phrase.
- `timing`: 8-bar ramp.
- `palette`: cyan to magenta.
- `variation_knobs`: mirror diagonal direction each build.

### CR-025 Harmonic Tension Split
- `energy`: 3 | `sections`: build, pre-drop | `moods`: uneasy
- `par`: warm/cool conflict increases saturation gradually.
- `movers`: M2 gobo rotation accelerates.
- `timing`: 4-bar increments.
- `palette`: amber vs green-blue.
- `variation_knobs`: introduce 1-beat white at bar 7.

### CR-026 Beam Count Increase
- `energy`: 3 | `sections`: build | `moods`: assembling
- `par`: stable low-mid base.
- `movers`: add active fixtures one-by-one (M3 -> M2 -> M1 -> M4).
- `timing`: add one mover every 2 bars.
- `palette`: dark blue with white attacks.
- `variation_knobs`: swap activation order.

### CR-027 Frequency Sweep
- `energy`: 3 | `sections`: build | `moods`: mechanical
- `par`: low frequency 2-bar pulses compress to 1-beat pulses.
- `movers`: M1 oscillation amplitude narrows while speed rises.
- `timing`: 8-bar acceleration.
- `palette`: cold white, violet.
- `variation_knobs`: random brief blackouts (<= 1/4 beat).

### CR-028 Inward Spiral
- `energy`: 3 | `sections`: build | `moods`: hypnotic, dark
- `par`: PAR_B rotating color wheel at low intensity.
- `movers`: M2 spiral around `C` with decreasing radius.
- `timing`: 4-bar loops, 2 cycles.
- `palette`: indigo, deep red.
- `variation_knobs`: reverse spiral direction on second cycle.

### CR-029 Snare Lift
- `energy`: 3 | `sections`: build | `moods`: anticipatory
- `par`: base remains steady, slight +8% bump on each snare.
- `movers`: M3 tilt increment on each snare hit.
- `timing`: 1-beat snare-driven staircase.
- `palette`: blue base, white snare.
- `variation_knobs`: final 2 beats switch to stutter.

### CR-030 False Drop Tease
- `energy`: 3 | `sections`: build, transition | `moods`: deceptive
- `par`: appears to hit full then cuts to 20%.
- `movers`: wide sweep aborts into static center hold.
- `timing`: fake release at bar 7, real release later.
- `palette`: white tease then return to dark cyan.
- `variation_knobs`: choose fake-drop bar 6 or 7.

### D) Drop / Peak / High Energy

### CR-031 White Strike + Color Flood
- `energy`: 5 | `sections`: drop | `moods`: explosive
- `par`: first hit full white 1 beat, then saturated flood.
- `movers`: M1/M2 fast crossing beams over `DANCE_FLOOR`.
- `timing`: 1-beat strike then 1-bar chase loop.
- `palette`: white -> red/cyan.
- `variation_knobs`: alternate post-hit palettes each phrase.

### CR-032 Crossfire
- `energy`: 5 | `sections`: drop, peak | `moods`: aggressive
- `par`: PAR_A pulse on kick, PAR_B on snare (split rhythm).
- `movers`: M1/M2 cross at center every beat.
- `timing`: beat-synced cross pattern.
- `palette`: red, white, deep blue.
- `variation_knobs`: rotate crossing target between `C`, `DSC`, `DJ_BOOTH`.

### CR-033 Strobe Corridor
- `energy`: 5 | `sections`: drop | `moods`: intense
- `par`: low color bed to preserve orientation.
- `movers`: short strobe bursts from M1/M2 in 1/4 beat packets.
- `timing`: 2 beats strobe, 2 beats release.
- `palette`: cool white + ultraviolet tint.
- `variation_knobs`: strobe rate 8-14 Hz, duty-cycle caps for comfort.

### CR-034 Prism Burst Lanes
- `energy`: 4 | `sections`: drop | `moods`: massive, wide
- `par`: alternating two-color blocks across PAR_A heads.
- `movers`: M2 prism opens on bar starts; M1 tracks diagonals.
- `timing`: 1-bar motif.
- `palette`: lime/magenta with white punctuation.
- `variation_knobs`: prism on odd bars only for cleaner contrast.

### CR-035 Sawtooth Energy
- `energy`: 4 | `sections`: peak groove | `moods`: driving
- `par`: intensity ramps up each beat then hard reset.
- `movers`: M3 profiles performer on reset beat.
- `timing`: 1-bar sawtooth.
- `palette`: electric blue, white.
- `variation_knobs`: apply sawtooth to color saturation instead of intensity.

### CR-036 Railgun
- `energy`: 5 | `sections`: drop | `moods`: brutal, tight
- `par`: minimal dark bed with occasional flash strips.
- `movers`: M1 tight beam snap targets `USL -> C -> DSR` rapidly.
- `timing`: 1/2 beat snaps.
- `palette`: white + blood red accents.
- `variation_knobs`: randomize target triplets by phrase.

### CR-037 High Contrast Bounce
- `energy`: 4 | `sections`: drop, chorus | `moods`: punchy
- `par`: alternating blackout and saturated fills each beat.
- `movers`: continuous motion so movement appears to jump.
- `timing`: 1-beat on/off contrast.
- `palette`: cyan, white, black intervals.
- `variation_knobs`: blackout depth 60-100%.

### CR-038 Quad-Head Blaster
- `energy`: 5 | `sections`: peak | `moods`: festival
- `par`: PAR_A four-head independent chases in opposite pairs.
- `movers`: M2 wide fast pan; M1 center punches on downbeats.
- `timing`: 1/4 beat chases.
- `palette`: full-sat primaries.
- `variation_knobs`: switch between pair-chase and all-head unison.

### CR-039 Mirror Sweep Impact
- `energy`: 4 | `sections`: drop | `moods`: symmetrical, huge
- `par`: balanced left/right base.
- `movers`: M1 and M2 mirrored pan/tilt with synchronized hits.
- `timing`: 2-beat mirror loop.
- `palette`: purple and white.
- `variation_knobs`: break symmetry every 8 bars for surprise.

### CR-040 Kick Cannon
- `energy`: 5 | `sections`: drop | `moods`: percussive
- `par`: every kick drives PAR_A full-hit then quick decay.
- `movers`: M3 and M1 fire short white punches to audience line.
- `timing`: ADSR-style 1-beat envelope.
- `palette`: white hits over dark blue bed.
- `variation_knobs`: decay time 120-260 ms.

### CR-041 Drop Spiral
- `energy`: 4 | `sections`: drop continuation | `moods`: vortex
- `par`: steady deep color for visual floor.
- `movers`: M2 spiral and M4 counter-rotate.
- `timing`: 4-bar evolution.
- `palette`: teal, magenta.
- `variation_knobs`: spiral radius expands each 4 bars.

### CR-042 Drumstep Switch
- `energy`: 4 | `sections`: double-time drops | `moods`: chaotic
- `par`: swap between half-time and double-time pulse maps.
- `movers`: motion speed follows mode switch instantly.
- `timing`: section-triggered mode toggles.
- `palette`: red/white and blue/white modes.
- `variation_knobs`: random 2-bar micro-breaker in each 16 bars.

### CR-043 Laserless Beam Matrix
- `energy`: 4 | `sections`: peak | `moods`: grid-like
- `par`: low uniform wash.
- `movers`: M1/M2/M3 create crossing matrix in haze.
- `timing`: 1-bar pattern with 4 matrix states.
- `palette`: lime and cyan.
- `variation_knobs`: rotate matrix state order per phrase.

### CR-044 Hyper Reveal
- `energy`: 5 | `sections`: big drop entry | `moods`: theatrical impact
- `par`: pre-drop near-black, then immediate full color world.
- `movers`: all movers snap from ceiling to crowd plane on first hit.
- `timing`: blackout cut + 1-beat snap + 4-bar sustain.
- `palette`: white reveal then saturated red/purple.
- `variation_knobs`: reveal target `DSC` vs `DANCE_FLOOR`.

### E) Breakdown / Emotional / Story Moments

### CR-045 Blue Void
- `energy`: 1 | `sections`: breakdown | `moods`: melancholic
- `par`: deep blue low level with very slow fade wave.
- `movers`: M3 single soft spotlight at `C`.
- `timing`: 8-bar fades.
- `palette`: navy, steel blue.
- `variation_knobs`: occasional amber memory flash (1 beat).

### CR-046 Warm Recall
- `energy`: 2 | `sections`: post-drop breakdown | `moods`: nostalgic
- `par`: amber/rose soft wash returns gradually.
- `movers`: M2 static breakup texture on back wall.
- `timing`: 4-bar warm-up.
- `palette`: amber, rose, warm white.
- `variation_knobs`: increase saturation by +10% each phrase.

### CR-047 Silhouette Choir
- `energy`: 2 | `sections`: vocal breakdown | `moods`: reverent
- `par`: back-heavy PAR_A creating silhouettes.
- `movers`: front movers dim/off except brief key pickups.
- `timing`: long 8-bar holds.
- `palette`: white backlight + cool shadow.
- `variation_knobs`: silhouette depth via front fill 0-12%.

### CR-048 Dual Color Drift
- `energy`: 2 | `sections`: breakdown | `moods`: emotional tension
- `par`: PAR_A cool, PAR_B warm; both drift toward center hue over time.
- `movers`: M3 slow side key alternates SL/SR.
- `timing`: 16-bar convergence.
- `palette`: cyan + amber -> neutral white.
- `variation_knobs`: reverse convergence at section exit.

### CR-049 Empty Stage Pulse
- `energy`: 1 | `sections`: vocal solo, pause | `moods`: fragile
- `par`: near-black with tiny 2-bar heartbeat pulse.
- `movers`: one fixture only (M3) on performer area.
- `timing`: 2-bar heartbeat.
- `palette`: desaturated lavender + warm white.
- `variation_knobs`: heartbeat doubles briefly at emotional lyric peaks.

### CR-050 Slow Rain
- `energy`: 2 | `sections`: breakdown | `moods`: reflective
- `par`: subtle descending dimmer steps across heads.
- `movers`: M2 gobo rotation very slow downward tilt moves.
- `timing`: 4-bar falling loop.
- `palette`: blue-green, cool white.
- `variation_knobs`: add M1 static shafts on last bar.

### CR-051 Cathedral Lift
- `energy`: 2 | `sections`: pre-climax emotional rise | `moods`: majestic
- `par`: broad low wash with gentle warm highlight center.
- `movers`: M1/M2 aim `CENTER_CEILING` and open out.
- `timing`: 8-bar expand.
- `palette`: gold + cobalt.
- `variation_knobs`: widen beam spread each 2 bars.

### CR-052 Piano Air
- `energy`: 1 | `sections`: piano bridge, outro | `moods`: clean, delicate
- `par`: static soft white/blue at 15-22%.
- `movers`: M3 slow manual-style follow of center activity.
- `timing`: 4-bar phrase-end shifts only.
- `palette`: cool white, pale cyan.
- `variation_knobs`: add faint magenta on chord change.

### F) Experimental / Signature Looks

### CR-053 Parallax Drift
- `energy`: 3 | `sections`: transition, interlude | `moods`: surreal
- `par`: PAR_A and PAR_B move color in opposite slow directions.
- `movers`: M1/M2 traverse matching physical directions for parallax illusion.
- `timing`: 8-bar opposing vectors.
- `palette`: teal/magenta opposition.
- `variation_knobs`: speed ratio 1:2 or 2:3.

### CR-054 Broken Symmetry
- `energy`: 3 | `sections`: groove, drop variation | `moods`: edgy
- `par`: mostly symmetrical look with one head intentionally offset.
- `movers`: mirror moves interrupted by random one-beat offset.
- `timing`: 4-bar symmetry, 1-bar break.
- `palette`: monochrome + one accent color.
- `variation_knobs`: choose different "broken" fixture each phrase.

### CR-055 Pixel Aura Emulation
- `energy`: 3 | `sections`: hook | `moods`: modern, digital
- `par`: alternating inner/outer head colors to fake pixel rings.
- `movers`: M2 beam plus soft aura-like wash overlap.
- `timing`: 1-beat pixel flips, 2-bar macro color drift.
- `palette`: neon cyan, violet, white.
- `variation_knobs`: swap inner/outer roles.

### CR-056 Cinematic Wipe
- `energy`: 3 | `sections`: transition | `moods`: filmic
- `par`: horizontal wipe across PAR_A from stage left to right.
- `movers`: M3 follows wipe edge as moving keylight.
- `timing`: 2-bar wipe.
- `palette`: tungsten white into cool moonlight.
- `variation_knobs`: reverse wipe direction per transition.

### CR-057 Glitch Blocks
- `energy`: 4 | `sections`: bass switch, fill | `moods`: digital chaos
- `par`: abrupt color block changes on 1/4 beat grid.
- `movers`: M1/M2 short random target snaps within safe zones.
- `timing`: 1-bar glitch packets.
- `palette`: white, red, cyan.
- `variation_knobs`: glitch density 20-70%.

### CR-058 Negative Space Drop
- `energy`: 4 | `sections`: alt drop | `moods`: minimal aggression
- `par`: very low base, using darkness as main design element.
- `movers`: narrow beams only, high contrast against dark room.
- `timing`: sparse beat-locked hits.
- `palette`: white + one saturated accent.
- `variation_knobs`: accent color per 8-bar phrase.

### CR-059 Disco Shatter
- `energy`: 4 | `sections`: house/disco moments | `moods`: celebratory
- `par`: warm party wash with pulse on clap.
- `movers`: beams to `DISCO_BALL`, then quick crowd scans.
- `timing`: 1-bar clap pulse + 4-bar ball hits.
- `palette`: gold, pink, white.
- `variation_knobs`: ball-hit rate by section density.

### CR-060 Ceiling Cathedral Strobe
- `energy`: 5 | `sections`: final peak | `moods`: monumental
- `par`: saturated low-mid wash to hold room color.
- `movers`: all fixtures target `CENTER_CEILING`; short synchronized strobe packets.
- `timing`: 2-bar motif, strobe only on bar 2.
- `palette`: deep blue + white.
- `variation_knobs`: strobe packet length 1/4 to 1 beat.

---

## 7) Section-to-Strategy Quick Map

Use this map before selecting recipes:

- `intro`: CR-001..CR-010, CR-045, CR-052
- `groove/verse`: CR-011..CR-020, CR-053, CR-054
- `build`: CR-021..CR-030
- `drop/peak`: CR-031..CR-044, CR-060
- `breakdown/emotional`: CR-045..CR-052
- `experimental transitions`: CR-053..CR-059

---

## 8) Genre Starting Packs (PAR + Mover Defaults)

### House / Melodic House (118-126 BPM)
- Base: warm PAR canvas (20-45%)
- Motion: smooth mover arcs (2-4 bar loops)
- Accents: white hits on phrase starts only
- Starter recipes: CR-011, CR-014, CR-019, CR-051, CR-059

### Techno / Melodic Techno (124-132 BPM)
- Base: cooler monochrome or dual-tone PAR bed
- Motion: geometric mover patterns + occasional prism
- Accents: restrained but high-contrast drops
- Starter recipes: CR-017, CR-022, CR-028, CR-039, CR-058

### Drum & Bass / 170-180 BPM
- Base: simpler PAR states to keep clarity at speed
- Motion: fast mover snaps, short strobe packets
- Accents: kick/snare split and phrase resets
- Starter recipes: CR-012, CR-023, CR-032, CR-036, CR-042

### Bass / Dubstep
- Base: dark floor with selective PAR blasts
- Motion: aggressive target snapping and hard cuts
- Accents: negative space before impact
- Starter recipes: CR-030, CR-033, CR-040, CR-044, CR-057

---

## 9) Anti-Patterns (What To Avoid)

- PAR and movers both running dense independent motion for long periods.
- Constant full-saturation rainbow looks with no visual hierarchy.
- Repeated all-white output that removes emotional color narrative.
- No dark moments; contrast requires controlled absence of light.
- Strobe overuse in verses/grooves where readability should lead.
- High-speed movement in every section (fatigue and loss of meaning).

---

## 10) AI Prompt Templates

### Template A: Section Look Generation

```text
Generate 3 lighting looks using schema v1.
Inputs:
- section: build
- bpm: 128
- mood: dark, driving
- energy_target: 3->4
- required_fixtures: PAR_A, PAR_B, M1_BEAM, M2_HYBRID
- keep_profile_for: vocalist readability
Constraints:
- no full strobe longer than 1 beat
- one blackout cut before drop
- keep PAR base between 18% and 55%
Output:
- YAML objects with id, strategy, timing, variation_knobs
```

### Template B: 32-Bar Arc

```text
Design a 32-bar arc:
- bars 1-8 intro (energy 1-2)
- bars 9-16 groove (energy 2)
- bars 17-24 build (energy 3-4)
- bars 25-32 drop (energy 5 then settle to 4)
Use recipe IDs as references and include transition notes.
```

### Template C: Safe Randomizer

```text
Randomize one look from [CR-011..CR-020] with these fixed rules:
- preserve palette family (cool)
- keep one static anchor fixture
- movement_rate max = medium
- no more than two simultaneous accent events per beat
Return: final cue with rationale.
```

---

## 11) Source Notes (Research)

Primary references used to build this document:

- ETC blog, Stage Lighting Design Part 3 (controllable properties):  
  https://blog.etcconnect.com/stage-lighting-design-part-3
- ETC blog, Stage Lighting Design Part 4 (fixture categories incl. PAR and moving lights):  
  https://blog.etcconnect.com/stage-lighting-design-part-4
- ETC blog, Stage Lighting Design Part 5 (lighting angles):  
  https://blog.etcconnect.com/stage-lighting-design-part-5
- ETC blog, Stage Lighting Design Part 6 (color behavior and palette intent):  
  https://blog.etcconnect.com/stage-lighting-design-part-6
- CHAUVET DJ 4BAR product/spec page (PAR-system behavior reference):  
  https://www.chauvetdj.com/products/4bar/
- CHAUVET DJ Intimidator Spot 360X page (moving spot feature reference):  
  https://www.chauvetdj.com/products/intimidator-spot-360x/
- Martin MAC Aura XIP page (moving wash/beam hybrid behavior reference):  
  https://www.martin.com/en-US/products/mac-aura-xip

Venue-local references aligned with each venue profile:
- `venue/<name>/plot.md`
- `venue/<name>/focus-positions.md`
- `venue/<name>/patch.md`
- `venue/<name>/references/creative-profile.json`
- `venue/<name>/references/creativity-venue.md`
- `references/bpm-timing.md`

---

## 12) EDM/Electronic Concept Expansion (48 Additional Concepts)

Use these as fast modular ideas. They are intentionally compact so AI can combine them.

### 12.1 Rhythm-Driven Concepts

| ID | Concept | Best For | PAR Role | Mover Role | Timing Hook |
|---|---|---|---|---|---|
| EDM-001 | Four-on-Floor Breather | House intros | Warm low canvas | Slow center orbit | 2-bar pulse |
| EDM-002 | Offbeat Lift | Deep house groove | Offbeat dimmer bumps | Beat-1 downlight hits | 1-bar loop |
| EDM-003 | Clap Bloom | House drops | Mid-sat bed | Clap-only prism bloom | Bars 2 and 4 |
| EDM-004 | Kick Rail | Tech house | Short kick flash lanes | Fast floor sweeps | 1-beat |
| EDM-005 | Ghost Hat Shimmer | Progressive house | Stable PAR bed | Tiny hat shimmer pans | 1/8 note accents |
| EDM-006 | Snare Ladder | Build sections | Rising PAR intensity | Tilt climbs on snares | 8-bar ramp |
| EDM-007 | Double-Time Switch | DnB drops | Simpler two-state base | Snap targets at double time | 2-bar toggle |
| EDM-008 | Half-Time Anchor | Dubstep groove | Heavy low base | Sparse heavy hits | 2-beat hits |
| EDM-009 | Triplet Surge | Psytrance | Triplet PAR accents | Circular beam chases | 1-bar triplets |
| EDM-010 | Gallop Engine | Hardstyle | Hard pulse + blackout gaps | Diagonal sweeps | 3+3+2 feel |
| EDM-011 | Fill Detonator | Any drop fill | PAR hold then flash | Fill-trigger strobe packet | Last beat of bar |
| EDM-012 | Delay Echo | Melodic techno | Echoed intensity tails | Delayed mirror sweep | 1/4 beat delay |
| EDM-013 | Sidechain Light | Future bass | Duck PAR on kicks | Lead beam stable | Kick envelope |
| EDM-014 | Riser Pressure | Builds | Saturation increase | Pan range shrink | 4-bar tension rise |
| EDM-015 | Downbeat Blade | Festival drop | Color flood | White blade on beat 1 | 1-bar |
| EDM-016 | Phrase Gate | All genres | PAR gate every 8 bars | Mover freeze then release | 8-bar phrase |

### 12.2 Space/Geometry Concepts

| ID | Concept | Best For | PAR Role | Mover Role | Timing Hook |
|---|---|---|---|---|---|
| EDM-017 | Tunnel Forward | Techno | Dark edge + center line | Converge to `DSC` | 4-bar push |
| EDM-018 | Ceiling Web | Progressive | Low room tone | Beams on `CENTER_CEILING` | 2-bar weave |
| EDM-019 | Wall Story | Minimal/acid | PAR_B dominant wall color | Center-only accents | 4-bar calls |
| EDM-020 | X-Cross Lattice | Peak drops | Alternating PAR side colors | M1/M2 cross patterns | Beat-synced |
| EDM-021 | Ring and Core | Main chorus | PAR ring around stage | Profile core at `C` | 1-bar |
| EDM-022 | Reverse Perspective | Experimental | Bright upstage PAR | Movers toward audience plane | 2-bar |
| EDM-023 | Triangle Sweep | Trance | 3-state PAR chase | 3-point beam route | 1-bar triangle |
| EDM-024 | Fan Collapse | Build/drop | Wide PAR fan to narrow | Beam fan collapses center | 8 bars |
| EDM-025 | Side Silhouette | Vocals | Back PAR silhouette | Side mover keys | 4-bar holds |
| EDM-026 | Floor Scan | Club groove | PAR floor wash | Fast low sweeps | 1-beat |
| EDM-027 | Backline Halo | DJ focus | PAR halo at booth | Slow aerial frame | 2 bars |
| EDM-028 | Parallax Slide | Interlude | PAR colors drift opposite | Matching spatial drift | 8 bars |
| EDM-029 | Corridor Cut | Build | Narrow PAR corridor | Sharp beam cuts across | 1 bar |
| EDM-030 | Orbit Cage | Techno peak | Static dark base | Circular opposing mover arcs | 2 bars |
| EDM-031 | Mirror Break | Transition | Symmetrical PAR base | One-beat asymmetry bursts | Every 4 bars |
| EDM-032 | Crowd Horizon | Festival chorus | Horizontal PAR stripe | Mover sweeps over crowd line | 1-2 bars |

### 12.3 FX/Transition Concepts

| ID | Concept | Best For | PAR Role | Mover Role | Timing Hook |
|---|---|---|---|---|---|
| EDM-033 | Blackout Slingshot | Pre-drop | Full cut to black | Snap return with beams | Last 1 beat |
| EDM-034 | White Flash Resolve | Big transitions | Color world reset | 1-beat white resolve | Phrase end |
| EDM-035 | Prism Unfold | Melodic build | Stable bed | Prism opens gradually | 4 bars |
| EDM-036 | Gobo Melt | Breakdown | Soft PAR haze tint | Slow gobo rotation | 8 bars |
| EDM-037 | Stutter Gate | Bass fills | PAR stutter packet | Target jump stutter | 1/4 beat |
| EDM-038 | Freeze Frame | Impact moments | PAR hold frame | Movers freeze then burst | 1-bar |
| EDM-039 | Color Inversion | Section change | Warm-cool swap | Mirror intensity swap | Beat 1 switch |
| EDM-040 | Saturation Punch | Hook entry | +30% sat step | White accents restrained | Beat 1 and 3 |
| EDM-041 | Monochrome Lock | Techno | One-hue PAR control | Movement-only variation | 8 bars |
| EDM-042 | RGB Slice | Electro | PAR heads in RGB slices | White mover knives | 1-bar |
| EDM-043 | Chase Cancel | Fake drop | Build chase then abort | Static stare-down | Bar 7/8 |
| EDM-044 | Spiral Abort | Psy build fakeout | Rotating PAR wheel | Spiral stops suddenly | Last beat |
| EDM-045 | Pulse-to-Glow | Post-drop settle | Rhythmic pulse fades out | Motion slows to static | 4 bars |
| EDM-046 | Memory Flash | Emotional callbacks | Base color world | 1-beat old palette flash | Every 16 bars |
| EDM-047 | Crowd Scan Tax | Peak control | PAR remains readable | Limit crowd scans to hooks | 4-bar windows |
| EDM-048 | End-Cap Fade | Outros | Warm low fade | Single final aerial sweep | 8-16 bars |

### 12.4 Quick Combination Rules

- Pick `1` rhythm concept + `1` geometry concept + `1` FX concept.
- Keep PAR strategy from one concept and mover strategy from another if they clash.
- Use one palette family for each 16-bar block, then evolve.
- Save hardest contrast (`blackout`, `white strike`, `strobe packet`) for structural moments.

---

## 13) Influential EDM/Electronic Lighting Designers To Study

Note: this is not an objective ranking; it is an influence list based on recurring coverage in touring/festival production media.

### 13.1 Designer Study Cards

### DSR-001 Steve Lieberman (SJ Lighting)
- `known_for`: Calvin Harris Ibiza + Coachella CircoLoco production design.
- `signature`: huge audience-readable geometry, strong section punctuation, clear drop architecture.
- `borrow_for_venue`: use mirrored sweeps and large contrast shifts (CR-031, CR-044, EDM-020).

### DSR-002 Andy Hurst
- `known_for`: Swedish House Mafia shows; credits with Faithless and The Prodigy.
- `signature`: aggressive kinetic movement with controlled theatrical framing.
- `borrow_for_venue`: high-energy mover aggression over disciplined PAR base (CR-032, CR-039, EDM-030).

### DSR-003 Ross Chapple
- `known_for`: Eric Prydz EPIC/HOLO era design direction.
- `signature`: integration of lighting with lasers/visual layers; precise futuristic spatial language.
- `borrow_for_venue`: ceiling architecture looks and geometric beam matrices (CR-043, EDM-018, EDM-029).

### DSR-004 Matt Smith
- `known_for`: RUFUS DU SOL design direction with emotion-forward lighting and visual cohesion.
- `signature`: atmospheric depth, restrained color transitions, narrative pacing.
- `borrow_for_venue`: long phrase morphs and emotional breakdown sculpting (CR-001, CR-045, EDM-045).

### DSR-005 Kyle Kegan
- `known_for`: ODESZA productions emphasizing immersive audience perspective.
- `signature`: hybrid festival-scale readability with cinematic mood arcs.
- `borrow_for_venue`: alternating intimate and massive looks while preserving continuity (CR-051, EDM-032).

### DSR-006 Ed Warren
- `known_for`: four tet / fred again.. / skrillex MSG era; TPi Lighting Designer of the Year (2023).
- `signature`: adaptable minimalist-to-maximalist transitions and musical responsiveness.
- `borrow_for_venue`: quick mode shifts without losing anchor (CR-038, CR-058, EDM-039).

### DSR-007 Erik Mahowald
- `known_for`: deadmau5 Retro5pective visual + lighting design.
- `signature`: playful visual architecture, strong identity color use, geometric object focus.
- `borrow_for_venue`: iconic color identities and object-centric beam framing (CR-055, EDM-042).

### DSR-008 Alex Ares
- `known_for`: deadmau5 tour lighting direction and Swedish House Mafia visual design era collaborations.
- `signature`: punchy EDM timing and robust touring practicalities.
- `borrow_for_venue`: beat-locked impact recipes with reliable fallback looks (CR-040, EDM-011).

### DSR-009 Patrick Dierson
- `known_for`: Ultra Main Stage production design (2025).
- `signature`: broad multi-artist adaptability while keeping a coherent headliner-ready visual language.
- `borrow_for_venue`: build "neutral but strong" base looks that can re-skin quickly (CR-011, EDM-016).

### DSR-010 Evan Bloom
- `known_for`: Ultra RESISTANCE 2025 lighting design.
- `signature`: underground techno emphasis with dense atmosphere and directional movement.
- `borrow_for_venue`: dark monochrome systems + geometric sweeps (CR-017, CR-041, EDM-030).

### 13.2 How To Use Designer Research In AI Generation

- Use one designer card as the primary style anchor per song.
- Blend no more than two cards per section to avoid style mud.
- Keep a stable project signature so shows still feel like your brand.

---

## 14) EDM Color Palette Inspiration Bank

### 14.1 Palette Usage Rules

- PAR fixtures should usually hold the dominant `world color`.
- Movers should carry contrast accents, targets, and white punctuation.
- For high-BPM content, simplify palettes rather than adding more colors.
- A 2-color system plus white often reads better than 5-color chaos.

### 14.2 Palette Library (AI-Ready)

Format:
- `base`: recommended PAR world color(s)
- `accent`: recommended mover contrast color(s)
- `hit`: transient color for drops/fills (often white)

### P-001 Neon Cyan Drive
- `hex`: `#00E5FF #007CFF #E6F9FF`
- `base`: cyan/blue
- `accent`: cool white blades
- `hit`: white
- `best_for`: progressive house, trance

### P-002 Infrared Techno
- `hex`: `#FF2A2A #8B0000 #FFEAEA`
- `base`: deep red
- `accent`: white cuts
- `hit`: desaturated white-red
- `best_for`: hard techno, industrial

### P-003 Void Indigo
- `hex`: `#1B1464 #3A2A9E #B8B8FF`
- `base`: indigo
- `accent`: violet highlights
- `hit`: pale ice
- `best_for`: melodic techno, dark intros

### P-004 Toxic Lime
- `hex`: `#B7FF00 #4D8F00 #F1FFD1`
- `base`: acid lime
- `accent`: dark green shadow
- `hit`: pale lime-white
- `best_for`: bass house, electro

### P-005 Amber + Steel
- `hex`: `#FFB347 #2F5D8A #F5F8FF`
- `base`: amber
- `accent`: steel blue
- `hit`: cool white
- `best_for`: organic house, melodic breakdowns

### P-006 Magenta Voltage
- `hex`: `#FF00A8 #7A0C5E #FFD6F3`
- `base`: magenta
- `accent`: deep wine
- `hit`: pink-white
- `best_for`: synthwave, electro-pop EDM

### P-007 Arctic Mint
- `hex`: `#8FFFE2 #00C9A7 #EFFFFA`
- `base`: mint wash
- `accent`: teal cuts
- `hit`: cold white
- `best_for`: chill electronic, downtempo

### P-008 Ultraviolet Core
- `hex`: `#6A00FF #2A005F #DCC7FF`
- `base`: violet
- `accent`: indigo
- `hit`: pale lilac
- `best_for`: psytrance, melodic techno

### P-009 Carbon White
- `hex`: `#0D0D0D #FFFFFF #7F7F7F`
- `base`: near-black
- `accent`: sharp white
- `hit`: full white
- `best_for`: minimal techno, dramatic drops

### P-010 Sunset Circuit
- `hex`: `#FF6B35 #FFB238 #5A2A83`
- `base`: orange/amber
- `accent`: violet
- `hit`: warm white
- `best_for`: house, disco-edm crossovers

### P-011 Oceanic Pulse
- `hex`: `#005377 #00A6D6 #C2F3FF`
- `base`: deep ocean blue
- `accent`: cyan pulse
- `hit`: ice white
- `best_for`: progressive, trance

### P-012 Crimson Orbit
- `hex`: `#D90429 #4A0010 #FFD9E0`
- `base`: crimson
- `accent`: black-red shadow
- `hit`: pale pink-white
- `best_for`: cinematic drops

### P-013 Emerald Alloy
- `hex`: `#00A86B #005F3B #D9FFE9`
- `base`: emerald
- `accent`: dark green
- `hit`: mint white
- `best_for`: groovy house, afro-electronic

### P-014 Electric Lavender
- `hex`: `#B76DFF #6B2CBF #F2E7FF`
- `base`: lavender
- `accent`: rich purple
- `hit`: lilac-white
- `best_for`: vocal trance, euphoric sections

### P-015 Ruby + Cyan Clash
- `hex`: `#E63946 #00D1FF #F1F8FF`
- `base`: ruby or cyan blocks
- `accent`: opposing color for movers
- `hit`: white
- `best_for`: high-contrast festival drops

### P-016 Mono Blue Discipline
- `hex`: `#0D3B66 #1D5FA2 #9DCBFF`
- `base`: single blue family
- `accent`: lighter blue highlights
- `hit`: cool white
- `best_for`: techno, long DJ journeys

### P-017 Laser Greenline
- `hex`: `#39FF14 #0F5A00 #E8FFD9`
- `base`: black/low
- `accent`: neon green lines
- `hit`: acid white
- `best_for`: psy, tech trance

### P-018 Desert Copper
- `hex`: `#B87333 #E09A5E #253046`
- `base`: copper amber
- `accent`: slate blue
- `hit`: warm white
- `best_for`: organic and melodic transitions

### P-019 Polar Night
- `hex`: `#102542 #1B3B6F #DDEBFF`
- `base`: midnight blue
- `accent`: steel
- `hit`: icy white
- `best_for`: intros, breakdowns

### P-020 Pulse Pink + Indigo
- `hex`: `#FF4DA6 #2D1E5F #FBE7FF`
- `base`: indigo
- `accent`: hot pink pulses
- `hit`: pink-white
- `best_for`: future bass, melodic drops

### P-021 Gold + Void
- `hex`: `#FFCC66 #3A2A00 #FFF5D6`
- `base`: dim gold
- `accent`: shadow amber-brown
- `hit`: gold-white
- `best_for`: anthem choruses

### P-022 Bronze + Teal
- `hex`: `#8C4A2F #0D8B8B #D9F7F7`
- `base`: bronze warmth
- `accent`: teal blades
- `hit`: neutral white
- `best_for`: hybrid electronic/world textures

### P-023 Cherry Storm
- `hex`: `#FF1744 #650019 #FFE4EB`
- `base`: dark cherry
- `accent`: bright cherry hits
- `hit`: white-pink
- `best_for`: high impact electro

### P-024 Ice and Fire
- `hex`: `#00C2FF #FF4D00 #F6FBFF`
- `base`: split warm/cool
- `accent`: whichever side is not base
- `hit`: bright white
- `best_for`: drops and fake-drop reveals

### 14.3 Palette Transition Recipes

- `cool -> warm`: lower saturation first, then shift hue over 2-4 bars.
- `warm -> cool`: keep intensity stable while hue rotates; avoid simultaneous dim drop.
- `mono -> dual-tone`: introduce second color in movers first, then PARs.
- `dual-tone -> mono`: remove accent color from PARs first, keep mover accents briefly.
- `color -> white impact`: max 1 beat full-white before returning to color world.

### 14.4 AI Palette Selection Rules

- `energy 1-2`: choose from P-003, P-007, P-019, P-016.
- `energy 3`: choose from P-005, P-010, P-014, P-018.
- `energy 4-5`: choose from P-001, P-002, P-015, P-023, P-024.
- For long sets, rotate palette family every 2-4 songs, not every section.

---

## 15) Additional EDM Designer Sources

- TPi, Calvin Harris / CircoLoco (Steve Lieberman):  
  https://www.tpimagazine.com/calvin-harris-circa-loco/
- Live Design, Swedish House Mafia and designer Andy Hurst:  
  https://www.livedesignonline.com/concerts/swedish-house-mafia-dance-tour-light
- TPi, Eric Prydz HOLO 2023 (Ross Chapple):  
  https://www.tpimagazine.com/eric-prydz-presents-holo/
- TPi, RUFUS DU SOL production profile (Matt Smith context):  
  https://www.tpimagazine.com/rufus-du-sol/
- TPi, ODESZA design profile (Kyle Kegan context):  
  https://www.tpimagazine.com/odesza/
- TPi, four tet/fred again../skrillex MSG (Ed Warren):  
  https://www.tpimagazine.com/four-tet-fred-again-skrillex/
- PLSN, deadmau5 Retro5pective (Erik Mahowald):  
  https://plsn.com/articles/production-profile/deadmau5-retro5pective/
- Live Design, deadmau5 Cube v3 and Alex Ares context:  
  https://www.livedesignonline.com/concerts/deadmau5-introduces-cube-v3-production-tour
- PLSN, Ultra Miami Main Stage 2025 (Patrick Dierson):  
  https://plsn.com/articles/production-profile/ultra-miami-main-stage-2025/
- PLSN, Ultra Miami RESISTANCE 2025 (Evan Bloom):  
  https://plsn.com/articles/production-profile/ultra-miami-resistance-stage-2025/
- PLSN, Armin van Buuren "The Orb" (Marc Heinz):  
  https://plsn.com/articles/production-profile/armin-van-buuren-the-orb/

---

## 16) EDM Pattern Engine For High Show Variety

This section is optimized for building hundreds of distinct shows without losing coherence.

Design defaults:
- Movers change position every `4 beats` (1 bar in 4/4) unless a variant is called.
- PAR behavior is primarily `fade` or `blink` quantized to `1`, `2`, or `4` beats.
- `8-beat` PAR patterns are reserved for breakdowns, intros, and emotional resets.
- Show uniqueness comes from an equal blend of:
  - movement structure differences
  - palette/effect differences

Zone shorthand used below:
- `C` center
- `SL/SR` stage left/right
- `USL/USC/USR` upstage left/center/right
- `DSL/DSC/DSR` downstage left/center/right
- `DJ` DJ Booth
- `DANCE` Dance Floor
- `CEIL` Center Ceiling
- `PAR_WALL` side-wall PAR target

Palette tags:
- `any`
- `mono-cool`
- `warm-cool`
- `neon-clash`
- `dark-white`
- `warm-organic`

### 16.1 Pattern Object Schemas

Use these fields in AI outputs.

```yaml
MoverPattern:
  id: MP-###
  name: string
  family: geometric|snap|atmospheric
  path_signature: "ZONE>ZONE>..."
  change_interval: "4b"   # default
  energy_range: "1-5"
  best_sections: [intro|verse|build|drop|breakdown|transition|outro]
  compatible_palettes: [palette tags]
  variation_knobs: [mirror, reverse, radius, dwell, fixture_subset]

ParPattern:
  id: PP-###
  mode: fade|blink|hybrid
  beat_quantization: 1|2|4|8
  grouping: PAR_A|PAR_B|split|alternating|all
  waveform: sine|triangle|square|pulse
  intensity_bounds: "min-max %"
  best_sections: [tags]
  pair_with_families: [geometric|snap|atmospheric]
```

### 16.2 Cadence Variants

All `MP-*` patterns are authored at `4b` step interval.

Allowed variants:
- `x2` variant: same path, `2b` step interval (build escalation).
- `x4` variant: same path, `1b` step interval (drop impact windows only).
- `hold` variant: every second step held for 2 bars (ambient control).

---

## 17) Mover Pattern Atlas (120 Patterns)

Distribution:
- `60` geometric (`MP-001..MP-060`)
- `36` snap/aggressive (`MP-061..MP-096`)
- `24` atmospheric (`MP-097..MP-120`)

### 17.1 Geometric Family (`MP-001..MP-060`)

| ID | Name | Path Signature (4b steps) | E | Best Sections | Palette Fit |
|---|---|---|---|---|---|
| MP-001 | Center Fan | `C>SL>C>SR` | 2-4 | verse, groove | any |
| MP-002 | Wide Rail | `USL>SL>SR>USR` | 2-4 | verse, build | any |
| MP-003 | Mirror Lane | `SL>C>SR>C` | 2-4 | verse, drop | warm-cool |
| MP-004 | Stage Edge Bounce | `DSL>SL>SR>DSR` | 3-4 | groove, drop | neon-clash |
| MP-005 | Right Bias Sweep | `C>SR>USR>SR` | 2-3 | verse, transition | mono-cool |
| MP-006 | Left Bias Sweep | `C>SL>USL>SL` | 2-3 | verse, transition | mono-cool |
| MP-007 | Crowd Traverse | `DSR>DSC>DSL>DSC` | 3-4 | drop, peak | neon-clash |
| MP-008 | Backline Traverse | `USR>USC>USL>USC` | 2-4 | build, transition | warm-cool |
| MP-009 | Out-In Rail | `SL>USL>USR>SR` | 2-4 | verse, build | any |
| MP-010 | In-Out Rail | `C>SR>C>SL` | 2-4 | groove, build | any |
| MP-011 | Depth Push | `C>DSC>C>USC` | 2-4 | build, verse | any |
| MP-012 | Front Lock | `DSC>C>USC>C` | 2-4 | verse, drop | warm-cool |
| MP-013 | Back Lock | `USC>C>DSC>C` | 2-4 | build, transition | mono-cool |
| MP-014 | Left Depth Ladder | `USL>SL>DSL>SL` | 2-4 | build, groove | any |
| MP-015 | Right Depth Ladder | `USR>SR>DSR>SR` | 2-4 | build, groove | any |
| MP-016 | Front Arc | `DSL>DSC>DSR>DSC` | 3-4 | drop, peak | neon-clash |
| MP-017 | Back Arc | `USL>USC>USR>USC` | 2-3 | intro, build | mono-cool |
| MP-018 | Center Breach | `USC>DSC>USC>DSC` | 3-4 | build, drop | dark-white |
| MP-019 | Depth Zig | `C>USC>DSC>USC` | 3-4 | build | warm-cool |
| MP-020 | Depth Zag | `C>DSC>USC>DSC` | 3-4 | build | warm-cool |
| MP-021 | X One | `USL>C>DSR>C` | 3-5 | build, drop | neon-clash |
| MP-022 | X Two | `USR>C>DSL>C` | 3-5 | build, drop | neon-clash |
| MP-023 | Full X | `USL>DSR>USR>DSL` | 4-5 | drop, peak | dark-white |
| MP-024 | Reverse X | `DSL>USR>DSR>USL` | 4-5 | drop, peak | dark-white |
| MP-025 | Diag Stair A | `USL>SR>DSL>C` | 3-4 | build, drop | warm-cool |
| MP-026 | Diag Stair B | `USR>SL>DSR>C` | 3-4 | build, drop | warm-cool |
| MP-027 | Cross Fan A | `USL>DSC>USR>C` | 3-4 | build, transition | mono-cool |
| MP-028 | Cross Fan B | `USR>DSC>USL>C` | 3-4 | build, transition | mono-cool |
| MP-029 | Corner Four | `USL>USR>DSR>DSL` | 3-4 | groove, drop | any |
| MP-030 | Corner Four Rev | `DSL>DSR>USR>USL` | 3-4 | groove, drop | any |
| MP-031 | Triangle Up | `SL>USC>SR>C` | 2-4 | verse, build | warm-cool |
| MP-032 | Triangle Down | `SL>DSC>SR>C` | 2-4 | groove, drop | warm-cool |
| MP-033 | Triangle Left | `USL>C>DSL>SL` | 2-4 | verse, transition | mono-cool |
| MP-034 | Triangle Right | `USR>C>DSR>SR` | 2-4 | verse, transition | mono-cool |
| MP-035 | Diamond Core | `C>USC>C>DSC` | 2-4 | intro, verse, build | any |
| MP-036 | Diamond Wide | `C>USL>C>DSR` | 3-4 | build, drop | neon-clash |
| MP-037 | Diamond Wide Rev | `C>USR>C>DSL` | 3-4 | build, drop | neon-clash |
| MP-038 | Kite Forward | `USC>SL>DSC>SR` | 3-4 | build | warm-cool |
| MP-039 | Kite Reverse | `DSC>SL>USC>SR` | 3-4 | build | warm-cool |
| MP-040 | Bowtie | `SL>USC>SR>DSC` | 3-5 | drop, peak | dark-white |
| MP-041 | Orbit Clockwise | `C>SL>USC>SR>DSC>C` | 2-4 | verse, transition | mono-cool |
| MP-042 | Orbit Counter | `C>SR>USC>SL>DSC>C` | 2-4 | verse, transition | mono-cool |
| MP-043 | Outer Ring | `USL>USR>DSR>DSL>USL` | 3-4 | build, drop | any |
| MP-044 | Inner Ring | `SL>USC>SR>DSC>SL` | 2-4 | groove, build | any |
| MP-045 | Figure8 A | `C>SL>C>SR>C>DSC>C>USC` | 2-4 | verse, transition | warm-cool |
| MP-046 | Figure8 B | `C>SR>C>SL>C>USC>C>DSC` | 2-4 | verse, transition | warm-cool |
| MP-047 | Clover L | `SL>USL>C>DSL>C` | 2-3 | intro, verse | mono-cool |
| MP-048 | Clover R | `SR>USR>C>DSR>C` | 2-3 | intro, verse | mono-cool |
| MP-049 | Spiral Out | `C>SL>USL>USR>SR>DSR>DSL>C` | 3-4 | build, transition | any |
| MP-050 | Spiral In | `DSL>DSR>SR>USR>USL>SL>C` | 3-4 | build, transition | any |
| MP-051 | Booth Frame | `DJ>SL>DJ>SR` | 2-4 | verse, build | warm-organic |
| MP-052 | Booth Pyramid | `DJ>USL>USC>USR>DJ` | 2-4 | intro, build | mono-cool |
| MP-053 | Ceiling Fan | `CEIL>SL>CEIL>SR` | 2-4 | build, transition | dark-white |
| MP-054 | Ceiling Cross | `CEIL>USL>CEIL>USR` | 3-5 | build, drop | dark-white |
| MP-055 | Ceiling Drop | `CEIL>C>DSC>C` | 3-5 | build, drop | dark-white |
| MP-056 | Ceiling Orbit | `CEIL>SL>USC>SR>CEIL` | 2-4 | transition, intro | mono-cool |
| MP-057 | Booth to Crowd | `DJ>C>DSC>C` | 2-4 | build, drop | warm-cool |
| MP-058 | Crowd to Booth | `DSC>C>DJ>C` | 2-4 | breakdown, verse | warm-organic |
| MP-059 | Ceiling to Corners | `CEIL>USL>DSR>USR>DSL>CEIL` | 4-5 | drop, peak | neon-clash |
| MP-060 | Par Wall Narrative | `PAR_WALL>C>SR>PAR_WALL` | 2-4 | verse, transition | warm-cool |

### 17.2 Snap/Aggressive Family (`MP-061..MP-096`)

| ID | Name | Path Signature (4b base) | E | Best Sections | Palette Fit |
|---|---|---|---|---|---|
| MP-061 | Quad Hit | `C>SL>SR>C` | 4-5 | drop, peak | dark-white |
| MP-062 | Hammer Left | `C>SL>C>USL` | 4-5 | drop | neon-clash |
| MP-063 | Hammer Right | `C>SR>C>USR` | 4-5 | drop | neon-clash |
| MP-064 | Front Jab | `C>DSC>C>DSL` | 4-5 | drop, chorus | dark-white |
| MP-065 | Back Jab | `C>USC>C>USL` | 4-5 | build, drop | dark-white |
| MP-066 | Split Jab A | `DSL>DSR>DSL>DSR` | 4-5 | drop | neon-clash |
| MP-067 | Split Jab B | `USL>USR>USL>USR` | 4-5 | build, drop | dark-white |
| MP-068 | Cross Jab A | `USL>DSR>USL>DSR` | 4-5 | drop | neon-clash |
| MP-069 | Cross Jab B | `USR>DSL>USR>DSL` | 4-5 | drop | neon-clash |
| MP-070 | Crowd Saw | `DSC>DSL>DSR>DSC` | 4-5 | drop, peak | any |
| MP-071 | Booth Saw | `DJ>USL>USR>DJ` | 3-5 | build, drop | warm-cool |
| MP-072 | Center Punch | `C>DSC>C>USC` | 4-5 | drop | dark-white |
| MP-073 | Zig One | `SL>SR>USL>USR` | 4-5 | drop, peak | neon-clash |
| MP-074 | Zig Two | `SR>SL>USR>USL` | 4-5 | drop, peak | neon-clash |
| MP-075 | Zig Three | `DSC>USC>DSL>USR` | 4-5 | build, drop | dark-white |
| MP-076 | Zig Four | `USC>DSC>USL>DSR` | 4-5 | build, drop | dark-white |
| MP-077 | Z Slash A | `USL>SR>USR>SL` | 4-5 | drop | neon-clash |
| MP-078 | Z Slash B | `DSL>USR>DSR>USL` | 4-5 | drop | neon-clash |
| MP-079 | Box Slash A | `SL>USR>SR>DSL` | 4-5 | peak | warm-cool |
| MP-080 | Box Slash B | `SR>USL>SL>DSR` | 4-5 | peak | warm-cool |
| MP-081 | Knife Left | `USL>SL>DSL>SL` | 4-5 | drop | dark-white |
| MP-082 | Knife Right | `USR>SR>DSR>SR` | 4-5 | drop | dark-white |
| MP-083 | Crank A | `C>USR>SL>DSC` | 4-5 | drop, fill | neon-clash |
| MP-084 | Crank B | `C>USL>SR>DSC` | 4-5 | drop, fill | neon-clash |
| MP-085 | Storm A | `USL>DSR>SL>USR>DSL>SR` | 4-5 | peak | any |
| MP-086 | Storm B | `USR>DSL>SR>USL>DSR>SL` | 4-5 | peak | any |
| MP-087 | Burst A | `C>USL>C>DSR>C` | 4-5 | fill, drop | dark-white |
| MP-088 | Burst B | `C>USR>C>DSL>C` | 4-5 | fill, drop | dark-white |
| MP-089 | Blitz Ring | `USL>USR>DSR>DSL` | 4-5 | drop | neon-clash |
| MP-090 | Blitz Ring Rev | `DSL>DSR>USR>USL` | 4-5 | drop | neon-clash |
| MP-091 | Ceiling Stab | `CEIL>SL>CEIL>SR>CEIL>DSC` | 4-5 | build, drop | dark-white |
| MP-092 | Booth Stab | `DJ>DSL>DJ>DSR>DJ>C` | 4-5 | build, drop | warm-cool |
| MP-093 | Crowd Rake | `DSR>DSC>DSL>SL>SR` | 4-5 | drop, peak | any |
| MP-094 | Back Rake | `USR>USC>USL>SL>SR` | 4-5 | build, drop | any |
| MP-095 | Cross Barrage | `USL>DSR>USR>DSL>USC>DSC` | 5 | peak | neon-clash |
| MP-096 | Center Chaos | `C>USL>SR>DSC>SL>USR>C` | 5 | peak, finale | any |

### 17.3 Atmospheric Family (`MP-097..MP-120`)

| ID | Name | Path Signature (4b steps) | E | Best Sections | Palette Fit |
|---|---|---|---|---|---|
| MP-097 | Slow LR | `SL>C>SR>C` | 1-2 | intro, breakdown | mono-cool |
| MP-098 | Slow Depth | `USC>C>DSC>C` | 1-2 | intro, breakdown | mono-cool |
| MP-099 | Slow Diagonal | `USL>C>DSR>C` | 1-2 | intro, breakdown | warm-cool |
| MP-100 | Slow Diagonal Rev | `USR>C>DSL>C` | 1-2 | intro, breakdown | warm-cool |
| MP-101 | Wide Drift | `USL>SL>C>SR>USR` | 1-2 | intro, verse | mono-cool |
| MP-102 | Back Drift | `USR>USC>USL>USC` | 1-2 | intro, break | mono-cool |
| MP-103 | Front Drift | `DSR>DSC>DSL>DSC` | 1-2 | intro, break | warm-organic |
| MP-104 | Halo Drift | `C>USC>C>SL>C>SR` | 1-2 | breakdown | warm-cool |
| MP-105 | Center Breathe | `C>CEIL>C>DSC` | 1-2 | intro, breakdown | mono-cool |
| MP-106 | Booth Breathe | `DJ>USC>DJ>C` | 1-2 | vocal, verse | warm-organic |
| MP-107 | Crowd Breathe | `DSC>C>DSC>C` | 1-2 | outro, break | warm-organic |
| MP-108 | Ceiling Breathe | `CEIL>C>CEIL>USC` | 1-2 | intro, transition | mono-cool |
| MP-109 | Side Breathe L | `SL>USL>SL>DSL` | 1-2 | intro, verse | mono-cool |
| MP-110 | Side Breathe R | `SR>USR>SR>DSR` | 1-2 | intro, verse | mono-cool |
| MP-111 | Wall Breathe | `PAR_WALL>SR>PAR_WALL>C` | 1-2 | transition | warm-cool |
| MP-112 | Cross Breathe | `USL>C>USR>C` | 1-2 | breakdown | warm-cool |
| MP-113 | Opening Arc | `USC>SL>C>SR>DSC` | 1-3 | intro, build | warm-organic |
| MP-114 | Closing Arc | `DSC>SR>C>SL>USC` | 1-3 | outro, break | warm-organic |
| MP-115 | Dream Ring | `C>SL>USC>SR>DSC>C` | 1-3 | breakdown, intro | mono-cool |
| MP-116 | Skyline Hold | `CEIL>USR>CEIL>USL` | 1-2 | intro, transition | dark-white |
| MP-117 | Memory Return | `C>DSC>C>USC>C` | 1-3 | breakdown, verse | warm-cool |
| MP-118 | Long Fall | `CEIL>USC>C>DSC` | 1-3 | breakdown, build | mono-cool |
| MP-119 | Long Rise | `DSC>C>USC>CEIL` | 1-3 | build, transition | mono-cool |
| MP-120 | Endcap Sweep | `SR>C>SL>USC>C` | 1-3 | outro, transition | any |

### 17.4 Mover Pattern Variation Knobs

Use these knobs to multiply uniqueness safely:
- `mirror`: swap left/right (`SL<->SR`, `USL<->USR`, `DSL<->DSR`)
- `reverse`: reverse path order
- `fixture_subset`: run path on `M1+M2`, keep `M3` as static key
- `radius`: use inner zones only (`SL/C/SR`) or full zones (corners included)
- `dwell`: hold every 2nd step for emotional versions
- `height_mode`: swap floor-facing routes with `CEIL` accents every 8 bars

---

## 18) PAR Pattern Cookbook (Fade/Blink Quantized)

### 18.1 PAR Patterns (`PP-001..PP-036`)

| ID | Mode | Beats | Grouping | Behavior | Best Sections | Pair With |
|---|---|---|---|---|---|---|
| PP-001 | fade | 1 | all | fast inhale/exhale all PARs | groove | snap |
| PP-002 | fade | 1 | alternating | PAR_A up while PAR_B down | groove | geometric |
| PP-003 | fade | 1 | PAR_A | 4BAR head-wave fade | groove | geometric |
| PP-004 | fade | 1 | PAR_B | side-wall pulse fade | groove | atmospheric |
| PP-005 | fade | 1 | split | center-out fade | build | geometric |
| PP-006 | fade | 1 | split | outer-in fade | build | geometric |
| PP-007 | fade | 2 | all | half-bar swell | verse | geometric |
| PP-008 | fade | 2 | alternating | A leads, B lags by 1 beat | verse | geometric |
| PP-009 | fade | 2 | alternating | B leads, A lags by 1 beat | verse | geometric |
| PP-010 | fade | 2 | PAR_A | odd-even 4BAR head fade | groove | geometric |
| PP-011 | fade | 2 | PAR_B | sidewall breathe | verse | atmospheric |
| PP-012 | fade | 2 | split | warm-cool crossfade | verse, build | geometric |
| PP-013 | fade | 4 | all | bar-length swell | intro, verse | atmospheric |
| PP-014 | fade | 4 | all | long plateau swell | intro, breakdown | atmospheric |
| PP-015 | fade | 4 | alternating | A/B bar morph | breakdown | atmospheric |
| PP-016 | fade | 4 | all | mono-color breathe | intro, breakdown | atmospheric |
| PP-017 | fade | 8 | all | ultra-slow inhale | intro, breakdown | atmospheric |
| PP-018 | fade | 8 | split | dusk-to-dawn color swell | breakdown, outro | atmospheric |
| PP-019 | blink | 1 | all | on-beat punch | drop | snap |
| PP-020 | blink | 1 | all | offbeat punch | drop | snap |
| PP-021 | blink | 1 | PAR_A | kick-only flashes | drop | snap |
| PP-022 | blink | 1 | PAR_B | snare-only flashes | drop | snap |
| PP-023 | blink | 1 | alternating | checker A/B blink | drop | snap |
| PP-024 | blink | 1 | all | 2-on / 2-off beat packet | drop, fill | snap |
| PP-025 | blink | 2 | all | half-bar toggle | groove, drop | geometric |
| PP-026 | blink | 2 | alternating | call/response A-B | groove, drop | geometric |
| PP-027 | blink | 2 | split | phrase stab on beats 1+3 | build, drop | snap |
| PP-028 | blink | 2 | PAR_A | bar-start accent only | build | geometric |
| PP-029 | blink | 4 | all | phrase marker flash | transition | geometric |
| PP-030 | blink | 4 | alternating | bar-1 flash, hold bar-2 | transition | atmospheric |
| PP-031 | blink | 8 | all | section beacon blink | transition, outro | atmospheric |
| PP-032 | blink | 8 | split | low-frequency warning blink | pre-drop | atmospheric |
| PP-033 | hybrid | 4 | all | 4-beat fade + beat-1 blink | build | geometric |
| PP-034 | hybrid | 2 | alternating | 2-beat fade + offbeat blink | groove | geometric |
| PP-035 | hybrid | 8 | all | 8-beat fade + 4-beat markers | breakdown | atmospheric |
| PP-036 | hybrid | 4 | split | long fade with syncopated stabs | build, drop | snap |

### 18.2 PAR Intensity Bounds

Recommended intensity envelopes:
- `intro/breakdown`: `10-35%`
- `verse/groove`: `20-55%`
- `build`: `30-70%`
- `drop/peak`: `45-100%` (brief)

---

## 19) Pairing Matrix: Mover Families x PAR Timing

| Mover Family | Energy | Primary PAR Timing | Secondary PAR Timing | Notes |
|---|---|---|---|---|
| geometric | 1-2 | 4b fade | 8b fade | keep room continuity high |
| geometric | 3 | 2b fade | 4b blink markers | good for verses/builds |
| geometric | 4-5 | 1b fade | 2b blink | avoid constant full-on blink |
| snap | 3-4 | 2b blink | 1b blink packets | strong for pre-drop motion |
| snap | 5 | 1b blink | hybrid 4b fade + accents | keep dark gaps for contrast |
| atmospheric | 1-2 | 8b fade | 4b fade | use as reset blocks |
| atmospheric | 3 | 4b fade | 4b blink markers | bridge into builds |

Anti-clash rules:
- If mover pattern is `snap` and running `1b` variant, PAR should not exceed 60% average.
- If PAR is `1b blink`, mover should use either:
  - 4b path changes, or
  - 2b path changes with reduced pan amplitude.
- Never run `MP-* x4` + `PP-019..PP-024` longer than 8 bars continuously.

---

## 20) Uniqueness Engine For Hundreds Of Shows

### 20.1 Show Fingerprint

Compute uniqueness fingerprint per show:
- ordered `MP` IDs per section
- ordered `PP` IDs per section
- palette IDs used (from `P-*`)
- FX flags (`strobe`, `prism`, `gobo`, `blackout_cuts`)

### 20.2 Hard Uniqueness Constraints

- No identical 32-bar pattern sequence within last `8` generated shows.
- First-drop 8-bar block cannot reuse exact `MP` order within last `12` shows.
- At least `3` different `MP` families used per 64-bar show.
- At least `2` palette families used per full show arc.
- No section can use same `PP` for more than 16 consecutive bars unless breakdown.

### 20.3 Soft Variety Targets

- Target overlap score `< 0.45` against rolling library (Jaccard on pattern IDs).
- At least one `mirror` or `reverse` transformation per major section.
- At least one low-motion reset every 24-32 bars.
- Keep white-hit moments to structural markers (phrase entry, drop entry, finales).

### 20.4 Transformation Stack

For each selected pattern, apply one transformation:
- `none`
- `mirror`
- `reverse`
- `mirror+reverse`
- `dwell`
- `fixture_subset`

This alone multiplies 120 patterns into a much larger unique set.

---

## 21) Show Assembly Blueprint (32/64 Bars)

### 21.1 32-Bar Blueprint

| Bars | Intent | Mover Family | Mover Interval | PAR Pattern Class | Notes |
|---|---|---|---|---|---|
| 1-8 | intro/setup | atmospheric | 4b hold | 4b or 8b fade | establish world |
| 9-16 | groove/verse | geometric | 4b | 2b fade or 2b blink | rhythm lock |
| 17-24 | build | geometric -> snap | 4b then 2b | hybrid / 2b blink | escalate every 4 bars |
| 25-32 | drop/peak | snap + geometric accents | 2b or 1b windows | 1b blink + 2b fallback | bar 25 impact, bars 29-32 variation |

### 21.2 64-Bar Blueprint

| Bars | Intent | Rule |
|---|---|---|
| 1-16 | Arc A | intro + groove with atmospheric/geometric blend |
| 17-32 | Arc B | build + drop using first pattern family set |
| 33-48 | Arc C | contrast arc with mirrored/reversed family set |
| 49-64 | Arc D | final build/drop with highest uniqueness transforms |

### 21.3 Selection Algorithm (Cookbook)

1. Pick energy curve and section map.
2. Pick palette family pair from `P-*` library.
3. Pick mover families by section from blueprint.
4. Pick `MP-*` IDs ensuring hard uniqueness constraints pass.
5. Pick `PP-*` IDs based on family pairing matrix.
6. Apply one transformation per section.
7. Add one reset moment every 24-32 bars.
8. Validate strobe/blackout usage caps.

### 21.4 Genre Preset Pattern Pools

### House Steady
- mover pool: `MP-001..MP-020`, `MP-031..MP-044`, `MP-097..MP-112`
- par pool: `PP-007..PP-018`, `PP-025..PP-030`
- palette pool: `P-005`, `P-010`, `P-018`, `P-021`

### Techno Drive
- mover pool: `MP-011..MP-040`, `MP-053..MP-060`, `MP-061..MP-084`
- par pool: `PP-012..PP-018`, `PP-019..PP-030`, `PP-033..PP-036`
- palette pool: `P-002`, `P-003`, `P-009`, `P-016`

### DnB Assault
- mover pool: `MP-021..MP-060`, `MP-061..MP-096`
- par pool: `PP-019..PP-028`, `PP-033..PP-036`
- palette pool: `P-001`, `P-015`, `P-023`, `P-024`

### Melodic Cinematic
- mover pool: `MP-035..MP-060`, `MP-097..MP-120`
- par pool: `PP-013..PP-018`, `PP-029..PP-035`
- palette pool: `P-003`, `P-005`, `P-014`, `P-019`

---

## 22) AI Prompts For Bulk Show Generation

### Prompt: 50 Unique Show Skeletons

```text
Generate 50 unique 32-bar show skeletons using:
- mover patterns from MP-001..MP-120
- par patterns from PP-001..PP-036
- palettes from P-001..P-024
Rules:
- movers change every 4 beats by default
- par quantization only 1/2/4 beats, allow 8 only in intro/breakdown
- no repeated first-drop MP sequence across outputs
- enforce at least 3 mover families per show
Output:
- list of 50 YAML blocks with bars, MP IDs, PP IDs, palette IDs, transformations
```

### Prompt: DnB Fast Variants

```text
Create 20 DnB drop variants (8 bars each):
- base on MP-061..MP-096
- use PP-019..PP-028
- allow MP x4 (1-beat) only on bars 1-2 and 7-8
- include one blackout cut and one white strike per variant
Return compact cue tables.
```

### Prompt: Emotional Reset Blocks

```text
Generate 12 breakdown blocks (8 bars):
- mover family: atmospheric only (MP-097..MP-120)
- par patterns: PP-013..PP-018 and PP-031..PP-035
- keep intensity 10-35%
- one CEIL or DJ focus motif per block
Return: block ID + cue recipe.
```

---

## 23) Research Addendum: Console Pattern Programming Principles

This section captures pattern-system ideas from modern console workflows and translates them to this project.

### 23.1 Practical Findings

1. Fixture order is not cosmetic; it changes how spread/phase patterns read.
2. One route can create many looks through phase/spread offsets and transform modes.
3. Keyframe effects are effectively flexible chases with interpolation control.
4. Beat-locked effect timing is more predictable when step widths sum to a clear beat measure.
5. Relative movement shapes (around a base position) scale better than hard absolute-only effects.
6. Position effects need realistic speed envelopes; over-fast cycles reduce readability and movement accuracy.
7. Per-step timing in chasers is critical for musicality and section-specific dynamics.

### 23.2 Translation To This Rig

- Keep mover routes explicit and quantized at `4 beats` by default.
- Apply transforms (`mirror`, `reverse`, `rotate`) before introducing speed changes.
- Use per-step timing as the primary section switch:
  - verse/groove: stable `4b`
  - build: `4b -> 2b`
  - drop windows: controlled `1b` bursts only
- Treat PARs as a separate rhythm layer:
  - `fade` or `chase` at `1/2/4` beats
  - reserve `8` beat only for intro/breakdown breathing

---

## 24) Mover Mega Pattern System (4-Beat Native)

Goal: make hundreds of shows different without manually authoring hundreds of full timelines.

### 24.1 ID Format

```text
MPX-R###-T##-L#
```

- `R###`: base route
- `T##`: transform
- `L#`: fixture role map

All `MPX` patterns are `4b` step interval by default.

### 24.2 Base Route Library (`R001..R064`)

#### Horizontal/Depth Core (`R001..R016`)

| Route ID | Path Signature |
|---|---|
| R001 | `C>SL>C>SR` |
| R002 | `C>SR>C>SL` |
| R003 | `SL>C>SR>C` |
| R004 | `SR>C>SL>C` |
| R005 | `USL>USC>USR>USC` |
| R006 | `USR>USC>USL>USC` |
| R007 | `DSL>DSC>DSR>DSC` |
| R008 | `DSR>DSC>DSL>DSC` |
| R009 | `USL>SL>DSL>SL` |
| R010 | `USR>SR>DSR>SR` |
| R011 | `C>USC>C>DSC` |
| R012 | `C>DSC>C>USC` |
| R013 | `C>USL>C>USR` |
| R014 | `C>DSL>C>DSR` |
| R015 | `DJ>C>DSC>C` |
| R016 | `CEIL>C>USC>C` |

#### Cross/Diagonal Core (`R017..R032`)

| Route ID | Path Signature |
|---|---|
| R017 | `USL>C>DSR>C` |
| R018 | `USR>C>DSL>C` |
| R019 | `USL>DSR>USR>DSL` |
| R020 | `DSL>USR>DSR>USL` |
| R021 | `USL>SR>DSL>C` |
| R022 | `USR>SL>DSR>C` |
| R023 | `SL>USC>SR>DSC` |
| R024 | `SR>USC>SL>DSC` |
| R025 | `DSL>USC>DSR>C` |
| R026 | `DSR>USC>DSL>C` |
| R027 | `USL>DSC>USR>C` |
| R028 | `USR>DSC>USL>C` |
| R029 | `C>USL>SR>DSC` |
| R030 | `C>USR>SL>DSC` |
| R031 | `CEIL>USL>DSR>CEIL` |
| R032 | `CEIL>USR>DSL>CEIL` |

#### Orbit/Polygon Core (`R033..R048`)

| Route ID | Path Signature |
|---|---|
| R033 | `USL>USR>DSR>DSL` |
| R034 | `DSL>DSR>USR>USL` |
| R035 | `C>SL>USC>SR>DSC>C` |
| R036 | `C>SR>USC>SL>DSC>C` |
| R037 | `C>SL>USL>USC>USR>SR>C` |
| R038 | `C>SR>USR>USC>USL>SL>C` |
| R039 | `C>DSL>DSC>DSR>C` |
| R040 | `C>USL>USC>USR>C` |
| R041 | `C>SL>C>USC>C>SR>C>DSC` |
| R042 | `C>SR>C>USC>C>SL>C>DSC` |
| R043 | `SL>USC>SR>C` |
| R044 | `SL>DSC>SR>C` |
| R045 | `USL>C>USR>C` |
| R046 | `DSL>C>DSR>C` |
| R047 | `CEIL>SL>USC>SR>CEIL` |
| R048 | `CEIL>SR>USC>SL>CEIL` |

#### Booth/Ceiling/FX Core (`R049..R064`)

| Route ID | Path Signature |
|---|---|
| R049 | `DJ>SL>DJ>SR` |
| R050 | `DJ>USL>USC>USR>DJ` |
| R051 | `DJ>C>USC>C` |
| R052 | `DJ>C>DSC>C` |
| R053 | `CEIL>USC>C>DSC` |
| R054 | `DSC>C>USC>CEIL` |
| R055 | `PAR_WALL>SR>C>SR` |
| R056 | `PAR_WALL>C>SL>C` |
| R057 | `DANCE>DSC>C>USC` |
| R058 | `DANCE>SL>C>SR` |
| R059 | `USR>USC>USL>SL>SR` |
| R060 | `DSR>DSC>DSL>SL>SR` |
| R061 | `CEIL>DSC>CEIL>C` |
| R062 | `CEIL>C>CEIL>USC` |
| R063 | `DJ>CEIL>DJ>C` |
| R064 | `PAR_WALL>CEIL>C>PAR_WALL` |

### 24.3 Transform Set (`T00..T11`)

| Transform | Logic |
|---|---|
| T00 | base route |
| T01 | mirror left/right |
| T02 | reverse route order |
| T03 | mirror + reverse |
| T04 | rotate route start by +1 step |
| T05 | rotate route start by +2 steps |
| T06 | rotate route start by +3 steps |
| T07 | hold every second step (2-bar dwell) |
| T08 | bounce extension (append reverse interior) |
| T09 | center-anchor insertion (`...>C>...`) |
| T10 | ceiling substitution every 4th step |
| T11 | booth substitution every 4th step |

### 24.4 Fixture Role Maps (`L1..L6`)

| Role Map | Behavior |
|---|---|
| L1 | all movers unison on same route |
| L2 | Sharpy + BSW mirrored, Profile static key at `C` |
| L3 | Sharpy lead, BSW one-step delayed, Profile key at `DSC` |
| L4 | Sharpy/BSW split route, Profile opposite-phase accent |
| L5 | Profile narrates route, Sharpy/BSW hold contrast beams |
| L6 | NI3K pan counter-rotates against route direction |

### 24.5 Pattern Count

`64 routes * 12 transforms * 6 role maps = 4608 mover patterns`

This is the recommended mover pattern backbone for "several hundred" show outputs.

### 24.6 Example Encodings

- `MPX-R019-T00-L1`: direct `USL>DSR>USR>DSL` unison cross at `4b`.
- `MPX-R033-T01-L2`: mirrored ring with split beams and static profile key.
- `MPX-R050-T03-L4`: reversed mirrored booth pyramid with split mover roles.
- `MPX-R061-T10-L6`: ceiling/crowd alternation with NI3K counter motion.

---

## 25) PAR Fade + Chase Expansion (1/2/4 Beat Focus)

Use this in addition to `PP-001..PP-036`.

Notation:
- `A1..A4` = 4BAR heads
- `B1..B2` = secondary PAR-role heads (per venue profile)

### 25.1 1-Beat Chase Set (`PP-037..PP-056`)

| ID | Beats | Chase Pattern | Grouping | Pair With |
|---|---|---|---|---|
| PP-037 | 1 | `A:1>2>3>4` | PAR_A | snap |
| PP-038 | 1 | `A:4>3>2>1` | PAR_A | snap |
| PP-039 | 1 | `A:1>2>3>4>3>2` | PAR_A | geometric |
| PP-040 | 1 | `A:2>3>1>4` | PAR_A | geometric |
| PP-041 | 1 | `A:1>4>2>3` | PAR_A | snap |
| PP-042 | 1 | `A:(1+3)>(2+4)` | PAR_A | geometric |
| PP-043 | 1 | `A:(1+2)>(3+4)` | PAR_A | geometric |
| PP-044 | 1 | `A:1>3>2>4` | PAR_A | snap |
| PP-045 | 1 | `A:4>2>3>1` | PAR_A | snap |
| PP-046 | 1 | `A:1>2>4>3` | PAR_A | snap |
| PP-047 | 1 | `B:1>2` | PAR_B | snap |
| PP-048 | 1 | `B:1>1>2>2` | PAR_B | geometric |
| PP-049 | 1 | `B:1>2>1>2` | PAR_B | snap |
| PP-050 | 1 | `A:1>2>3>4 + B:1>2` | all | snap |
| PP-051 | 1 | `A:4>3>2>1 + B:2>1` | all | snap |
| PP-052 | 1 | `A:1>2>3>4 + B:2>1` | all | geometric |
| PP-053 | 1 | `A:(1+3)>(2+4) + B:1>2` | all | geometric |
| PP-054 | 1 | `A:2>3>1>4 + B:1>2` | all | snap |
| PP-055 | 1 | `A:seed-rand-01 + B:toggle` | all | snap |
| PP-056 | 1 | `A:seed-rand-02 + B:toggle` | all | snap |

### 25.2 2-Beat Chase Set (`PP-057..PP-076`)

| ID | Beats | Chase Pattern | Grouping | Pair With |
|---|---|---|---|---|
| PP-057 | 2 | `A:1>2>3>4` | PAR_A | geometric |
| PP-058 | 2 | `A:4>3>2>1` | PAR_A | geometric |
| PP-059 | 2 | `A:1>2>3>4>3>2` | PAR_A | geometric |
| PP-060 | 2 | `A:2>3>2>3` | PAR_A | atmospheric |
| PP-061 | 2 | `A:1>4>1>4` | PAR_A | atmospheric |
| PP-062 | 2 | `A:1>2>3>4>4>3>2>1` | PAR_A | geometric |
| PP-063 | 2 | `A:4>3>2>1>1>2>3>4` | PAR_A | geometric |
| PP-064 | 2 | `A:(1+3)>(2+4)` | PAR_A | geometric |
| PP-065 | 2 | `B:1>2` | PAR_B | atmospheric |
| PP-066 | 2 | `B:1>1>2>2` | PAR_B | geometric |
| PP-067 | 2 | `A:1>2>3>4 + B:offset+1` | all | geometric |
| PP-068 | 2 | `A:1>2>3>4 + B:offset+2` | all | geometric |
| PP-069 | 2 | `A:4>3>2>1 + B:2>1` | all | geometric |
| PP-070 | 2 | `A:1>3>2>4 + B:1>2` | all | snap |
| PP-071 | 2 | `A:2>4>1>3 + B:2>1` | all | snap |
| PP-072 | 2 | `A:crossfade-ladder + B:toggle` | all | geometric |
| PP-073 | 2 | `A:(1+2)>(3+4) + B:1>2` | all | geometric |
| PP-074 | 2 | `A:wave-01 + B:1>2` | all | atmospheric |
| PP-075 | 2 | `A:syncopate-01 + B:toggle` | all | geometric |
| PP-076 | 2 | `A:seed-rand-03 + B:toggle` | all | geometric |

### 25.3 4-Beat Chase Set (`PP-077..PP-096`)

| ID | Beats | Chase Pattern | Grouping | Pair With |
|---|---|---|---|---|
| PP-077 | 4 | `A:1>2>3>4` | PAR_A | atmospheric |
| PP-078 | 4 | `A:4>3>2>1` | PAR_A | atmospheric |
| PP-079 | 4 | `A:1>2>3>4>3>2` | PAR_A | atmospheric |
| PP-080 | 4 | `A:2>3>1>4` | PAR_A | geometric |
| PP-081 | 4 | `A:1>4>2>3` | PAR_A | geometric |
| PP-082 | 4 | `A:(1+3)>(2+4)` | PAR_A | geometric |
| PP-083 | 4 | `A:pendulum-slow` | PAR_A | atmospheric |
| PP-084 | 4 | `B:1>2` | PAR_B | atmospheric |
| PP-085 | 4 | `B:1>1>2>2` | PAR_B | atmospheric |
| PP-086 | 4 | `A:1>2>3>4 + B:1>2` | all | geometric |
| PP-087 | 4 | `A:4>3>2>1 + B:2>1` | all | geometric |
| PP-088 | 4 | `A:mirror-lanes + B:toggle` | all | atmospheric |
| PP-089 | 4 | `A:alt-bars-cw/ccw + B:toggle` | all | geometric |
| PP-090 | 4 | `A:call-response A/B` | split | atmospheric |
| PP-091 | 4 | `A:staircase-slow + B:toggle` | all | geometric |
| PP-092 | 4 | `A:tunnel-in + B:hold` | all | atmospheric |
| PP-093 | 4 | `A:ring-slow + B:toggle` | all | atmospheric |
| PP-094 | 4 | `A:phrase-marker beat1 only` | all | geometric |
| PP-095 | 4 | `A:pre-drop marker bars 7-8` | all | snap |
| PP-096 | 4 | `A:seed-rand-04 + B:toggle` | all | atmospheric |

### 25.4 PAR Mode Priority For Your Preference

When using your preferred style:
- primary PAR modes: `fade` + `chase`
- secondary PAR modes: minimal `blink` only for impact punctuation

Recommended distribution for long runs:
- `45%` fade patterns
- `45%` chase patterns
- `10%` blink/hybrid accents

### 25.5 Sync Rules (Movers + PAR)

- If movers are `4b` position changes:
  - PAR can run at `1b`, `2b`, or `4b` safely.
- If PAR is `1b` chase:
  - movers should stay `4b` unless in short drop windows.
- If movers accelerate to `2b`:
  - PAR should usually step up one level slower (`4b` or `2b`), not equal or faster.

---

## 26) 300-Show Diversity Blueprint

### 26.1 Deterministic Show Key

Use:

```text
SHOW_KEY = ARC + MPX_POOL + PP_POOL + PALETTE_ARC + FX_PROFILE
```

Where:
- `ARC`: high-level 32/64-bar structure template
- `MPX_POOL`: selected mover IDs (`MPX-R###-T##-L#`)
- `PP_POOL`: selected PAR IDs (`PP-001..PP-096`)
- `PALETTE_ARC`: ordered `P-*` palette IDs
- `FX_PROFILE`: strobe/prism/gobo/blackout profile

### 26.2 Diversity Controls

Hard controls:
- no duplicate `SHOW_KEY` ever
- no duplicate first-drop `MPX` 8-bar sequence in last 20 shows
- no duplicate PAR 8-bar sequence in last 12 shows
- at least 1 transform (`T01..T11`) per major section

Soft controls:
- keep overall similarity score `< 0.40`
- include at least one atmospheric reset every 24-32 bars
- keep max strobe density under 20% of bars in non-peak sections

### 26.3 Arc Template Pack (`ARC-01..ARC-12`)

| ARC | Bars 1-8 | Bars 9-16 | Bars 17-24 | Bars 25-32 |
|---|---|---|---|---|
| ARC-01 | atmo + fade4 | geom + chase2 | geom->snap + chase2 | snap + chase1 |
| ARC-02 | atmo + fade8 | geom + fade2 | geom + chase2 | snap + chase1 |
| ARC-03 | geom + fade4 | geom + chase1 | snap + chase2 | geom/snap mix + chase1 |
| ARC-04 | atmo + fade8 | geom + fade4 | geom + chase2 | snap + blink1 accents |
| ARC-05 | geom + chase2 | geom + chase1 | snap + chase2 | snap + chase1 |
| ARC-06 | atmo + fade4 | geom + chase4 | geom + chase2 | snap + chase1 |
| ARC-07 | atmo + fade8 | geom + chase4 | geom + fade2 | geom + chase2 |
| ARC-08 | geom + fade2 | geom + chase2 | snap + chase2 | snap + chase1 |
| ARC-09 | atmo + fade4 | geom + chase2 | geom + chase1 | snap + chase1 |
| ARC-10 | atmo + fade8 | geom + fade2 | geom + chase2 | geom + chase2 |
| ARC-11 | geom + chase4 | geom + chase2 | snap + chase2 | snap + chase1 |
| ARC-12 | atmo + fade8 | geom + chase4 | geom + chase2 | snap + chase1 |

### 26.4 Expected Combinatorics

With conservative options:
- `12` arcs
- `120` mover picks per show from `MPX` space
- `32` PAR picks per show from `PP-001..PP-096`
- `24` palettes

Even with strong filtering and no-repeat windows, this supports several hundred unique shows.

---

## 27) Additional Research Sources (Pattern Programming)

Console/effects workflow references used for sections 23-26:

- Avolites Manual, Shapes and Effects introduction:  
  https://manual.avolites.com/docs/effects/
- Avolites Manual, Shape Generator (spread/phase and fixture offset concepts):  
  https://manual.avolites.com/docs/18.0/effects/shape-generator/
- Avolites Manual, Key Frame Shapes (keyframe chase-style interpolation):  
  https://manual.avolites.com/docs/effects/key-frame-shapes/
- Avolites Manual, Controlling Fixtures (fixture order and spread behavior):  
  https://manual.avolites.com/docs/quick-start/controlling-fixtures/
- grandMA3 User Manual, Phasers:  
  https://help.malighting.com/grandMA3/2.2/HTML/phaser.html
- grandMA3 User Manual, Measure keyword (beat-accurate phaser cycle logic):  
  https://help.malighting.com/grandMA3/2.0/HTML/keyword_measure.html
- grandMA3 User Manual, MAtricks Transform (mirror/transform behavior):  
  https://help.malighting.com/grandMA3/2.0/HTML/matricks_transform.html
- QLC+ Documentation, Chaser Editor (per-step fade/hold/duration and run order):  
  https://docs.qlcplus.org/v5/function-manager/chaser-editor
- QLC+ Documentation, Glossary and Concepts (chaser/sequence behavior):  
  https://docs.qlcplus.org/v4/basics/glossary-and-concepts

---

## 28) Whole-Rig Coordination Techniques (30)

Goal: all fixtures should either move together or clearly play off each other.

Default timing baseline:
- movers: `4b` position changes
- PARs: `fade` or `chase` at `1b`, `2b`, or `4b`

Technique schema:

```yaml
id: INT-###
relationship: unison|counterpoint|inclusion
core_logic: short description
timing_recipe: "movers=4b, pars=..."
starter_combo: "MPX-... + PP-..."
```

### 28.1 Unison Cohesion (`INT-001..INT-010`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-001 | Full Lane Lock | unison | PAR chase direction matches mover route direction exactly. | `movers=4b, pars=1b chase` | `MPX-R001-T00-L1 + PP-037` |
| INT-002 | Downbeat Unison Hit | unison | All fixtures accent beat 1 each bar, then return to base motion. | `movers=4b, pars=2b chase + beat1 hit` | `MPX-R011-T00-L2 + PP-067` |
| INT-003 | Phrase Gate Open | unison | First bar of each 8-bar phrase is fully synchronized. | `movers=4b, pars=4b chase marker` | `MPX-R035-T04-L1 + PP-094` |
| INT-004 | Color World Lock | unison | PAR and mover colors rotate together but positions differ. | `movers=4b, pars=2b fade/chase` | `MPX-R043-T00-L3 + PP-012` |
| INT-005 | Ceiling Lift Together | unison | Both PAR intensity and mover height rise together into phrase peak. | `movers=4b, pars=4b fade` | `MPX-R053-T00-L2 + PP-013` |
| INT-006 | Booth Focus Envelope | unison | Whole rig converges around booth moments for section framing. | `movers=4b, pars=2b fade` | `MPX-R049-T00-L1 + PP-008` |
| INT-007 | Ring March | unison | Circular mover route with matching PAR ring chase. | `movers=4b, pars=1b chase` | `MPX-R033-T00-L1 + PP-050` |
| INT-008 | Fade-to-Chase Sync | unison | PARs fade for 4 bars then switch to chase exactly when movers switch pattern family. | `movers=4b, pars=4b fade -> 1b chase` | `MPX-R041-T02-L2 + PP-033` |
| INT-009 | Chorus Stack | unison | Verse uses restrained sync, chorus adds full-fixture alignment. | `movers=4b, pars=2b chase -> 1b chase` | `MPX-R029-T01-L4 + PP-070` |
| INT-010 | White Resolve Together | unison | Phrase end: synchronized white resolve then return to color. | `movers=4b, pars=4b chase + beat1 white` | `MPX-R061-T00-L6 + PP-095` |

### 28.2 Counterpoint Play-Off (`INT-011..INT-020`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-011 | Opposing Rails | counterpoint | PAR chase runs L->R while movers run R->L. | `movers=4b, pars=1b chase` | `MPX-R002-T00-L2 + PP-038` |
| INT-012 | In-Out Duel | counterpoint | PARs chase outer->inner while movers route center->edges. | `movers=4b, pars=2b chase` | `MPX-R014-T00-L3 + PP-062` |
| INT-013 | Front-Back Tug | counterpoint | PAR pulse emphasizes downstage while movers oscillate upstage. | `movers=4b, pars=2b fade` | `MPX-R005-T00-L1 + PP-011` |
| INT-014 | Warm-Cool Opposition | counterpoint | PAR warm chase against cool mover beams, swapped every 8 bars. | `movers=4b, pars=2b chase` | `MPX-R021-T03-L4 + PP-068` |
| INT-015 | Beat-Parity Split | counterpoint | PARs own odd beats, movers own even beats. | `movers=4b, pars=1b chase` | `MPX-R017-T00-L2 + PP-023` |
| INT-016 | Diagonal Clash | counterpoint | PAR chase follows one diagonal while movers strike opposite diagonal. | `movers=4b, pars=1b chase` | `MPX-R019-T00-L4 + PP-041` |
| INT-017 | Late Entry Shadow | counterpoint | PAR chase leads by one beat; movers echo one beat late. | `movers=4b delayed, pars=1b chase` | `MPX-R023-T05-L3 + PP-044` |
| INT-018 | Density Offset | counterpoint | Fast PAR chase over sparse mover positions for readable tension. | `movers=4b, pars=1b chase` | `MPX-R052-T00-L5 + PP-039` |
| INT-019 | Height Split | counterpoint | PARs stay floor/wall; movers stay ceiling/high plane. | `movers=4b high routes, pars=2b chase` | `MPX-R062-T00-L2 + PP-066` |
| INT-020 | Polarity Flip | counterpoint | Every 8 bars swap leader/follower roles between PAR and movers. | `movers=4b, pars=2b chase` | `MPX-R036-T02-L4 + PP-071` |

### 28.3 PAR Chase Includes Movers (`INT-021..INT-030`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-021 | Chase Leader | inclusion | Active mover follows the currently lit PAR chase step. | `movers=4b anchor + 1b leader accents, pars=1b chase` | `MPX-R001-T00-L3 + PP-037` |
| INT-022 | Every-4th-Step Join | inclusion | Movers join PAR chase on every 4th PAR step only. | `movers=4b, pars=1b chase` | `MPX-R011-T00-L2 + PP-050` |
| INT-023 | Alternating Joiners | inclusion | Bar A: Sharpy joins PAR chase; Bar B: BSW joins. | `movers=4b swaps, pars=1b chase` | `MPX-R003-T04-L4 + PP-052` |
| INT-024 | Pair Chase + Counter Beams | inclusion | PAR pairs chase while movers hit opposite pair endpoints. | `movers=4b, pars=1b pair chase` | `MPX-R031-T01-L4 + PP-053` |
| INT-025 | Ladder Inclusion | inclusion | Each bar adds one mover into the PAR chase stack. | `movers=4b ladder, pars=2b chase` | `MPX-R050-T00-L1 + PP-057` |
| INT-026 | Expand/Collapse Inclusion | inclusion | Start with PAR-only chase, expand to full rig, collapse back. | `movers=4b phases, pars=2b chase` | `MPX-R049-T07-L2 + PP-073` |
| INT-027 | Fill Burst Inclusion | inclusion | During fills, all movers briefly snap into the running PAR chase. | `movers=4b + 1b burst windows, pars=1b chase` | `MPX-R019-T08-L6 + PP-055` |
| INT-028 | Phrase-End Catch | inclusion | End of phrase: movers catch the final PAR chase step and hold. | `movers=4b with phrase hold, pars=2b chase` | `MPX-R043-T09-L3 + PP-074` |
| INT-029 | Relay Chase | inclusion | PAR heads pass chase to movers, then movers pass back to PARs. | `movers=4b relay points, pars=1b/2b chase` | `MPX-R041-T04-L5 + PP-072` |
| INT-030 | Ghosted Mover Trace | inclusion | Movers trace a slower 4-beat “ghost” of a fast PAR chase pattern. | `movers=4b ghost route, pars=1b chase` | `MPX-R034-T02-L2 + PP-040` |

### 28.4 Selection Rules For These 30 Techniques

- For verses: prioritize `INT-001..INT-020` with fewer inclusion bursts.
- For builds/drops: use `INT-021..INT-030` to merge PAR chase + movers.
- Keep inclusion techniques in windows (4-8 bars) so they stay special.
- After any high-density inclusion block, insert a simpler 4-bar reset look.

---

## 29) Web Research Synthesis (Parallel Tracks)

This section distills web research from multiple programming/design tracks into direct rules for this project.

### 29.1 Track A: Console Effect Engines

### Finding A1: Fixture order controls effect readability
- `source insight`: Avolites ties shape spread/phase to fixture selection order and group layout.
- `applied rule`: keep explicit fixture order maps and store pattern variants per order profile.
- `use`: treat order as a first-class variable, not an implementation detail.

### Finding A2: Spread + phase are the core pattern multipliers
- `source insight`: Avolites and ChamSys both expose spread/phase-style offsets as primary look multipliers.
- `applied rule`: keep route fixed; vary spread/phase/offset before inventing new routes.
- `use`: for each base route, generate multiple offset variants for fast variety.

### Finding A3: Keyframe effects are “chase-plus”
- `source insight`: Avolites key frame shapes are chase-like but with richer interpolation and spread behavior.
- `applied rule`: program PAR chase ideas as keyframe states, then apply spread/offset transforms.
- `use`: better continuity between fade and chase looks.

### Finding A4: Phaser timing must be beat-consistent
- `source insight`: grandMA3 phaser docs emphasize Width, Speed, and Measure consistency for predictable loops.
- `applied rule`: for any beat-synced pattern, ensure step widths sum cleanly to intended measure.
- `use`: eliminate drift in long-running 1/2/4-beat systems.

### Finding A5: Symmetry should be transform-based
- `source insight`: grandMA3 MAtricks Transform (Mirror with Blocks/Groups/Wings) preserves symmetry efficiently.
- `applied rule`: prefer transform operations (`mirror`, `reverse`, `rotate`) over duplicate hand-authored routes.
- `use`: large pattern count with controlled maintenance cost.

### Finding A6: Part/segment grouping drives controllable complexity
- `source insight`: ChamSys FX Parts/Segments allow repeated subgroup offsets across fixture arrays.
- `applied rule`: add subgroup modes to PAR and mover patterns (pairs, quads, odd/even).
- `use`: keep dense looks structured instead of random noise.

### 29.2 Track B: Production Design Case Studies

### Finding B1: Architectural moments + detail moments need contrast
- `source insight`: ODESZA case studies highlight large architectural looks alternating with intricate song-specific details.
- `applied rule`: every 16 bars should contain at least one “macro” and one “micro” visual moment.
- `use`: prevents visual monotony across long sets.

### Finding B2: Big EDM shows rely on modular systems under setup pressure
- `source insight`: Swedish House Mafia festival deployment cited fast integration with existing house rigs.
- `applied rule`: keep reusable pattern blocks and quick-reskin color systems.
- `use`: robust show building across venues and timelines.

### Finding B3: Multi-discipline sync works by role separation
- `source insight`: Prydz/HOLO coverage emphasizes separate visual layers with coordinated moments.
- `applied rule`: define leader/follower roles per section (PAR leads vs mover leads) and swap intentionally.
- `use`: cleaner storytelling when adding video/laser/FX later.

### 29.3 Track C: Safety + Audience Reliability

### Finding C1: Nighttime strobe-heavy EDM conditions increase seizure risk
- `source insight`: BMJ Open cohort linked darkness + strobe exposure with higher seizure incidence at EDM festivals.
- `applied rule`: cap sustained high-frequency strobe behavior and reserve intense packets for short windows.
- `use`: maintain impact while reducing risk.

### Finding C2: Photosensitivity triggers are multi-factor
- `source insight`: Epilepsy Foundation guidance notes frequency, brightness, contrast, and exposure duration all matter.
- `applied rule`: control duty cycle, intensity, and duration together; not frequency alone.
- `use`: safer strobe design without flattening show dynamics.

### 29.4 Immediate System Upgrades From Research

Apply these upgrades across generated shows:

1. Add `fixture_order_profile` field to mover/PAR pattern metadata.
2. Add `offset_mode` field: `spread`, `phase`, `segment`, `part`.
3. Add `measure_check` validation: step widths must match target beat measure.
4. Add `macro_micro_balance` validation per 16-bar block.
5. Add `strobe_exposure_budget` per 32 bars.

---

## 30) Research-Backed Guardrails For Large Batch Generation

### 30.1 Pattern Programming Guardrails

- Prefer transform-derived variants before creating net-new base routes.
- Keep one “anchor layer” static or low-motion in every dense section.
- Use `4b` mover stepping as baseline; escalate only in short intentional windows.
- For PARs, prioritize `fade/chase` over constant blink in non-peak sections.
- Use subgroup structures (pairs/segments) to maintain legibility in complex chases.

### 30.2 Section Behavior Guardrails

- `intro/break`: atmospheric movers + 4b/8b PAR fades.
- `groove/verse`: geometric movers + 2b or 4b PAR chase/fade.
- `build`: gradual transform density increase before speed increase.
- `drop`: short high-density windows, then return to readable motion.
- `outro`: simplify fixture interactions, reduce chase density.

### 30.3 Safety/Comfort Guardrails

- Keep sustained high-frequency strobe windows short and sparse.
- Avoid extended full-field high-contrast flashes.
- Preserve non-strobing visual anchors during high-intensity passages.
- Insert low-motion recovery bars after aggressive sections.

---

## 31) Extra Source Links For Sections 28-30

Console/effect programming references:
- Avolites Shape Generator:  
  https://manual.avolites.com/docs/18.0/effects/shape-generator/
- Avolites Key Frame Shapes:  
  https://manual.avolites.com/docs/effects/key-frame-shapes/
- Avolites Controlling Fixtures (selection order/group layout context):  
  https://manual.avolites.com/docs/quick-start/controlling-fixtures/
- grandMA3 MAtricks Transform:  
  https://help.malighting.com/grandMA3/2.1/HTML/matricks_transform.html
- grandMA3 MAtricks core (groups/blocks/wings/interleave):  
  https://help.malighting.com/grandMA3/2.3/HTML/matricks.html
- grandMA3 MAtricks Shuffle:  
  https://help.malighting.com/grandMA3/2.3/HTML/matricks_shuffle.html
- grandMA3 Phasers:  
  https://help.malighting.com/grandMA3/2.2/HTML/phaser.html
- grandMA3 Measure keyword:  
  https://help.malighting.com/grandMA3/2.3/HTML/keyword_measure.html
- grandMA3 Phaser Editor:  
  https://help.malighting.com/grandMA3/2.2/HTML/phaser_editor.html
- ChamSys FX Engine (Spread/Parts/Segments):  
  https://docs.chamsys.co.uk/magicq/manual/FX_engine.html
- QLC+ Chaser Editor:  
  https://docs.qlcplus.org/v5/function-manager/chaser-editor

Design/case-study references:
- ETC Stage Lighting Design Part 3 (controllable properties):  
  https://blog.etcconnect.com/stage-lighting-design-part-3
- ETC Stage Lighting Design Part 4 (fixture categories incl. PAR/movers):  
  https://blog.etcconnect.com/stage-lighting-design-part-4
- ETC Stage Lighting Design Part 5 (angles):  
  https://blog.etcconnect.com/stage-lighting-design-part-5
- ETC Stage Lighting Design Part 6 (color):  
  https://blog.etcconnect.com/stage-lighting-design-part-6
- TPi: ODESZA The Last Goodbye (Kyle Kegan):  
  https://www.tpimagazine.com/kyle-kegan-elates-crowds-on-odeszas-the-last-goodbye-tour/
- TPi: Swedish House Mafia (Andy Hurst):  
  https://www.tpimagazine.com/glp-lights-swedish-house-mafia/
- TPi: Eric Prydz HOLO context:  
  https://www.tpimagazine.com/eric-prydz-goes-holographic-with-avolites-ai/

Safety references:
- BMJ Open report summary (EDM strobe risk cohort):  
  https://blogs.bmj.com/bmjopen/2019/06/11/strobe-lighting-at-dance-music-festivals-linked-to-tripling-in-epileptic-fit-risk/
- BMJ Open article page:  
  https://bmjopen.bmj.com/content/9/6/e023442
- Epilepsy Foundation photosensitivity guidance:  
  https://www.epilepsy.com/what-is-epilepsy/seizure-triggers/photosensitivity

---

## 32) Parallel Web Research Expansion (Subagent Batches)

This pass used parallel research tracks so techniques are grounded in console behavior, EDM case studies, and audience safety.

### 32.1 Batch Map

| Batch ID | Focus | Core Sources | Output Applied Here |
|---|---|---|---|
| B-01 | Effect engines | Avolites Shape/Key Frame, grandMA3 Phaser/MAtricks, ChamSys FX, QLC+ Chaser | Added spread/phase/transform rules and beat-locked constraints |
| B-02 | Fixture ordering | Avolites fixture control, grandMA3 MAtricks | Added explicit fixture-order profiles and mirror/reverse variants |
| B-03 | Large EDM show case studies | TPi, Live Design, PLSN electronic tour/festival profiles | Added macro vs micro look alternation and modular block strategy |
| B-04 | Designer study set | ODESZA, SHM, Prydz, deadmau5, Garrix, Ultra profiles | Added designer-driven style prompts and transfer tactics |
| B-05 | Color theory for stage | ETC color section, gel-family references (Lee) | Added more palette families and transition rules |
| B-06 | Song phrase behavior | rekordbox phrase analysis docs | Added phrase-to-look maps and fill handling for 4-beat logic |
| B-07 | Comfort and seizure risk | BMJ Open + Epilepsy Foundation | Added stronger strobe exposure budgeting rules |
| B-08 | Repeatability at scale | Cross-source synthesis | Added anti-repetition constraints for hundreds of shows |

### 32.2 Cross-Source Rules To Keep

- Use `shape route` as the base asset and produce most variety via `phase`, `spread`, `mirror`, `reverse`, and `group offsets`.
- Preserve one readable anchor layer in dense sections (usually PAR world wash or a slow mover canopy).
- Alternate `macro` looks (big architectural gestures) and `micro` looks (tight detail/chase logic) every 8-16 bars.
- Keep strobe-heavy windows short; use recovery bars with non-strobing motion/intensity.
- Build sections from reusable blocks so rig swaps and venue changes do not break show logic.

---

## 33) EDM/Electronic Lighting Designers To Study (Research-Backed)

Use this as a style research deck. Each row includes a direct transferable idea for this project.

Schema:

```yaml
id: LD-###
name: designer/programmer
anchor_context: artist_or_event
study_focus: what to observe
transfer_rule: how to apply in venue profile
```

| ID | Name | Anchor Context | Study Focus | Transfer Rule |
|---|---|---|---|---|
| LD-001 | Kyle Kegan | ODESZA tour profiles | Contrast between huge scenic geometry and song-specific details | Force at least one macro look and one detail look per 16 bars |
| LD-002 | Andy Hurst | Swedish House Mafia festival/tour context | Clean, strong beam architecture under high-energy tracks | Use fewer directions at once; prioritize bold readable beam lanes |
| LD-003 | Ross Chapple | Eric Prydz HOLO context | Visual hierarchy with layered disciplines | Assign leader/follower roles per section and swap deliberately |
| LD-004 | Erik Mahowald | deadmau5 Retro5pective | Large timecoded structure with musical punctuation | Keep drop punctuation windows short, then return to groove motion |
| LD-005 | Alex Ares | deadmau5 Cube era context | Geometry-first framing and object-centric staging | Route movers around one virtual stage object per section |
| LD-006 | Gabe Fraboni | Martin Garrix production profile | Pop-precise cue punctuation merged with festival scale | Add repeatable accent tokens on phrase starts and fills |
| LD-007 | Steve Lieberman | EDC/Calvin Harris context | Arena-scale consistency and spectacle pacing | Rotate complexity density: simple, medium, dense, release |
| LD-008 | Patrick Dierson | Ultra main stage technical profile | Robustness under massive rig/system pressure | Keep fallback looks for each section if fixtures are missing |
| LD-009 | Richard Milstein | Ultra creative direction context | Coherent visual language across many artists | Define a per-show visual thesis (2 colors + 1 geometry family) |
| LD-010 | Ray Steinman | Ultra technical production context | Reliability at festival scale | Prefer modular cue blocks over fragile one-off sequences |
| LD-011 | Liam Tomaszewski | SHM visual direction context | Tight alignment of narrative and lighting structure | Map emotional arc first, then assign pattern families |
| LD-012 | Ed Warren | four tet/fred again../skrillex profile | Playful high/low intensity alternation | Intentionally insert restrained bars after dense peaks |
| LD-013 | Marc Heinz | Armin van Buuren production profile | Long-form trance phrasing and lift design | Use multi-bar lift ladders before peak drops |
| LD-014 | Matt Smith | RUFUS DU SOL production context | Textural atmospherics and emotional transitions | Use slower PAR fade worlds in breakdowns, not constant chase |
| LD-015 | Romain Pissenem | David Guetta / large EDM productions | Monumental framing and high-impact moments | Reserve full-rig inclusion techniques for major phrase markers |
| LD-016 | Tom Edwards | Jamie xx In Waves (Alexandra Palace) | Projection-first language plus mirrorball punctuation and crowd-immersive flow | Pair mover geometry with projection line direction, then punctuate with one practical "special" moment |
| LD-017 | Tim Fawkes | The Prodigy at Glastonbury 2025 | Pod-based tilting strobe waves balanced for live and broadcast readability | Alternate high-intensity pod wave windows with recovery bars to avoid constant visual fatigue |
| LD-018 | Haydn Cruickshank | Underworld tour methodology | Timing-first live operation and video-light intensity harmonization | Keep fixture maps simple and generate variation from timing, phrase rhythm, and intensity interplay |
| LD-019 | Andre Beekmans | Amsterdam Music Festival (AMF) | Repeating branded geometry to scale arenas into nightclub energy | Repeat one signature shape across stage and crowd planes with limited but high-impact motion cues |
| LD-020 | Sam Tozer | Axwell & Ingrosso / SHM context | Logo-shaped stage framing and aggressive audience immersion from bars/strobes | Build one recognizable shape family, then vary density and pixel logic inside that frame |
| LD-021 | Rob Lister | DJ Snake Paris Zenith | Concentric rings + matrix grids + automation tilt/pitch for object-centered architecture | Drive movers as geometric objects first (rings, grids), then add PAR support as contour and punctuation |
| LD-022 | Pascal Bach | Afterlife Dubai concept | Massive beam arrays behaving like one organic object | Treat large mover arrays as a single organism with long-form phase evolution over rapid chaos |
| LD-023 | Adam Smith | The Chemical Brothers arena show | Strobe walls as musical lead voice rather than constant background | Reserve dense strobe-wall states for phrase climaxes and route back to color-rich intermediate looks |
| LD-024 | Marcus Lyall | The Chemical Brothers arena show | Laddered grid architecture with lift-in/lift-out reveal timing | Use vertical reveal/collapse geometry to mark phrase transitions and create depth changes |
| LD-025 | Toby Dennis | The Chemical Brothers technical design | Cell-level fixture repurposing for shape/texture density | Build cell-mode shape libraries so one fixture family can switch between wash, strobe, and texture roles |
| LD-026 | Alex Hesse | Axwell & Ingrosso programming collaboration | Co-programming discipline across lighting, pyro, laser, and video | Predefine "integration windows" where lighting density leaves deliberate space for pyro/laser accents |
| LD-027 | Rane Renshaw | Club/festival programming practice | Rig calibration and orientation discipline under dense fixture counts | Run alignment and orientation checks before creative layers to keep spatial effects repeatable |
| LD-028 | Victor Sanchez | Ultra RESISTANCE guest-LD context | Warm-white contrast plates inside RGB-heavy rigs | Use warm-white plate moments as periodic contrast anchors against saturated color worlds |
| LD-029 | Zach Delzotti | Ultra RESISTANCE L2/program role | Universe-efficient mode planning with retained eye-candy | Use reduced channel modes on support fixtures and full modes only where phrase detail demands it |
| LD-030 | Josh Spodick | Ultra main-stage programming context | High-fixture-count matrix organization with fast guest handoff | Separate macro architecture pages from per-artist detail pages for rapid, stable festival transitions |

### 33.1 Designer Study Prompt Template

```yaml
prompt_template:
  input:
    - ld_id
    - track_energy_profile
    - phrase_map
  output:
    - 3 signature looks inspired by ld_id
    - 2 anti-look rules (what to avoid)
    - 1 hybrid look blending with house style
```

### 33.2 Machine-Readable Technical Motif Map (`LD-016..LD-030`)

Use this as a compact bridge from designer research into cue planning.

```yaml
designer_signature_patterns:
  - pattern_id: DSP-001
    source_ld: LD-016
    mover_recipe: projection-follow sweeps + mirror accent holds
    par_recipe: sparse 2b chase during projection-heavy bars
    phrase_fit: [verse_groove, build, breakdown]
  - pattern_id: DSP-002
    source_ld: LD-017
    mover_recipe: pod waves with controlled tilt accelerations
    par_recipe: amber/red 1b attacks then 4b fade recovery
    phrase_fit: [build, drop]
  - pattern_id: DSP-003
    source_ld: LD-018
    mover_recipe: fixed geometry, rhythm-led timing pivots
    par_recipe: low-density fades matching live busk dynamics
    phrase_fit: [intro, verse_groove, breakdown]
  - pattern_id: DSP-004
    source_ld: LD-019
    mover_recipe: repeated brand-shape anchors in multiple zones
    par_recipe: contour chases reinforcing shape edges
    phrase_fit: [verse_groove, build, drop]
  - pattern_id: DSP-005
    source_ld: LD-020
    mover_recipe: logo-frame symmetry with pixelized accents
    par_recipe: 1b/2b chase bursts aimed into crowd lanes
    phrase_fit: [build, drop]
  - pattern_id: DSP-006
    source_ld: LD-021
    mover_recipe: concentric ring routes + matrix punctuations
    par_recipe: arc-follow chase along video contour
    phrase_fit: [verse_groove, drop]
  - pattern_id: DSP-007
    source_ld: LD-022
    mover_recipe: long-form organic beam array morph
    par_recipe: restrained fades with occasional beat puncture
    phrase_fit: [intro, build, breakdown]
  - pattern_id: DSP-008
    source_ld: LD-023
    mover_recipe: hold geometry while strobe-wall leads
    par_recipe: saturation wash -> strobe wall -> saturation reset
    phrase_fit: [build, drop]
  - pattern_id: DSP-009
    source_ld: LD-024
    mover_recipe: vertical reveal and collapse sequences
    par_recipe: ladder-step chase tied to lift moments
    phrase_fit: [build, drop, outro]
  - pattern_id: DSP-010
    source_ld: LD-025
    mover_recipe: cell-mode shape swaps per 4 bars
    par_recipe: texture chase using cell subsets, not all heads
    phrase_fit: [verse_groove, build]
  - pattern_id: DSP-011
    source_ld: LD-026
    mover_recipe: integration windows around pyro/laser slots
    par_recipe: leave beat-space before and after FX hits
    phrase_fit: [build, drop]
  - pattern_id: DSP-012
    source_ld: LD-027
    mover_recipe: orientation-safe symmetric paths
    par_recipe: calibration-check chase templates
    phrase_fit: [intro, verse_groove]
  - pattern_id: DSP-013
    source_ld: LD-028
    mover_recipe: saturated worlds punctuated by warm-white plates
    par_recipe: brief warm-white anchors every 8-16 bars
    phrase_fit: [build, drop]
  - pattern_id: DSP-014
    source_ld: LD-029
    mover_recipe: hero-fixture detail plus support-fixture economy
    par_recipe: low-channel chase with strategic high-detail inserts
    phrase_fit: [verse_groove, build, drop]
  - pattern_id: DSP-015
    source_ld: LD-030
    mover_recipe: macro matrix pages with artist-specific overlays
    par_recipe: shared festival base chase + quick artist deltas
    phrase_fit: [verse_groove, build, drop, outro]
```

---

## 34) Whole-Rig Coordination Techniques (30 More)

Goal: extend beyond `INT-001..INT-030` with more options where PARs and movers are always cooperating or intentionally countering.

Default timing baseline:
- movers: `4b` position base
- PARs: `fade` or `chase` at `1b`, `2b`, or `4b`

Technique schema:

```yaml
id: INT-###
relationship: unison|counterpoint|inclusion
core_logic: short description
timing_recipe: "movers=4b, pars=..."
starter_combo: "R### + PP-###"
```

### 34.1 Cohesion Extensions (`INT-031..INT-040`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-031 | Phase Ladder Lock | unison | Each bar advances mover phase and PAR chase phase together by one step. | `movers=4b, pars=1b chase` | `R041 + PP-037` |
| INT-032 | Barline Clamp | unison | All fixtures freeze for beat 1, then resume motion for beats 2-4. | `movers=4b + beat1 hold, pars=1b chase` | `R011 + PP-066` |
| INT-033 | Two-Bar Breath | unison | Both fixture families swell and release over 2-bar envelopes. | `movers=4b, pars=4b fade` | `R053 + PP-013` |
| INT-034 | Beat-4 Sling | unison | Movers pre-position on beat 4 while PARs pre-hit as lead-in. | `movers=4b with beat4 prep, pars=1b pulse` | `R021 + PP-019` |
| INT-035 | Phrase Door Open | unison | First bar each 8 bars is full synchronization, then layers split. | `movers=4b, pars=2b chase` | `R049 + PP-070` |
| INT-036 | Center Spine | unison | One center axis remains common while side fixtures vary. | `movers=4b center lock, pars=2b chase` | `R014 + PP-062` |
| INT-037 | Color-Step Unison | unison | Color changes only occur when both mover and PAR steps change. | `movers=4b, pars=2b fade/chase` | `R043 + PP-012` |
| INT-038 | Arc-and-Ring Sync | unison | Movers draw arcs while PARs run ring chase in matching direction. | `movers=4b arcs, pars=1b ring chase` | `R033 + PP-050` |
| INT-039 | Lift Stack | unison | Intensity and tilt both rise across 4 bars, then resolve. | `movers=4b lift, pars=4b fade` | `R061 + PP-014` |
| INT-040 | Downbeat White Spine | unison | Every bar starts with short shared white punctuation. | `movers=4b + beat1 hit, pars=2b chase` | `R029 + PP-095` |

### 34.2 Counterpoint Extensions (`INT-041..INT-050`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-041 | Opposite Orbit | counterpoint | Movers orbit clockwise while PAR chase runs counterclockwise. | `movers=4b, pars=1b chase` | `R034 + PP-040` |
| INT-042 | Hold-vs-Chase | counterpoint | Movers hold 1 bar while PARs chase, then swap roles. | `movers=4b hold/swap, pars=1b chase` | `R050 + PP-057` |
| INT-043 | Odd-Even Ownership | counterpoint | PARs own odd beats, movers emphasize even beats. | `movers=4b accents on 2/4, pars=1b` | `R017 + PP-023` |
| INT-044 | Slow-Fast Tension | counterpoint | Slow mover route under fast PAR chase, then reverse in breakdown. | `movers=4b -> 2b, pars=1b -> 4b` | `R052 + PP-039` |
| INT-045 | Front-Back Pull | counterpoint | PAR intensity pushes downstage while movers pull upstage. | `movers=4b, pars=2b fade` | `R005 + PP-011` |
| INT-046 | Ceiling-Floor Split | counterpoint | Movers paint high plane while PARs travel low perimeter chase. | `movers=4b high plane, pars=1b perimeter` | `R062 + PP-055` |
| INT-047 | Zoom Counterphase | counterpoint | Mover zoom opens as PAR intensity closes, then invert. | `movers=4b zoom env, pars=2b fade` | `R023 + PP-008` |
| INT-048 | Warm-Cool Duel | counterpoint | Warm PAR base versus cool mover accents, swapped every 8 bars. | `movers=4b, pars=2b chase` | `R036 + PP-068` |
| INT-049 | Diagonal Conflict | counterpoint | PAR diagonal chase counters mover diagonal hit map. | `movers=4b diag, pars=1b diag chase` | `R019 + PP-041` |
| INT-050 | Echo Handoff | counterpoint | PAR pattern leads by 1 beat and movers echo at reduced intensity. | `movers=4b delayed echo, pars=1b chase` | `R024 + PP-044` |

### 34.3 Inclusion Extensions (`INT-051..INT-060`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-051 | Baton Chase | inclusion | One mover joins whichever PAR node is currently active. | `movers=4b + 1b baton accents, pars=1b chase` | `R001 + PP-037` |
| INT-052 | Pair Relay Join | inclusion | PAR pair chase passes token to mover pair every 2 beats. | `movers=4b pair joins, pars=1b pair chase` | `R031 + PP-053` |
| INT-053 | Every-2 Joiner | inclusion | Movers enter the PAR chase every second beat only. | `movers=4b base + 2b joins, pars=1b chase` | `R003 + PP-052` |
| INT-054 | Every-4 Joiner | inclusion | Movers only join on beat 1 each bar for stronger punctuation. | `movers=4b joins, pars=1b chase` | `R041 + PP-072` |
| INT-055 | Phrase-End Catch | inclusion | Movers catch final PAR chase node and hold through transition. | `movers=4b catch/hold, pars=2b chase` | `R043 + PP-074` |
| INT-056 | Kick Include | inclusion | Movers inject short chase joins on kick-heavy windows only. | `movers=4b + kick inserts, pars=1b chase` | `R002 + PP-038` |
| INT-057 | Snare Include | inclusion | Movers answer PAR chase on backbeat moments. | `movers=4b + backbeat inserts, pars=1b chase` | `R022 + PP-042` |
| INT-058 | Expanding Inclusion Ring | inclusion | PAR chase starts tight, movers join as radius expands every bar. | `movers=4b expanding, pars=1b chase` | `R049 + PP-073` |
| INT-059 | Mirror Inclusion Collapse | inclusion | Full-rig chase mirrors at phrase midpoint then collapses to PAR-only. | `movers=4b mirror step, pars=1b/2b chase` | `R048 + PP-075` |
| INT-060 | Ghost Canopy Trace | inclusion | Movers run a slow canopy ghost of PAR chase trajectories. | `movers=4b canopy ghost, pars=1b chase` | `R035 + PP-040` |

### 34.4 Selection Rules For `INT-031..INT-060`

- Start with `INT-031..INT-040` for intros, verse grooves, and restrained sections.
- Use `INT-041..INT-050` when you need tension without pure chaos.
- Reserve `INT-051..INT-060` for build/drop windows and phrase punctuation.
- Avoid running inclusion techniques for more than 8 bars without a reset.

---

## 35) EDM Color Palette Expansion (P-025..P-048)

These palettes extend Section 14 with additional worlds oriented to electronic music. Use as starting points; calibrate fixture-specific output in venue.

Format:
- `base`: PAR world color(s)
- `accent`: mover contrast color(s)
- `hit`: transient impact color

### P-025 Midnight Cyan Steel
- `hex`: `#003B5C #00AFC4 #DCEBFF`
- `base`: deep cyan-blue
- `accent`: steel/ice beams
- `hit`: cool white
- `best_for`: progressive house, late-night groove

### P-026 Laser Lime Charcoal
- `hex`: `#A6FF00 #2C2C2C #EFFFCC`
- `base`: charcoal low fill
- `accent`: acid-lime traces
- `hit`: pale lime-white
- `best_for`: techno, acid sets

### P-027 Amber Dust Indigo
- `hex`: `#D98C3A #2E2A68 #FFF0D9`
- `base`: warm amber haze
- `accent`: indigo sweeps
- `hit`: warm white
- `best_for`: melodic transitions

### P-028 Arctic White Teal
- `hex`: `#EAFBFF #00B3A4 #124E66`
- `base`: cold white wash
- `accent`: teal and dark aqua
- `hit`: pure white
- `best_for`: breakdowns, vocal sections

### P-029 Crimson Smoke
- `hex`: `#B3122F #3A0B16 #FFE3E9`
- `base`: dark crimson
- `accent`: rose-white hits
- `hit`: white-pink
- `best_for`: heavy drops, cinematic moments

### P-030 Magenta Ice Blue
- `hex`: `#E5008A #5DA9E9 #F3E8FF`
- `base`: magenta
- `accent`: ice-blue blades
- `hit`: lilac-white
- `best_for`: electro-pop EDM

### P-031 Deep Violet Silver
- `hex`: `#3D1A78 #8B78E6 #E8E8F5`
- `base`: deep violet
- `accent`: silver-lilac beams
- `hit`: cool silver-white
- `best_for`: trance lifts

### P-032 Cobalt Fire
- `hex`: `#0D47A1 #FF5A1F #EAF2FF`
- `base`: cobalt
- `accent`: fire-orange accents
- `hit`: crisp white
- `best_for`: big room drop callouts

### P-033 Mono Slate White
- `hex`: `#1E2A38 #4D647D #F8FBFF`
- `base`: slate monochrome
- `accent`: lighter slate beams
- `hit`: white
- `best_for`: minimal techno, long-form DJ sets

### P-034 Emerald Gold
- `hex`: `#009B77 #C8A646 #F4FFE8`
- `base`: emerald
- `accent`: gold highlights
- `hit`: pale gold-white
- `best_for`: afro/organic electronic

### P-035 Neon Peach Purple
- `hex`: `#FF8A65 #6A1B9A #FFE9E1`
- `base`: neon peach
- `accent`: deep purple
- `hit`: warm white
- `best_for`: future house and crossover pop EDM

### P-036 Petrol Blue Copper
- `hex`: `#0F4C5C #B66A3D #E7F5F8`
- `base`: petrol blue
- `accent`: copper sweeps
- `hit`: neutral white
- `best_for`: moody progressive sections

### P-037 Ruby Violet Ice
- `hex`: `#9B1B30 #4A2C8A #EAF1FF`
- `base`: ruby
- `accent`: violet
- `hit`: ice white
- `best_for`: dramatic build/drop contrasts

### P-038 Acid Yellow Navy
- `hex`: `#E8FF1A #102A43 #FFFEDC`
- `base`: navy base field
- `accent`: acid yellow scans
- `hit`: yellow-white
- `best_for`: warehouse techno accents

### P-039 Sunset Rose Cobalt
- `hex`: `#FF5C8A #174EA6 #FFE3EC`
- `base`: sunset rose
- `accent`: cobalt cuts
- `hit`: soft white
- `best_for`: euphoric melodic house

### P-040 Infra Blue Mint
- `hex`: `#16213E #00D2B5 #E9FFFA`
- `base`: infrared blue darkness
- `accent`: mint pulses
- `hit`: cold mint-white
- `best_for`: deep and hypnotic sections

### P-041 Steel Blue Amber
- `hex`: `#3F72AF #E09F3E #F5F9FF`
- `base`: steel blue
- `accent`: amber punctuation
- `hit`: neutral white
- `best_for`: dynamic groove shifts

### P-042 Graphite UV
- `hex`: `#1A1A1A #7F00FF #EEDCFF`
- `base`: graphite low world
- `accent`: ultraviolet beams
- `hit`: violet-white
- `best_for`: dark club intros

### P-043 Solar Orange Cyan
- `hex`: `#FF7A00 #00B7C2 #FFF1D9`
- `base`: solar orange
- `accent`: cyan opposition
- `hit`: warm white
- `best_for`: high-impact chorus moments

### P-044 Mint Violet Black
- `hex`: `#9CFFD6 #7B4BFF #0A0A0A`
- `base`: black + mint texture
- `accent`: violet sweeps
- `hit`: white-mint
- `best_for`: experimental electronic

### P-045 Pearl White Split
- `hex`: `#F7F7F2 #00A8FF #FF3366`
- `base`: pearl white canopy
- `accent`: alternating cyan/magenta
- `hit`: full white
- `best_for`: anthem drops

### P-046 Scarlet Indigo
- `hex`: `#E63946 #2B2D82 #FFE5E8`
- `base`: indigo field
- `accent`: scarlet hits
- `hit`: pink-white
- `best_for`: tension-release sequences

### P-047 Copper Orchid
- `hex`: `#B87333 #B565D9 #FFF3EA`
- `base`: copper glow
- `accent`: orchid beams
- `hit`: warm pastel white
- `best_for`: melodic breakdowns

### P-048 Glacier Indigo
- `hex`: `#8FD3FF #243B7C #F3FAFF`
- `base`: glacier blue
- `accent`: indigo structure
- `hit`: icy white
- `best_for`: closing journeys and outros

### 35.1 Palette Rotation Rules For Hundreds Of Shows

- Keep one palette world for 16-32 bars before rotating.
- Rotate by `temperature` first (warm/cool), then by `hue`.
- Do not introduce more than one new accent color per 8 bars.
- Use white hits as punctuation, not as constant base.
- Prefer 2-color + white systems for drop readability.

---

## 36) Phrase-Aware Show Building (Song Data + Phrase Analysis)

Use this layer to make generated shows feel musical instead of random. Phrase info from analysis should drive look families.

### 36.1 Phrase Classes (Practical Map)

```yaml
phrase_map:
  intro:
    mover_mode: slow geometry (4b/8b)
    par_mode: fade 4b/8b
    coordination_pool: [INT-001, INT-013, INT-033, INT-036, INT-063, INT-069]
  verse_groove:
    mover_mode: structured routes (4b)
    par_mode: fade/chase 2b
    coordination_pool: [INT-005, INT-011, INT-041, INT-047, INT-066, INT-075]
  build:
    mover_mode: density lift, transform add
    par_mode: chase density increase 2b->1b
    coordination_pool: [INT-020, INT-035, INT-044, INT-058, INT-072, INT-086]
  drop:
    mover_mode: high-contrast pattern windows
    par_mode: 1b chase with controlled burst accents
    coordination_pool: [INT-021, INT-027, INT-051, INT-056, INT-081, INT-088]
  breakdown:
    mover_mode: canopy or slow sweeps
    par_mode: long fades 4b/8b
    coordination_pool: [INT-014, INT-019, INT-033, INT-060, INT-071, INT-074]
  outro:
    mover_mode: simplify and reduce movement planes
    par_mode: fade-out or sparse chase
    coordination_pool: [INT-006, INT-018, INT-039, INT-055, INT-070, INT-089]
```

### 36.2 Fill Handling Rule (Up To 4 Beats)

- If phrase analyzer flags a fill or transition up to 4 beats, use one short inclusion technique from `INT-021..INT-030`, `INT-051..INT-060`, or `INT-081..INT-090`.
- Immediately return to the section base look after the fill.
- Keep fill effects to 1-2 bars maximum.

### 36.3 Anti-Repetition Constraints

```yaml
uniqueness_constraints:
  no_same_mover_route_within: 64_bars
  no_same_par_pattern_within: 32_bars
  no_same_palette_within: 3_sections
  include_density_peak_per_song: 1_to_3
  mandatory_reset_after_peak: 4_bars
```

### 36.4 Fast Assembly Template

```yaml
show_builder_template:
  step_1: choose_palette_world (P-001..P-048)
  step_2: choose_mover_route_family (R001..R064)
  step_3: choose_par_base (fade/chase 1b|2b|4b)
  step_4: assign_coordination_ids (INT-001..INT-090)
  step_5: map_to_phrase_blocks (intro/verse/build/drop/break/outro)
  step_6: run_safety_budget_check
  step_7: export_and_tag (energy, style, complexity)
```

---

## 37) Additional Source Links For Sections 32-38

Programming and console mechanics:
- Avolites Shape Generator:  
  https://manual.avolites.com/docs/18.0/effects/shape-generator/
- Avolites Key Frame Shapes:  
  https://manual.avolites.com/docs/effects/key-frame-shapes/
- grandMA3 Phaser overview:  
  https://help.malighting.com/grandMA3/2.2/HTML/phaser.html
- grandMA3 MAtricks Transform:  
  https://help.malighting.com/grandMA3/2.1/HTML/matricks_transform.html
- grandMA3 Measure keyword:  
  https://help.malighting.com/grandMA3/2.3/HTML/keyword_measure.html
- grandMA3 DelayToPhase keyword:  
  https://help.malighting.com/grandMA3/2.3/HTML/keyword_delay_to_phase.html
- ChamSys FX Engine:  
  https://docs.chamsys.co.uk/magicq/manual/FX_engine.html
- QLC+ Chaser Editor:  
  https://docs.qlcplus.org/v5/function-manager/chaser-editor

Designer and production references:
- TPi ODESZA profile index:  
  https://www.tpimagazine.com/odesza/
- TPi Swedish House Mafia and GLP context:  
  https://www.tpimagazine.com/glp-lights-swedish-house-mafia/
- TPi Eric Prydz HOLO profile:  
  https://www.tpimagazine.com/eric-prydz-presents-holo/
- PLSN deadmau5 Retro5pective profile:  
  https://plsn.com/articles/production-profile/deadmau5-retro5pective/
- Live Design deadmau5 Cube v3:  
  https://www.livedesignonline.com/concerts/deadmau5-introduces-cube-v3-production-tour
- PLSN Martin Garrix profile:  
  https://plsn.com/articles/production-profile/martin-garrix-live-2024/
- TPi Calvin Harris / CircoLoco context:  
  https://www.tpimagazine.com/calvin-harris-circa-loco/
- PLSN Ultra Miami Main Stage 2025:  
  https://plsn.com/articles/production-profile/ultra-miami-main-stage-2025/
- PLSN Ultra Miami RESISTANCE 2025 (VOLUX):  
  https://plsn.com/articles/production-profile/ultra-miami-resistance-stage-2025/
- TPi four tet / fred again.. / skrillex (MSG):  
  https://www.tpimagazine.com/four-tet-fred-again-skrillex/
- TPi four tet at Alexandra Palace (JDC Line deployment):  
  https://www.tpimagazine.com/ppds-lights-up-four-tet-at-alexandra-palace-with-jdc-line/
- TPi Jamie xx production profile (Tom Edwards):  
  https://www.tpimagazine.com/uk-ltd-jamie-xx/
- TPi Underworld live experience (Haydn Cruickshank):  
  https://www.tpimagazine.com/underworlds-electrifying-live-experience/
- TPi AMF energises with Robe (Andre Beekmans):  
  https://www.tpimagazine.com/amf-energises-with-robe/
- TPi Axwell & Ingrosso profile (Sam Tozer / Alex Hesse context):  
  https://www.tpimagazine.com/glp-fixtures-support-axwell-ingrosso/
- PLSN The Prodigy at Glastonbury 2025 (Tim Fawkes):  
  https://plsn.com/articles/production-profile/the-prodigy-goes-all-in-at-glastonbury/
- Live Design Chemical Brothers arena profile (Adam Smith / Marcus Lyall / Toby Dennis):  
  https://www.livedesignonline.com/concerts/chemical-brothers-go-where-no-band-has-gone
- Robe DJ Snake at Zenith Paris (Rob Lister):  
  https://www.robe.cz/news/dj-snake-live-at-zenith-paris
- Robe Afterlife Dubai (Pascal Bach):  
  https://www.robe.cz/news/afterlife-live

Color and visual design references:
- ETC Stage Lighting Design Part 6 (Color):  
  https://blog.etcconnect.com/stage-lighting-design-part-6
- Lee Filters color list reference:  
  https://wiki.mar.io/books/lighting/page/lee-filters

Phrase and analysis references:
- rekordbox Phrase Analysis operation guide:  
  https://cdn.rekordbox.com/files/20200420110028/rekordbox_5.8.5_phrase_analysis_operation_guide_EN.pdf
- rekordbox phrase analysis notes (DJ software article):  
  https://wearecrossfader.co.uk/blog/rekordbox-phrase-analysis/

Safety references:
- BMJ Open article page:  
  https://bmjopen.bmj.com/content/9/6/e023442
- BMJ Open blog summary:  
  https://blogs.bmj.com/bmjopen/2019/06/11/strobe-lighting-at-dance-music-festivals-linked-to-tripling-in-epileptic-fit-risk/
- Epilepsy Foundation photosensitivity guidance:  
  https://www.epilepsy.com/what-is-epilepsy/seizure-triggers/photosensitivity

---

## 38) Advanced Coordination Techniques (30 More, `INT-061..INT-090`)

Goal: inject more technically distinct looks informed by console effect mechanics (phase, wings, blocks, interleave, grid, measure/restart logic) while keeping PAR/mover cooperation readable.

### 38.1 Console-Synced Cohesion (`INT-061..INT-070`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-061 | Measure Grid Lock | unison | Both mover and PAR engines restart on shared barline measure points for hard structural clarity. | `movers=4b measure restart, pars=2b chase` | `R046 + PP-061` |
| INT-062 | Winged Mirror Pulse | unison | Movers run winged symmetry while PAR pairs pulse in the same mirrored ownership map. | `movers=4b wing mirror, pars=2b pulse` | `R028 + PP-067` |
| INT-063 | Delayed Spine Echo | unison | PAR chase forms a center spine and movers echo that spine one beat later. | `movers=4b + 1b echo, pars=1b spine chase` | `R014 + PP-052` |
| INT-064 | Block-Step Accord | unison | Fixture blocks step together each bar so movers and PARs change zone in unified chunks. | `movers=4b block step, pars=1b block chase` | `R040 + PP-048` |
| INT-065 | Interleave Bloom | unison | Interleaved fixture sets alternate activation but still land on shared phrase accents. | `movers=4b interleave, pars=2b chase` | `R030 + PP-059` |
| INT-066 | Grid Overlay Match | unison | Vertical mover sweeps and PAR grid overlays advance in the same directional order. | `movers=4b grid v, pars=1b grid chase` | `R063 + PP-078` |
| INT-067 | Width Snap Sync | unison | Both layers run narrow width in groove bars, then widen together at phrase markers. | `movers=4b width env, pars=2b chase` | `R022 + PP-064` |
| INT-068 | Phase Fan Sweep | unison | Phase fan movement in movers is matched by phase-shift PAR fan chase direction. | `movers=4b phase fan, pars=1b fan chase` | `R057 + PP-050` |
| INT-069 | One-Cycle Landing | unison | One complete motion cycle per 8 bars, then both fixture families settle on a shared landing frame. | `movers=8b single cycle, pars=4b fade` | `R053 + PP-013` |
| INT-070 | Rate-Duck Breath | unison | Fast bars are followed by synchronized half-rate bars to protect clarity and groove. | `movers=4b->8b duck, pars=1b->4b duck` | `R006 + PP-015` |

### 38.2 Console Counterpoint Extensions (`INT-071..INT-080`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-071 | Delay-Phase Drift | counterpoint | Movers drift forward by delay-phase while PAR chase stays quantized on strict beats. | `movers=4b phased drift, pars=2b chase` | `R034 + PP-060` |
| INT-072 | Odd-Even Segment Split | counterpoint | Movers own odd bars and PARs own even bars with shared marker hits at transitions. | `movers=4b odd bars, pars=1b even bars` | `R017 + PP-023` |
| INT-073 | Horizontal-Vertical Duel | counterpoint | Movers sweep horizontal planes while PAR chase climbs vertical lanes. | `movers=4b horizontal, pars=1b vertical chase` | `R019 + PP-041` |
| INT-074 | Hold-vs-Ripple | counterpoint | Movers hold geometry while PARs ripple through nodes, then roles invert at phrase midpoint. | `movers=4b hold/invert, pars=1b ripple` | `R050 + PP-057` |
| INT-075 | Transform Clash | counterpoint | Movers compress while PAR patterns expand, then both swap transform direction. | `movers=4b compress/expand, pars=2b expand/compress` | `R024 + PP-044` |
| INT-076 | Shuffle-Vs-Lock | counterpoint | PAR chase order shuffles while mover positions remain locked to a static frame. | `movers=4b lock, pars=1b shuffle chase` | `R011 + PP-072` |
| INT-077 | Rate Swap Conflict | counterpoint | Movers start slow against fast PARs, then timing ownership swaps every 4 bars. | `movers=8b->4b, pars=1b->2b` | `R052 + PP-039` |
| INT-078 | Width Compression Fight | counterpoint | Mover beam width narrows as PAR chase broadens, creating push-pull visual tension. | `movers=4b width close, pars=2b width open` | `R023 + PP-008` |
| INT-079 | Gobo-vs-Color Push | counterpoint | Movers emphasize gobo texture while PARs carry bold color rhythm in opposite phrasing. | `movers=4b texture, pars=1b color chase` | `R043 + PP-068` |
| INT-080 | Cell-vs-Group Split | counterpoint | Cell-level mover effects run against group-level PAR chase ownership to create layered conflict. | `movers=4b cell fx, pars=2b group chase` | `R031 + PP-053` |

### 38.3 Inclusion Extensions (`INT-081..INT-090`)

| ID | Technique | Relationship | Core Logic | Timing Recipe | Starter Combo |
|---|---|---|---|---|---|
| INT-081 | Segmented Baton Include | inclusion | PAR chase token passes through segments and movers join only on segment boundaries. | `movers=4b segment joins, pars=1b segmented chase` | `R001 + PP-037` |
| INT-082 | Ping-Pong Join | inclusion | PAR ping-pong chase triggers matching mover pair joins at each edge bounce. | `movers=4b edge joins, pars=1b ping-pong chase` | `R041 + PP-074` |
| INT-083 | Random Catch Resolve | inclusion | PAR random chase runs for one bar, then movers catch and force a deterministic resolve shape. | `movers=4b resolve catch, pars=1b random->lock` | `R048 + PP-075` |
| INT-084 | Palette Chase Include | inclusion | Movers join PAR chase only on accent-color steps while base-color steps stay PAR-only. | `movers=4b accent joins, pars=1b color-step chase` | `R036 + PP-070` |
| INT-085 | Wing Relay Join | inclusion | PAR wing groups relay a chase and movers join whichever wing currently owns the downbeat. | `movers=4b wing joins, pars=1b wing relay` | `R033 + PP-040` |
| INT-086 | Measure-End Surge | inclusion | Movers join in a short surge at each measure end, then drop back to support mode. | `movers=4b + beat4 surge, pars=1b chase` | `R021 + PP-019` |
| INT-087 | Burst-Then-Breathe Include | inclusion | Two bars of aggressive inclusion are followed by two bars of PAR-only breathing space. | `movers=4b 2on/2off, pars=1b->4b` | `R002 + PP-038` |
| INT-088 | Inverted Downbeat Include | inclusion | Movers include on downbeats while PAR chase intentionally blanks downbeats for contrast. | `movers=4b downbeat joins, pars=1b offbeat chase` | `R029 + PP-095` |
| INT-089 | Center Catch Decay | inclusion | Movers catch center PAR nodes at phrase end and decay out while PAR chase continues lightly. | `movers=4b center catch, pars=2b chase/fade` | `R035 + PP-055` |
| INT-090 | Layer Stack Peel | inclusion | PAR+mover inclusion stacks across 4 bars, then peels back one layer per bar. | `movers=4b stack/peel, pars=1b->2b chase` | `R049 + PP-073` |

### 38.4 Selection Rules For `INT-061..INT-090`

- Use `INT-061..INT-070` when you need technical polish and strong structure without overloading energy.
- Use `INT-071..INT-080` for controlled friction sections where musical tension should rise.
- Use `INT-081..INT-090` for drop punctuation, fill handling, and short inclusion windows.
- Keep random/shuffle behavior (`INT-076`, `INT-083`) to 1-2 bars before resolving back to deterministic geometry.
- After any stack/burst inclusion (`INT-087`, `INT-090`), schedule at least one reset bar with fade-led PAR behavior.
