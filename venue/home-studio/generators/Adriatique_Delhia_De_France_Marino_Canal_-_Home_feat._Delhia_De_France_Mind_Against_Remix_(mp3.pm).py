#!/usr/bin/env python3
"""
Show Generator: Home feat. Delhia De France (Mind Against Remix)
================================================================
BPM: 120 | Duration: ~7:12 | Genre: Melodic techno / Afterlife

Aesthetic: Mind Against's "celestial techno" — dark, hypnotic, spiralling.
Monochromatic cold base (steel blue, slate, navy) with selective warm amber
reveals when vocals appear. Restraint is the design language.

Song Structure (grouped from analysis — raw segment labels are noisy):
  0:00 - 0:43  INTRO       (22 bars, rms=0.75) Cold space, establishing groove
  0:43 - 1:36  FIRST WAVE  (26 bars, rms=0.65) Melodic elements enter
  1:36 - 3:12  PEAK A      (48 bars, rms=0.84) Full driving energy
  3:12 - 5:20  BREAKDOWN   (64 bars, rms=0.31) Deep hypnotic descent — the heart
  5:20 - 6:40  PEAK B      (40 bars, rms=0.74) Rebuild, "coming home"
  6:40 - 7:17  OUTRO       (19 bars, rms→0)    Return to cold, fade to silence

Movement: Almost exclusively smooth crossfades. 4-bar minimum during groove,
8-bar during breakdown. Movers breathe (dimmer modulation), never strobe
except one brief climax moment.
"""

import json
import os
import sys
import bisect

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

# =============================================================================
# LOAD ANALYSIS DATA
# =============================================================================

SONG_STEM = "Adriatique_Delhia_De_France_Marino_Canal_-_Home_feat._Delhia_De_France_Mind_Against_Remix_(mp3.pm)"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")
DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")

with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]  # 120
beats = data["beats"]
downbeats = data["downbeats"]
segments = data["segments"]

# Energy arrays (beat-indexed, 0.0-1.0)
e_sub = data["energy"]["sub_bass"]
e_rms = data["energy"]["rms"]
e_high = data["energy"]["high"]

# Per-stem energy and onsets
vocal_e = data["stems"]["vocals"]["energy"]
vocal_onsets = data["stems"]["vocals"]["onsets"]
bass_onsets = data["stems"]["bass"]["onsets"]
drum_onsets = data["stems"]["drums"]["onsets"]
other_onsets = data["stems"]["other"]["onsets"]

BAR_MS = bpm_to_ms(BPM, 4)   # 2000ms
BEAT_MS = bpm_to_ms(BPM, 1)  # 500ms

# =============================================================================
# HELPERS
# =============================================================================

def beat_at(t):
    """Find the beat index closest to timestamp t."""
    idx = bisect.bisect_left(beats, t)
    if idx == 0:
        return 0
    if idx >= len(beats):
        return len(beats) - 1
    if abs(beats[idx] - t) < abs(beats[idx - 1] - t):
        return idx
    return idx - 1

def avg_energy(energy_arr, t_start, t_end):
    """Average energy between two timestamps."""
    i_start = beat_at(t_start)
    i_end = beat_at(t_end)
    if i_start >= i_end:
        return 0.0
    return sum(energy_arr[i_start:i_end]) / (i_end - i_start)

def vocal_present(t_start, t_end):
    """Check if vocal energy is significant in a time range."""
    avg_v = avg_energy(vocal_e, t_start, t_end)
    return avg_v > 0.02

def energy_to_dim(e, low=30, high=255):
    """Map energy (0-1) to dimmer value."""
    return int(low + (high - low) * min(1.0, max(0.0, e)))

# =============================================================================
# COLOR PALETTE — Afterlife-inspired: cold base, selective warm reveals
# =============================================================================

# Cold palette (default)
SLATE_BLUE = (60, 80, 130)
STEEL_GREY = (90, 100, 120)
COLD_WHITE = (180, 190, 210)
DEEP_NAVY = (15, 20, 50)
MUTED_VIOLET = (70, 40, 110)
DEEP_INDIGO = (30, 15, 80)
CHARCOAL = (30, 30, 40)

# Warm palette (vocal reveals only)
WARM_AMBER = (200, 140, 40)
DUSTY_GOLD = (180, 150, 60)

NOTHING = (0, 0, 0)

