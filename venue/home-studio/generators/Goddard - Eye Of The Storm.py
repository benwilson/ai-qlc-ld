#!/usr/bin/env python3
"""
Show Generator: Goddard - Eye Of The Storm
=============================================================================
BPM: 174 | Duration: ~2:40 | Genre: drum-and-bass
Moods: aggressive + building (peak for climax)

Aesthetic: Storm as visual metaphor. Building mood gathers cool blue tension,
Aggressive mood unleashes red fury on drops, Peak mood is category-5 climax.
Cool-to-hot color arc (blue → cyan → red → white).

Sections:
  0:00 - 0:22  intro        (16 bars)  "Gathering Storm" — darkness, blue glow
  0:22 - 0:44  build        (16 bars)  "Storm Front" — fixtures adding, blue→red
  0:44 - 1:17  drop 1       (24 bars)  "First Strike" — red assault, all fixtures
  1:17 - 1:39  breakdown    (16 bars)  "Eye of Storm" — reset to blue calm
  1:39 - 1:55  bridge       (12 bars)  "Pressure Rising" — fast build, cyan→red
  1:55 - 2:17  drop 2       (16 bars)  "Second Wave" — RGB lasers, wider sweeps
  2:17 - 2:39  climax       (16 bars)  "Category 5" — peak, everything max
  2:39 -       snap black              "Aftermath"
"""

import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

BPM = 174
BEAT_MS = bpm_to_ms(BPM, 1)   # 345ms
BAR_MS = bpm_to_ms(BPM, 4)    # 1379ms

# =============================================================================
# PALETTE — Building→Aggressive: cool blue → electric cyan → fury red → white
# =============================================================================

STORM_BLUE = (0, 0, 200)
ELECTRIC   = (0, 255, 255)
FURY_RED   = (255, 0, 0)
LIGHTNING  = (255, 255, 255)

# Mover color lookups
BSW_C = {
    STORM_BLUE: BSW_BLUE, ELECTRIC: BSW_TEAL,
    FURY_RED: BSW_RED, LIGHTNING: BSW_WHITE,
}
SHARPY_C = {
    STORM_BLUE: SHARPY_BLUE, ELECTRIC: SHARPY_TEAL,
    FURY_RED: SHARPY_RED, LIGHTNING: SHARPY_WHITE,
}
PROF_C = {
    STORM_BLUE: PROF_BLUE, ELECTRIC: PROF_TEAL,
    FURY_RED: PROF_RED, LIGHTNING: PROF_WHITE,
}
HALO_C = {
    STORM_BLUE: H_BLU, ELECTRIC: H_CYN,
    FURY_RED: H_RED, LIGHTNING: H_RGB,
}

# =============================================================================
# POSITIONS — from focus-positions.md (verified)
# (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)
# =============================================================================

POS = {
    "C":    (153, 0,   177, 19,  0,   123, 128),
    "SL":   (170, 0,   189, 29,  50,  165, 80),
    "SR":   (149, 5,   170, 23,  110, 145, 176),
    "DSC":  (158, 6,   179, 27,  64,  145, 128),
    "USC":  (157, 0,   181, 21,  52,  136, 128),
    "DJ":   (142, 3,   196, 25,  95,  107, 128),
    "CEIL": (158, 73,  180, 86,  91,  30,  128),
    "X":    (149, 5,   189, 29,  0,   123, 128),
}

# Position sequences
DROP_SEQ = ["DSC", "SL", "X", "SR", "DSC", "C", "USC", "X",
            "SL", "DSC", "SR", "C", "X", "USC", "DSC", "C",
            "SL", "X", "DSC", "SR", "C", "X", "USC", "DSC"]
BUILD_SEQ = ["DSC", "C", "SL", "C", "SR", "DSC", "C", "USC"]
CLIMAX_SEQ = ["DSC", "C", "X", "CEIL", "SL", "SR", "DSC", "C",
              "X", "CEIL", "SL", "SR", "USC", "DSC", "DJ", "DSC"]

# =============================================================================
# SCENE MANAGEMENT
# =============================================================================

