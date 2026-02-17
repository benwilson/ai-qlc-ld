#!/usr/bin/env python3
"""
Show Generator: Tvboo - Fixin's (Fire & Ice Edition) (v2)
==========================================================
BPM: 144 | Duration: ~3:25 | Genre: Dirty bass / riddim

v2 Changes:
  - ALL positions now use hardware-verified focus positions from focus-positions.md
  - 7-tuple format: (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)
  - Replaced hardcoded positions (many unsafe: BSW pan=210 behind, Sharpy pan=80 behind,
    Profile pan=220 outside safe range, tilt=170 outside safe range)
  - NI3K pan now varies per position via pos_key parameter
  - Position sequences redesigned using verified positions (DSL/DSR/X/CEIL/DISCO/AUD etc.)

Creative Direction:
  - FIRE & ICE palette: red/orange/amber vs blue/cyan/white
  - Every beat gets a par change — flashing constantly
  - Full send strobes on ALL fixtures during drops
  - Lasers: strobe during builds, solid ON during drops
  - NI3K tilts: full chaos (auto-rotating) whenever beat is going, positioned on breakdowns
  - Back wall movers (Sharpy + BSW) aimed towards front/audience
  - Front mover (Profile) aimed towards back wall
  - Sweeping movements on breakdowns, fast repositioning on drops
  - Go BIG on drops — prisms, gobos, strobes, lasers, everything

Song Structure (from allin1 analysis, corrected to 144 BPM):
  0:00 - 0:26  verse     (16 bars)  "Intro/Build" — ice establishing, fire creeping in
  0:26 - 0:53  chorus    (16 bars)  "DROP 1" — FULL SEND fire & ice alternating
  0:53 - 1:06  chorus    (8 bars)   "DROP 1 cont" — keep hammering
  1:06 - 1:19  inst      (8 bars)   "Breakdown 1" — sweeps, ice only, movers slow
  1:19 - 1:34  chorus    (8 bars)   "DROP 2" — fire dominant, different positions
  1:34 - 1:59  verse     (16 bars)  "Breakdown 2" — ice sweeps, laser strobe tease
  1:59 - 2:13  verse     (8 bars)   "Build" — accelerating into drop 3
  2:13 - 2:26  chorus    (8 bars)   "DROP 3" — biggest drop, all prisms, all lasers
  2:26 - 2:39  chorus    (8 bars)   "DROP 3 cont" — sustained mayhem
  2:39 - 2:52  chorus    (8 bars)   "FINAL DROP" — maximum everything
  2:52 - 3:07  outro     (8 bars)   "Cool down" — ice fade
  3:07 - 3:25  outro     (12 bars)  "Fade out" — to black
"""

import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

BPM = 144
BEAT_MS = bpm_to_ms(BPM, 1)  # ~417ms
BAR_MS = bpm_to_ms(BPM, 4)   # ~1667ms

# =============================================================================
# FIRE & ICE PALETTE
# =============================================================================

# Fire colors (RGB for pars)
FIRE_RED     = (255, 0, 0)
FIRE_ORANGE  = (255, 80, 0)
FIRE_AMBER   = (255, 140, 0)
FIRE_WHITE   = (255, 200, 120)  # warm white

# Ice colors (RGB for pars)
ICE_BLUE     = (0, 40, 255)
ICE_CYAN     = (0, 255, 200)
ICE_WHITE    = (180, 220, 255)  # cool white
ICE_TEAL     = (0, 200, 180)

# Combined rotation sets
FIRE_COLORS = [FIRE_RED, FIRE_ORANGE, FIRE_AMBER, FIRE_WHITE]
ICE_COLORS  = [ICE_BLUE, ICE_CYAN, ICE_WHITE, ICE_TEAL]
ALL_COLORS  = [FIRE_RED, ICE_BLUE, FIRE_ORANGE, ICE_CYAN, FIRE_AMBER, ICE_WHITE]

# BSW color wheel mapping
BSW_FIRE = [BSW_RED, BSW_ORANGE, BSW_YELLOW, BSW_WHITE]
BSW_ICE  = [BSW_BLUE, BSW_TEAL, BSW_WHITE, BSW_TEAL]