# =============================================================================
# MOVER POSITIONS — loaded from venue focus-positions.md
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# =============================================================================
# LOGICAL SECTIONS (grouped from noisy raw segments using energy data)
# =============================================================================

SECTIONS = [
    {"name": "INTRO",      "start": 0.0,    "end": 43.14,  "bars": 22},
    {"name": "FIRST_WAVE", "start": 43.14,  "end": 96.14,  "bars": 26},
    {"name": "PEAK_A",     "start": 96.14,  "end": 192.13, "bars": 48},
    {"name": "BREAKDOWN",  "start": 192.13, "end": 320.15, "bars": 64},
    {"name": "PEAK_B",     "start": 320.15, "end": 400.12, "bars": 40},
    {"name": "OUTRO",      "start": 400.12, "end": 437.67, "bars": 19},
]

# =============================================================================
# SCENE GENERATION
# =============================================================================

scenes = []
folder = "Home (Mind Against Remix)"

# Scene 0 = blackout (always)
scenes.append(scene("Blackout", *blackout_all(), path=folder))

steps = []  # (scene_id, (fade_ms, hold_ms))
scene_cache = {}

def get_or_create_scene(key, create_fn):
    """Cache scenes by key to avoid duplicates."""
    if key not in scene_cache:
        sc = create_fn()
        scene_cache[key] = len(scenes)
        scenes.append(sc)
    return scene_cache[key]


def make_atmosphere_scene(name, pos_key, energy, frost_val,
                          sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                          prof_color=PROF_BLUE,
                          par_rgb=SLATE_BLUE, miss_rgb=DEEP_NAVY,
                          ni3k_rgb=SLATE_BLUE, halo=H_OFF,
                          sharpy_dim=None, bsw_dim=None, prof_dim=None,
                          par_master=None,
                          prism=False, gobo=False,
                          lasers=False, strobe_sharpy=SHARPY_OPEN,
                          shutter_bsw=BSW_SHUT_OPEN,
                          ni3k_tilt=(64, 64, 64)):
    """Build an atmosphere scene — the workhorse for this show.

    Everything is smooth and controlled. Energy modulates dimmer/frost.
    """
    p = POS[pos_key]
    sp, st, bp, bt, pp, pt, ni_pan = p

    # Dimmer from energy unless overridden
    s_dim = sharpy_dim if sharpy_dim is not None else energy_to_dim(energy, low=40, high=220)
    b_dim = bsw_dim if bsw_dim is not None else energy_to_dim(energy, low=30, high=200)
    p_dim = prof_dim if prof_dim is not None else energy_to_dim(energy * 0.6, low=0, high=160)
    p_mst = par_master if par_master is not None else energy_to_dim(energy, low=20, high=200)

    prism_val = 128 if prism else 0
    prism_rot = 200 if prism else 0
    gobo_val = BSW_G1_3 if gobo else 0

    ni_r, ni_g, ni_b = ni3k_rgb
    ni_dim = energy_to_dim(energy * 0.5, low=0, high=180)
    t1, t2, t3 = ni3k_tilt

    laser_r = LASER_ON if lasers else LASER_OFF
    laser_g = LASER_ON if lasers else LASER_OFF
    laser_b = LASER_ON if lasers else LASER_OFF

    return scene(name,
        sharpy(pan=sp, tilt=st, strobe=strobe_sharpy, dim=s_dim,
               frost=frost_val, colormacro=sharpy_color, focus=128,
               prism1=prism_val, p1r=prism_rot),
        bsw(pan=bp, tilt=bt, color=bsw_color, shutter=shutter_bsw,
            dim=b_dim, frost=min(255, frost_val),
            prism=prism_val, prot=prism_rot,
            gobo1=gobo_val, focus=128),
        profile(pan=pp, tilt=pt, color=prof_color, dim=p_dim, focus=128),
        fourbar_solid(*par_rgb, master=p_mst),
        miss1(*miss_rgb, master=p_mst // 2),
        miss2(*miss_rgb, master=p_mst // 2),
        ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, rl=laser_r, gl=laser_g, bl=laser_b,
             dim=ni_dim, strobe=0),
        path=folder)


def make_dark_mover_scene(name, pos_key, active_mover, dim,
                           sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                           prof_color=PROF_BLUE, frost=200,
                           ni3k_rgb=DEEP_INDIGO, halo=H_OFF):
    """Scene with only one active mover, others dark but parked at same position."""
    p = POS[pos_key]
    sp, st, bp, bt, pp, pt, ni_pan = p

    ni_r, ni_g, ni_b = ni3k_rgb

    if active_mover == "sharpy":
        s = sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=dim,
                   frost=frost, colormacro=sharpy_color, focus=128)
        b = dark_bsw(pan=bp, tilt=bt)
        pr = dark_profile(pan=pp, tilt=pt)
    elif active_mover == "bsw":
        s = dark_sharpy(pan=sp, tilt=st)
        b = bsw(pan=bp, tilt=bt, color=bsw_color, shutter=BSW_SHUT_OPEN,
                dim=dim, frost=frost, focus=128)
        pr = dark_profile(pan=pp, tilt=pt)
    elif active_mover == "profile":
        s = dark_sharpy(pan=sp, tilt=st)
        b = dark_bsw(pan=bp, tilt=bt)
        pr = profile(pan=pp, tilt=pt, color=prof_color, dim=dim, focus=128)
    else:
        s = dark_sharpy(pan=sp, tilt=st)
        b = dark_bsw(pan=bp, tilt=bt)
        pr = dark_profile(pan=pp, tilt=pt)

    return scene(name, s, b, pr,
        fourbar_solid(*NOTHING),
        miss1(*NOTHING),
        miss2(*NOTHING),
        ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, dim=30 if sum(ni3k_rgb) > 0 else 0, strobe=0),
        path=folder)