folder = "Eye Of The Storm"
scenes = []
scene_cache = {}
dedup_hits = 0
steps = []


def add(name, *fixtures):
    """Add scene with dedup."""
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


def beat(scene_idx, beats=1):
    """Beat-synced step: instant change, hold."""
    steps.append((scene_idx, (0, bpm_to_ms(BPM, beats))))


def xfade(scene_idx, bars=2):
    """Smooth crossfade step over N bars."""
    steps.append((scene_idx, (bpm_to_ms(BPM, bars * 4), 0)))


# =============================================================================
# FIXTURE BUILDERS
# =============================================================================

def mvrs(pos_key, color, dim=255, frost=0, focus=128,
         prism_s=0, p1r_s=0, prism_b=0, prot_b=0, prism_p=0,
         gobo_b1=0, gobo_s=0,
         s_strobe=SHARPY_OPEN, b_shutter=BSW_SHUT_OPEN):
    """Build all 3 movers from position + color."""
    sp, st, bp, bt, pp, pt, _ = POS[pos_key]
    return (
        sharpy(pan=sp, tilt=st, strobe=s_strobe, dim=dim,
               frost=frost, focus=focus, gobo=gobo_s,
               prism1=prism_s, p1r=p1r_s,
               colormacro=SHARPY_C.get(color, SHARPY_WHITE)),
        bsw(pan=bp, tilt=bt, color=BSW_C.get(color, BSW_WHITE),
            gobo1=gobo_b1, shutter=b_shutter, dim=dim,
            prism=prism_b, prot=prot_b, focus=focus),
        profile(pan=pp, tilt=pt, dim=dim, prism=prism_p, focus=focus,
                color=PROF_C.get(color, PROF_WHITE))
    )


def solo_sharpy(pos_key, color, dim=255, gobo=0, prism=0, pr=0,
                strobe=SHARPY_OPEN):
    """Sharpy only, others dark at same position (prevents pan spins)."""
    sp, st, bp, bt, pp, pt, _ = POS[pos_key]
    s = sharpy(pan=sp, tilt=st, strobe=strobe, dim=dim, gobo=gobo,
               prism1=prism, p1r=pr,
               colormacro=SHARPY_C.get(color, SHARPY_WHITE))
    b = dark_bsw(pan=bp, tilt=bt)
    p = dark_profile(pan=pp, tilt=pt)
    return s, b, p


def solo_bsw(pos_key, color, dim=255, gobo1=0, prism=0, prot=0):
    """BSW only, others dark at same position (prevents pan spins)."""
    sp, st, bp, bt, pp, pt, _ = POS[pos_key]
    s = dark_sharpy(pan=sp, tilt=st)
    b = bsw(pan=bp, tilt=bt, color=BSW_C.get(color, BSW_WHITE),
            gobo1=gobo1, dim=dim, prism=prism, prot=prot)
    p = dark_profile(pan=pp, tilt=pt)
    return s, b, p


def pars_off():
    """All pars blackout."""
    return (blackout(FX_4BAR, CH_4BAR),
            blackout(FX_MISS1, CH_MISS),
            blackout(FX_MISS2, CH_MISS))


def pars_color(color, master=255):
    """All pars solid color."""
    r, g, b = color
    return (fourbar_solid(r, g, b, master=master),
            miss1(r, g, b, master=master),
            miss2(r, g, b, master=master))


def nk(color, pos_key="DSC", dim=255, halo="sync",
       rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF,
       t1=64, t2=64, t3=64, strobe=0):
    """Build NI3K."""
    r, g, b = color
    halo_map = {"sync": HALO_C.get(color, H_RGB),
                "jump_fast": H_JUMP_FAST, "jump_med": H_JUMP_MED,
                "jump_slow": H_JUMP_SLOW, "off": H_OFF}
    h = halo_map.get(halo, H_RGB)
    return ni3k(pan=POS[pos_key][6], t1=t1, t2=t2, t3=t3,
                r=r, g=g, b=b, halo=h, dim=dim, strobe=strobe,
                rl=rl, gl=gl, bl=bl)