# Sharpy color macro mapping
SHARPY_FIRE = [SHARPY_RED, SHARPY_ORANGE, SHARPY_YELLOW, SHARPY_WHITE]
SHARPY_ICE  = [SHARPY_BLUE, SHARPY_TEAL, SHARPY_WHITE, SHARPY_TEAL]

# Profile color wheel mapping
PROF_FIRE = [PROF_RED, PROF_ORANGE, PROF_YELLOW, PROF_WHITE]
PROF_ICE  = [PROF_BLUE, PROF_TEAL, PROF_WHITE, PROF_TEAL]

# NI3K halo mapping
HALO_FIRE = [H_RED, H_RED, H_YEL, H_RGB]
HALO_ICE  = [H_BLU, H_CYN, H_RGB, H_CYN]

# =============================================================================
# MOVER POSITIONS — ALL HARDWARE-VERIFIED from focus-positions.md
# Format: (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)
# =============================================================================

POS = {
    # Areas (all verified)
    "C":     (153, 0,   177, 19,  0,   123, 128),  # Center
    "SL":    (170, 0,   189, 29,  50,  165, 80),   # Stage Left
    "SR":    (149, 5,   170, 23,  110, 145, 176),  # Stage Right
    "DSC":   (158, 6,   179, 27,  64,  145, 128),  # Downstage Center
    "DSL":   (170, 0,   189, 29,  50,  165, 80),   # = SL (verified)
    "DSR":   (149, 5,   170, 23,  110, 145, 176),  # = SR (verified)
    "USC":   (157, 0,   181, 21,  52,  136, 128),  # Upstage Center
    # Specials (all verified)
    "DJ":    (142, 3,   196, 25,  95,  107, 128),  # DJ Booth
    "DISCO": (144, 34,  170, 56,  154, 168, 128),  # Disco Ball
    "CEIL":  (158, 73,  180, 86,  91,  30,  128),  # Center Ceiling
    # Cross: Sharpy aims SR side, BSW aims SL side = crossing beams
    "X":     (149, 5,   189, 29,  0,   123, 128),
    # Audience Blinder — UNVERIFIED calc values, use sparingly
    "AUD":   (153, 15,  177, 5,   0,   155, 128),
}

# Position sequences for different energies — using verified positions
POS_DROP   = ["C", "DSL", "DSR", "X", "AUD", "CEIL", "SL", "C"]
POS_SWEEP  = ["SL", "C", "SR", "C"]    # smooth sweeps for breakdowns
POS_BIG    = ["C", "X", "CEIL", "AUD", "DSL", "DSR", "SR", "DISCO",
              "X", "SL", "AUD", "CEIL", "C", "DSL", "DSR", "X"]

# =============================================================================
# SCENE BUILDING WITH DEDUP
# =============================================================================

folder = "Fixin's"
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


def smooth_step(scene_idx, beats=4):
    """Add chaser step with smooth crossfade over the full duration."""
    ms = bpm_to_ms(BPM, beats)
    steps.append((scene_idx, (ms, 0)))


# =============================================================================
# FIXTURE BUILDERS
# =============================================================================

def mk_movers(pos_key, palette="ice", color_idx=0, dim=255,
              frost=0, focus=128,
              prism_s=0, p1r_s=0, prism2_s=0, p2r_s=0,
              prism_b=0, prot_b=0, prism_p=0,
              gobo_b=0, gobo_p=0,
              s_strobe=SHARPY_OPEN, b_shutter=BSW_SHUT_OPEN):
    """Build all 3 movers from position key + fire/ice palette. Uses 7-tuple positions."""
    sp, st, bp, bt, pp, pt, _ni = POS[pos_key]
    bsw_colors = BSW_FIRE if palette == "fire" else BSW_ICE
    sharpy_colors = SHARPY_FIRE if palette == "fire" else SHARPY_ICE
    prof_colors = PROF_FIRE if palette == "fire" else PROF_ICE
    bsw_c = bsw_colors[color_idx % len(bsw_colors)]
    sharpy_c = sharpy_colors[color_idx % len(sharpy_colors)]
    prof_c = prof_colors[color_idx % len(prof_colors)]
    s = sharpy(pan=sp, tilt=st, strobe=s_strobe, dim=dim,
               frost=frost, focus=focus,
               prism1=prism_s, p1r=p1r_s, prism2=prism2_s, p2r=p2r_s,
               colormacro=sharpy_c)
    b = bsw(pan=bp, tilt=bt, color=bsw_c, shutter=b_shutter,
            dim=dim, prism=prism_b, prot=prot_b, focus=focus,
            gobo1=gobo_b)
    p = profile(pan=pp, tilt=pt, dim=dim, prism=prism_p, focus=focus,
                gobo=gobo_p, color=prof_c)
    return s, b, p