# =============================================================================
# SECTION BUILDERS
# =============================================================================

def build_intro(sec):
    """INTRO (0:00-0:43, 22 bars): Cold space, establishing groove.

    Start near-dark, gradually raise dimmer. Movers at center, frosted beams.
    4BAR: slate blue wash. NI3K: faint blue LED glow.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000
    step_bars = 4  # 4-bar smooth crossfades

    step_num = 0
    while t < t_end - 0.5:
        next_t = min(t + bar_dur * step_bars, t_end)
        progress = (t - sec["start"]) / total_dur  # 0→1 across section
        energy = avg_energy(e_rms, t, next_t)

        # Gradually open up: start very dim, end at moderate
        dim_scale = 0.3 + 0.5 * progress
        frost = int(220 - 60 * progress)  # start very frosted, gradually sharpen

        # Stay at center, slight drift toward USC at end
        pos = "C" if progress < 0.6 else "USC"

        sid = get_or_create_scene(f"intro_{step_num}", lambda:
            make_atmosphere_scene(f"Intro {step_num}", pos,
                energy=energy * dim_scale, frost_val=frost,
                sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                prof_color=PROF_BLUE,
                par_rgb=SLATE_BLUE, miss_rgb=DEEP_NAVY,
                ni3k_rgb=SLATE_BLUE, halo=H_OFF,
                par_master=energy_to_dim(energy * dim_scale * 0.5, low=10, high=120)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))

        t = next_t
        step_num += 1


def build_first_wave(sec):
    """FIRST WAVE (0:43-1:36, 26 bars): Melodic elements enter.

    Movers begin slow L-R drift. Add violet undertones to pars.
    Profile comes on with teal fill. Energy dips slightly.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000
    step_bars = 4

    # Slow sweep path: C → SL → C → SR → C
    sweep_positions = ["C", "SL", "C", "SR", "C", "SL", "DSC"]
    step_num = 0

    while t < t_end - 0.5:
        next_t = min(t + bar_dur * step_bars, t_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)

        pos = sweep_positions[step_num % len(sweep_positions)]
        frost = int(180 - 40 * progress)

        # Add violet to pars as section progresses
        if progress < 0.5:
            par_rgb = SLATE_BLUE
            miss_rgb = DEEP_NAVY
        else:
            par_rgb = MUTED_VIOLET
            miss_rgb = DEEP_INDIGO

        # Warm accent if vocal present
        if has_vocal:
            par_rgb = DUSTY_GOLD
            miss_rgb = WARM_AMBER

        sid = get_or_create_scene(f"wave_{step_num}", lambda:
            make_atmosphere_scene(f"Wave {step_num}", pos,
                energy=energy * 0.8, frost_val=frost,
                sharpy_color=SHARPY_BLUE if not has_vocal else SHARPY_AMBER,
                bsw_color=BSW_TEAL,
                prof_color=PROF_TEAL,
                par_rgb=par_rgb, miss_rgb=miss_rgb,
                ni3k_rgb=SLATE_BLUE, halo=H_BLU))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))

        t = next_t
        step_num += 1