# =============================================================================
# BLACKOUT (scene 0)
# =============================================================================

add("Blackout", *blackout_all())


# =============================================================================
# 1. GATHERING STORM — Intro (16 bars, 4 smooth 4-bar sweeps)
# Building Phase 1: Near-darkness → single blue beam → slow drift.
# Movers reset to DSC at section start.
# =============================================================================

# Step 1: Total darkness. NI3K barely visible blue halo. Movers at DSC.
idx = add("Gather-Void",
    *solo_sharpy("DSC", STORM_BLUE, dim=0),
    *pars_off(),
    nk(STORM_BLUE, dim=20, halo="sync"))
xfade(idx, bars=4)

# Step 2: NI3K glow grows. Sharpy fades in at DSC, dim blue.
idx = add("Gather-Glow",
    *solo_sharpy("DSC", STORM_BLUE, dim=40),
    *pars_off(),
    nk(STORM_BLUE, dim=60, halo="sync"))
xfade(idx, bars=4)

# Step 3: Sharpy brighter, drifts to SL. Building Phase 1 → 2 transition.
idx = add("Gather-Drift",
    *solo_sharpy("SL", STORM_BLUE, dim=80),
    *pars_off(),
    nk(STORM_BLUE, dim=100, halo="sync"))
xfade(idx, bars=4)

# Step 4: Sharpy at SR, brighter still. Storm clouds visible. Pre-build.
idx = add("Gather-Loom",
    *solo_sharpy("SR", STORM_BLUE, dim=120, gobo=BSW_G1_3),
    *pars_off(),
    nk(STORM_BLUE, dim=140, halo="jump_slow", rl=LASER_OFF))
xfade(idx, bars=4)


# =============================================================================
# 2. STORM FRONT — Build (16 bars)
# Building Phase 2→3: Fixtures add one by one. Blue → cyan → red.
# Movement accelerates. Strobe ramp last 4 bars.
# =============================================================================

# Phase A: Sharpy solo, blue (4 bars, 2x 2-bar smooth)
for i in range(2):
    pos = ["DSC", "C"][i]
    idx = add(f"Front-A{i+1}",
        *solo_sharpy(pos, STORM_BLUE, dim=140 + i * 30),
        *pars_off(),
        nk(STORM_BLUE, dim=100 + i * 20, halo="sync"))
    xfade(idx, bars=2)