def par_chase_fire_ice(beat_idx, master=255):
    """4BAR: one par lit per beat cycling fire/ice alternating. Missyees alternate."""
    # Even beats = fire, odd beats = ice
    if beat_idx % 2 == 0:
        c = FIRE_COLORS[beat_idx % len(FIRE_COLORS)]
    else:
        c = ICE_COLORS[beat_idx % len(ICE_COLORS)]
    r, g, b = c
    v = [(0, 0, 0)] * 4
    v[beat_idx % 4] = (r, g, b)
    fb = fourbar(v[0][0], v[0][1], v[0][2], v[1][0], v[1][1], v[1][2],
                 v[2][0], v[2][1], v[2][2], v[3][0], v[3][1], v[3][2],
                 master=master)
    if beat_idx % 2 == 0:
        return fb, miss1(r, g, b, master=master), miss2(0, 0, 0, master=0)
    else:
        return fb, miss1(0, 0, 0, master=0), miss2(r, g, b, master=master)


def par_alternating(beat_idx, c1, c2, master=255):
    """4BAR: alternates between two colors every beat. Both missyees active."""
    c = c1 if beat_idx % 2 == 0 else c2
    r, g, b = c
    # 4BAR: all pars same color, flashing
    fb = fourbar_solid(r, g, b, master=master)
    m1 = miss1(*c1, master=master) if beat_idx % 2 == 0 else miss1(*c2, master=master)
    m2 = miss2(*c2, master=master) if beat_idx % 2 == 0 else miss2(*c1, master=master)
    return fb, m1, m2


def par_pairs_fi(beat_idx, master=255):
    """4BAR: fire on P1+P3, ice on P2+P4, flipping each beat."""
    fc = FIRE_COLORS[beat_idx % len(FIRE_COLORS)]
    ic = ICE_COLORS[beat_idx % len(ICE_COLORS)]
    if beat_idx % 2 == 0:
        fb = fourbar_pairs(fc[0], fc[1], fc[2], ic[0], ic[1], ic[2], master=master)
        m1 = miss1(*fc, master=master)
        m2 = miss2(*ic, master=master)
    else:
        fb = fourbar_pairs(ic[0], ic[1], ic[2], fc[0], fc[1], fc[2], master=master)
        m1 = miss1(*ic, master=master)
        m2 = miss2(*fc, master=master)
    return fb, m1, m2


def par_solid(color, master=255, strobe=0):
    """All pars same color for impact hits."""
    r, g, b = color
    return (fourbar_solid(r, g, b, master=master, strobe=strobe),
            miss1(r, g, b, master=master, strobe=strobe),
            miss2(r, g, b, master=master, strobe=strobe))


def mk_ni(palette="ice", color_idx=0, dim=255, halo_mode="sync",
           rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF,
           t1=64, t2=64, t3=64, strobe=0, pos_key="C"):
    """Build NI3K with fire/ice palette matching. Uses position lookup for pan."""
    if palette == "fire":
        colors = FIRE_COLORS
        halos = HALO_FIRE
    else:
        colors = ICE_COLORS
        halos = HALO_ICE
    c = colors[color_idx % len(colors)]
    r, g, b = c
    halo_map = {"sync": halos[color_idx % len(halos)],
                "jump_fast": H_JUMP_FAST, "jump_med": H_JUMP_MED,
                "jump_slow": H_JUMP_SLOW, "off": H_OFF}
    halo = halo_map.get(halo_mode, H_RGB)
    ni_pan = POS[pos_key][6]
    return ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3, r=r, g=g, b=b,
                halo=halo, dim=dim, strobe=strobe, rl=rl, gl=gl, bl=bl)


# =============================================================================
# BLACKOUT (always scene 0)
# =============================================================================

add_scene("Blackout", *blackout_all())


# =============================================================================
# INTRO/BUILD — 16 bars (64 beats)
# Ice establishing, fire creeping in. Pars every 2 beats building to every beat.
# Movers sweeping slowly. NI3K tilts starting to rotate.
# Laser strobe teasing in last 4 bars.
# =============================================================================

