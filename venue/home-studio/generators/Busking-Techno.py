#!/usr/bin/env python3
"""
Busking workspace generator for Home Studio - Techno (High Energy)
10-minute looping show at 128 BPM with beat-synced blinking.

Design: Industrial techno with heavy beat-locked scene changes.
Palette: White, Deep Red, Cool Blue, Amber — max 2 colors at once.
Movement: Geometric, deliberate, sharp snaps on the beat.
Beat sync: Groove/Release sections use 1-beat or 2-beat step timing
           so lights snap to a new look on every beat.

Custom positions extrapolated from verified focus-positions.md values.

VC triggers (all loop):
  - FULL SHOW (10 min, all sections in sequence)
  - BLACKOUT
  - Section triggers: Opening, Tension Build, Groove Lock, Filter Build,
    Release 1, Strip Back, Second Build, Release 2, Outro

Run from project root:
    python3 "venue/home-studio/generators/Busking-Techno.py"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from showlib import *

# =============================================================================
# CONFIGURATION
# =============================================================================
VENUE = "venue/home-studio"
BPM = 128
OUTPUT = f"{VENUE}/shows/Busking-Techno.qxw"

BAR_MS = bpm_to_ms(BPM, 4)    # 1875ms
BEAT_MS = bpm_to_ms(BPM, 1)   # 469ms
HALF_BEAT = bpm_to_ms(BPM, 0.5)  # 234ms

# =============================================================================
# TECHNO COLOR PALETTE (from genres/techno.md)
# =============================================================================
# RGB for pars
DEEP_RED = (200, 0, 0)
COOL_BLUE = (0, 0, 200)
T_WHITE = (255, 255, 255)
T_AMBER = (255, 128, 0)
T_OFF = (0, 0, 0)
DIM_RED = (80, 0, 0)
DIM_WHITE = (60, 60, 60)
DIM_BLUE = (0, 0, 80)

# Mover color sets: (sharpy_wheel, bsw_wheel, profile_wheel)
CLR_WHITE = (SHARPY_WHITE, BSW_WHITE, PROF_WHITE)
CLR_RED = (SHARPY_RED, BSW_RED, PROF_RED)
CLR_BLUE = (SHARPY_BLUE, BSW_BLUE, PROF_BLUE)
CLR_AMBER = (SHARPY_AMBER, BSW_ORANGE, PROF_ORANGE)

# =============================================================================
# FOCUS POSITIONS — Verified + Custom Extrapolated
# Each entry: (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt,
#              profile_pan, profile_tilt, ni3k_pan)
# =============================================================================
POS = {
    # --- Verified positions ---
    "C":        (153, 0,   177, 19,  0,   123, 128),
    "DSC":      (158, 6,   179, 27,  64,  145, 128),
    "USC":      (157, 0,   181, 21,  52,  136, 128),
    "SL":       (170, 0,   189, 29,  50,  165, 80),
    "SR":       (149, 5,   170, 23,  110, 145, 176),
    "DSL":      (168, 4,   187, 32,  56,  170, 80),
    "DSR":      (151, 8,   168, 27,  115, 150, 176),
    "USL":      (172, 0,   192, 25,  40,  155, 80),
    "USR":      (147, 2,   173, 18,  105, 138, 176),
    "DJ":       (142, 3,   196, 25,  95,  107, 128),
    "CEIL":     (158, 73,  180, 86,  91,  30,  128),
    "DISCO":    (144, 34,  170, 56,  154, 168, 128),
    "DANCE":    (158, 6,   179, 27,  64,  145, 128),
    "FAR_L":    (90,  5,   198, 25,  45,  120, 40),
    "FAR_R":    (220, 5,   162, 20,  0,   120, 216),
    # --- Custom extrapolated positions ---
    # Split Wide: Sharpy far left + BSW far right (maximum forward-facing divergence)
    "SPLIT_W":  (90,  5,   162, 20,  0,   123, 128),
    # Cross Beams: Sharpy aims SR, BSW aims SL (X in center)
    "CROSS":    (149, 5,   189, 29,  0,   123, 128),
    # Quarter Left: midpoint between SL and C
    "Q_LEFT":   (162, 0,   183, 24,  25,  144, 104),
    # Quarter Right: midpoint between SR and C
    "Q_RIGHT":  (151, 3,   174, 21,  55,  134, 152),
    # Near Wall Left: between SL and Far Left
    "NW_LEFT":  (130, 3,   194, 27,  48,  143, 60),
    # Near Wall Right: between SR and Far Right
    "NW_RIGHT": (185, 5,   166, 21,  55,  133, 196),
    # Back Corners: Sharpy USL, BSW USR, Profile USC (spread upstage)
    "BACK_CRN": (170, 0,   170, 23,  52,  136, 128),
    # Front Spread: Sharpy DSL, BSW DSR, Profile DSC (spread downstage)
    "FRT_SPR":  (170, 0,   170, 23,  64,  145, 128),
    # Mid Ceiling: halfway between C and CEIL (for build to ceiling)
    "MID_CEIL": (156, 37,  179, 53,  46,  77,  128),
    # Deep Downstage: extrapolated past DSC toward audience
    "DEEP_DS":  (160, 10,  180, 32,  70,  152, 128),
}

def _pos(pos_name, sharpy_color, bsw_color, prof_color,
         par_rgb, ni3k_rgb=T_OFF, ni3k_halo=H_OFF, ni3k_dim=0,
         mover_dim=255, sharpy_gobo=0, bsw_gobo1=0,
         sharpy_prism1=0, bsw_prism=0, sharpy_frost=0, bsw_frost=0,
         ni3k_lasers=False, ni3k_rl=LASER_OFF, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
         par_strobe=0, miss_strobe=0, ni3k_strobe=0,
         ni3k_t1=64, ni3k_t2=64, ni3k_t3=64):
    """Build a full scene at a named position."""
    sp, st, bp, bt, pp, pt, np = POS[pos_name]
    return [
        sharpy(pan=sp, tilt=st, colormacro=sharpy_color, dim=mover_dim,
               gobo=sharpy_gobo, prism1=sharpy_prism1, frost=sharpy_frost),
        bsw(pan=bp, tilt=bt, color=bsw_color, dim=mover_dim,
            gobo1=bsw_gobo1, prism=bsw_prism, frost=bsw_frost),
        profile(pan=pp, tilt=pt, color=prof_color, dim=mover_dim),
        fourbar_solid(*par_rgb, strobe=par_strobe),
        *miss_both(*par_rgb, strobe=miss_strobe),
        ni3k(pan=np, dim=ni3k_dim, r=ni3k_rgb[0], g=ni3k_rgb[1], b=ni3k_rgb[2],
             halo=ni3k_halo, rl=ni3k_rl, gl=ni3k_gl, bl=ni3k_bl,
             strobe=ni3k_strobe, t1=ni3k_t1, t2=ni3k_t2, t3=ni3k_t3),
    ]

def _split(pos_s, pos_b, pos_p, sharpy_color, bsw_color, prof_color,
           par_rgb, ni3k_rgb=T_OFF, ni3k_halo=H_OFF, ni3k_dim=0,
           mover_dim=255, ni3k_lasers=False, par_strobe=0, miss_strobe=0):
    """Build a scene where each mover is at a DIFFERENT position."""
    sp, st, _, _, _, _, _ = POS[pos_s]  # sharpy position
    _, _, bp, bt, _, _, _ = POS[pos_b]  # bsw position
    _, _, _, _, pp, pt, np = POS[pos_p]  # profile + ni3k position
    rl = LASER_ON if ni3k_lasers else LASER_OFF
    gl = LASER_ON if ni3k_lasers else LASER_OFF
    bl = LASER_ON if ni3k_lasers else LASER_OFF
    return [
        sharpy(pan=sp, tilt=st, colormacro=sharpy_color, dim=mover_dim),
        bsw(pan=bp, tilt=bt, color=bsw_color, dim=mover_dim),
        profile(pan=pp, tilt=pt, color=prof_color, dim=mover_dim),
        fourbar_solid(*par_rgb, strobe=par_strobe),
        *miss_both(*par_rgb, strobe=miss_strobe),
        ni3k(pan=np, dim=ni3k_dim, r=ni3k_rgb[0], g=ni3k_rgb[1], b=ni3k_rgb[2],
             halo=ni3k_halo, rl=rl, gl=gl, bl=bl),
    ]

PATH = "Busking/Techno"

all_scenes = []
def add(name, *fixtures):
    idx = len(all_scenes)
    all_scenes.append(scene(name, *fixtures, path=PATH))
    return idx

# =============================================================================
# BLACKOUT
# =============================================================================
s_black = add("BLACKOUT", *blackout_all())

# =============================================================================
# SECTION 1: OPENING (32 bars) — Single red beam, stark darkness
# 2 unique scenes cycling every 4 bars. Mostly darkness with a red pulse.
# =============================================================================
s_open_1 = add("Open - Red Beam",
    *_pos("C", *CLR_RED, T_OFF, mover_dim=200,
          ni3k_dim=0))
# Barely-there dim pulse
s_open_2 = add("Open - Dim Pulse",
    *_pos("C", *CLR_RED, T_OFF, mover_dim=40,
          ni3k_dim=0))
OPENING = [s_open_1, s_open_2]

# =============================================================================
# SECTION 2: TENSION BUILD (32 bars) — Add fixtures one by one
# 4 unique scenes, smooth 8-bar crossfades
# =============================================================================
# Sharpy only, red, center
s_tens_1 = add("Tension - Sharpy Only",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=200),
    bsw(dim=0), profile(dim=0),
    fourbar_solid(*T_OFF), *miss_both(*T_OFF),
    ni3k(dim=0))
# + BSW, split
s_tens_2 = add("Tension - Two Movers",
    *_split("SL", "SR", "C", *CLR_RED, T_OFF, mover_dim=200))
# + Profile + dim pars
s_tens_3 = add("Tension - Three Movers",
    *_pos("C", *CLR_RED, DIM_RED, mover_dim=220, ni3k_dim=0))
# + NI3K dim
s_tens_4 = add("Tension - Full Rig Dim",
    *_pos("C", *CLR_RED, DIM_RED, ni3k_rgb=DIM_RED, ni3k_halo=H_RED,
          ni3k_dim=80, mover_dim=220))
TENSION = [s_tens_1, s_tens_2, s_tens_3, s_tens_4]

# =============================================================================
# SECTION 3: GROOVE LOCK (48 bars) — Beat-locked alternation, hypnotic
# 4 scenes on 1-beat timing: white/red color swaps with position shifts
# "Berghain" pair: Deep Red ↔ White
# =============================================================================
s_grv_1 = add("Groove - White C",
    *_pos("C", *CLR_WHITE, DEEP_RED, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=160, mover_dim=255))
s_grv_2 = add("Groove - Red C",
    *_pos("C", *CLR_RED, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=160, mover_dim=255))
s_grv_3 = add("Groove - White QL",
    *_pos("Q_LEFT", *CLR_WHITE, DEEP_RED, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=160, mover_dim=255))
s_grv_4 = add("Groove - Red QR",
    *_pos("Q_RIGHT", *CLR_RED, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=160, mover_dim=255))
GROOVE = [s_grv_1, s_grv_2, s_grv_3, s_grv_4]

# =============================================================================
# SECTION 4: FILTER BUILD (16 bars) — Industrial pulse, half-beat alternation
# 2 scenes: full white ↔ deep red dim. Fastest beat-sync section before release.
# =============================================================================
s_filt_1 = add("Filter - WHITE FLASH",
    *_pos("C", *CLR_WHITE, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=255, mover_dim=255))
s_filt_2 = add("Filter - RED DIM",
    *_pos("C", *CLR_RED, DIM_RED, ni3k_rgb=DIM_RED, ni3k_halo=H_RED,
          ni3k_dim=60, mover_dim=60))
FILTER = [s_filt_1, s_filt_2]

# =============================================================================
# SECTION 5: RELEASE 1 (48 bars) — Full rig, geometric beat patterns
# 8 scenes on 1-beat timing: movers snap to different positions each beat
# Berghain pair (White/Red) with geometric movement
# =============================================================================
s_rel1_1 = add("Rel1 - Split White",
    *_split("FAR_L", "FAR_R", "C", *CLR_WHITE, DEEP_RED,
            ni3k_rgb=DEEP_RED, ni3k_halo=H_RED, ni3k_dim=200, mover_dim=255))
s_rel1_2 = add("Rel1 - Center Red",
    *_pos("C", *CLR_RED, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=200, mover_dim=255))
s_rel1_3 = add("Rel1 - Cross White",
    *_pos("CROSS", *CLR_WHITE, DEEP_RED, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=200, mover_dim=255))
s_rel1_4 = add("Rel1 - Ceil Red",
    *_pos("CEIL", *CLR_RED, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=200, mover_dim=255))
s_rel1_5 = add("Rel1 - NW Left White",
    *_pos("NW_LEFT", *CLR_WHITE, DEEP_RED, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=200, mover_dim=255))
s_rel1_6 = add("Rel1 - NW Right Red",
    *_pos("NW_RIGHT", *CLR_RED, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=200, mover_dim=255))
s_rel1_7 = add("Rel1 - Back Corners White",
    *_pos("BACK_CRN", *CLR_WHITE, DEEP_RED, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=200, mover_dim=255, sharpy_prism1=128, bsw_prism=8))
s_rel1_8 = add("Rel1 - Front Spread Red",
    *_pos("FRT_SPR", *CLR_RED, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=200, mover_dim=255, sharpy_prism1=128, bsw_prism=8))
RELEASE1 = [s_rel1_1, s_rel1_2, s_rel1_3, s_rel1_4,
            s_rel1_5, s_rel1_6, s_rel1_7, s_rel1_8]

# =============================================================================
# SECTION 6: STRIP BACK (16 bars) — Remove elements, return to minimal
# 4 scenes, smooth 4-bar crossfade each
# =============================================================================
s_strip_1 = add("Strip - Full Dim",
    *_pos("C", *CLR_RED, DIM_RED, ni3k_rgb=DIM_RED, ni3k_halo=H_RED,
          ni3k_dim=120, mover_dim=180))
s_strip_2 = add("Strip - Movers Only",
    *_pos("C", *CLR_RED, T_OFF, ni3k_dim=0, mover_dim=140))
s_strip_3 = add("Strip - Two Dim",
    *_split("C", "C", "C", *CLR_RED, T_OFF, mover_dim=80))
s_strip_4 = add("Strip - Single Beam",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=120),
    bsw(dim=0), profile(dim=0),
    fourbar_solid(*T_OFF), *miss_both(*T_OFF),
    ni3k(dim=0))
STRIP = [s_strip_1, s_strip_2, s_strip_3, s_strip_4]

# =============================================================================
# SECTION 7: SECOND BUILD (32 bars) — Cold Steel palette (Blue/White)
# 4 scenes on 2-beat timing, building from single blue to full rig
# =============================================================================
s_bld2_1 = add("Build2 - Blue Beam",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_BLUE, dim=200),
    bsw(dim=0), profile(dim=0),
    fourbar_solid(*T_OFF), *miss_both(*T_OFF),
    ni3k(dim=0))
s_bld2_2 = add("Build2 - Blue Split",
    *_split("SL", "SR", "C", *CLR_BLUE, T_OFF, mover_dim=220))
s_bld2_3 = add("Build2 - Blue Full + Pars",
    *_pos("C", *CLR_BLUE, DIM_BLUE, ni3k_rgb=DIM_BLUE, ni3k_halo=H_BLU,
          ni3k_dim=100, mover_dim=240))
s_bld2_4 = add("Build2 - Cold Steel Ready",
    *_pos("C", *CLR_BLUE, T_WHITE, ni3k_rgb=COOL_BLUE, ni3k_halo=H_CYN,
          ni3k_dim=180, mover_dim=255))
BUILD2 = [s_bld2_1, s_bld2_2, s_bld2_3, s_bld2_4]

# =============================================================================
# SECTION 8: RELEASE 2 (64 bars) — PEAK ENERGY. All fixtures blinking on beat.
# 8 scenes on 1-beat timing. Lasers on. NI3K tilt heads spinning.
# Alternating Cold Steel (Blue/White) and Berghain (Red/White).
# Maximum position variety using custom extrapolated positions.
# =============================================================================
s_rel2_1 = add("Rel2 - SPLIT BLUE",
    *_pos("SPLIT_W", *CLR_BLUE, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=255, mover_dim=255, ni3k_lasers=True,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=160, ni3k_t2=180, ni3k_t3=170))
s_rel2_2 = add("Rel2 - CENTER RED",
    *_pos("C", *CLR_RED, T_WHITE, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=255, mover_dim=255,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=170, ni3k_t2=160, ni3k_t3=180))
s_rel2_3 = add("Rel2 - CROSS WHITE",
    *_pos("CROSS", *CLR_WHITE, DEEP_RED, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=255, mover_dim=255, sharpy_prism1=128, bsw_prism=8,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=180, ni3k_t2=170, ni3k_t3=160))
s_rel2_4 = add("Rel2 - BACK RED",
    *_pos("BACK_CRN", *CLR_RED, T_WHITE, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=255, mover_dim=255,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=160, ni3k_t2=180, ni3k_t3=170))
s_rel2_5 = add("Rel2 - FAR LEFT BLUE",
    *_pos("FAR_L", *CLR_BLUE, T_WHITE, ni3k_rgb=COOL_BLUE, ni3k_halo=H_BLU,
          ni3k_dim=255, mover_dim=255,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=170, ni3k_t2=160, ni3k_t3=180))
s_rel2_6 = add("Rel2 - FAR RIGHT RED",
    *_pos("FAR_R", *CLR_RED, T_WHITE, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=255, mover_dim=255, sharpy_prism1=128, bsw_prism=8,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=180, ni3k_t2=170, ni3k_t3=160))
s_rel2_7 = add("Rel2 - CEIL WHITE",
    *_pos("CEIL", *CLR_WHITE, T_WHITE, ni3k_rgb=T_WHITE, ni3k_halo=H_OFF,
          ni3k_dim=255, mover_dim=255,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=160, ni3k_t2=180, ni3k_t3=170))
s_rel2_8 = add("Rel2 - DSC RED ALL",
    *_pos("DEEP_DS", *CLR_RED, DEEP_RED, ni3k_rgb=DEEP_RED, ni3k_halo=H_RED,
          ni3k_dim=255, mover_dim=255, sharpy_prism1=128, bsw_prism=8,
          ni3k_rl=LASER_ON, ni3k_gl=LASER_OFF, ni3k_bl=LASER_OFF,
          ni3k_t1=170, ni3k_t2=160, ni3k_t3=180))
RELEASE2 = [s_rel2_1, s_rel2_2, s_rel2_3, s_rel2_4,
            s_rel2_5, s_rel2_6, s_rel2_7, s_rel2_8]

# =============================================================================
# SECTION 9: OUTRO (32 bars) — Fade back to single red beam in darkness
# 4 scenes, smooth 8-bar crossfade each
# =============================================================================
s_out_1 = add("Outro - Red Full",
    *_pos("C", *CLR_RED, DIM_RED, ni3k_rgb=DIM_RED, ni3k_halo=H_RED,
          ni3k_dim=120, mover_dim=200))
s_out_2 = add("Outro - Red Movers",
    *_pos("C", *CLR_RED, T_OFF, ni3k_dim=0, mover_dim=140))
s_out_3 = add("Outro - Single Dim",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=80),
    bsw(dim=0), profile(dim=0),
    fourbar_solid(*T_OFF), *miss_both(*T_OFF),
    ni3k(dim=0))
s_out_4 = add("Outro - Near Dark",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=20),
    bsw(dim=0), profile(dim=0),
    fourbar_solid(*T_OFF), *miss_both(*T_OFF),
    ni3k(dim=0))
OUTRO = [s_out_1, s_out_2, s_out_3, s_out_4]

# =============================================================================
# SECTION CHASERS (all Loop — used as individual VC triggers)
# =============================================================================
all_chasers = []

# Opening: 2 scenes, 4-bar hold each. Slow red pulse in darkness.
all_chasers.append(make_chaser("OPENING", OPENING,
    [hold(BPM, 4)] * 2, run_order="Loop", path=PATH))

# Tension: 4 scenes, 8-bar smooth crossfade.
all_chasers.append(make_chaser("TENSION BUILD", TENSION,
    [smooth(BPM, 8)] * 4, run_order="Loop", path=PATH))

# Groove Lock: 4 scenes, 1-beat snap. Beat-locked color swap.
all_chasers.append(make_chaser("GROOVE LOCK", GROOVE,
    [hold(BPM, 0.25)] * 4, run_order="Loop", path=PATH))

# Filter Build: 2 scenes, 2-beat snap. Industrial pulse.
all_chasers.append(make_chaser("FILTER BUILD", FILTER,
    [hold(BPM, 0.5)] * 2, run_order="Loop", path=PATH))

# Release 1: 8 scenes, 1-beat snap. Geometric beat patterns.
all_chasers.append(make_chaser("RELEASE 1", RELEASE1,
    [hold(BPM, 0.25)] * 8, run_order="Loop", path=PATH))

# Strip Back: 4 scenes, 4-bar smooth.
all_chasers.append(make_chaser("STRIP BACK", STRIP,
    [smooth(BPM, 4)] * 4, run_order="Loop", path=PATH))

# Second Build: 4 scenes, 2-beat snap. Cold steel build.
all_chasers.append(make_chaser("SECOND BUILD", BUILD2,
    [hold(BPM, 0.5)] * 4, run_order="Loop", path=PATH))

# Release 2: 8 scenes, 1-beat snap. PEAK energy with lasers.
all_chasers.append(make_chaser("RELEASE 2", RELEASE2,
    [hold(BPM, 0.25)] * 8, run_order="Loop", path=PATH))

# Outro: 4 scenes, 8-bar smooth.
all_chasers.append(make_chaser("OUTRO", OUTRO,
    [smooth(BPM, 8)] * 4, run_order="Loop", path=PATH))

# =============================================================================
# FULL SHOW CHASER — 10 minutes, all sections in sequence, Loop
#
# Strategy: repeat each section's scene pool to fill its bar allocation.
# Bar allocations (total 320 = 10 min at 128 BPM):
#   Opening:       32 bars  → 8 reps of 2 scenes × 4-bar hold = 32 bars ✓
#   Tension:       32 bars  → 4 scenes × 8-bar smooth           = 32 bars ✓
#   Groove Lock:   48 bars  → 48 reps of 4 scenes × 1-beat hold = 48 bars ✓
#   Filter Build:  16 bars  → 32 reps of 2 scenes × 2-beat hold = 16 bars ✓
#   Release 1:     48 bars  → 24 reps of 8 scenes × 1-beat hold = 48 bars ✓
#   Strip Back:    16 bars  → 4 scenes × 4-bar smooth           = 16 bars ✓
#   Second Build:  32 bars  → 16 reps of 4 scenes × 2-beat hold = 32 bars ✓
#   Release 2:     64 bars  → 32 reps of 8 scenes × 1-beat hold = 64 bars ✓
#   Outro:         32 bars  → 4 scenes × 8-bar smooth           = 32 bars ✓
# =============================================================================

def repeat_pattern(scenes, count):
    """Repeat a scene pattern N times."""
    result = []
    for _ in range(count):
        result.extend(scenes)
    return result

full_ids = []
full_timing = []

# Opening: 32 bars = 8 cycles of 2 scenes at 4-bar hold (16 bars per full cycle, need 2 cycles)
# Actually 2 scenes × 4 bars each = 8 bars per cycle. Need 4 cycles = 32 bars.
full_ids += repeat_pattern(OPENING, 4)
full_timing += [hold(BPM, 4)] * 8

# Tension: 32 bars = 4 scenes × 8-bar smooth
full_ids += TENSION
full_timing += [smooth(BPM, 8)] * 4

# Groove Lock: 48 bars = 192 beats. 4 scenes at 1 beat each = 4 beats per cycle.
# 192/4 = 48 cycles → 192 steps. That's a lot. Let's use 2-beat timing instead.
# 48 bars = 96 half-bars. 4 scenes × 2 beats = 8 beats per cycle = 2 bars.
# Need 24 cycles = 96 steps. Still a lot but manageable.
# Actually let's use 1-bar timing for the full show (still feels beat-locked):
# 4 scenes × 1 bar each = 4 bars per cycle. Need 12 cycles = 48 steps.
full_ids += repeat_pattern(GROOVE, 12)
full_timing += [hold(BPM, 1)] * 48

# Filter Build: 16 bars = 64 beats. 2 scenes × 2 beats = 4 beats per cycle.
# Need 16 cycles = 32 steps.
full_ids += repeat_pattern(FILTER, 16)
full_timing += [hold(BPM, 0.5)] * 32

# Release 1: 48 bars = 192 beats. 8 scenes × 1 beat = 8 beats per cycle.
# Need 24 cycles = 192 steps... too many. Use 2-beat timing: 8 scenes × 2 = 16 beats = 4 bars.
# Need 12 cycles = 96 steps. Still a lot. Use 1-bar: 8 × 4 beats = 32 beats = 8 bars per cycle.
# Need 6 cycles = 48 steps.
full_ids += repeat_pattern(RELEASE1, 6)
full_timing += [hold(BPM, 1)] * 48

# Strip Back: 16 bars = 4 scenes × 4-bar smooth
full_ids += STRIP
full_timing += [smooth(BPM, 4)] * 4

# Second Build: 32 bars. 4 scenes × 2-beat hold = 8 beats = 2 bars per cycle.
# Need 16 cycles = 64 steps. Use 1-bar timing: 4 × 1 bar = 4 bars/cycle, 8 cycles = 32 steps.
full_ids += repeat_pattern(BUILD2, 8)
full_timing += [hold(BPM, 1)] * 32

# Release 2: 64 bars. 8 scenes × 1-beat = 8 beats = 2 bars/cycle.
# Need 32 cycles = 256 steps → too many. Use 1 bar: 8 × 1 bar = 8 bars/cycle, 8 cycles = 64 steps.
full_ids += repeat_pattern(RELEASE2, 8)
full_timing += [hold(BPM, 1)] * 64

# Outro: 32 bars = 4 scenes × 8-bar smooth
full_ids += OUTRO
full_timing += [smooth(BPM, 8)] * 4

all_chasers.append(make_chaser("FULL SHOW", full_ids, full_timing,
                                run_order="Loop", path=PATH))

# =============================================================================
# VIRTUAL CONSOLE LAYOUT
# =============================================================================
num_scenes = len(all_scenes)

# Chaser function IDs (scenes are 0..N-1, chasers are N..N+M-1)
CH_OPENING_ID  = num_scenes + 0
CH_TENSION_ID  = num_scenes + 1
CH_GROOVE_ID   = num_scenes + 2
CH_FILTER_ID   = num_scenes + 3
CH_REL1_ID     = num_scenes + 4
CH_STRIP_ID    = num_scenes + 5
CH_BUILD2_ID   = num_scenes + 6
CH_REL2_ID     = num_scenes + 7
CH_OUTRO_ID    = num_scenes + 8
CH_FULL_ID     = num_scenes + 9

vc_buttons = []
vc_id = 0

# FULL SHOW (top left, big green)
vc_buttons.append({
    "caption": "FULL SHOW", "vc_id": vc_id, "func_id": CH_FULL_ID,
    "x": 10, "y": 10, "w": 220, "h": 80,
    "color": "#22AA22", "action": "Toggle"
})
vc_id += 1

# BLACKOUT (below full show, big red)
vc_buttons.append({
    "caption": "BLACKOUT", "vc_id": vc_id, "func_id": s_black,
    "x": 10, "y": 100, "w": 220, "h": 80,
    "color": "#FF0000", "action": "Toggle"
})
vc_id += 1

# Section triggers (right column)
section_btns = [
    ("OPENING",        CH_OPENING_ID, "#440000"),  # dark red
    ("TENSION BUILD",  CH_TENSION_ID, "#880000"),  # medium red
    ("GROOVE LOCK",    CH_GROOVE_ID,  "#FFFFFF"),  # white (berghain)
    ("FILTER BUILD",   CH_FILTER_ID,  "#CCCCCC"),  # light grey
    ("RELEASE 1",      CH_REL1_ID,    "#CC0000"),  # bright red
    ("STRIP BACK",     CH_STRIP_ID,   "#330000"),  # very dark red
    ("SECOND BUILD",   CH_BUILD2_ID,  "#0000CC"),  # cold blue
    ("RELEASE 2",      CH_REL2_ID,    "#FF0000"),  # peak red
    ("OUTRO",          CH_OUTRO_ID,   "#220000"),  # near-dark red
]

y_pos = 10
for caption, func_id, color in section_btns:
    vc_buttons.append({
        "caption": caption, "vc_id": vc_id, "func_id": func_id,
        "x": 250, "y": y_pos, "w": 220, "h": 60,
        "color": color, "action": "Toggle"
    })
    vc_id += 1
    y_pos += 70

# =============================================================================
# WRITE WORKSPACE
# =============================================================================
write_workspace(OUTPUT, all_scenes, all_chasers, bpm=BPM, vc_buttons=vc_buttons)

# =============================================================================
# SUMMARY
# =============================================================================
total_full_steps = len(full_ids)
# Calculate actual full show duration
dur_ms = 0
for fi, ho in full_timing:
    dur_ms += fi + ho
print(f"\n  Total scenes: {len(all_scenes)}")
print(f"  Total chasers: {len(all_chasers)}")
print(f"  Full show steps: {total_full_steps}")
print(f"  Full show duration: {dur_ms/1000:.0f}s ({dur_ms/60000:.1f} min)")

sections_info = [
    ("Opening", 32), ("Tension Build", 32), ("Groove Lock", 48),
    ("Filter Build", 16), ("Release 1", 48), ("Strip Back", 16),
    ("Second Build", 32), ("Release 2", 64), ("Outro", 32)
]
print(f"\n  Section breakdown:")
total_bars = 0
for name, bars in sections_info:
    dur_s = bars * BAR_MS / 1000
    print(f"    {name:20s}: {bars:3d} bars ({dur_s:.1f}s)")
    total_bars += bars
print(f"    {'TOTAL':20s}: {total_bars:3d} bars ({total_bars * BAR_MS / 1000:.1f}s = {total_bars * BAR_MS / 60000:.1f} min)")

print(f"\n  Custom extrapolated positions: SPLIT_W, CROSS, Q_LEFT, Q_RIGHT,")
print(f"    NW_LEFT, NW_RIGHT, BACK_CRN, FRT_SPR, MID_CEIL, DEEP_DS")