def build_peak_a(sec):
    """PEAK A (1:36-3:12, 48 bars): Full driving energy.

    Wider mover movements, warm amber reveals on vocal. Cross-beam effects.
    BSW prism on during high-energy moments. NI3K halo blue.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000
    step_bars = 2  # faster changes during peak

    # Wider sweep path with cross-beams
    sweep = ["DSC", "X", "SL", "C", "SR", "DSC", "X", "USC",
             "C", "DSR", "DSL", "C", "CEIL", "DSC", "SL", "SR",
             "X", "DSC", "C", "USC", "DSL", "X", "DSR", "C"]
    step_num = 0

    while t < t_end - 0.3:
        next_t = min(t + bar_dur * step_bars, t_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)

        pos = sweep[step_num % len(sweep)]
        frost = int(140 - 80 * energy)  # sharper when energy high
        use_prism = energy > 0.8

        # Color strategy: cold default, warm on vocal
        if has_vocal:
            s_color = SHARPY_AMBER
            par_rgb = WARM_AMBER
            miss_rgb = DUSTY_GOLD
        else:
            s_color = SHARPY_BLUE
            par_rgb = SLATE_BLUE
            miss_rgb = MUTED_VIOLET

        # Alternate 4BAR colors on 4-bar cycle
        cycle = (step_num // 2) % 2
        if cycle == 1 and not has_vocal:
            par_rgb = MUTED_VIOLET
            miss_rgb = SLATE_BLUE

        sid = get_or_create_scene(f"peakA_{step_num}", lambda:
            make_atmosphere_scene(f"Peak A {step_num}", pos,
                energy=energy, frost_val=frost,
                sharpy_color=s_color, bsw_color=BSW_BLUE,
                prof_color=PROF_TEAL,
                par_rgb=par_rgb, miss_rgb=miss_rgb,
                ni3k_rgb=SLATE_BLUE, halo=H_BLU,
                prism=use_prism,
                ni3k_tilt=(64, 64, 64) if not use_prism else (160, 180, 170)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))

        t = next_t
        step_num += 1

    # Reset to DSC before breakdown
    reset_sid = get_or_create_scene("peakA_reset", lambda:
        make_atmosphere_scene("Peak A Reset", "DSC",
            energy=0.5, frost_val=200,
            par_rgb=DEEP_NAVY, miss_rgb=DEEP_NAVY,
            ni3k_rgb=DEEP_NAVY, halo=H_OFF))
    steps.append((reset_sid, smooth(BPM, 2)))


def build_breakdown(sec):
    """BREAKDOWN (3:12-5:20, 64 bars): The heart of the track.

    Strip to near-nothing over first 8 bars. Then: single mover (Sharpy)
    with frosted beam, deep navy, very dim. Slow diamond sweep over 32 bars.
    NI3K barely visible deep indigo glow. All other fixtures dark.
    Gradual rebuild in final 16 bars.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000

    # Phase 1: Strip down (0-16 bars, ~32 seconds)
    strip_end = t + bar_dur * 16
    step_num = 0
    step_bars = 4

    while t < strip_end - 0.5:
        next_t = min(t + bar_dur * step_bars, strip_end)
        progress = (t - sec["start"]) / (strip_end - sec["start"])
        energy = avg_energy(e_rms, t, next_t)

        # Progressively dim everything
        dim_factor = max(0.05, 1.0 - progress * 0.9)

        sid = get_or_create_scene(f"bd_strip_{step_num}", lambda:
            make_atmosphere_scene(f"BD Strip {step_num}", "DSC",
                energy=energy * dim_factor, frost_val=220,
                sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                prof_color=PROF_BLUE,
                par_rgb=tuple(int(c * dim_factor) for c in DEEP_NAVY),
                miss_rgb=NOTHING,
                ni3k_rgb=tuple(int(c * dim_factor) for c in DEEP_INDIGO),
                halo=H_OFF,
                sharpy_dim=int(60 * dim_factor + 20),
                bsw_dim=int(40 * dim_factor),
                prof_dim=0,
                par_master=int(80 * dim_factor)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))
        t = next_t
        step_num += 1

    # Phase 2: Single mover diamond sweep (16-48 bars, ~64 seconds)
    # Sharpy alone, slow diamond: DSC → SR → USC → SL → DSC repeated
    diamond = ["DSC", "SR", "USC", "SL"]
    sweep_end = sec["start"] + bar_dur * 48
    step_bars = 8  # 8-bar crossfades — very slow

    while t < sweep_end - 0.5:
        next_t = min(t + bar_dur * step_bars, sweep_end)
        pos = diamond[step_num % len(diamond)]

        sid = get_or_create_scene(f"bd_sweep_{step_num}", lambda:
            make_dark_mover_scene(f"BD Sweep {step_num}", pos,
                active_mover="sharpy", dim=50,
                sharpy_color=SHARPY_BLUE, frost=220,
                ni3k_rgb=DEEP_INDIGO, halo=H_OFF))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))
        t = next_t
        step_num += 1

    # Phase 3: Gradual rebuild (48-64 bars, ~32 seconds)
    # Add fixtures back one at a time: BSW → NI3K halo → Profile → Pars
    rebuild_positions = ["C", "SL", "SR", "DSC"]
    rebuild_step = 0

    while t < t_end - 0.5:
        next_t = min(t + bar_dur * 4, t_end)
        rebuild_progress = (t - (sec["start"] + bar_dur * 48)) / (t_end - (sec["start"] + bar_dur * 48))
        rebuild_progress = max(0, min(1, rebuild_progress))
        energy = avg_energy(e_rms, t, next_t)

        pos = rebuild_positions[rebuild_step % len(rebuild_positions)]

        # Gradually add fixtures
        s_dim = int(40 + 80 * rebuild_progress)
        b_dim = int(60 * rebuild_progress) if rebuild_progress > 0.2 else 0
        p_dim = int(40 * rebuild_progress) if rebuild_progress > 0.5 else 0
        par_mst = int(60 * rebuild_progress) if rebuild_progress > 0.4 else 0

        halo_val = H_BLU if rebuild_progress > 0.3 else H_OFF

        p = POS[pos]
        sp, st, bp, bt, pp, pt, ni_pan = p

        sid = get_or_create_scene(f"bd_rebuild_{rebuild_step}", lambda:
            scene(f"BD Rebuild {rebuild_step}",
                sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=s_dim,
                       frost=int(200 - 40 * rebuild_progress),
                       colormacro=SHARPY_BLUE, focus=128),
                bsw(pan=bp, tilt=bt, color=BSW_BLUE,
                    shutter=BSW_SHUT_OPEN, dim=b_dim,
                    frost=200, focus=128) if b_dim > 0
                    else dark_bsw(pan=bp, tilt=bt),
                profile(pan=pp, tilt=pt, color=PROF_TEAL,
                        dim=p_dim, focus=128) if p_dim > 0
                    else dark_profile(pan=pp, tilt=pt),
                fourbar_solid(*DEEP_NAVY, master=par_mst),
                miss1(*DEEP_INDIGO, master=par_mst // 2),
                miss2(*DEEP_INDIGO, master=par_mst // 2),
                ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
                     r=SLATE_BLUE[0], g=SLATE_BLUE[1], b=SLATE_BLUE[2],
                     w=0, halo=halo_val, dim=int(40 * rebuild_progress),
                     strobe=0),
                path=folder))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))
        t = next_t
        rebuild_step += 1