for bar in range(16):
    # First 8 bars: pars every 2 beats (ice dominant)
    if bar < 8:
        for half in range(2):
            beat = bar * 4 + half * 2
            ci = beat // 2
            master = 80 + bar * 18
            if bar < 6:
                fb, m1, m2 = par_pairs_fi(ci, master=master)
                pal = "ice"
            else:
                # Fire starts creeping in
                fb, m1, m2 = par_chase_fire_ice(ci, master=master)
                pal = "fire" if half == 1 else "ice"

            pos = POS_SWEEP[bar % len(POS_SWEEP)]
            s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=40 + bar * 20,
                                frost=200 - bar * 15, focus=180)
            t_base = 64
            n = mk_ni(palette="ice", color_idx=ci, dim=40 + bar * 20,
                      halo_mode="sync", t1=t_base, t2=t_base, t3=t_base, pos_key=pos)
            idx = add_scene(f"Intro-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
            beat_step(idx, beats=2)
    else:
        # Bars 9-16: pars every beat, building intensity
        for bib in range(4):
            beat = bar * 4 + bib
            ci = beat
            master = 160 + (bar - 8) * 12
            fb, m1, m2 = par_chase_fire_ice(ci, master=master)

            pos = POS_SWEEP[(bar // 2) % len(POS_SWEEP)]
            pal = "fire" if bib % 2 == 0 else "ice"
            dim_val = 80 + (bar - 8) * 20
            s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=dim_val,
                                frost=100 - (bar - 8) * 10)

            # NI3K tilts start rotating in last 4 bars
            if bar >= 12:
                t1 = 140 + (bib % 3) * 10
                t2 = 150 + (bib % 2) * 15
                t3 = 135 + (bib % 4) * 8
                laser_r = LASER_STROBE_SLOW if bar >= 14 else LASER_OFF
                laser_g = LASER_OFF
                laser_b = LASER_STROBE_SLOW if bar >= 15 else LASER_OFF
            else:
                t1 = 64; t2 = 64; t3 = 64
                laser_r = LASER_OFF; laser_g = LASER_OFF; laser_b = LASER_OFF

            n = mk_ni(palette=pal, color_idx=ci, dim=dim_val,
                      halo_mode="sync",
                      t1=t1, t2=t2, t3=t3,
                      rl=laser_r, gl=laser_g, bl=laser_b, pos_key=pos)
            idx = add_scene(f"Intro-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
            beat_step(idx, beats=1)


# =============================================================================
# DROP 1 — 16 bars (64 beats) — FULL SEND
# Fire & ice alternating every beat. All strobes. Lasers ON.
# Movers repositioning every bar. Prisms on. NI3K tilts rotating.
# =============================================================================

for beat in range(64):
    bar = beat // 4
    bib = beat % 4
    ci = beat
    pal = "fire" if beat % 2 == 0 else "ice"
    pos = POS_DROP[bar % len(POS_DROP)]

    # Pars: chase pattern, full brightness
    fb, m1, m2 = par_chase_fire_ice(beat, master=255)

    # Movers: strobe on every beat, prisms spinning
    s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=255,
                         prism_s=128, p1r_s=200, prism_b=80, prot_b=180, prism_p=60,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)

    # NI3K: full chaos tilts, lasers ON, jump halo
    t1 = 140 + (beat % 5) * 12
    t2 = 155 + (beat % 3) * 15
    t3 = 130 + (beat % 7) * 10
    n = mk_ni(palette=pal, color_idx=ci, dim=255,
              halo_mode="jump_fast",
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
              t1=t1, t2=t2, t3=t3, pos_key=pos)

    idx = add_scene(f"Drop1-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# DROP 1 CONTINUED — 8 bars (32 beats) — keep hammering
# Same energy, switch to alternating solid hits for variety
# =============================================================================

for beat in range(32):
    bar = beat // 4
    bib = beat % 4
    ci = beat
    pal = "fire" if beat % 2 == 0 else "ice"
    pos = POS_DROP[(bar + 4) % len(POS_DROP)]  # offset position sequence

    # Alternating solid hits — full par walls of fire then ice
    if beat % 2 == 0:
        fb, m1, m2 = par_solid(FIRE_COLORS[beat % len(FIRE_COLORS)])
    else:
        fb, m1, m2 = par_solid(ICE_COLORS[beat % len(ICE_COLORS)])

    # Movers with different gobo for variety
    s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=255,
                         prism_s=128, p1r_s=200,
                         prism2_s=128, p2r_s=200,  # double prism!
                         prism_b=128, prot_b=200, prism_p=80,
                         gobo_b=BSW_G1_3, gobo_p=0,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)

    t1 = 150 + (beat % 4) * 10
    t2 = 140 + (beat % 3) * 18
    t3 = 160 + (beat % 5) * 8
    n = mk_ni(palette=pal, color_idx=ci, dim=255,
              halo_mode="jump_fast",
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
              t1=t1, t2=t2, t3=t3, pos_key=pos)

    idx = add_scene(f"Drop1B-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# BREAKDOWN 1 — 8 bars (32 beats) — sweeps, ice only
# Movers slow sweep through positions. Frosted beams. Pars every 2 beats.
# Kill lasers. NI3K tilts positioned (not rotating). Smooth transitions.
# =============================================================================

for bar in range(8):
    for half in range(2):
        beat = bar * 4 + half * 2
        ci = beat // 2
        pos = POS_SWEEP[bar % len(POS_SWEEP)]

        # Pars: ice palette, pairs pattern, softer
        ic = ICE_COLORS[ci % len(ICE_COLORS)]
        fb = fourbar_pairs(ic[0], ic[1], ic[2], 0, 20, 80, master=140 + bar * 10)
        m1 = miss1(*ic, master=120 + bar * 12)
        m2 = miss2(0, 20, 80, master=120 + bar * 12)

        # Movers: frosted, slow, ice only
        s, b, p = mk_movers(pos, palette="ice", color_idx=ci,
                             dim=120 + bar * 15, frost=180, focus=200)

        # NI3K: positioned, soft halo, no lasers
        n = mk_ni(palette="ice", color_idx=ci, dim=80 + bar * 15,
                  halo_mode="sync", t1=64, t2=64, t3=64, pos_key=pos)

        idx = add_scene(f"BD1-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
        smooth_step(idx, beats=2)


# =============================================================================
# DROP 2 — 8 bars (32 beats) — fire dominant
# Different positions from Drop 1. More fire, less ice.
# Full strobes, lasers on, prisms.
# =============================================================================

for beat in range(32):
    bar = beat // 4
    bib = beat % 4
    ci = beat
    # Fire dominant: 3 fire beats to 1 ice
    pal = "ice" if beat % 4 == 3 else "fire"
    pos = POS_BIG[bar % len(POS_BIG)]

    # Pars: mostly fire with ice accents
    if beat % 4 == 3:
        fb, m1, m2 = par_solid(ICE_COLORS[beat % len(ICE_COLORS)])
    else:
        fb, m1, m2 = par_chase_fire_ice(beat, master=255)

    s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=255,
                         prism_s=128, p1r_s=200, prism_b=128, prot_b=200,
                         prism_p=80,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)

    t1 = 145 + (beat % 6) * 10
    t2 = 135 + (beat % 4) * 15
    t3 = 155 + (beat % 5) * 8
    n = mk_ni(palette=pal, color_idx=ci, dim=255,
              halo_mode="jump_fast",
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
              t1=t1, t2=t2, t3=t3, pos_key=pos)

    idx = add_scene(f"Drop2-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# BREAKDOWN 2 — 16 bars (64 beats) — ice sweeps with laser strobe tease
# First 8 bars: slow ice wash, pars every 2 beats
# Last 8 bars: building tension, laser strobes increasing, pars every beat
# =============================================================================

# First 8 bars: slow and cold
for bar in range(8):
    for half in range(2):
        beat = bar * 4 + half * 2
        ci = beat // 2
        pos = POS_SWEEP[bar % len(POS_SWEEP)]

        ic = ICE_COLORS[ci % len(ICE_COLORS)]
        fb = fourbar_gradient(ic[0], ic[1], ic[2], 0, 0, 60, master=100 + bar * 15)
        m1 = miss1(*ic, master=80 + bar * 15)
        m2 = miss2(*ICE_COLORS[(ci + 1) % len(ICE_COLORS)], master=80 + bar * 15)

        s, b, p = mk_movers(pos, palette="ice", color_idx=ci,
                             dim=80 + bar * 18, frost=200 - bar * 10, focus=200)

        # Laser strobe tease in bars 5-8
        if bar >= 4:
            laser_spd = LASER_STROBE_SLOW + (bar - 4) * 40
            rl = laser_spd if bar >= 6 else LASER_OFF
            bl = laser_spd
            gl = LASER_OFF
        else:
            rl = LASER_OFF; gl = LASER_OFF; bl = LASER_OFF

        n = mk_ni(palette="ice", color_idx=ci, dim=60 + bar * 18,
                  halo_mode="sync", t1=64, t2=64, t3=64,
                  rl=rl, gl=gl, bl=bl, pos_key=pos)

        idx = add_scene(f"BD2-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
        smooth_step(idx, beats=2)

# Last 8 bars: building — pars every beat, laser strobes increasing
for bar in range(8):
    for bib in range(4):
        beat = bar * 4 + bib
        ci = beat
        pos = POS_SWEEP[(bar // 2) % len(POS_SWEEP)]

        # Pars: fire starting to creep back in
        if bar < 4:
            fb, m1, m2 = par_pairs_fi(beat, master=160 + bar * 20)
        else:
            fb, m1, m2 = par_chase_fire_ice(beat, master=200 + (bar - 4) * 14)

        pal = "ice" if bar < 4 else ("fire" if bib % 2 == 0 else "ice")
        dim_val = 120 + bar * 16
        # Movers: gradually de-frosting, faster strobe buildup in last 4 bars
        if bar >= 6:
            s_str = SHARPY_STROBE_SLOW + (bar - 6) * 30
            b_str = 20 + (bar - 6) * 25
        else:
            s_str = SHARPY_OPEN
            b_str = BSW_SHUT_OPEN

        s, b, p = mk_movers(pos, palette=pal, color_idx=ci,
                             dim=dim_val, frost=120 - bar * 15,
                             s_strobe=s_str, b_shutter=b_str)

        # NI3K tilts start rotating again, laser strobe accelerating
        if bar >= 4:
            t1 = 130 + (bib % 3) * 12
            t2 = 145 + (bib % 2) * 15
            t3 = 138 + (bib % 4) * 10
            laser_spd = LASER_STROBE_SLOW + bar * 25
            rl = laser_spd; bl = laser_spd
            gl = laser_spd if bar >= 6 else LASER_OFF
        else:
            t1 = 64; t2 = 64; t3 = 64
            rl = LASER_STROBE_SLOW; bl = LASER_STROBE_SLOW; gl = LASER_OFF

        n = mk_ni(palette=pal, color_idx=ci, dim=dim_val,
                  halo_mode="sync" if bar < 4 else "jump_slow",
                  t1=t1, t2=t2, t3=t3,
                  rl=rl, gl=gl, bl=bl, pos_key=pos)

        idx = add_scene(f"Build-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
        beat_step(idx, beats=1)


# =============================================================================
# DROP 3 — 8 bars (32 beats) — BIGGEST DROP
# All prisms on all movers, all lasers, all strobes.
# Double prism on sharpy. BSW gobos. Widest movements.
# =============================================================================

for beat in range(32):
    bar = beat // 4
    bib = beat % 4
    ci = beat
    pal = "fire" if beat % 2 == 0 else "ice"
    pos = POS_BIG[beat % len(POS_BIG)]  # change position EVERY BEAT

    # Pars: solid walls alternating fire/ice
    if beat % 2 == 0:
        fb, m1, m2 = par_solid(FIRE_COLORS[beat % len(FIRE_COLORS)], strobe=0)
    else:
        fb, m1, m2 = par_solid(ICE_COLORS[beat % len(ICE_COLORS)], strobe=0)

    # Movers: everything cranked
    s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=255,
                         prism_s=128, p1r_s=200,
                         prism2_s=128, p2r_s=200,  # double prism sharpy
                         prism_b=128, prot_b=200, prism_p=120,
                         gobo_b=BSW_G1_4, gobo_p=0,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)

    t1 = 140 + (beat * 7 % 50)
    t2 = 160 + (beat * 11 % 40)
    t3 = 130 + (beat * 13 % 45)
    n = mk_ni(palette=pal, color_idx=ci, dim=255,
              halo_mode="jump_fast",
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
              t1=t1, t2=t2, t3=t3, pos_key=pos)

    idx = add_scene(f"Drop3-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# DROP 3 CONTINUED — 8 bars (32 beats) — sustained mayhem
# Different gobo, color wheel spinning on BSW for extra chaos
# =============================================================================

for beat in range(32):
    bar = beat // 4
    bib = beat % 4
    ci = beat
    pal = "fire" if beat % 2 == 0 else "ice"
    pos = POS_BIG[(beat + 8) % len(POS_BIG)]

    fb, m1, m2 = par_alternating(beat, FIRE_RED, ICE_BLUE, master=255)

    s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=255,
                         prism_s=128, p1r_s=200,
                         prism2_s=128, p2r_s=200,
                         prism_b=128, prot_b=200, prism_p=120,
                         gobo_b=BSW_G1_5,
                         s_strobe=SHARPY_STROBE_FAST,
                         b_shutter=BSW_SHUT_STROBE_FAST)

    t1 = 150 + (beat * 9 % 45)
    t2 = 135 + (beat * 7 % 50)
    t3 = 145 + (beat * 11 % 40)
    n = mk_ni(palette=pal, color_idx=ci, dim=255,
              halo_mode="jump_fast",
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
              t1=t1, t2=t2, t3=t3, pos_key=pos)

    idx = add_scene(f"Drop3B-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# FINAL DROP — 8 bars (32 beats) — MAXIMUM EVERYTHING
# Every fixture at full send. Par strobe. All movers strobe.
# All lasers. NI3K tilts auto-rotating. Fastest color changes.
# White strobe bursts on downbeats.
# =============================================================================

for beat in range(32):
    bar = beat // 4
    bib = beat % 4
    ci = beat
    pos = POS_DROP[bar % len(POS_DROP)]

    # Downbeats: WHITE BLAST
    if bib == 0:
        fb, m1, m2 = par_solid(WHITE, strobe=0)
        pal = "ice"
        # Sharpy and BSW go white
        sp, st, bp, bt, pp, pt, _ni = POS[pos]
        s = sharpy(pan=sp, tilt=st, strobe=SHARPY_STROBE_FAST, dim=255,
                   prism1=128, p1r=200, prism2=128, p2r=200)
        b = bsw(pan=bp, tilt=bt, color=BSW_WHITE,
                shutter=BSW_SHUT_STROBE_FAST, dim=255,
                prism=128, prot=200, gobo1=BSW_G1_3)
        p = profile(pan=pp, tilt=pt, dim=255, prism=120)
    else:
        # Other beats: fire/ice alternating
        if beat % 2 == 0:
            fb, m1, m2 = par_solid(FIRE_COLORS[beat % len(FIRE_COLORS)])
            pal = "fire"
        else:
            fb, m1, m2 = par_solid(ICE_COLORS[beat % len(ICE_COLORS)])
            pal = "ice"
        s, b, p = mk_movers(pos, palette=pal, color_idx=ci, dim=255,
                             prism_s=128, p1r_s=200,
                             prism2_s=128, p2r_s=200,
                             prism_b=128, prot_b=200, prism_p=120,
                             gobo_b=BSW_G1_6,
                             s_strobe=SHARPY_STROBE_FAST,
                             b_shutter=BSW_SHUT_STROBE_FAST)

    t1 = 160 + (beat % 3) * 12
    t2 = 140 + (beat % 4) * 15
    t3 = 170 + (beat % 5) * 8
    n = mk_ni(palette=pal, color_idx=ci, dim=255,
              halo_mode="jump_fast",
              rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
              t1=t1, t2=t2, t3=t3, pos_key=pos)

    idx = add_scene(f"Final-{bar+1}.{bib+1}", s, b, p, fb, m1, m2, n)
    beat_step(idx, beats=1)


# =============================================================================
# OUTRO — 8 bars — cool down to ice
# Pars every 2 beats, fading. Movers sweeping slowly back to center.
# Kill lasers. NI3K tilts settling.
# =============================================================================

for bar in range(8):
    for half in range(2):
        beat = bar * 4 + half * 2
        ci = beat // 2
        dim_val = max(20, 200 - bar * 22)
        master_val = max(20, 180 - bar * 20)

        ic = ICE_COLORS[ci % len(ICE_COLORS)]
        fb = fourbar_gradient(ic[0], ic[1], ic[2], 0, 0, 40,
                              master=master_val)
        m1 = miss1(*ic, master=master_val)
        m2 = miss2(0, 20, 60, master=master_val)

        # Movers converging to center
        pos_seq = ["X", "DSR", "DSL", "C", "C", "C", "C", "C"]
        pos = pos_seq[bar]
        s, b, p = mk_movers(pos, palette="ice", color_idx=ci,
                             dim=dim_val, frost=80 + bar * 15, focus=200)

        t_val = 64  # settled
        n = mk_ni(palette="ice", color_idx=ci, dim=max(10, dim_val - 40),
                  halo_mode="sync", t1=t_val, t2=t_val, t3=t_val, pos_key=pos)

        idx = add_scene(f"Outro-{bar+1}{chr(65+half)}", s, b, p, fb, m1, m2, n)
        smooth_step(idx, beats=2)


# =============================================================================
# FADE OUT — 12 bars — to black
# Very slow fade. Last 4 bars just NI3K halo fading.
# =============================================================================

for bar in range(12):
    dim_val = max(0, 60 - bar * 5)
    master_val = max(0, 80 - bar * 7)

    if bar < 8:
        ic = ICE_BLUE
        fb = fourbar_solid(0, 0, max(0, 40 - bar * 5), master=master_val)
        m1 = miss1(0, 0, max(0, 30 - bar * 4), master=master_val)
        m2 = miss2(0, 0, max(0, 30 - bar * 4), master=master_val)

        s, b, p = mk_movers("C", palette="ice", color_idx=0,
                             dim=dim_val, frost=255, focus=200)

        n = mk_ni(palette="ice", color_idx=0, dim=max(0, dim_val - 10),
                  halo_mode="sync", t1=64, t2=64, t3=64)
    else:
        # Last 4 bars: just fading NI3K halo
        fb = fourbar_solid(0, 0, 0, master=0)
        m1 = miss1(0, 0, 0, master=0)
        m2 = miss2(0, 0, 0, master=0)
        s = sharpy(dim=0, strobe=SHARPY_CLOSED)
        b = bsw(dim=0, shutter=BSW_SHUT_CLOSED)
        p = profile(dim=0)
        halo_dim = max(0, 30 - (bar - 8) * 10)
        n = ni3k(dim=halo_dim, r=0, g=0, b=max(0, 40 - (bar - 8) * 14),
                 halo=H_BLU if halo_dim > 0 else H_OFF)

    idx = add_scene(f"Fade-{bar+1}", s, b, p, fb, m1, m2, n)
    smooth_step(idx, beats=4)

# Final blackout
beat_step(0, beats=1)


# =============================================================================
# STATS & VERIFICATION
# =============================================================================

total_ms = sum(fi + ho for _, (fi, ho) in steps)
total_bars = total_ms / BAR_MS

print(f"\nScene dedup: {len(scenes)} unique scenes ({dedup_hits} reuses)")
print(f"Total steps: {len(steps)}")
print(f"Total duration: {total_ms/1000:.1f}s ({total_bars:.1f} bars)")
print(f"Target: ~205s (3:25)")

# Section timing breakdown
sections = [
    ("Intro/Build",    16 + 32),    # 8 bars × 2-beat + 8 bars × 1-beat
    ("DROP 1",         64),
    ("DROP 1 cont",    32),
    ("Breakdown 1",    16),
    ("DROP 2",         32),
    ("Breakdown 2",    16 + 32),    # 8 bars × 2-beat + 8 bars × 1-beat
    ("DROP 3",         32),
    ("DROP 3 cont",    32),
    ("FINAL DROP",     32),
    ("Outro",          16),
    ("Fade out",       12 + 1),     # 12 bars + blackout
]
offset = 0
for name, count in sections:
    section_steps = steps[offset:offset + count]
    section_ms = sum(fi + ho for _, (fi, ho) in section_steps)
    print(f"  {name:16s}: {count:3d} steps, {section_ms/1000:.1f}s")
    offset += count


# =============================================================================
# BUILD AND WRITE
# =============================================================================

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Fixin's", scene_ids, timing,
                          run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "▶ FIXIN'S", "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#FF4400", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace(os.path.join(VENUE_DIR, "shows", "Tvboo - Fixin's.qxw"),
                scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
