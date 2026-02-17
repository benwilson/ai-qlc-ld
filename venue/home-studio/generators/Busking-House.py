#!/usr/bin/env python3
"""
Busking workspace generator for Home Studio - House Music
5-minute looping show at 128 BPM with section triggers.

VC Layout:
  - FULL SHOW (looping through all sections)
  - BLACKOUT
  - Section triggers: Intro, Groove Build, Melodic Rise, Peak,
    Emotional Break, Final Build, Peak 2, Outro

Run from project root:
    python3 "venue/home-studio/generators/Busking-House.py"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from showlib import *

# =============================================================================
# CONFIGURATION
# =============================================================================
VENUE = "venue/home-studio"
BPM = 128
OUTPUT = f"{VENUE}/shows/Busking-House.qxw"

# Timing helpers
BAR_MS = bpm_to_ms(BPM, 4)  # 1875ms per bar
BEAT_MS = bpm_to_ms(BPM, 1)  # ~469ms per beat

# =============================================================================
# HOUSE COLOR PALETTE (from genres/house.md)
# =============================================================================
# Primary: Warm White, Deep Blue, Magenta
# Accent: Amber, Teal, Pink, Cyan
# Two-color pairs: Sunset, Deep Ocean, Club Classic, Golden Hour, Cool Dawn, Neon Rose

# RGB values for pars
WARM_WHITE = (255, 180, 100)
DEEP_BLUE = (0, 0, 255)
HOUSE_MAGENTA = (255, 0, 255)
HOUSE_AMBER = (255, 128, 0)
HOUSE_TEAL = (0, 255, 128)
HOUSE_PINK = (255, 64, 128)
HOUSE_CYAN = (0, 255, 255)
HOUSE_PURPLE = (128, 0, 255)

# =============================================================================
# FOCUS POSITIONS (from focus-positions.md - verified values)
# =============================================================================
POS = {
    "C":    {"sharpy": (153, 0),  "bsw": (177, 19), "profile": (0, 123),   "ni3k": 128},
    "DSC":  {"sharpy": (158, 6),  "bsw": (179, 27), "profile": (64, 145),  "ni3k": 128},
    "USC":  {"sharpy": (157, 0),  "bsw": (181, 21), "profile": (52, 136),  "ni3k": 128},
    "SL":   {"sharpy": (170, 0),  "bsw": (189, 29), "profile": (50, 165),  "ni3k": 80},
    "SR":   {"sharpy": (149, 5),  "bsw": (170, 23), "profile": (110, 145), "ni3k": 176},
    "DSL":  {"sharpy": (170, 0),  "bsw": (189, 29), "profile": (50, 165),  "ni3k": 80},
    "DSR":  {"sharpy": (149, 5),  "bsw": (170, 23), "profile": (110, 145), "ni3k": 176},
    "USL":  {"sharpy": (170, 0),  "bsw": (189, 29), "profile": (50, 165),  "ni3k": 80},
    "USR":  {"sharpy": (149, 5),  "bsw": (170, 23), "profile": (110, 145), "ni3k": 176},
    "DJ":   {"sharpy": (142, 3),  "bsw": (196, 25), "profile": (95, 107),  "ni3k": 128},
    "CEIL": {"sharpy": (158, 73), "bsw": (180, 86), "profile": (91, 30),   "ni3k": 128},
    "DISCO":{"sharpy": (144, 34), "bsw": (170, 56), "profile": (154, 168), "ni3k": 128},
    "DANCE":{"sharpy": (158, 6),  "bsw": (179, 27), "profile": (64, 145),  "ni3k": 128},
    "FAR_L":{"sharpy": (90, 5),   "bsw": (100, 15), "profile": (45, 120),  "ni3k": 40},
    "FAR_R":{"sharpy": (220, 5),  "bsw": (0, 15),   "profile": (0, 120),   "ni3k": 216},
}

def pos_movers(pos_name, sharpy_color=SHARPY_WHITE, bsw_color=BSW_WHITE, prof_color=PROF_WHITE,
               sharpy_dim=255, bsw_dim=255, prof_dim=255,
               sharpy_strobe=SHARPY_OPEN, bsw_shutter=BSW_SHUT_OPEN, prof_strobe=PROFILE_STROBE_OFF,
               sharpy_gobo=0, bsw_gobo1=0, sharpy_prism1=0, bsw_prism=0,
               sharpy_frost=0, bsw_frost=0):
    """Return mover fixtures aimed at a named position with color and effects."""
    p = POS[pos_name]
    sp, st = p["sharpy"]
    bp, bt = p["bsw"]
    pp, pt = p["profile"]
    return [
        sharpy(pan=sp, tilt=st, colormacro=sharpy_color, dim=sharpy_dim,
               strobe=sharpy_strobe, gobo=sharpy_gobo, prism1=sharpy_prism1, frost=sharpy_frost),
        bsw(pan=bp, tilt=bt, color=bsw_color, dim=bsw_dim,
            shutter=bsw_shutter, gobo1=bsw_gobo1, prism=bsw_prism, frost=bsw_frost),
        profile(pan=pp, tilt=pt, color=prof_color, dim=prof_dim,
                strobe=prof_strobe),
    ]

def house_scene(name, pos_name, mover_color_set, par_rgb, ni3k_rgb=(0,0,0),
                ni3k_halo=H_OFF, ni3k_dim=0, mover_dim=255,
                sharpy_gobo=0, bsw_gobo1=0, sharpy_prism1=0, bsw_prism=0,
                sharpy_frost=0, bsw_frost=0, ni3k_lasers=False,
                path="Busking/House"):
    """Build a full house scene with movers at position + pars + NI3K."""
    sharpy_c, bsw_c, prof_c = mover_color_set
    movers = pos_movers(pos_name, sharpy_color=sharpy_c, bsw_color=bsw_c, prof_color=prof_c,
                        sharpy_dim=mover_dim, bsw_dim=mover_dim, prof_dim=mover_dim,
                        sharpy_gobo=sharpy_gobo, bsw_gobo1=bsw_gobo1,
                        sharpy_prism1=sharpy_prism1, bsw_prism=bsw_prism,
                        sharpy_frost=sharpy_frost, bsw_frost=bsw_frost)
    pars = [
        fourbar_solid(*par_rgb),
        *miss_both(*par_rgb),
    ]
    ni3k_fix = ni3k(pan=POS[pos_name]["ni3k"], dim=ni3k_dim,
                    r=ni3k_rgb[0], g=ni3k_rgb[1], b=ni3k_rgb[2],
                    halo=ni3k_halo,
                    rl=LASER_ON if ni3k_lasers else LASER_OFF,
                    gl=LASER_ON if ni3k_lasers else LASER_OFF,
                    bl=LASER_ON if ni3k_lasers else LASER_OFF)
    return scene(name, *movers, *pars, ni3k_fix, path=path)

# =============================================================================
# COLOR SETS: (sharpy_wheel, bsw_wheel, profile_wheel)
# =============================================================================
CLR_WHITE = (SHARPY_WHITE, BSW_WHITE, PROF_WHITE)
CLR_AMBER = (SHARPY_AMBER, BSW_ORANGE, PROF_ORANGE)
CLR_BLUE = (SHARPY_BLUE, BSW_BLUE, PROF_BLUE)
CLR_MAGENTA = (SHARPY_PURPLE, BSW_MAG, PROF_PINK)
CLR_TEAL = (SHARPY_TEAL, BSW_TEAL, PROF_TEAL)
CLR_PINK = (SHARPY_PINK, BSW_PINK, PROF_PINK)
CLR_CYAN = (SHARPY_TEAL, BSW_TEAL, PROF_TEAL)  # closest to cyan on wheels

# =============================================================================
# SCENES
# =============================================================================
all_scenes = []
section_scenes = {}  # section_name -> [scene_indices]

def add_scene(s):
    idx = len(all_scenes)
    all_scenes.append(s)
    return idx

# --- BLACKOUT ---
blackout_id = add_scene(scene("BLACKOUT", *blackout_all(), path="Busking/House"))

# =============================================================================
# SECTION 1: INTRO (16 bars) — Warm wash, minimal movement, establish groove
# Golden Hour pair: Warm White movers + Amber pars
# Movers at center, slow drift to DJ and back
# =============================================================================
intro_ids = []
# Warm white center
intro_ids.append(add_scene(house_scene("Intro - Warm Center", "C",
    CLR_WHITE, WARM_WHITE, ni3k_rgb=WARM_WHITE, ni3k_halo=H_YEL, ni3k_dim=80, mover_dim=180)))
# Amber at DJ
intro_ids.append(add_scene(house_scene("Intro - Amber DJ", "DJ",
    CLR_AMBER, WARM_WHITE, ni3k_rgb=WARM_WHITE, ni3k_halo=H_YEL, ni3k_dim=80, mover_dim=180)))
# Warm white back to center
intro_ids.append(add_scene(house_scene("Intro - Warm Center 2", "USC",
    CLR_WHITE, WARM_WHITE, ni3k_rgb=WARM_WHITE, ni3k_halo=H_YEL, ni3k_dim=80, mover_dim=180)))
# Amber drift
intro_ids.append(add_scene(house_scene("Intro - Amber Drift", "C",
    CLR_AMBER, HOUSE_AMBER, ni3k_rgb=HOUSE_AMBER, ni3k_halo=H_YEL, ni3k_dim=80, mover_dim=180)))
section_scenes["Intro"] = intro_ids

# =============================================================================
# SECTION 2: GROOVE BUILD (16 bars) — Gentle evolution, add layers
# Deep Ocean pair: Deep Blue movers + Teal pars
# =============================================================================
groove_ids = []
groove_ids.append(add_scene(house_scene("Groove - Blue Center", "C",
    CLR_BLUE, HOUSE_TEAL, ni3k_rgb=HOUSE_TEAL, ni3k_halo=H_CYN, ni3k_dim=120, mover_dim=200)))
groove_ids.append(add_scene(house_scene("Groove - Blue SL", "SL",
    CLR_BLUE, HOUSE_TEAL, ni3k_rgb=HOUSE_TEAL, ni3k_halo=H_CYN, ni3k_dim=120, mover_dim=200)))
groove_ids.append(add_scene(house_scene("Groove - Teal Center", "C",
    CLR_TEAL, DEEP_BLUE, ni3k_rgb=DEEP_BLUE, ni3k_halo=H_BLU, ni3k_dim=120, mover_dim=220)))
groove_ids.append(add_scene(house_scene("Groove - Teal SR", "SR",
    CLR_TEAL, DEEP_BLUE, ni3k_rgb=DEEP_BLUE, ni3k_halo=H_BLU, ni3k_dim=120, mover_dim=220)))
section_scenes["Groove Build"] = groove_ids

# =============================================================================
# SECTION 3: MELODIC RISE (16 bars) — Colors deepen, movers widen
# Neon Rose pair: Pink movers + Magenta pars, wider movement
# =============================================================================
melodic_ids = []
melodic_ids.append(add_scene(house_scene("Melodic - Pink SL", "SL",
    CLR_PINK, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=160, mover_dim=240)))
melodic_ids.append(add_scene(house_scene("Melodic - Pink C", "C",
    CLR_PINK, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=160, mover_dim=240)))
melodic_ids.append(add_scene(house_scene("Melodic - Mag SR", "SR",
    CLR_MAGENTA, HOUSE_PINK, ni3k_rgb=HOUSE_PINK, ni3k_halo=H_PNK, ni3k_dim=160, mover_dim=240)))
melodic_ids.append(add_scene(house_scene("Melodic - Mag DSC", "DSC",
    CLR_MAGENTA, HOUSE_PINK, ni3k_rgb=HOUSE_PINK, ni3k_halo=H_PNK, ni3k_dim=160, mover_dim=240)))
section_scenes["Melodic Rise"] = melodic_ids

# =============================================================================
# SECTION 4: PEAK (32 bars) — Full palette, sweeping movers, smooth and joyful
# Sunset pair: Amber movers + Magenta pars, wide sweeps, prism
# Club Classic pair: Magenta movers + White pars
# =============================================================================
peak_ids = []
# Sunset wide sweep
peak_ids.append(add_scene(house_scene("Peak - Sunset SL", "SL",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=200, mover_dim=255,
    sharpy_prism1=128, bsw_prism=8)))
peak_ids.append(add_scene(house_scene("Peak - Sunset C", "C",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=200, mover_dim=255)))
peak_ids.append(add_scene(house_scene("Peak - Sunset SR", "SR",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=200, mover_dim=255,
    sharpy_prism1=128, bsw_prism=8)))
peak_ids.append(add_scene(house_scene("Peak - Sunset DSC", "DSC",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=200, mover_dim=255)))
# Club Classic: Magenta + White
peak_ids.append(add_scene(house_scene("Peak - Classic SL", "SL",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=220, mover_dim=255)))
peak_ids.append(add_scene(house_scene("Peak - Classic C", "C",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=220, mover_dim=255)))
peak_ids.append(add_scene(house_scene("Peak - Classic SR", "SR",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=220, mover_dim=255,
    sharpy_prism1=128, bsw_prism=8)))
peak_ids.append(add_scene(house_scene("Peak - Classic Dance", "DANCE",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=220, mover_dim=255)))
section_scenes["Peak"] = peak_ids

# =============================================================================
# SECTION 5: EMOTIONAL BREAK (16 bars) — Strip back, intimate, single color
# Night Sky pair: Deep Blue movers + Purple pars, converge to center/DJ
# =============================================================================
emo_ids = []
emo_ids.append(add_scene(house_scene("Emo - Blue DJ", "DJ",
    CLR_BLUE, HOUSE_PURPLE, ni3k_rgb=HOUSE_PURPLE, ni3k_halo=H_BLU, ni3k_dim=100, mover_dim=160,
    sharpy_frost=128, bsw_frost=129)))
emo_ids.append(add_scene(house_scene("Emo - Blue C", "C",
    CLR_BLUE, HOUSE_PURPLE, ni3k_rgb=HOUSE_PURPLE, ni3k_halo=H_BLU, ni3k_dim=100, mover_dim=160,
    sharpy_frost=128, bsw_frost=129)))
emo_ids.append(add_scene(house_scene("Emo - Blue USC", "USC",
    CLR_BLUE, DEEP_BLUE, ni3k_rgb=DEEP_BLUE, ni3k_halo=H_BLU, ni3k_dim=80, mover_dim=140,
    sharpy_frost=128, bsw_frost=129)))
emo_ids.append(add_scene(house_scene("Emo - Blue DJ 2", "DJ",
    CLR_BLUE, DEEP_BLUE, ni3k_rgb=DEEP_BLUE, ni3k_halo=H_BLU, ni3k_dim=80, mover_dim=140,
    sharpy_frost=128, bsw_frost=129)))
section_scenes["Emotional Break"] = emo_ids

# =============================================================================
# SECTION 6: FINAL BUILD (16 bars) — Layer everything back, build to climax
# Cool Dawn pair: Cyan movers + Blue pars, spreading movement
# =============================================================================
build_ids = []
build_ids.append(add_scene(house_scene("Build - Cyan C", "C",
    CLR_CYAN, DEEP_BLUE, ni3k_rgb=DEEP_BLUE, ni3k_halo=H_CYN, ni3k_dim=160, mover_dim=220)))
build_ids.append(add_scene(house_scene("Build - Cyan SL", "SL",
    CLR_CYAN, HOUSE_CYAN, ni3k_rgb=HOUSE_CYAN, ni3k_halo=H_CYN, ni3k_dim=180, mover_dim=240)))
build_ids.append(add_scene(house_scene("Build - Cyan SR", "SR",
    CLR_CYAN, HOUSE_CYAN, ni3k_rgb=HOUSE_CYAN, ni3k_halo=H_CYN, ni3k_dim=200, mover_dim=250)))
build_ids.append(add_scene(house_scene("Build - Cyan Wide", "DSC",
    CLR_CYAN, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=220, mover_dim=255)))
section_scenes["Final Build"] = build_ids

# =============================================================================
# SECTION 7: PEAK 2 (32 bars) — Biggest moment, lasers, full send
# Sunset + Club Classic interleaved, with lasers on NI3K
# =============================================================================
peak2_ids = []
peak2_ids.append(add_scene(house_scene("Peak2 - Sunset SL", "FAR_L",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=255, mover_dim=255,
    sharpy_prism1=128, bsw_prism=8, ni3k_lasers=True)))
peak2_ids.append(add_scene(house_scene("Peak2 - Classic C", "C",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=255, mover_dim=255,
    ni3k_lasers=True)))
peak2_ids.append(add_scene(house_scene("Peak2 - Sunset SR", "FAR_R",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=255, mover_dim=255,
    sharpy_prism1=128, bsw_prism=8, ni3k_lasers=True)))
peak2_ids.append(add_scene(house_scene("Peak2 - Classic DSC", "DSC",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=255, mover_dim=255,
    ni3k_lasers=True)))
peak2_ids.append(add_scene(house_scene("Peak2 - Sunset Dance", "DANCE",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=255, mover_dim=255,
    ni3k_lasers=True)))
peak2_ids.append(add_scene(house_scene("Peak2 - Classic SL", "SL",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=255, mover_dim=255,
    sharpy_prism1=128, bsw_prism=8, ni3k_lasers=True)))
peak2_ids.append(add_scene(house_scene("Peak2 - Sunset C", "C",
    CLR_AMBER, HOUSE_MAGENTA, ni3k_rgb=HOUSE_MAGENTA, ni3k_halo=H_PNK, ni3k_dim=255, mover_dim=255,
    ni3k_lasers=True)))
peak2_ids.append(add_scene(house_scene("Peak2 - Classic SR", "SR",
    CLR_MAGENTA, WHITE, ni3k_rgb=WHITE, ni3k_halo=H_RGB, ni3k_dim=255, mover_dim=255,
    ni3k_lasers=True)))
section_scenes["Peak 2"] = peak2_ids

# =============================================================================
# SECTION 8: OUTRO (16 bars) — Return to opening feel, gentle fade
# Golden Hour pair: back to warm white + amber, converge, dim down
# =============================================================================
outro_ids = []
outro_ids.append(add_scene(house_scene("Outro - Warm C", "C",
    CLR_WHITE, WARM_WHITE, ni3k_rgb=WARM_WHITE, ni3k_halo=H_YEL, ni3k_dim=120, mover_dim=200)))
outro_ids.append(add_scene(house_scene("Outro - Amber DJ", "DJ",
    CLR_AMBER, WARM_WHITE, ni3k_rgb=WARM_WHITE, ni3k_halo=H_YEL, ni3k_dim=80, mover_dim=160)))
outro_ids.append(add_scene(house_scene("Outro - Warm USC", "USC",
    CLR_WHITE, HOUSE_AMBER, ni3k_rgb=HOUSE_AMBER, ni3k_halo=H_YEL, ni3k_dim=60, mover_dim=120)))
outro_ids.append(add_scene(house_scene("Outro - Dim C", "C",
    CLR_AMBER, WARM_WHITE, ni3k_rgb=(0,0,0), ni3k_halo=H_OFF, ni3k_dim=0, mover_dim=80)))
section_scenes["Outro"] = outro_ids

# =============================================================================
# CHASERS — One per section (looping) + Full Show (looping)
# =============================================================================
all_chasers = []

# Section timing: House uses smooth crossfades
# Intro: 16 bars / 4 steps = 4 bars per step smooth
# Groove: 16 bars / 4 steps = 4 bars per step smooth
# Melodic: 16 bars / 4 steps = 4 bars per step smooth
# Peak: 32 bars / 8 steps = 4 bars per step smooth
# Emo Break: 16 bars / 4 steps = 4 bars per step smooth
# Final Build: 16 bars / 4 steps = 4 bars per step smooth
# Peak 2: 32 bars / 8 steps = 4 bars per step smooth
# Outro: 16 bars / 4 steps = 4 bars per step smooth

def section_chaser(name, scene_ids, bars_per_step=4, run_order="Loop"):
    """Build a looping section chaser with smooth crossfades."""
    timing = [smooth(BPM, bars_per_step)] * len(scene_ids)
    return make_chaser(name, scene_ids, timing, run_order=run_order, path="Busking/House")

# Individual section chasers (all loop)
ch_intro = section_chaser("INTRO", intro_ids, bars_per_step=4)
all_chasers.append(ch_intro)

ch_groove = section_chaser("GROOVE BUILD", groove_ids, bars_per_step=4)
all_chasers.append(ch_groove)

ch_melodic = section_chaser("MELODIC RISE", melodic_ids, bars_per_step=4)
all_chasers.append(ch_melodic)

ch_peak = section_chaser("PEAK", peak_ids, bars_per_step=4)
all_chasers.append(ch_peak)

ch_emo = section_chaser("EMOTIONAL BREAK", emo_ids, bars_per_step=4)
all_chasers.append(ch_emo)

ch_build = section_chaser("FINAL BUILD", build_ids, bars_per_step=4)
all_chasers.append(ch_build)

ch_peak2 = section_chaser("PEAK 2", peak2_ids, bars_per_step=4)
all_chasers.append(ch_peak2)

ch_outro = section_chaser("OUTRO", outro_ids, bars_per_step=4)
all_chasers.append(ch_outro)

# Full show chaser: all section scenes in order, looping
# Intro: 16 bars = 4 steps × 4 bars smooth
# Groove: 16 bars = 4 steps × 4 bars smooth
# Melodic: 16 bars = 4 steps × 4 bars smooth
# Peak: 32 bars = 8 steps × 4 bars smooth
# Emo: 16 bars = 4 steps × 4 bars smooth
# Build: 16 bars = 4 steps × 4 bars smooth
# Peak 2: 32 bars = 8 steps × 4 bars smooth
# Outro: 16 bars = 4 steps × 4 bars smooth
# Total: 160 bars = 5 minutes at 128 BPM
full_show_ids = (intro_ids + groove_ids + melodic_ids + peak_ids +
                 emo_ids + build_ids + peak2_ids + outro_ids)
full_show_timing = [smooth(BPM, 4)] * len(full_show_ids)
ch_full = make_chaser("FULL SHOW", full_show_ids, full_show_timing,
                       run_order="Loop", path="Busking/House")
all_chasers.append(ch_full)

# =============================================================================
# VIRTUAL CONSOLE LAYOUT
# Custom XML generation for Solo Frames and proper layout
# =============================================================================

# Function ID mapping: scenes 0..N-1, chasers N..N+M-1
num_scenes = len(all_scenes)

# Chaser function IDs (in order added to all_chasers)
CH_INTRO_ID    = num_scenes + 0
CH_GROOVE_ID   = num_scenes + 1
CH_MELODIC_ID  = num_scenes + 2
CH_PEAK_ID     = num_scenes + 3
CH_EMO_ID      = num_scenes + 4
CH_BUILD_ID    = num_scenes + 5
CH_PEAK2_ID    = num_scenes + 6
CH_OUTRO_ID    = num_scenes + 7
CH_FULL_ID     = num_scenes + 8

# VC button definitions
# Layout: Left column = Full Show + Blackout, Right = Section triggers in a solo frame
vc_buttons = []
vc_id = 0

# FULL SHOW button (top left, big)
vc_buttons.append({
    "caption": "FULL SHOW", "vc_id": vc_id, "func_id": CH_FULL_ID,
    "x": 10, "y": 10, "w": 220, "h": 80,
    "color": "#22AA22", "action": "Toggle"
})
vc_id += 1

# BLACKOUT button (below full show)
vc_buttons.append({
    "caption": "BLACKOUT", "vc_id": vc_id, "func_id": blackout_id,
    "x": 10, "y": 100, "w": 220, "h": 80,
    "color": "#FF0000", "action": "Toggle"
})
vc_id += 1

# Section trigger buttons (right column, in a solo frame conceptually)
# These are individual buttons the user can tap to jump to a section
section_btns = [
    ("INTRO",           CH_INTRO_ID,   "#FFB464"),  # warm amber
    ("GROOVE BUILD",    CH_GROOVE_ID,  "#0088AA"),  # teal
    ("MELODIC RISE",    CH_MELODIC_ID, "#FF40AA"),  # pink
    ("PEAK",            CH_PEAK_ID,    "#FF8800"),  # amber/orange
    ("EMOTIONAL BREAK", CH_EMO_ID,     "#4444FF"),  # deep blue
    ("FINAL BUILD",     CH_BUILD_ID,   "#00CCCC"),  # cyan
    ("PEAK 2",          CH_PEAK2_ID,   "#FF00FF"),  # magenta
    ("OUTRO",           CH_OUTRO_ID,   "#FFB464"),  # warm amber
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

# Print summary
print(f"\n  Total scenes: {len(all_scenes)}")
print(f"  Total chasers: {len(all_chasers)}")
print(f"  Full show: {len(full_show_ids)} steps × {smooth(BPM, 4)[0]}ms = {len(full_show_ids) * smooth(BPM, 4)[0] / 1000:.0f}s ({len(full_show_ids) * smooth(BPM, 4)[0] / 60000:.1f} min)")
print(f"\n  Sections:")
sections_info = [
    ("Intro", 16), ("Groove Build", 16), ("Melodic Rise", 16), ("Peak", 32),
    ("Emotional Break", 16), ("Final Build", 16), ("Peak 2", 32), ("Outro", 16)
]
total_bars = 0
for name, bars in sections_info:
    dur_s = bars * BAR_MS / 1000
    print(f"    {name:20s}: {bars:3d} bars ({dur_s:.1f}s)")
    total_bars += bars
print(f"    {'TOTAL':20s}: {total_bars:3d} bars ({total_bars * BAR_MS / 1000:.1f}s = {total_bars * BAR_MS / 60000:.1f} min)")
