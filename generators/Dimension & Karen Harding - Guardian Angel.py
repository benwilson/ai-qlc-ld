#!/usr/bin/env python3
"""
Show Generator: Dimension & Karen Harding - Guardian Angel
==========================================================
BPM: 174 | Duration: ~3:44 | Genre: Drum & Bass (euphoric/liquid)

Creative Direction:
  - Theme: Angels, heaven, clouds, feeling a rush
  - Palette: Ethereal & pure — white, gold, ice blue, soft teal
  - Every sound pops — beat-level scene changes in drops
  - Breakdowns: wide, sweeping, luxurious slow continuous mover sweeps
  - Movers: NEVER point behind themselves — forward, left, right, up, down only
  - Pars: Cohesive but dynamic — fade out in quiet parts, go crazy during builds
  - Par patterns: wash (drops), gradient (verses), pairs (transitions), chase (builds)
  - NI3K: Lasers ONLY (no RGBW, no halo), high movement channel values
  - Laser progression: blue only → blue+green → all 3 by final drops
  - Triple drop staircase: each drop adds prisms, wider movement, more lasers

Song Structure (from allin1 analysis @ 174 BPM):
  0:00 - 0:11  verse     (8 bars)   "Ambient Intro" — pre-beat, dark, atmosphere
  0:11 - 0:44  verse     (24 bars)  "Verse 1" — vocals build, pars+movers fade in
  0:44 - 1:06  chorus    (16 bars)  "Drop 1" — first chorus, full energy, blue laser
  1:06 - 1:28  bridge    (16 bars)  "Bridge" — dreamy sweeps, gold/white, single laser
  1:28 - 2:01  chorus    (24 bars)  "Drop 2" — bigger, wider, blue+green lasers
  2:01 - 2:35  verse     (24 bars)  "Verse 2" — luxurious sweeps, green laser
  2:35 - 2:57  chorus    (16 bars)  "Triple #1" — strong, clean, blue+green lasers
  2:57 - 3:18  chorus    (16 bars)  "Triple #2" — prisms, wider, all 3 lasers
  3:18 - 3:40  chorus    (16 bars)  "Triple #3" — EVERYTHING maxed, all lasers, strobes
  3:40 - 3:43  end       (2 bars)   "End" — snap to black
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from showlib import *

BPM = 174
BEAT_MS = bpm_to_ms(BPM, 1)   # ~345ms
BAR_MS = bpm_to_ms(BPM, 4)    # ~1379ms

# =============================================================================
# ETHEREAL PALETTE
# =============================================================================

ICE_BLUE   = (150, 200, 255)
PURE_WHITE = (255, 255, 255)
GOLD       = (255, 200, 80)
SOFT_TEAL  = (100, 255, 200)

ETHEREAL_3 = [ICE_BLUE, PURE_WHITE, SOFT_TEAL]
ETHEREAL_4 = [ICE_BLUE, PURE_WHITE, GOLD, SOFT_TEAL]

# RGB → Mover color wheel mapping
BSW_FOR = {
    ICE_BLUE: BSW_BLUE, PURE_WHITE: BSW_WHITE,
    GOLD: BSW_YELLOW, SOFT_TEAL: BSW_TEAL,
}
SHARPY_FOR = {
    ICE_BLUE: SHARPY_BLUE, PURE_WHITE: SHARPY_WHITE,
    GOLD: SHARPY_AMBER, SOFT_TEAL: SHARPY_TEAL,
}
PROF_FOR = {
    ICE_BLUE: PROF_BLUE, PURE_WHITE: PROF_WHITE,
    GOLD: PROF_YELLOW, SOFT_TEAL: PROF_TEAL,
}

# =============================================================================
# MOVER POSITIONS — Forward-facing only (never behind fixtures)
# (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt)
# =============================================================================

POS = {
    "C":  (153, 0,   7,   19,  0,   123),   # Center floor
    "L":  (115, 8,   65,  22,  40,  118),   # Left
    "R":  (195, 8,   190, 15,  210, 118),   # Right
    "UP": (153, 30,  7,   42,  0,   90),    # High/ceiling
    "W":  (210, 12,  75,  25,  45,  100),   # Wide spread
    "FW": (153, 15,  7,   28,  0,   138),   # Forward (audience)
    "X":  (100, 5,   195, 18,  200, 125),   # Cross (swapped sides)
}

# Position sequences
POS_SWEEP = ["C", "L", "UP", "R", "FW", "W", "C", "X"]
POS_DROP  = ["C", "L", "R", "W", "X", "UP", "FW", "C"]
POS_WIDE  = ["W", "X", "FW", "UP", "W", "L", "R", "X"]
POS_BIG   = ["C", "W", "X", "FW", "UP", "L", "R", "C",
             "X", "W", "UP", "FW", "L", "R", "C", "W"]

# =============================================================================
# SCENE BUILDING WITH DEDUP
# =============================================================================

folder = "Guardian Angel"
scenes = []
scene_cache = {}
dedup_hits = 0
steps = []


def add_scene(name, *fixtures):
    """Add scene with dedup — identical channel values reuse existing scene."""
    global dedup_hits
    flat = []
    for f in fixtures:
        if isinstance(f, list):
            flat.extend(f)
        else:
            flat.append(f)
    flat.sort(key=lambda x: x[0])
    key = tuple((fid, tuple(tuple(cv) for cv in chs)) for fid, chs in flat)
    if key in scene_cache:
        dedup_hits += 1
        return scene_cache[key]
    idx = len(scenes)
    scenes.append(scene(name, *fixtures, path=folder))
    scene_cache[key] = idx
    return idx


def beat_step(scene_idx, beats=1):
    """Add chaser step: instant snap (FadeIn=0), hold for N beats."""
    ms = bpm_to_ms(BPM, beats)
    steps.append((scene_idx, (0, ms)))


def smooth_step(scene_idx, bars=1):
    """Add chaser step: smooth crossfade over N bars (FadeIn=duration, Hold=0)."""
    fi, ho = smooth(BPM, bars)
    steps.append((scene_idx, (fi, ho)))


# =============================================================================
# FIXTURE BUILDERS
# =============================================================================

def mkvrs(pos_key, color, dim=255, frost=0, focus=128,
          prism_s=0, p1r_s=0, prism2_s=0, p2r_s=0,
          prism_b=0, prot_b=0, prism_p=0,
          s_strobe=SHARPY_OPEN, b_shutter=BSW_SHUT_OPEN,
          gobo_b=0, gobo_p=0):
    """Build all 3 movers from position key + color."""
    sp, st, bp, bt, pp, pt = POS[pos_key]
    bsw_c = BSW_FOR.get(color, BSW_WHITE)
    sharpy_c = SHARPY_FOR.get(color, SHARPY_WHITE)
    prof_c = PROF_FOR.get(color, PROF_WHITE)
    s = sharpy(pan=sp, tilt=st, strobe=s_strobe, dim=dim,
               frost=frost, focus=focus, prism1=prism_s, p1r=p1r_s,
               prism2=prism2_s, p2r=p2r_s, colormacro=sharpy_c)
    b = bsw(pan=bp, tilt=bt, color=bsw_c, shutter=b_shutter,
            dim=dim, prism=prism_b, prot=prot_b, focus=focus,
            gobo1=gobo_b)
    p = profile(pan=pp, tilt=pt, dim=dim, prism=prism_p, focus=focus,
                color=prof_c, gobo=gobo_p)
    return s, b, p


def par_wash(color, master=255, strobe=0):
    """All 6 pars same color — maximum cohesion and uniformity."""
    r, g, b = color
    return (fourbar_solid(r, g, b, master=master, strobe=strobe),
            miss1(r, g, b, master=master, strobe=strobe),
            miss2(r, g, b, master=master, strobe=strobe))


def par_gradient(c1, c2, master=255):
    """4BAR gradient + missyees split for subtle texture."""
    fb = fourbar_gradient(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], master=master)
    return fb, miss1(*c1, master=master), miss2(*c2, master=master)


def par_pairs(c1, c2, flip=False, master=255):
    """4BAR: P1+P3=c1, P2+P4=c2 (or flipped). Missyees split."""
    if flip:
        c1, c2 = c2, c1
    fb = fourbar_pairs(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], master=master)
    return fb, miss1(*c1, master=master), miss2(*c2, master=master)


def par_chase(color, beat_idx, master=255):
    """4BAR: one par lit per beat, cycling. Missyees alternate each beat."""
    r, g, b = color
    v = [(0, 0, 0)] * 4
    v[beat_idx % 4] = (r, g, b)
    fb = fourbar(v[0][0], v[0][1], v[0][2], v[1][0], v[1][1], v[1][2],
                 v[2][0], v[2][1], v[2][2], v[3][0], v[3][1], v[3][2],
                 master=master)
    if beat_idx % 2 == 0:
        return fb, miss1(r, g, b, master=master), miss2(0, 0, 0, master=0)
    else:
        return fb, miss1(0, 0, 0, master=0), miss2(r, g, b, master=master)


def par_off():
    """All pars off."""
    return (fourbar_solid(0, 0, 0, master=0),
            miss1(0, 0, 0, master=0),
            miss2(0, 0, 0, master=0))


def mk_ni3k(rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF,
            pan=200, t1=170, t2=190, t3=210):
    """NI3K lasers only — no RGBW, no halo, high movement values."""
    return ni3k(pan=pan, t1=t1, t2=t2, t3=t3,
                r=0, g=0, b=0, w=0, dim=0,
                halo=H_OFF, rl=rl, gl=gl, bl=bl)


# =============================================================================
# BLACKOUT (always scene 0)
# =============================================================================

add_scene("Blackout", *blackout_all())


# =============================================================================
# AMBIENT INTRO — 8 bars, 4-beat steps
# Pre-beat atmosphere. Pars barely visible, fading up from black.
# Movers dark. NI3K dark.
# =============================================================================

for bar in range(8):
    master = bar * 5  # 0 → 35 (barely a glow)
    if master == 0:
        fb, m1, m2 = par_off()
    else:
        fb, m1, m2 = par_wash(ICE_BLUE, master=master)
    s, b, p = mkvrs("C", ICE_BLUE, dim=0)
    n = mk_ni3k()  # dark
    idx = add_scene(f"Amb-{bar+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=4)


# =============================================================================
# VERSE 1A — 12 bars, 4-beat steps (gentle build)
# Vocals enter. Pars fade in with gradients, building from dim.
# Movers slowly appear, frosted.
# =============================================================================

v1a_positions = ["C", "C", "C", "L", "L", "C", "R", "R", "C", "UP", "C", "C"]

for bar in range(12):
    c1 = ETHEREAL_3[bar % 3]
    c2 = ETHEREAL_3[(bar + 1) % 3]
    master = 30 + bar * 14  # 30 → 184 (gradual fade in)
    fb, m1, m2 = par_gradient(c1, c2, master=master)
    pos = v1a_positions[bar]
    mover_dim = min(255, bar * 18)  # 0 → 198
    s, b, p = mkvrs(pos, PURE_WHITE, dim=mover_dim, frost=180, focus=200)
    n = mk_ni3k()  # still dark
    idx = add_scene(f"V1A-{bar+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=4)


# =============================================================================
# VERSE 1B — 12 bars, 2-beat steps (building to drop)
# Pars go CRAZY during this build: gradient → pairs → chase
# First 4 bars: gradients. Next 4: pairs flipping. Last 4: chase cycling.
# Master ramps hard: 140 → 255. This is the buildup — pars should feel urgent.
# =============================================================================

v1b_positions = POS_SWEEP[:8] + POS_SWEEP[:4]  # 12 positions for 12 bars

for i in range(24):
    bar = i // 2
    half = i % 2
    c1 = ETHEREAL_4[i % 4]
    c2 = ETHEREAL_4[(i + 2) % 4]
    master = 140 + bar * 10  # 140 → 250

    if bar < 4:
        # Bars 1-4: gradients cycling — gentle start
        fb, m1, m2 = par_gradient(c1, c2, master=master)
    elif bar < 8:
        # Bars 5-8: pairs flipping each half-bar — more movement
        fb, m1, m2 = par_pairs(c1, c2, flip=(half == 1), master=master)
    else:
        # Bars 9-12: chase pattern — one par at a time, urgent energy
        fb, m1, m2 = par_chase(c1, i, master=master)

    pos = v1b_positions[bar]
    mover_dim = 180 + bar * 6  # 180 → 246
    frost_val = max(0, 160 - bar * 14)  # 160 → 6
    s, b, p = mkvrs(pos, c1, dim=mover_dim, frost=frost_val, focus=160)
    n = mk_ni3k()  # still dark — saving laser reveal for drop
    idx = add_scene(f"V1B-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=2)


# =============================================================================
# DROP 1 — 16 bars, 1-beat steps (64 beats)
# First chorus! Full energy. Beat-synced color snaps.
# Pars alternate wash + pairs every 2 bars for texture.
# Movers reposition every bar. Blue laser reveal on NI3K.
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    c2 = ETHEREAL_4[(beat + 2) % 4]
    pos = POS_DROP[bar % len(POS_DROP)]

    # NI3K movement — rotating tilts, high values
    t1 = 160 + (beat % 5) * 8   # 160-192
    t2 = 175 + (beat % 3) * 10  # 175-195
    t3 = 185 + (beat % 7) * 5   # 185-215

    # Strobe accent on beat 1 every 4 bars — white flash
    if bib == 0 and bar % 4 == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        s, b, p = mkvrs(pos, PURE_WHITE,
                         s_strobe=SHARPY_STROBE_MED,
                         b_shutter=BSW_SHUT_STROBE_FAST)
    else:
        # Alternate: wash on even bars, pairs on odd bars
        if (bar // 2) % 2 == 0:
            fb, m1, m2 = par_wash(c)
        else:
            fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))
        s, b, p = mkvrs(pos, c)

    n = mk_ni3k(bl=LASER_ON, pan=200, t1=t1, t2=t2, t3=t3)
    idx = add_scene(f"D1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# BRIDGE — 16 bars, 2-bar smooth crossfades (8 steps)
# Dreamy. Pars fade out to near-dark — let the movers and laser carry it.
# Slow continuous mover sweeps. Frosted. Gold → ice blue evolution.
# =============================================================================

bridge_sweep = ["C", "L", "UP", "R", "FW", "W", "X", "C"]
bridge_colors = [GOLD, ICE_BLUE, PURE_WHITE, SOFT_TEAL,
                 GOLD, ICE_BLUE, PURE_WHITE, SOFT_TEAL]

for i in range(8):
    c = bridge_colors[i]
    pos = bridge_sweep[i]
    master = max(10, 80 - i * 10)  # 80 → 10 (fading to near-dark)
    fb, m1, m2 = par_wash(c, master=master)
    s, b, p = mkvrs(pos, c, dim=180, frost=200, focus=200)
    n = mk_ni3k(bl=LASER_ON, pan=190 + i * 5, t1=165, t2=180, t3=200)
    idx = add_scene(f"Br-{i+1}", s, b, p, fb, m1, m2, n)
    smooth_step(idx, bars=2)


# =============================================================================
# DROP 2 — 24 bars, 1-beat steps (96 beats)
# Bigger than Drop 1. Wider positions. Color changes every beat.
# Par patterns rotate every 4 bars: wash → pairs → chase → wash...
# Blue + green lasers. Strobe accents every 4 bars.
# =============================================================================

drop2_positions = POS_DROP + POS_WIDE + POS_DROP  # 24 positions for 24 bars

for beat in range(96):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    c2 = ETHEREAL_4[(beat + 2) % 4]
    pos = drop2_positions[bar % len(drop2_positions)]

    t1 = 160 + (beat % 7) * 6   # 160-196
    t2 = 170 + (beat % 5) * 8   # 170-202
    t3 = 180 + (beat % 3) * 12  # 180-204

    # Strobe accent on beat 1 every 4 bars — white solid hit
    if bib == 0 and bar % 4 == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        s, b, p = mkvrs(pos, PURE_WHITE,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)
        n = mk_ni3k(bl=LASER_ON, gl=LASER_ON,
                     pan=210, t1=t1, t2=t2, t3=t3)
    else:
        # Rotate par patterns: wash (4 bars) → pairs (4 bars) → chase (4 bars)
        pat = (bar // 4) % 3
        if pat == 0:
            fb, m1, m2 = par_wash(c)
        elif pat == 1:
            fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))
        else:
            fb, m1, m2 = par_chase(c, beat)
        s, b, p = mkvrs(pos, c)
        n = mk_ni3k(bl=LASER_ON, gl=LASER_ON,
                     pan=200, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"D2-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# VERSE 2A — 16 bars, 2-bar smooth crossfades (8 steps)
# Luxurious sweeps. Pars nearly off — barely a whisper of color.
# Movers and green laser carry the vibe.
# =============================================================================

v2a_sweep = ["C", "R", "UP", "L", "FW", "W", "X", "C"]
v2a_colors = [ICE_BLUE, SOFT_TEAL, PURE_WHITE, GOLD,
              ICE_BLUE, SOFT_TEAL, PURE_WHITE, GOLD]

for i in range(8):
    c = v2a_colors[i]
    pos = v2a_sweep[i]
    master = 15 + i * 5  # 15 → 50 (whisper-level, slowly returning)
    fb, m1, m2 = par_wash(c, master=master)
    s, b, p = mkvrs(pos, c, dim=160, frost=200, focus=200)
    n = mk_ni3k(gl=LASER_ON, pan=195 + i * 3, t1=168, t2=185, t3=195)
    idx = add_scene(f"V2A-{i+1}", s, b, p, fb, m1, m2, n)
    smooth_step(idx, bars=2)


# =============================================================================
# VERSE 2B — 8 bars, 2-beat steps (16 steps)
# Building back up HARD. Pars go from gradient → pairs → chase.
# Master ramps 50 → 255. This build should feel like a rocket launch.
# =============================================================================

v2b_positions = POS_SWEEP  # 8 positions for 8 bars

for i in range(16):
    bar = i // 2
    half = i % 2
    c1 = ETHEREAL_4[i % 4]
    c2 = ETHEREAL_4[(i + 2) % 4]
    master = 50 + bar * 29  # 50 → 253

    if bar < 3:
        # Bars 1-3: gradients, easing in from the quiet
        fb, m1, m2 = par_gradient(c1, c2, master=master)
    elif bar < 6:
        # Bars 4-6: pairs flipping, building energy
        fb, m1, m2 = par_pairs(c1, c2, flip=(half == 1), master=master)
    else:
        # Bars 7-8: chase cycling, full urgency
        fb, m1, m2 = par_chase(c1, i, master=master)

    pos = v2b_positions[bar % len(v2b_positions)]
    mover_dim = 180 + bar * 9  # 180 → 243
    frost_val = max(0, 150 - bar * 20)  # 150 → 10
    s, b, p = mkvrs(pos, c1, dim=mover_dim, frost=frost_val, focus=150)

    # Green laser sustains from Verse 2A
    n = mk_ni3k(gl=LASER_ON, pan=200, t1=170, t2=185, t3=200)

    idx = add_scene(f"V2B-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=2)


# =============================================================================
# TRIPLE #1 — 16 bars, 1-beat (64 beats)
# Staircase Level 1: Strong but not maxed. Clean beams. No prisms.
# Blue + green lasers. Standard drop positions.
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    pos = POS_DROP[bar % len(POS_DROP)]

    t1 = 165 + (beat % 5) * 7   # 165-193
    t2 = 178 + (beat % 3) * 9   # 178-196
    t3 = 188 + (beat % 7) * 5   # 188-218

    # Alternate wash and pairs every 2 bars
    if (bar // 2) % 2 == 0:
        fb, m1, m2 = par_wash(c)
    else:
        c2 = ETHEREAL_4[(beat + 2) % 4]
        fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))
    s, b, p = mkvrs(pos, c)
    n = mk_ni3k(bl=LASER_ON, gl=LASER_ON,
                 pan=205, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"T1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# TRIPLE #2 — 16 bars, 1-beat (64 beats)
# Staircase Level 2: Add prisms. Wider positions. All 3 lasers.
# Pars rotate: wash → chase → pairs every 4 bars. Strobe every 4 bars.
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    c2 = ETHEREAL_4[(beat + 2) % 4]
    pos = POS_WIDE[bar % len(POS_WIDE)]

    t1 = 170 + (beat % 5) * 8   # 170-202
    t2 = 180 + (beat % 3) * 10  # 180-200
    t3 = 190 + (beat % 7) * 6   # 190-226

    # Strobe accent on beat 1 every 4 bars — white flash with prisms
    if bib == 0 and bar % 4 == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        s, b, p = mkvrs(pos, PURE_WHITE,
                         prism_s=128, p1r_s=200,
                         prism_b=80, prot_b=180, prism_p=60,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)
    else:
        # Rotate patterns: wash (4 bars) → chase (4 bars) → pairs (4 bars) → chase
        pat = (bar // 4) % 4
        if pat == 0:
            fb, m1, m2 = par_wash(c)
        elif pat == 1 or pat == 3:
            fb, m1, m2 = par_chase(c, beat)
        else:
            fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))
        s, b, p = mkvrs(pos, c,
                         prism_s=128, p1r_s=200,
                         prism_b=80, prot_b=180, prism_p=60)

    n = mk_ni3k(rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
                 pan=215, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"T2-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# TRIPLE #3 — 16 bars, 1-beat (64 beats)
# Staircase Level 3: EVERYTHING MAXED. Full blowout.
# Dual prisms. Widest 16-position cycle. All lasers. Fastest rotation.
# Pars: chase every beat with solid white hits on strobes.
# Strobe accents every 2 bars (double frequency).
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    pos = POS_BIG[bar % len(POS_BIG)]

    t1 = 175 + (beat % 5) * 9   # 175-211
    t2 = 185 + (beat % 3) * 12  # 185-209
    t3 = 195 + (beat % 7) * 7   # 195-237

    # Strobe accent on beat 1 every 2 bars — solid white hit
    if bib == 0 and bar % 2 == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        s, b, p = mkvrs(pos, PURE_WHITE,
                         prism_s=128, p1r_s=200,
                         prism2_s=128, p2r_s=200,
                         prism_b=128, prot_b=200, prism_p=120,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)
    else:
        # Chase on every non-strobe beat — maximum par activity
        fb, m1, m2 = par_chase(c, beat)
        s, b, p = mkvrs(pos, c,
                         prism_s=128, p1r_s=200,
                         prism2_s=128, p2r_s=200,
                         prism_b=128, prot_b=200, prism_p=120)

    n = mk_ni3k(rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
                 pan=220, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"T3-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# END — snap to black, hold 2 bars
# =============================================================================

beat_step(0, beats=8)


# =============================================================================
# STATS & VERIFICATION
# =============================================================================

total_ms = sum(fi + ho for _, (fi, ho) in steps)
total_bars = total_ms / bpm_to_ms(BPM, 4)

print(f"\nScene dedup: {len(scenes)} unique scenes ({dedup_hits} reuses)")
print(f"Total steps: {len(steps)}")
print(f"Total duration: {total_ms/1000:.1f}s ({total_bars:.1f} bars)")
print(f"Target: ~224s (162 bars)")

# Section timing breakdown
sections = [
    ("Ambient",    8),
    ("Verse 1A",   12),
    ("Verse 1B",   24),
    ("Drop 1",     64),
    ("Bridge",     8),
    ("Drop 2",     96),
    ("Verse 2A",   8),
    ("Verse 2B",   16),
    ("Triple #1",  64),
    ("Triple #2",  64),
    ("Triple #3",  64),
    ("End",        1),
]
offset = 0
for name, count in sections:
    section_steps = steps[offset:offset + count]
    section_ms = sum(fi + ho for _, (fi, ho) in section_steps)
    print(f"  {name:12s}: {count:3d} steps, {section_ms/1000:.1f}s")
    offset += count


# =============================================================================
# BUILD AND WRITE
# =============================================================================

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Guardian Angel", scene_ids, timing,
                          run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "\u25b6 GUARDIAN ANGEL", "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#96C8FF", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace("shows/Dimension & Karen Harding - Guardian Angel.qxw",
                scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
