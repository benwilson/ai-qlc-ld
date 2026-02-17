#!/usr/bin/env python3
"""
Show Generator: Dimension & Karen Harding - Guardian Angel (v3)
================================================================
BPM: 174 | Duration: ~3:44 (162 bars) | Genre: Drum & Bass (euphoric/liquid)

v3 Changes from v2:
  - ALL positions now use hardware-verified focus positions from focus-positions.md
  - 7-tuple format: (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)
  - SL=DSL=USL and SR=DSR=USR (room too small for depth difference on sides)
  - Added verified specials: DJ Booth, Disco Ball, Center Ceiling
  - Cross position (X) built from verified SL/SR values
  - NI3K pan varies per position (was fixed at 128/200/etc)
  - Position sequences redesigned to showcase specials:
    * Disco Ball in bridge sweeps and verse 2 — ethereal reflections
    * Center Ceiling for dramatic upward beams in builds and triple sections
    * DJ Booth for intimate verse moments and bridge transitions
    * Cross (X) for drop accents
  - AUD (audience blinder) kept with calc values — use sparingly

Creative Direction:
  - Theme: Angels, heaven, clouds, feeling a rush
  - Palette: Ethereal & pure — white, gold, ice blue, soft teal
  - Every sound pops — beat-level scene changes in drops
  - Breakdowns: wide, sweeping, luxurious slow continuous mover sweeps
  - Movers: NEVER point behind themselves — forward only
  - Pars: Cohesive — wash for unity, gradient/pairs for texture, chase for builds
  - NI3K: Subtle atmosphere in verses (dim RGBW + halo), lasers in drops
  - Laser progression: blue only → blue+green → all 3 by final drops
  - Triple drop staircase: each drop adds prisms, gobos, wider movement, more lasers
  - Gobo staircase: none (Drop 1) → G1_3 (Drop 2) → G1_4 (T1) → G1_5 (T2/T3)

Song Structure (from allin1 analysis @ 174 BPM):
  0:00 - 0:11  intro     (8 bars)   "Ambient Intro" — pre-beat, dark, atmosphere
  0:11 - 0:44  verse     (24 bars)  "Verse 1" — vocals build, pars+movers fade in
  0:44 - 1:06  chorus    (16 bars)  "Drop 1" — first chorus, full energy, blue laser
  1:06 - 1:28  bridge    (16 bars)  "Bridge" — dreamy sweeps, gold/white, single laser
  1:28 - 2:01  chorus    (24 bars)  "Drop 2" — bigger, wider, blue+green lasers
  2:01 - 2:35  verse     (24 bars)  "Verse 2" — luxurious sweeps, green laser
  2:35 - 2:57  chorus    (16 bars)  "Triple #1" — strong, clean, blue+green lasers
  2:57 - 3:18  chorus    (16 bars)  "Triple #2" — prisms+gobos, wider, all 3 lasers
  3:18 - 3:40  chorus    (16 bars)  "Triple #3" — EVERYTHING maxed, all lasers, white blasts
  3:40 - 3:44  end       (4 bars)   "Cool Down" — fade to black
"""

import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
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
# FOCUS POSITIONS — ALL HARDWARE-VERIFIED from focus-positions.md
# Format: (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)
# =============================================================================

POS = {
    # Areas (all verified — SL=DSL=USL, SR=DSR=USR in this room)
    "C":     (153, 0,   177, 19,  0,   123, 128),  # Center
    "SL":    (170, 0,   189, 29,  50,  165, 80),   # Stage Left
    "SR":    (149, 5,   170, 23,  110, 145, 176),  # Stage Right
    "DSC":   (158, 6,   179, 27,  64,  145, 128),  # Downstage Center
    "DSL":   (170, 0,   189, 29,  50,  165, 80),   # = SL (verified)
    "DSR":   (149, 5,   170, 23,  110, 145, 176),  # = SR (verified)
    "USC":   (157, 0,   181, 21,  52,  136, 128),  # Upstage Center
    "USL":   (170, 0,   189, 29,  50,  165, 80),   # = SL (verified)
    "USR":   (149, 5,   170, 23,  110, 145, 176),  # = SR (verified)
    # Specials (all verified)
    "DJ":    (142, 3,   196, 25,  95,  107, 128),  # DJ Booth
    "DISCO": (144, 34,  170, 56,  154, 168, 128),  # Disco Ball
    "CEIL":  (158, 73,  180, 86,  91,  30,  128),  # Center Ceiling
    # Cross: Sharpy aims SR side, BSW aims SL side = crossing beams
    "X":     (149, 5,   189, 29,  0,   123, 128),
    # Audience Blinder — UNVERIFIED calc values, use sparingly
    "AUD":   (153, 15,  177, 5,   0,   155, 128),
}

