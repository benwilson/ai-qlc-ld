#!/usr/bin/env python3
"""
Show Generator: Prodigy - No Good For Me (A.way Bootleg)
=============================================================================
BPM: 174 | Duration: ~3:17 | Genre: drum-and-bass
Moods: aggressive + dark

Aesthetic: Darkness as canvas, red violence as punctuation.
Breakdowns near-blackout (1-2 fixtures, stalking). Drops are sudden
devastating assaults (all fixtures, red + white strobe, instant snaps).

Sections:
  0:00 - 0:22  intro        (custom)   "The Warning" — darkness, single red glow
  0:22 - 0:42  drop 1       (15 bars)  "First Blood" — red assault, angular snaps
  0:42 - 1:04  breakdown    (16 bars)  "The Reckoning" — dark→build→pre-drop
  1:04 - 1:26  main drop    (16 bars)  "No Good" — FULL SEND, all lasers, strobe
  1:26 - 1:48  verse        (16 bars)  "Rolling" — 2 fixtures, stalking red beam
  1:48 - 2:10  chorus       (16 bars)  "The Hook" — rising aggression, 3-4 fixtures
  2:10 - 2:32  breakdown    (16 bars)  "Descent" — darkest point, blue→build→red
  2:32 - 2:54  drop 2       (16 bars)  "Blood Moon" — RGB lasers, wider sweeps
  2:54 - 3:17  final        (16 bars)  "Inferno" — maximum, white out, snap black
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
# PALETTE — Aggressive Dark: single color at a time, deep red dominant
# =============================================================================

BLOOD_RED    = (255, 0, 0)
DEEP_BLUE    = (0, 0, 180)
DARK_AMBER   = (200, 80, 0)
ICE_WHITE    = (255, 255, 255)

# Mover color lookups
BSW_C = {
    BLOOD_RED: BSW_RED, DEEP_BLUE: BSW_BLUE,
    DARK_AMBER: BSW_ORANGE, ICE_WHITE: BSW_WHITE,
}
SHARPY_C = {
    BLOOD_RED: SHARPY_RED, DEEP_BLUE: SHARPY_BLUE,
    DARK_AMBER: SHARPY_AMBER, ICE_WHITE: SHARPY_WHITE,
}
PROF_C = {
    BLOOD_RED: PROF_RED, DEEP_BLUE: PROF_BLUE,
    DARK_AMBER: PROF_ORANGE, ICE_WHITE: PROF_WHITE,
}
HALO_C = {
    BLOOD_RED: H_RED, DEEP_BLUE: H_BLU,
    DARK_AMBER: H_RED, ICE_WHITE: H_RGB,
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

# Position sequences per section type
DROP_SEQ = ["C", "SL", "X", "SR", "DSC", "C", "USC", "X",
            "SL", "DSC", "SR", "C", "X", "USC", "DSC", "C"]
ROLL_SEQ = ["C", "SL", "C", "SR", "DSC", "C", "USC", "C"]
HOOK_SEQ = ["C", "SL", "SR", "DSC", "X", "USC", "C", "X",
            "SL", "DSC", "SR", "C", "USC", "DSC", "X", "C"]
CLIMAX_SEQ = ["C", "DSC", "X", "CEIL", "SL", "SR", "DSC", "C",
              "X", "CEIL", "SL", "SR", "USC", "DSC", "DJ", "C"]

# =============================================================================
# SCENE MANAGEMENT
# =============================================================================

folder = "No Good For Me"
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


def snap(scene_idx, beats=1):
    """Beat-synced step: instant change, hold."""
    steps.append((scene_idx, (0, bpm_to_ms(BPM, beats))))


def xfade(scene_idx, bars=2):
    """Smooth crossfade step over N bars."""
    steps.append((scene_idx, (bpm_to_ms(BPM, bars * 4), 0)))


def timed(scene_idx, ms):
    """Custom ms hold."""
    steps.append((scene_idx, (0, ms)))


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
    """All pars blackout (Dark mood: pars off during breakdowns)."""
    return (blackout(FX_4BAR, CH_4BAR),
            blackout(FX_MISS1, CH_MISS),
            blackout(FX_MISS2, CH_MISS))


def pars_red(master=255):
    """All pars solid red."""
    return (fourbar_solid(255, 0, 0, master=master),
            miss1(255, 0, 0, master=master),
            miss2(255, 0, 0, master=master))


def pars_blue(master=255):
    """All pars solid deep blue."""
    return (fourbar_solid(0, 0, 180, master=master),
            miss1(0, 0, 180, master=master),
            miss2(0, 0, 180, master=master))


def pars_color(color, master=255):
    """All pars solid custom color."""
    r, g, b = color
    return (fourbar_solid(r, g, b, master=master),
            miss1(r, g, b, master=master),
            miss2(r, g, b, master=master))


def nk(color, pos_key="C", dim=255, halo="sync",
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
# 1. THE WARNING — Intro (22,000ms custom timing)
# Dark Phase 1→2: Near-total darkness → single red glow → stalking beam
# =============================================================================

# Total darkness. NI3K barely visible red halo.
idx = add("Intro-Void",
    *solo_sharpy("C", BLOOD_RED, dim=0),
    *pars_off(),
    nk(BLOOD_RED, dim=20, halo="sync"))
timed(idx, 5000)

# NI3K glow grows. Still pure darkness otherwise.
idx = add("Intro-Glow",
    *solo_sharpy("C", BLOOD_RED, dim=0),
    *pars_off(),
    nk(BLOOD_RED, dim=60, halo="sync"))
timed(idx, 4000)

# Single Sharpy beam fades in at center. Dim, stalking. (Dark Phase 2)
idx = add("Intro-Stalk",
    *solo_sharpy("C", BLOOD_RED, dim=40),
    *pars_off(),
    nk(BLOOD_RED, dim=80, halo="sync"))
timed(idx, 4000)

# Sharpy brighter, slight position shift. Tension building.
idx = add("Intro-Hunt",
    *solo_sharpy("SL", BLOOD_RED, dim=80, gobo=BSW_G1_3),
    *pars_off(),
    nk(BLOOD_RED, dim=120, halo="sync"))
timed(idx, 3500)

# BSW joins. Two red beams converging. NI3K laser reveals as architecture.
sp, st, _, _, _, _, _ = POS["C"]
bp, bt = POS["SR"][2], POS["SR"][3]
idx = add("Intro-Converge",
    sharpy(pan=sp, tilt=st, dim=120, colormacro=SHARPY_RED),
    bsw(pan=bp, tilt=bt, color=BSW_RED, dim=100),
    dark_profile(pan=POS["SR"][4], tilt=POS["SR"][5]),
    *pars_off(),
    nk(BLOOD_RED, dim=160, halo="sync", rl=LASER_ON))
timed(idx, 3000)

# Pre-drop tension. Both movers at center, brighter. Red laser cutting.
idx = add("Intro-Tension",
    *mvrs("C", BLOOD_RED, dim=160, gobo_b1=BSW_G1_3),
    *pars_off(),
    nk(BLOOD_RED, dim=200, halo="jump_slow", rl=LASER_ON))
timed(idx, 2500)


# =============================================================================
# 2. FIRST BLOOD — Drop 1 (15 bars, 60 beats)
# Aggressive dominates. Red assault, angular snaps. Pars dim red.
# 1-beat blackout accents every 4 bars (Aggressive: blackouts as weapon).
# =============================================================================

for beat in range(60):
    bar = beat // 4
    bib = beat % 4
    pos = DROP_SEQ[bar % len(DROP_SEQ)]
    t1v = 50 + (beat % 7) * 12
    t2v = 70 + (beat % 5) * 10
    t3v = 60 + (beat % 6) * 9

    # 1-beat blackout accent on beat 3 of every 4th bar
    if bib == 2 and bar % 4 == 3:
        idx = add(f"D1-Black{bar}", *blackout_all())
        snap(idx)
        continue

    # White strobe burst on beat 1 every 2nd bar
    if bib == 0 and bar % 2 == 0 and bar > 0:
        s, b, p = mvrs(pos, ICE_WHITE, prism_s=128, p1r_s=200,
                        prism_b=80, prot_b=180, gobo_b1=BSW_G1_3,
                        s_strobe=SHARPY_STROBE_FAST,
                        b_shutter=BSW_SHUT_STROBE_FAST)
        fb, m1, m2 = pars_red(master=130)
        n = nk(ICE_WHITE, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, t1=t1v, t2=t2v, t3=t3v)
    else:
        s, b, p = mvrs(pos, BLOOD_RED, prism_s=128, p1r_s=200,
                        prism_b=80, prot_b=180, gobo_b1=BSW_G1_3)
        fb, m1, m2 = pars_red(master=130)
        n = nk(BLOOD_RED, pos_key=pos, halo="jump_med",
               rl=LASER_ON, t1=t1v, t2=t2v, t3=t3v)

    idx = add(f"D1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    snap(idx)


# =============================================================================
# 3. THE RECKONING — Breakdown→Build (16 bars)
# Phase A (4 bars): SNAP to near-blackout. Single fixture stalking.
# Phase B (8 bars): Fixtures add one by one. Blue→amber→red.
# Phase C (4 bars): Strobe build, laser reveal.
# =============================================================================

# Phase A: Dark Phase 1 — near-blackout, single BSW stalking
stalk_pos = ["C", "SL", "C", "SR"]
for bar in range(4):
    pos = stalk_pos[bar]
    s, b, p = solo_bsw(pos, DEEP_BLUE, dim=40 + bar * 10, gobo1=BSW_G1_3)
    fb, m1, m2 = pars_off()
    n = nk(DEEP_BLUE, dim=30, halo="sync")
    idx = add(f"Reck-Stalk{bar+1}", s, b, p, fb, m1, m2, n)
    snap(idx, beats=4)

# Phase B: Build — fixtures add, blue→amber→red (8 bars, 2-beat steps = 16)
build_pos = ["C", "C", "SL", "SR", "DSC", "USC", "X", "C"]
for i in range(16):
    bar_in_phase = i // 2
    progress = i / 15.0

    if progress < 0.35:
        color = DEEP_BLUE
    elif progress < 0.65:
        color = DARK_AMBER
    else:
        color = BLOOD_RED

    pos = build_pos[bar_in_phase % len(build_pos)]
    dim_val = int(40 + 215 * progress)

    # First 4 steps: solo Sharpy. Next 4: add BSW. Last 8: all movers.
    if i < 4:
        s, b, p = solo_sharpy(pos, color, dim=min(dim_val, 255))
        fb, m1, m2 = pars_off()
    elif i < 8:
        sp, st = POS[pos][0], POS[pos][1]
        bp, bt = POS[pos][2], POS[pos][3]
        pp, pt = POS[pos][4], POS[pos][5]
        s = sharpy(pan=sp, tilt=st, dim=min(dim_val, 255),
                   colormacro=SHARPY_C.get(color, SHARPY_WHITE))
        b = bsw(pan=bp, tilt=bt, color=BSW_C.get(color, BSW_WHITE),
                dim=min(dim_val - 40, 200))
        p = dark_profile(pan=pp, tilt=pt)
        fb, m1, m2 = pars_off()
    else:
        s, b, p = mvrs(pos, color, dim=min(dim_val, 255),
                        gobo_b1=BSW_G1_3 if progress > 0.7 else 0)
        par_m = int(30 + 100 * progress)
        fb, m1, m2 = pars_color(color, master=min(par_m, 130))

    n = nk(color, pos_key=pos, dim=min(dim_val - 20, 200),
           halo="sync" if progress < 0.5 else "jump_slow")
    idx = add(f"Reck-B{i+1}", s, b, p, fb, m1, m2, n)
    snap(idx, beats=2)

# Phase C: Pre-drop strobe build (4 bars, beat-level = 16 beats)
strobe_ramp = [SHARPY_STROBE_SLOW] * 4 + [SHARPY_STROBE_MED] * 4 + \
              [SHARPY_STROBE_FAST] * 8
bsw_ramp = [20] * 4 + [70] * 4 + [BSW_SHUT_STROBE_FAST] * 8
pre_pos = ["C", "X", "DSC", "C"] * 4
for beat in range(16):
    s, b, p = mvrs(pre_pos[beat], BLOOD_RED, dim=255,
                    gobo_b1=BSW_G1_3, prism_s=128, p1r_s=200,
                    prism_b=80, prot_b=180,
                    s_strobe=strobe_ramp[beat],
                    b_shutter=bsw_ramp[beat])
    fb, m1, m2 = pars_red(master=160)
    laser = LASER_ON if beat >= 8 else LASER_OFF
    n = nk(BLOOD_RED, pos_key=pre_pos[beat], halo="jump_fast",
           rl=laser, gl=LASER_OFF,
           t1=80 + beat * 4, t2=60 + beat * 5, t3=70 + beat * 4)
    idx = add(f"Reck-Pre{beat+1}", s, b, p, fb, m1, m2, n)
    snap(idx)


# =============================================================================
# 4. NO GOOD — Main Drop (16 bars, 64 beats)
# Aggressive peak. All fixtures. Red + white strobe. All lasers.
# 1-beat blackout accents every 4 bars.
# =============================================================================

MAIN_POS = ["C", "SL", "X", "SR", "DSC", "USC", "C", "X",
            "SL", "DSC", "CEIL", "SR", "C", "X", "DSC", "C"]

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    pos = MAIN_POS[bar % len(MAIN_POS)]
    t1v = 150 + (beat % 5) * 14
    t2v = 160 + (beat % 3) * 18
    t3v = 140 + (beat % 7) * 12

    # 1-beat blackout accent
    if bib == 3 and bar % 4 == 3:
        idx = add(f"NG-Black{bar}", *blackout_all())
        snap(idx)
        continue

    # White strobe burst on beat 1 every 2nd bar
    if bib == 0 and bar % 2 == 0:
        s, b, p = mvrs(pos, ICE_WHITE,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200,
                        gobo_b1=BSW_G1_3,
                        s_strobe=SHARPY_STROBE_FAST,
                        b_shutter=BSW_SHUT_STROBE_FAST)
        fb, m1, m2 = pars_color(ICE_WHITE, master=160)
        n = nk(ICE_WHITE, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)
    else:
        s, b, p = mvrs(pos, BLOOD_RED,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200,
                        gobo_b1=BSW_G1_3)
        fb, m1, m2 = pars_red(master=160)
        n = nk(BLOOD_RED, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)

    idx = add(f"NG-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    snap(idx)


# =============================================================================
# 5. ROLLING — Verse (16 bars, 8 smooth 2-bar sweeps)
# Dark dominates. 2 fixtures: Sharpy + NI3K. Everything else OFF.
# Single red beam stalking slowly. Menacing restraint.
# =============================================================================

for i in range(8):
    pos = ROLL_SEQ[i]
    s, b, p = solo_sharpy(pos, BLOOD_RED, dim=100, gobo=BSW_G1_3)
    fb, m1, m2 = pars_off()
    n = nk(BLOOD_RED, pos_key=pos, dim=80, halo="sync",
           t1=50, t2=60, t3=55)
    idx = add(f"Roll-{i+1}", s, b, p, fb, m1, m2, n)
    xfade(idx, bars=2)


# =============================================================================
# 6. THE HOOK — Chorus (16 bars, 32 two-beat steps)
# Aggressive rising. 3-4 fixtures. Red with strobe accents.
# BSW rejoins Sharpy. Profile on downbeat accents.
# =============================================================================

for i in range(32):
    bar = i // 2
    half = i % 2
    pos = HOOK_SEQ[bar % len(HOOK_SEQ)]
    t1v = 50 + (i % 5) * 10
    t2v = 70 + (i % 3) * 12
    t3v = 60 + (i % 7) * 7

    # Strobe accent on beat 1 every 4 bars
    if half == 0 and bar % 4 == 0:
        s, b, p = mvrs(pos, BLOOD_RED, gobo_b1=BSW_G1_3,
                        prism_s=128, p1r_s=200,
                        s_strobe=SHARPY_STROBE_MED,
                        b_shutter=70)
        fb, m1, m2 = pars_red(master=100)
    else:
        # Sharpy + BSW active, Profile dim
        sp, st = POS[pos][0], POS[pos][1]
        bp, bt = POS[pos][2], POS[pos][3]
        pp, pt = POS[pos][4], POS[pos][5]
        s = sharpy(pan=sp, tilt=st, dim=220, gobo=BSW_G1_3,
                   colormacro=SHARPY_RED)
        b = bsw(pan=bp, tilt=bt, color=BSW_RED, dim=200,
                gobo1=BSW_G1_3)
        p = profile(pan=pp, tilt=pt, dim=80, color=PROF_RED)
        fb, m1, m2 = pars_red(master=80)

    n = nk(BLOOD_RED, pos_key=pos, dim=180, halo="jump_med",
           t1=t1v, t2=t2v, t3=t3v)
    idx = add(f"Hook-{bar+1}.{half+1}", s, b, p, fb, m1, m2, n)
    snap(idx, beats=2)


# =============================================================================
# 7. DESCENT — Breakdown→Build (16 bars)
# Darkest point. Dark Phase 1: Stillness → Phase 2: Stalking → Strike
# Phase A (6 bars): Near-total blackout, single blue beam.
# Phase B (6 bars): Build from darkness. Blue→red.
# Phase C (4 bars): Strobe build, laser reveal.
# =============================================================================

# Phase A: Darkness (6 bars, bar-level)
dark_pos = ["C", "SL", "C", "SR", "C", "DSC"]
for bar in range(6):
    pos = dark_pos[bar]
    dim_val = max(20, 50 - bar * 5)  # fading darker
    if bar < 3:
        # Single BSW, deep blue, stalking
        s, b, p = solo_bsw(pos, DEEP_BLUE, dim=dim_val, gobo1=BSW_G1_3)
    else:
        # Switch to Sharpy
        s, b, p = solo_sharpy(pos, DEEP_BLUE, dim=dim_val)
    fb, m1, m2 = pars_off()
    n = nk(DEEP_BLUE, dim=max(15, 30 - bar * 3), halo="sync")
    idx = add(f"Desc-Dark{bar+1}", s, b, p, fb, m1, m2, n)
    snap(idx, beats=4)

# Phase B: Build (6 bars, 2-beat = 12 steps)
for i in range(12):
    progress = i / 11.0
    bar_in_phase = i // 2

    if progress < 0.4:
        color = DEEP_BLUE
    elif progress < 0.7:
        color = DARK_AMBER
    else:
        color = BLOOD_RED

    pos = build_pos[bar_in_phase % len(build_pos)]
    dim_val = int(30 + 225 * progress)

    # Gradual fixture addition
    if i < 3:
        s, b, p = solo_sharpy(pos, color, dim=min(dim_val, 255))
    elif i < 6:
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
                        gobo_b1=BSW_G1_3 if progress > 0.6 else 0)

    par_m = int(progress * 100) if progress > 0.5 else 0
    if par_m > 0:
        fb, m1, m2 = pars_color(color, master=par_m)
    else:
        fb, m1, m2 = pars_off()

    n = nk(color, pos_key=pos, dim=min(dim_val - 10, 200),
           halo="sync" if progress < 0.5 else "jump_slow")
    idx = add(f"Desc-B{i+1}", s, b, p, fb, m1, m2, n)
    snap(idx, beats=2)

# Phase C: Pre-drop (4 bars, beat-level = 16 beats)
strobe_ramp2 = [SHARPY_STROBE_SLOW] * 4 + [SHARPY_STROBE_MED] * 4 + \
               [SHARPY_STROBE_FAST] * 8
bsw_ramp2 = [20] * 4 + [70] * 4 + [BSW_SHUT_STROBE_FAST] * 8
pre_pos2 = ["C", "X", "DSC", "C"] * 4
for beat in range(16):
    s, b, p = mvrs(pre_pos2[beat], BLOOD_RED, dim=255,
                    gobo_b1=BSW_G1_3, prism_s=128, p1r_s=200,
                    prism_b=80, prot_b=180,
                    s_strobe=strobe_ramp2[beat],
                    b_shutter=bsw_ramp2[beat])
    fb, m1, m2 = pars_red(master=160)
    laser = LASER_ON if beat >= 8 else LASER_OFF
    n = nk(BLOOD_RED, pos_key=pre_pos2[beat], halo="jump_fast",
           rl=laser, gl=laser,
           t1=80 + beat * 4, t2=60 + beat * 5, t3=70 + beat * 4)
    idx = add(f"Desc-Pre{beat+1}", s, b, p, fb, m1, m2, n)
    snap(idx)


# =============================================================================
# 8. BLOOD MOON — Drop 2 (16 bars, 64 beats)
# Different texture: wider sweeps, RGB lasers, more gobos.
# 1-beat blackout accents.
# =============================================================================

DROP2_POS = ["C", "DSC", "SL", "X", "CEIL", "SR", "DSC", "C",
             "X", "SL", "SR", "CEIL", "DSC", "C", "USC", "X"]

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    pos = DROP2_POS[bar % len(DROP2_POS)]
    t1v = 160 + (beat % 5) * 14
    t2v = 170 + (beat % 3) * 18
    t3v = 150 + (beat % 7) * 12

    # 1-beat blackout
    if bib == 3 and bar % 4 == 3:
        idx = add(f"BM-Black{bar}", *blackout_all())
        snap(idx)
        continue

    # White strobe every 2nd bar
    if bib == 0 and bar % 2 == 0:
        s, b, p = mvrs(pos, ICE_WHITE,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200, prism_p=60,
                        gobo_b1=BSW_G1_5,
                        s_strobe=SHARPY_STROBE_FAST,
                        b_shutter=BSW_SHUT_STROBE_FAST)
        fb, m1, m2 = pars_color(ICE_WHITE, master=160)
        n = nk(ICE_WHITE, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)
    else:
        s, b, p = mvrs(pos, BLOOD_RED,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200, prism_p=60,
                        gobo_b1=BSW_G1_5)
        fb, m1, m2 = pars_red(master=160)
        n = nk(BLOOD_RED, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)

    idx = add(f"BM-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    snap(idx)


# =============================================================================
# 9. INFERNO — Final (16 bars, 64 beats)
# Aggressive overrides everything. Maximum. Last 2 bars: all white.
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    pos = CLIMAX_SEQ[bar % len(CLIMAX_SEQ)]
    t1v = 170 + (beat % 4) * 15
    t2v = 150 + (beat % 3) * 20
    t3v = 180 + (beat % 5) * 10

    # Last 2 bars: all white strobe whiteout
    if bar >= 14:
        s, b, p = mvrs(pos, ICE_WHITE,
                        prism_s=128, p1r_s=200,
                        prism_b=128, prot_b=200, prism_p=120,
                        s_strobe=SHARPY_STROBE_FAST,
                        b_shutter=BSW_SHUT_STROBE_FAST)
        fb, m1, m2 = pars_color(ICE_WHITE)
        n = nk(ICE_WHITE, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)
    else:
        # Strobe on beat 1 every bar
        if bib == 0:
            s, b, p = mvrs(pos, BLOOD_RED,
                            prism_s=128, p1r_s=200,
                            prism_b=128, prot_b=200, prism_p=80,
                            gobo_b1=BSW_G1_3,
                            s_strobe=SHARPY_STROBE_FAST,
                            b_shutter=BSW_SHUT_STROBE_FAST)
        else:
            s, b, p = mvrs(pos, BLOOD_RED,
                            prism_s=128, p1r_s=200,
                            prism_b=128, prot_b=200, prism_p=80,
                            gobo_b1=BSW_G1_3)
        fb, m1, m2 = pars_red(master=200)
        n = nk(BLOOD_RED, pos_key=pos, halo="jump_fast",
               rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
               t1=t1v, t2=t2v, t3=t3v)

    idx = add(f"Inf-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    snap(idx)


# =============================================================================
# END — snap to black
# =============================================================================

snap(0)


# =============================================================================
# STATS & VERIFICATION
# =============================================================================

total_ms = sum(fi + ho for _, (fi, ho) in steps)
main_bars = (total_ms - 22000) / bpm_to_ms(BPM, 4)

print(f"\nScene dedup: {len(scenes)} unique ({dedup_hits} reuses)")
print(f"Steps: {len(steps)}")
print(f"Duration: {total_ms/1000:.1f}s (intro 22.0s + {main_bars:.1f} bars @ {BPM} BPM)")
print(f"Target: ~197s")

sections = [
    ("Intro",       6),
    ("Drop 1",      60),
    ("Reckoning",   4 + 16 + 16),
    ("Main Drop",   64),
    ("Rolling",     8),
    ("The Hook",    32),
    ("Descent",     6 + 12 + 16),
    ("Blood Moon",  64),
    ("Inferno",     64),
    ("Blackout",    1),
]
offset = 0
for name, count in sections:
    section_ms = sum(fi + ho for _, (fi, ho) in steps[offset:offset + count])
    print(f"  {name:12s}: {count:3d} steps, {section_ms/1000:.1f}s")
    offset += count


# =============================================================================
# BUILD AND WRITE
# =============================================================================

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("No Good For Me", scene_ids, timing,
                          run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "\u25b6 NO GOOD FOR ME", "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#CC0000", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace(
    os.path.join(VENUE_DIR, "shows",
                 "Prodigy - No Good For Me (A.way Bootleg).qxw"),
    scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