def build_peak_b(sec):
    """PEAK B (5:20-6:40, 40 bars): Rebuild, "coming home."

    Warmer than Peak A — amber + blue cross-beam pairing.
    Full fixture involvement. Brief strobe accent at climax.
    NI3K lasers on at highest energy moment.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000
    step_bars = 2

    sweep = ["DSC", "SL", "X", "C", "SR", "DSC", "USC", "X",
             "DSL", "C", "DSR", "DSC", "CEIL", "C", "X", "DSC",
             "SL", "SR", "DSC", "C"]
    step_num = 0

    # Find climax point (highest energy in this section)
    climax_t = t
    climax_e = 0
    scan_t = t
    while scan_t < t_end:
        e = avg_energy(e_rms, scan_t, min(scan_t + bar_dur * 2, t_end))
        if e > climax_e:
            climax_e = e
            climax_t = scan_t
        scan_t += bar_dur * 2

    while t < t_end - 0.3:
        next_t = min(t + bar_dur * step_bars, t_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)

        pos = sweep[step_num % len(sweep)]
        frost = int(120 - 60 * energy)

        # Is this the climax?
        is_climax = abs(t - climax_t) < bar_dur * 2

        # Warmer palette than Peak A — "coming home" feeling
        if has_vocal or progress > 0.3:
            s_color = SHARPY_AMBER
            par_rgb = WARM_AMBER
            miss_rgb = DUSTY_GOLD
        else:
            s_color = SHARPY_BLUE
            par_rgb = SLATE_BLUE
            miss_rgb = MUTED_VIOLET

        use_lasers = is_climax and energy > 0.7
        use_strobe = is_climax and energy > 0.75
        use_prism = energy > 0.7

        sid = get_or_create_scene(f"peakB_{step_num}", lambda:
            make_atmosphere_scene(f"Peak B {step_num}", pos,
                energy=energy, frost_val=frost,
                sharpy_color=s_color, bsw_color=BSW_TEAL,
                prof_color=PROF_TEAL,
                par_rgb=par_rgb, miss_rgb=miss_rgb,
                ni3k_rgb=WARM_AMBER if has_vocal else SLATE_BLUE,
                halo=H_CYN,
                prism=use_prism, lasers=use_lasers,
                strobe_sharpy=SHARPY_STROBE_MED if use_strobe else SHARPY_OPEN,
                shutter_bsw=BSW_SHUT_STROBE_SLOW if use_strobe else BSW_SHUT_OPEN,
                ni3k_tilt=(160, 180, 170) if use_prism else (64, 64, 64)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))

        t = next_t
        step_num += 1


def build_outro(sec):
    """OUTRO (6:40-7:17, 19 bars): Return to cold, fade to silence.

    Progressive dimming. Movers converge to center.
    Final 8 bars: near-blackout, single blue glow fading.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000
    step_bars = 4
    step_num = 0

    while t < t_end - 0.5:
        next_t = min(t + bar_dur * step_bars, t_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)

        # Progressively dim and converge to center
        dim_factor = max(0.0, 1.0 - progress * 0.9)

        sid = get_or_create_scene(f"outro_{step_num}", lambda:
            make_atmosphere_scene(f"Outro {step_num}", "C",
                energy=energy * dim_factor, frost_val=220,
                sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                prof_color=PROF_BLUE,
                par_rgb=tuple(int(c * dim_factor) for c in SLATE_BLUE),
                miss_rgb=tuple(int(c * dim_factor) for c in DEEP_NAVY),
                ni3k_rgb=tuple(int(c * dim_factor) for c in DEEP_INDIGO),
                halo=H_BLU if progress < 0.5 else H_OFF,
                sharpy_dim=int(80 * dim_factor),
                bsw_dim=int(60 * dim_factor),
                prof_dim=int(30 * dim_factor),
                par_master=int(60 * dim_factor)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, smooth(BPM, bars_here)))
        t = next_t
        step_num += 1

    # Final blackout
    steps.append((0, smooth(BPM, 2)))