# Position sequences — redesigned for specials
POS_SWEEP   = ["C", "SL", "DISCO", "SR", "DSC", "DJ", "CEIL", "DSR"]     # dreamy sweep with specials
POS_DROP    = ["C", "SL", "SR", "X", "DSC", "CEIL", "DSR", "C"]          # standard drop + specials
POS_WIDE    = ["DSL", "DSR", "USL", "USR", "X", "DISCO", "CEIL", "DSR"]  # widest + specials for T2
POS_BIG     = ["C", "DSL", "DSR", "DISCO", "CEIL", "X", "DJ", "C",      # 16 positions for T3
               "SL", "SR", "DSL", "AUD", "USR", "DISCO", "CEIL", "DSR"]

# Sweep paths for smooth breakdowns
SWEEP_LR    = ["SL", "C", "SR"]              # narrow left-right
SWEEP_DIAG  = ["USR", "C", "DSL"]            # diagonal
SWEEP_FRONT = ["USC", "C", "DSC"]            # front-back push

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
    """Build all 3 movers from position key + color. Uses 7-tuple positions."""
    sp, st, bp, bt, pp, pt, _ni = POS[pos_key]
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


def mk_ni3k_laser(rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF,
                   pos_key="C", t1=170, t2=190, t3=210):
    """NI3K lasers only — no RGBW, no halo, high movement values.
    v3: pan from position lookup."""
    ni_pan = POS[pos_key][6]
    return ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3,
                r=0, g=0, b=0, w=0, dim=0,
                halo=H_OFF, rl=rl, gl=gl, bl=bl)


def mk_ni3k_atmo(color=ICE_BLUE, dim=40, halo=H_BLU, pos_key="C",
                  t1=64, t2=64, t3=64,
                  rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF):
    """NI3K in atmosphere mode — subtle RGBW glow + halo for quiet sections.
    v3: pan from position lookup."""
    r, g, b = color
    ni_pan = POS[pos_key][6]
    return ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3,
                r=r, g=g, b=b, w=0, dim=dim,
                halo=halo, rl=rl, gl=gl, bl=bl)


# NI3K palette → halo mapping
HALO_FOR = {
    ICE_BLUE: H_BLU, PURE_WHITE: H_RGB,
    GOLD: H_YEL, SOFT_TEAL: H_CYN,
}


# =============================================================================
# BLACKOUT (always scene 0)
# =============================================================================

add_scene("Blackout", *blackout_all())


# =============================================================================
# AMBIENT INTRO — 8 bars, 4-beat steps
# Pre-beat atmosphere. Pars barely visible, fading up from black.
# Movers dark. NI3K provides subtle blue atmosphere.
# =============================================================================