# Phase B: Add BSW, shift to cyan (4 bars, 4x 1-bar)
phase_b_pos = ["DSC", "SL", "C", "SR"]
for i in range(4):
    pos = phase_b_pos[i]
    sp, st = POS[pos][0], POS[pos][1]
    bp, bt = POS[pos][2], POS[pos][3]
    pp, pt = POS[pos][4], POS[pos][5]
    s = sharpy(pan=sp, tilt=st, dim=180 + i * 15,
               colormacro=SHARPY_C[ELECTRIC])
    b = bsw(pan=bp, tilt=bt, color=BSW_C[ELECTRIC],
            dim=80 + i * 30)
    p = dark_profile(pan=pp, tilt=pt)
    fb, m1, m2 = pars_off()
    n = nk(ELECTRIC, pos_key=pos, dim=120 + i * 20, halo="sync")
    idx = add(f"Front-B{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx, beats=4)

# Phase C: Add Profile + pars, shift toward red (4 bars, 2-beat steps = 8)
for i in range(8):
    progress = i / 7.0
    color = ELECTRIC if progress < 0.5 else FURY_RED
    pos = BUILD_SEQ[i % len(BUILD_SEQ)]
    dim_val = int(200 + 55 * progress)

    s, b, p = mvrs(pos, color, dim=min(dim_val, 255),
                    gobo_b1=BSW_G1_3 if progress > 0.5 else 0)
    par_m = int(40 + 120 * progress)
    fb, m1, m2 = pars_color(color, master=min(par_m, 160))
    n = nk(color, pos_key=pos, dim=min(dim_val - 20, 230),
           halo="sync" if progress < 0.5 else "jump_slow")
    idx = add(f"Front-C{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx, beats=2)

# Phase D: Strobe ramp pre-drop (4 bars, beat-level = 16 beats)
strobe_ramp = ([SHARPY_STROBE_SLOW] * 4 + [SHARPY_STROBE_MED] * 4 +
               [SHARPY_STROBE_FAST] * 8)
bsw_ramp = [20] * 4 + [70] * 4 + [BSW_SHUT_STROBE_FAST] * 8
pre_pos = ["DSC", "X", "C", "DSC"] * 4
for i in range(16):
    s, b, p = mvrs(pre_pos[i], FURY_RED, dim=255,
                    gobo_b1=BSW_G1_3, prism_s=128, p1r_s=200,
                    prism_b=80, prot_b=180,
                    s_strobe=strobe_ramp[i],
                    b_shutter=bsw_ramp[i])
    fb, m1, m2 = pars_color(FURY_RED, master=160)
    laser = LASER_ON if i >= 12 else LASER_OFF
    n = nk(FURY_RED, pos_key=pre_pos[i], halo="jump_fast",
           rl=laser, t1=80 + i * 4, t2=60 + i * 5, t3=70 + i * 4)
    idx = add(f"Front-D{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx)


# =============================================================================
# 3. FIRST STRIKE — Drop 1 (24 bars, 96 beats)
# Aggressive dominates. Red assault. Beat-level position cycling.
# 1-beat blackout accents every 4 bars. White strobe bursts.
# =============================================================================

for b_idx in range(96):
    bar = b_idx // 4
    bib = b_idx % 4
    pos = DROP_SEQ[bar % len(DROP_SEQ)]
    t1v = 150 + (b_idx % 5) * 14
    t2v = 160 + (b_idx % 3) * 18
    t3v = 140 + (b_idx % 7) * 12

    # 1-beat blackout accent on beat 3 of every 4th bar
    if bib == 2 and bar % 4 == 3:
        idx = add(f"D1-Black{bar}", *blackout_all())
        beat(idx)
        continue

    # White strobe burst on beat 1 every 2nd bar
    if bib == 0 and bar % 2 == 0:
        s, b, p = mvrs(pos, LIGHTNING,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200,
                        gobo_b1=BSW_G1_3,
                        s_strobe=SHARPY_STROBE_FAST,
                        b_shutter=BSW_SHUT_STROBE_FAST)
        fb, m1, m2 = pars_color(FURY_RED, master=160)
        n = nk(LIGHTNING, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, t1=t1v, t2=t2v, t3=t3v)
    else:
        s, b, p = mvrs(pos, FURY_RED,
                        prism_s=128, p1r_s=200,
                        prism_b=80, prot_b=180,
                        gobo_b1=BSW_G1_3)
        fb, m1, m2 = pars_color(FURY_RED, master=160)
        n = nk(FURY_RED, pos_key=pos, halo="jump_med",
               rl=LASER_ON, t1=t1v, t2=t2v, t3=t3v)

    idx = add(f"D1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat(idx)


# =============================================================================
# 4. EYE OF STORM — Breakdown (16 bars)
# Building Phase 1 reset. SNAP to near-blackout, single blue beam.
# Calm before the next wave. Movers reset to DSC.
# =============================================================================

# First bar: snap to DSC blackout (movers reset)
idx = add("Eye-Reset",
    *mvrs("DSC", STORM_BLUE, dim=0),
    *pars_off(),
    nk(STORM_BLUE, dim=10, halo="sync"))
beat(idx, beats=4)

# Bars 2-8: single BSW stalking in blue (7 bars, smooth 1-bar each)
stalk_pos = ["DSC", "SL", "C", "SR", "DSC", "C", "SL"]
for i in range(7):
    pos = stalk_pos[i]
    dim_val = 30 + i * 8
    s, b, p = solo_bsw(pos, STORM_BLUE, dim=dim_val, gobo1=BSW_G1_3)
    fb, m1, m2 = pars_off()
    n = nk(STORM_BLUE, dim=20 + i * 5, halo="sync")
    idx = add(f"Eye-Stalk{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx, beats=4)

# Bars 9-12: Sharpy joins, building gathers (4 bars, 2-beat steps = 8)
gather_pos = ["DSC", "C", "SL", "C", "SR", "DSC", "C", "DSC"]
for i in range(8):
    progress = i / 7.0
    pos = gather_pos[i]
    dim_val = int(60 + 80 * progress)

    if i < 4:
        # BSW + Sharpy
        sp, st = POS[pos][0], POS[pos][1]
        bp, bt = POS[pos][2], POS[pos][3]
        pp, pt = POS[pos][4], POS[pos][5]
        s = sharpy(pan=sp, tilt=st, dim=dim_val,
                   colormacro=SHARPY_C[STORM_BLUE])
        b = bsw(pan=bp, tilt=bt, color=BSW_C[STORM_BLUE],
                dim=dim_val - 20, gobo1=BSW_G1_3)
        p = dark_profile(pan=pp, tilt=pt)
    else:
        color = ELECTRIC if progress > 0.7 else STORM_BLUE
        s, b, p = mvrs(pos, color, dim=min(dim_val + 40, 200))
    fb, m1, m2 = pars_off()
    n = nk(STORM_BLUE, pos_key=pos, dim=min(dim_val - 10, 150),
           halo="sync" if progress < 0.6 else "jump_slow")
    idx = add(f"Eye-Gather{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx, beats=2)

# Bars 13-16: building cresting, fixtures ramping (4 bars, beat-level = 16)
crest_pos = ["DSC", "C", "SL", "DSC"] * 4
for i in range(16):
    progress = i / 15.0
    pos = crest_pos[i]
    color = ELECTRIC if progress < 0.5 else FURY_RED
    dim_val = int(140 + 115 * progress)

    s, b, p = mvrs(pos, color, dim=min(dim_val, 255),
                    gobo_b1=BSW_G1_3 if progress > 0.5 else 0)
    par_m = int(60 * progress) if progress > 0.3 else 0
    if par_m > 0:
        fb, m1, m2 = pars_color(color, master=par_m)
    else:
        fb, m1, m2 = pars_off()
    n = nk(color, pos_key=pos, dim=min(dim_val - 20, 200),
           halo="sync" if progress < 0.5 else "jump_slow")
    idx = add(f"Eye-Crest{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx)


# =============================================================================
# 5. PRESSURE RISING — Bridge/Build (12 bars)
# Building Phase 2→3 accelerated. Faster than Storm Front.
# Blue → cyan → red in 12 bars. Strobe ramp, laser reveal.
# =============================================================================

# Phase A: Quick fixture layering (4 bars, 2-beat = 8 steps)
pressure_pos = ["DSC", "C", "SL", "SR", "DSC", "C", "X", "DSC"]
for i in range(8):
    progress = i / 7.0
    pos = pressure_pos[i]

    if progress < 0.3:
        color = STORM_BLUE
    elif progress < 0.6:
        color = ELECTRIC
    else:
        color = FURY_RED

    dim_val = int(120 + 135 * progress)

    if i < 2:
        # Solo sharpy
        s, b, p = solo_sharpy(pos, color, dim=min(dim_val, 255))
    elif i < 4:
        # Sharpy + BSW
        sp, st = POS[pos][0], POS[pos][1]
        bp, bt = POS[pos][2], POS[pos][3]
        pp, pt = POS[pos][4], POS[pos][5]
        s = sharpy(pan=sp, tilt=st, dim=min(dim_val, 255),
                   colormacro=SHARPY_C.get(color, SHARPY_WHITE))
        b = bsw(pan=bp, tilt=bt, color=BSW_C.get(color, BSW_WHITE),
                dim=min(dim_val - 30, 200))
        p = dark_profile(pan=pp, tilt=pt)
    else:
        s, b, p = mvrs(pos, color, dim=min(dim_val, 255),
                        gobo_b1=BSW_G1_3 if progress > 0.5 else 0)

    par_m = int(80 * progress) if progress > 0.4 else 0
    if par_m > 0:
        fb, m1, m2 = pars_color(color, master=par_m)
    else:
        fb, m1, m2 = pars_off()
    n = nk(color, pos_key=pos, dim=min(dim_val - 20, 200),
           halo="sync" if progress < 0.4 else "jump_slow")
    idx = add(f"Press-A{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx, beats=2)

# Phase B: Full rig build (4 bars, beat-level = 16 beats)
for i in range(16):
    progress = i / 15.0
    pos = ["DSC", "X", "C", "DSC"] [i % 4]
    color = ELECTRIC if progress < 0.3 else FURY_RED
    dim_val = int(200 + 55 * progress)

    s, b, p = mvrs(pos, color, dim=min(dim_val, 255),
                    gobo_b1=BSW_G1_3, prism_s=128 if progress > 0.5 else 0,
                    p1r_s=200 if progress > 0.5 else 0,
                    prism_b=80 if progress > 0.5 else 0,
                    prot_b=180 if progress > 0.5 else 0)
    fb, m1, m2 = pars_color(color, master=int(80 + 80 * progress))
    laser = LASER_ON if i >= 12 else LASER_OFF
    n = nk(color, pos_key=pos, halo="jump_med" if progress > 0.3 else "sync",
           rl=laser, t1=60 + i * 5, t2=80 + i * 4, t3=70 + i * 5)
    idx = add(f"Press-B{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx)

# Phase C: Strobe ramp (4 bars, beat-level = 16 beats)
strobe_ramp2 = ([SHARPY_STROBE_SLOW] * 4 + [SHARPY_STROBE_MED] * 4 +
                [SHARPY_STROBE_FAST] * 8)
bsw_ramp2 = [20] * 4 + [70] * 4 + [BSW_SHUT_STROBE_FAST] * 8
pre_pos2 = ["DSC", "X", "C", "DSC"] * 4
for i in range(16):
    s, b, p = mvrs(pre_pos2[i], FURY_RED, dim=255,
                    gobo_b1=BSW_G1_3, prism_s=128, p1r_s=200,
                    prism_b=80, prot_b=180,
                    s_strobe=strobe_ramp2[i],
                    b_shutter=bsw_ramp2[i])
    fb, m1, m2 = pars_color(FURY_RED, master=200)
    laser = LASER_ON if i >= 8 else LASER_OFF
    n = nk(FURY_RED, pos_key=pre_pos2[i], halo="jump_fast",
           rl=laser, gl=laser,
           t1=80 + i * 4, t2=60 + i * 5, t3=70 + i * 4)
    idx = add(f"Press-C{i+1}", s, b, p, fb, m1, m2, n)
    beat(idx)


# =============================================================================
# 6. SECOND WAVE — Drop 2 (16 bars, 64 beats)
# Aggressive intensifies. All RGB lasers. Wider sweeps.
# Different gobo for texture variety.
# =============================================================================

DROP2_SEQ = ["DSC", "C", "SL", "X", "CEIL", "SR", "DSC", "C",
             "X", "SL", "SR", "CEIL", "DSC", "C", "USC", "DSC"]

for b_idx in range(64):
    bar = b_idx // 4
    bib = b_idx % 4
    pos = DROP2_SEQ[bar % len(DROP2_SEQ)]
    t1v = 160 + (b_idx % 5) * 14
    t2v = 170 + (b_idx % 3) * 18
    t3v = 150 + (b_idx % 7) * 12

    # 1-beat blackout accent
    if bib == 3 and bar % 4 == 3:
        idx = add(f"D2-Black{bar}", *blackout_all())
        beat(idx)
        continue

    # White strobe every 2nd bar
    if bib == 0 and bar % 2 == 0:
        s, b, p = mvrs(pos, LIGHTNING,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200, prism_p=60,
                        gobo_b1=BSW_G1_5,
                        s_strobe=SHARPY_STROBE_FAST,
                        b_shutter=BSW_SHUT_STROBE_FAST)
        fb, m1, m2 = pars_color(LIGHTNING, master=160)
        n = nk(LIGHTNING, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)
    else:
        s, b, p = mvrs(pos, FURY_RED,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200, prism_p=60,
                        gobo_b1=BSW_G1_5)
        fb, m1, m2 = pars_color(FURY_RED, master=160)
        n = nk(FURY_RED, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)

    idx = add(f"D2-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat(idx)


# =============================================================================
# 7. CATEGORY 5 — Climax (16 bars, 64 beats)
# Peak mood. Maximum everything. 120% energy.
# Color swap every 4 bars: Red → White → Red → White (internal dynamics)
# Last 2 bars: full white whiteout.
# =============================================================================

for b_idx in range(64):
    bar = b_idx // 4
    bib = b_idx % 4
    pos = CLIMAX_SEQ[bar % len(CLIMAX_SEQ)]
    t1v = 170 + (b_idx % 4) * 15
    t2v = 150 + (b_idx % 3) * 20
    t3v = 180 + (b_idx % 5) * 10

    # Last 2 bars: full white whiteout
    if bar >= 14:
        s, b, p = mvrs(pos, LIGHTNING,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200, prism_p=120,
                        s_strobe=SHARPY_STROBE_FAST,
                        b_shutter=BSW_SHUT_STROBE_FAST)
        fb, m1, m2 = pars_color(LIGHTNING)
        n = nk(LIGHTNING, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)
    else:
        # 4-bar color swap: Red (0-3), White (4-7), Red (8-11), White (12-13)
        phase = (bar // 4) % 2
        base_color = FURY_RED if phase == 0 else LIGHTNING

        # 1-beat blackout accent on beat 3 of every 4th bar
        if bib == 3 and bar % 4 == 3:
            idx = add(f"C5-Black{bar}", *blackout_all())
            beat(idx)
            continue

        # Strobe on beat 1 every bar
        if bib == 0:
            s, b, p = mvrs(pos, base_color,
                            prism_s=128, p1r_s=200,
                            prism_b=128, prot_b=200, prism_p=80,
                            gobo_b1=BSW_G1_3,
                            s_strobe=SHARPY_STROBE_FAST,
                            b_shutter=BSW_SHUT_STROBE_FAST)
        else:
            s, b, p = mvrs(pos, base_color,
                            prism_s=128, p1r_s=200,
                            prism_b=128, prot_b=200, prism_p=80,
                            gobo_b1=BSW_G1_3)

        fb, m1, m2 = pars_color(base_color, master=200)
        n = nk(base_color, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)

    idx = add(f"C5-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat(idx)


# =============================================================================
# 8. AFTERMATH — snap to black
# =============================================================================

beat(0)


# =============================================================================
# STATS & VERIFICATION
# =============================================================================

total_ms = sum(fi + ho for _, (fi, ho) in steps)
total_bars = total_ms / BAR_MS

print(f"\nScene dedup: {len(scenes)} unique ({dedup_hits} reuses)")
print(f"Steps: {len(steps)}")
print(f"Duration: {total_ms/1000:.1f}s ({total_bars:.1f} bars @ {BPM} BPM)")
print(f"Target: ~160s (116 bars)")

sections = [
    ("Gathering",       4),
    ("Storm Front",     2 + 4 + 8 + 16),
    ("First Strike",    96),
    ("Eye of Storm",    1 + 7 + 8 + 16),
    ("Pressure Rising", 8 + 16 + 16),
    ("Second Wave",     64),
    ("Category 5",      64),
    ("Blackout",        1),
]
offset = 0
for name, count in sections:
    section_ms = sum(fi + ho for _, (fi, ho) in steps[offset:offset + count])
    print(f"  {name:17s}: {count:3d} steps, {section_ms/1000:.1f}s")
    offset += count


# =============================================================================
# BUILD AND WRITE
# =============================================================================

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Eye Of The Storm", scene_ids, timing,
                          run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "\u25b6 EYE OF THE STORM", "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#0044CC", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace(
    os.path.join(VENUE_DIR, "shows",
                 "Goddard - Eye Of The Storm.qxw"),
    scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