# =============================================================================
# MAIN: Build all sections
# =============================================================================

BUILDERS = {
    "INTRO": build_intro,
    "FIRST_WAVE": build_first_wave,
    "PEAK_A": build_peak_a,
    "BREAKDOWN": build_breakdown,
    "PEAK_B": build_peak_b,
    "OUTRO": build_outro,
}

print(f"Generating show: Home (Mind Against Remix)")
print(f"  BPM: {BPM}, Beats: {len(beats)}, Duration: {beats[-1]:.1f}s")
print()

for sec in SECTIONS:
    print(f"  Building {sec['name']:12s} ({sec['bars']:2d} bars, "
          f"{sec['start']:.1f}s–{sec['end']:.1f}s)")
    BUILDERS[sec["name"]](sec)

# =============================================================================
# BUILD CHASER AND WRITE
# =============================================================================

print(f"\nTotal scenes: {len(scenes)} (cache hits: {sum(1 for k in scene_cache if scene_cache[k] < len(scenes)) - len(set(scene_cache.values()))})")
print(f"Total chaser steps: {len(steps)}")

total_ms = sum(fi + ho for _, (fi, ho) in steps)
print(f"Total duration: {total_ms/1000:.1f}s (target: ~438s)")

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Home (Mind Against Remix)", scene_ids, timing,
                           run_order="SingleShot", path=folder)

# VC buttons
vc_buttons = [
    {"caption": "HOME (Mind Against Remix)", "vc_id": 0,
     "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#1A2844", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

output_path = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(output_path, scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