for bar in range(8):
    master = bar * 5  # 0 → 35 (barely a glow)
    if master == 0:
        fb, m1, m2 = par_off()
    else:
        fb, m1, m2 = par_wash(ICE_BLUE, master=master)
    s, b, p = mkvrs("C", ICE_BLUE, dim=0)
    ni_dim = bar * 5  # 0 → 35 (very subtle glow building)
    n = mk_ni3k_atmo(ICE_BLUE, dim=ni_dim, halo=H_BLU if bar >= 2 else H_OFF,
                      pos_key="C", t1=64, t2=64, t3=64)
    idx = add_scene(f"Amb-{bar+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=4)


# =============================================================================
# VERSE 1A — 12 bars, 4-beat steps (gentle build)
# Vocals enter. Pars fade in with gradients, building from dim.
# Movers slowly appear, frosted. NI3K halo syncs to palette.
# v3: DJ Booth and CEIL in position sequence for intimate moments.
# =============================================================================

v1a_positions = ["C", "C", "DJ", "SL", "SL", "C", "SR", "SR", "C", "CEIL", "DJ", "C"]

for bar in range(12):
    c1 = ETHEREAL_3[bar % 3]
    c2 = ETHEREAL_3[(bar + 1) % 3]
    master = 30 + bar * 14  # 30 → 184 (gradual fade in)
    fb, m1, m2 = par_gradient(c1, c2, master=master)
    pos = v1a_positions[bar]
    mover_dim = min(255, bar * 18)  # 0 → 198
    s, b, p = mkvrs(pos, PURE_WHITE, dim=mover_dim, frost=180, focus=200)
    ni_dim = 30 + bar * 6  # 30 → 96 (gentle build)
    halo = HALO_FOR.get(c1, H_BLU)
    n = mk_ni3k_atmo(c1, dim=ni_dim, halo=halo, pos_key=pos, t1=64, t2=64, t3=64)
    idx = add_scene(f"V1A-{bar+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=4)


# =============================================================================
# VERSE 1B — 12 bars, 2-beat steps (building to drop)
# Pars go CRAZY during this build: gradient → pairs → chase
# Laser strobe tease in last 4 bars, mover strobe ramp in last 2
# v3: Sweep includes DISCO and CEIL for variety
# =============================================================================

v1b_positions = POS_SWEEP[:8] + POS_SWEEP[:4]  # 12 positions for 12 bars

for i in range(24):
    bar = i // 2
    half = i % 2
    c1 = ETHEREAL_4[i % 4]
    c2 = ETHEREAL_4[(i + 2) % 4]
    master = 140 + bar * 10  # 140 → 250

    if bar < 4:
        fb, m1, m2 = par_gradient(c1, c2, master=master)
    elif bar < 8:
        fb, m1, m2 = par_pairs(c1, c2, flip=(half == 1), master=master)
    else:
        fb, m1, m2 = par_chase(c1, i, master=master)

    pos = v1b_positions[bar]
    mover_dim = 180 + bar * 6  # 180 → 246
    frost_val = max(0, 160 - bar * 14)  # 160 → 6

    # Mover strobe ramp in last 2 bars of build
    if bar >= 10:
        s_str = SHARPY_STROBE_SLOW + (bar - 10) * 25
        b_str = 20 + (bar - 10) * 20
    else:
        s_str = SHARPY_OPEN
        b_str = BSW_SHUT_OPEN

    s, b, p = mkvrs(pos, c1, dim=mover_dim, frost=frost_val, focus=160,
                     s_strobe=s_str, b_shutter=b_str)

    # Laser strobe tease in last 4 bars (blue laser only)
    if bar >= 8:
        laser_spd = LASER_STROBE_SLOW + (bar - 8) * 50
        n = mk_ni3k_atmo(c1, dim=80, halo=HALO_FOR.get(c1, H_BLU),
                          pos_key=pos, t1=64, t2=64, t3=64,
                          bl=laser_spd)
    else:
        ni_dim = 60 + bar * 8  # 60 → 116
        n = mk_ni3k_atmo(c1, dim=ni_dim, halo=HALO_FOR.get(c1, H_BLU),
                          pos_key=pos, t1=64, t2=64, t3=64)

    idx = add_scene(f"V1B-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=2)


# =============================================================================
# DROP 1 — 16 bars, 1-beat steps (64 beats)
# First chorus! Full energy. Beat-synced color snaps.
# Blue laser reveal on NI3K. No gobos yet (staircase level 0).
# v3: POS_DROP includes X and CEIL for verified specials
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    c2 = ETHEREAL_4[(beat + 2) % 4]
    pos = POS_DROP[bar % len(POS_DROP)]

    # Prime-number tilt math for chaotic rotation
    t1 = 160 + (beat * 7 % 37)    # 160-196
    t2 = 175 + (beat * 11 % 29)   # 175-203
    t3 = 185 + (beat * 13 % 31)   # 185-215

    # Strobe accent on beat 1 every 4 bars — white flash
    if bib == 0 and bar % 4 == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        s, b, p = mkvrs(pos, PURE_WHITE,
                         s_strobe=SHARPY_STROBE_MED,
                         b_shutter=BSW_SHUT_STROBE_FAST)
    else:
        if (bar // 2) % 2 == 0:
            fb, m1, m2 = par_wash(c)
        else:
            fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))
        s, b, p = mkvrs(pos, c)

    n = mk_ni3k_laser(bl=LASER_ON, pos_key=pos, t1=t1, t2=t2, t3=t3)
    idx = add_scene(f"D1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# BRIDGE — 16 bars, 2-bar smooth crossfades (8 steps)
# Dreamy. Pars fade out to near-dark — movers and laser carry it.
# NI3K atmosphere mode with subtle RGBW glow matching palette.
# v3: Sweep features DISCO and DJ for ethereal variety
# =============================================================================

bridge_sweep = ["C", "SL", "DISCO", "SR", "DJ", "CEIL", "C", "DSC"]
bridge_colors = [GOLD, ICE_BLUE, PURE_WHITE, SOFT_TEAL,
                 GOLD, ICE_BLUE, PURE_WHITE, SOFT_TEAL]

for i in range(8):
    c = bridge_colors[i]
    pos = bridge_sweep[i]
    master = max(10, 80 - i * 10)  # 80 → 10 (fading to near-dark)
    fb, m1, m2 = par_wash(c, master=master)
    s, b, p = mkvrs(pos, c, dim=180, frost=200, focus=200)
    halo = HALO_FOR.get(c, H_BLU)
    n = mk_ni3k_atmo(c, dim=60, halo=halo,
                      pos_key=pos, t1=64, t2=64, t3=64,
                      bl=LASER_ON)  # blue laser sustains
    idx = add_scene(f"Br-{i+1}", s, b, p, fb, m1, m2, n)
    smooth_step(idx, bars=2)


# =============================================================================
# DROP 2 — 24 bars, 1-beat steps (96 beats)
# Bigger than Drop 1. Wider positions. Color changes every beat.
# BSW gobo G1_3 for beam texture, blue + green lasers.
# v3: POS_DROP + POS_WIDE include specials
# =============================================================================

drop2_positions = POS_DROP + POS_WIDE + POS_DROP  # 24 positions for 24 bars

for beat in range(96):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    c2 = ETHEREAL_4[(beat + 2) % 4]
    pos = drop2_positions[bar % len(drop2_positions)]

    # Prime tilt math
    t1 = 160 + (beat * 7 % 41)    # 160-200
    t2 = 170 + (beat * 11 % 37)   # 170-206
    t3 = 180 + (beat * 13 % 29)   # 180-208

    # Strobe accent on beat 1 every 4 bars — white solid hit
    if bib == 0 and bar % 4 == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        s, b, p = mkvrs(pos, PURE_WHITE,
                         gobo_b=BSW_G1_3,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)
        n = mk_ni3k_laser(bl=LASER_ON, gl=LASER_ON,
                           pos_key=pos, t1=t1, t2=t2, t3=t3)
    else:
        pat = (bar // 4) % 3
        if pat == 0:
            fb, m1, m2 = par_wash(c)
        elif pat == 1:
            fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))
        else:
            fb, m1, m2 = par_chase(c, beat)
        s, b, p = mkvrs(pos, c, gobo_b=BSW_G1_3)
        n = mk_ni3k_laser(bl=LASER_ON, gl=LASER_ON,
                           pos_key=pos, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"D2-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# VERSE 2A — 16 bars, 2-bar smooth crossfades (8 steps)
# Luxurious sweeps. Pars nearly off — whisper of color.
# NI3K atmosphere mode with green tint, halo matching palette.
# v3: Sweep includes DISCO and DJ for ethereal variety
# =============================================================================

v2a_sweep = ["C", "SR", "DISCO", "SL", "DJ", "CEIL", "DSC", "C"]
v2a_colors = [ICE_BLUE, SOFT_TEAL, PURE_WHITE, GOLD,
              ICE_BLUE, SOFT_TEAL, PURE_WHITE, GOLD]

for i in range(8):
    c = v2a_colors[i]
    pos = v2a_sweep[i]
    master = 15 + i * 5  # 15 → 50 (whisper-level, slowly returning)
    fb, m1, m2 = par_wash(c, master=master)
    s, b, p = mkvrs(pos, c, dim=160, frost=200, focus=200)
    halo = HALO_FOR.get(c, H_CYN)
    n = mk_ni3k_atmo(c, dim=50, halo=halo,
                      pos_key=pos, t1=64, t2=64, t3=64,
                      gl=LASER_ON)
    idx = add_scene(f"V2A-{i+1}", s, b, p, fb, m1, m2, n)
    smooth_step(idx, bars=2)


# =============================================================================
# VERSE 2B — 8 bars, 2-beat steps (16 steps)
# Building back up HARD. gradient → pairs → chase. Master 50 → 253.
# Laser strobe tease (green → green+blue), mover strobe ramp
# v3: POS_SWEEP for verified positions
# =============================================================================

v2b_positions = POS_SWEEP  # 8 positions for 8 bars

for i in range(16):
    bar = i // 2
    half = i % 2
    c1 = ETHEREAL_4[i % 4]
    c2 = ETHEREAL_4[(i + 2) % 4]
    master = 50 + bar * 29  # 50 → 253

    if bar < 3:
        fb, m1, m2 = par_gradient(c1, c2, master=master)
    elif bar < 6:
        fb, m1, m2 = par_pairs(c1, c2, flip=(half == 1), master=master)
    else:
        fb, m1, m2 = par_chase(c1, i, master=master)

    pos = v2b_positions[bar % len(v2b_positions)]
    mover_dim = 180 + bar * 9  # 180 → 243
    frost_val = max(0, 150 - bar * 20)  # 150 → 10

    # Mover strobe ramp in last 2 bars
    if bar >= 6:
        s_str = SHARPY_STROBE_SLOW + (bar - 6) * 25
        b_str = 20 + (bar - 6) * 20
    else:
        s_str = SHARPY_OPEN
        b_str = BSW_SHUT_OPEN

    s, b, p = mkvrs(pos, c1, dim=mover_dim, frost=frost_val, focus=150,
                     s_strobe=s_str, b_shutter=b_str)

    # Laser strobe tease — green sustains, blue strobes in
    if bar >= 4:
        bl_spd = LASER_STROBE_SLOW + (bar - 4) * 50
        n = mk_ni3k_atmo(c1, dim=80, halo=HALO_FOR.get(c1, H_CYN),
                          pos_key=pos, t1=64, t2=64, t3=64,
                          gl=LASER_ON, bl=bl_spd)
    else:
        n = mk_ni3k_atmo(c1, dim=60, halo=HALO_FOR.get(c1, H_CYN),
                          pos_key=pos, t1=64, t2=64, t3=64,
                          gl=LASER_ON)

    idx = add_scene(f"V2B-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=2)


# =============================================================================
# TRIPLE #1 — 16 bars, 1-beat (64 beats)
# Staircase Level 1: Strong but not maxed. Clean beams. No prisms.
# BSW gobo G1_4 for beam texture, blue + green lasers.
# v3: POS_DROP with verified specials
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    pos = POS_DROP[bar % len(POS_DROP)]

    # Prime tilt math
    t1 = 165 + (beat * 7 % 31)    # 165-195
    t2 = 178 + (beat * 11 % 23)   # 178-200
    t3 = 188 + (beat * 13 % 37)   # 188-224

    # Alternate wash and pairs every 2 bars
    if (bar // 2) % 2 == 0:
        fb, m1, m2 = par_wash(c)
    else:
        c2 = ETHEREAL_4[(beat + 2) % 4]
        fb, m1, m2 = par_pairs(c, c2, flip=(bib % 2 == 1))

    s, b, p = mkvrs(pos, c, gobo_b=BSW_G1_4)
    n = mk_ni3k_laser(bl=LASER_ON, gl=LASER_ON,
                       pos_key=pos, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"T1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# TRIPLE #2 — 16 bars, 1-beat (64 beats)
# Staircase Level 2: Add prisms + gobos. Wider positions. All 3 lasers.
# BSW gobo G1_5, rotating par patterns, strobe accents.
# v3: POS_WIDE includes DISCO and CEIL
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    c2 = ETHEREAL_4[(beat + 2) % 4]
    pos = POS_WIDE[bar % len(POS_WIDE)]

    # Prime tilt math — wider range
    t1 = 170 + (beat * 7 % 43)    # 170-212
    t2 = 180 + (beat * 11 % 31)   # 180-210
    t3 = 190 + (beat * 13 % 47)   # 190-236

    # Strobe accent on beat 1 every 4 bars — white flash with prisms
    if bib == 0 and bar % 4 == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        s, b, p = mkvrs(pos, PURE_WHITE,
                         prism_s=128, p1r_s=200,
                         prism_b=80, prot_b=180, prism_p=60,
                         gobo_b=BSW_G1_5,
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
                         prism_b=80, prot_b=180, prism_p=60,
                         gobo_b=BSW_G1_5)

    n = mk_ni3k_laser(rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
                       pos_key=pos, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"T2-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# TRIPLE #3 — 16 bars, 1-beat (64 beats)
# Staircase Level 3: EVERYTHING MAXED. Full blowout.
# White downbeat blast every bar, BSW gobo G1_5, AUD position in mix,
# dual prisms, 16-position cycle, all lasers, fastest rotation.
# v3: POS_BIG includes DISCO, CEIL, DJ, X, AUD
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    c = ETHEREAL_4[beat % 4]
    pos = POS_BIG[bar % len(POS_BIG)]

    # Prime tilt math — maximum range and chaos
    t1 = 175 + (beat * 7 % 47)    # 175-221
    t2 = 185 + (beat * 11 % 37)   # 185-221
    t3 = 195 + (beat * 13 % 53)   # 195-247

    # WHITE DOWNBEAT BLAST on beat 1 of every bar
    if bib == 0:
        fb, m1, m2 = par_wash(PURE_WHITE)
        # Every bar gets white blast; every 2 bars adds strobe
        if bar % 2 == 0:
            s_str = SHARPY_STROBE_FAST
            b_str = BSW_SHUT_STROBE_FAST
        else:
            s_str = SHARPY_OPEN
            b_str = BSW_SHUT_OPEN
        s, b, p = mkvrs(pos, PURE_WHITE,
                         prism_s=128, p1r_s=200,
                         prism2_s=128, p2r_s=200,
                         prism_b=128, prot_b=200, prism_p=120,
                         gobo_b=BSW_G1_5,
                         s_strobe=s_str,
                         b_shutter=b_str)
    else:
        # Chase on every non-blast beat — maximum par activity
        fb, m1, m2 = par_chase(c, beat)
        s, b, p = mkvrs(pos, c,
                         prism_s=128, p1r_s=200,
                         prism2_s=128, p2r_s=200,
                         prism_b=128, prot_b=200, prism_p=120,
                         gobo_b=BSW_G1_5)

    n = mk_ni3k_laser(rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
                       pos_key=pos, t1=t1, t2=t2, t3=t3)

    idx = add_scene(f"T3-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# COOL DOWN — 4 bars, 1-bar smooth crossfades (4 steps)
# Breathing-out moment. Movers converge to center, frost up, dim down.
# Pars fade. NI3K returns to soft atmosphere mode. Lasers off.
# =============================================================================

cooldown_colors = [ICE_BLUE, PURE_WHITE, SOFT_TEAL, ICE_BLUE]
cooldown_pos    = ["C", "C", "C", "C"]

for i in range(4):
    c = cooldown_colors[i]
    pos = cooldown_pos[i]
    # Everything fading
    mover_dim = max(0, 120 - i * 35)   # 120 → 15
    par_master = max(0, 100 - i * 30)   # 100 → 10
    frost_val = 150 + i * 25            # 150 → 225
    ni_dim = max(0, 50 - i * 15)        # 50 → 5

    fb, m1, m2 = par_wash(c, master=par_master)
    s, b, p = mkvrs(pos, c, dim=mover_dim, frost=frost_val, focus=200)
    halo = HALO_FOR.get(c, H_BLU)
    n = mk_ni3k_atmo(c, dim=ni_dim, halo=halo if ni_dim > 0 else H_OFF,
                      pos_key=pos, t1=64, t2=64, t3=64)

    idx = add_scene(f"Cool-{i+1}", s, b, p, fb, m1, m2, n)
    smooth_step(idx, bars=1)

# Final blackout
beat_step(0, beats=4)


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
    ("Cool Down",  4),
    ("Blackout",   1),
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

write_workspace(os.path.join(VENUE_DIR, "shows", "Dimension & Karen Harding - Guardian Angel.qxw"),
                scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
