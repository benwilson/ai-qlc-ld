#!/usr/bin/env python3
"""
Show Generator: Lorn - Acid Rain (Skeler Remix) — v3 Data-Driven
=================================================================
BPM: 115 | Duration: ~4:23 | Genre: Dark electronic / wave

Fully reactive to analysis data: energy envelopes drive intensity,
stem onsets trigger individual light cues, spectral dynamics control
movement speed and color temperature.

Creative Direction:
  - Every bass hit triggers a visible reaction (strobe, color snap, position snap)
  - Quiet sections: individual synth/piano onsets fire single fixtures
  - Energy curves drive dimmer levels and movement speed
  - 4BAR + Missyees snap colors on drum/bass onsets (beat-reactive)
  - NI3K halo follows energy, lasers reserved for peak moments
  - Movers react to spectral centroid (brighter sound = wider spread)
  - Color palette shifts per segment (cool→corrupt→aggressive→echo)

Song Structure (from allin1 analysis — 14 segments):
  0:00 - 0:02  start      (~0 bars)   Click
  0:02 - 18.6  intro      (9 bars)    False calm — sparse synth, near-silence
  18.6 - 37.2  intro      (9 bars)    Layers building, sub-bass enters
  37.2 - 55.9  intro      (9 bars)    Drums enter, corruption complete
  55.9 - 82.8  solo       (13 bars)   Main melodic solo — bass hits begin
  82.8 - 95.2  solo       (6 bars)    Melodic climax
  95.2 - 111.7 chorus     (8 bars)    Peak intensity
  111.7 - 128.3 solo      (8 bars)    Melodic decay
  128.3 - 151.8 break     (11 bars)   Sparse, minimal — individual note triggers
  151.8 - 180.8 solo      (14 bars)   Extended melodic section, sub-bass peak
  180.8 - 204.8 solo      (12 bars)   Synth exploration, building
  204.8 - 223.4 solo      (9 bars)    Heavy drums build toward climax
  223.4 - 242.1 chorus    (9 bars)    Final climax — maximum everything
  242.1 - 262.8 outro     (10 bars)   Fade to silence
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

DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", "Lorn - Acid Rain (Skeler Remix).json")

with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]  # 115
beats = data["beats"]
downbeats = data["downbeats"]
beat_positions = data["beat_positions"]
segments = data["segments"]

# Energy arrays (beat-indexed, 0.0–1.0)
e_sub = data["energy"]["sub_bass"]
e_bass = data["energy"]["bass"]
e_mid = data["energy"]["mid"]
e_high = data["energy"]["high"]
e_rms = data["energy"]["rms"]

# Dynamics (beat-indexed)
centroid = data["dynamics"]["spectral_centroid"]
flux = data["dynamics"]["spectral_flux"]
onset_str = data["dynamics"]["onset_strength"]

# Per-stem onsets (timestamps in seconds)
bass_onsets = data["stems"]["bass"]["onsets"]
drum_onsets = data["stems"]["drums"]["onsets"]
vocal_onsets = data["stems"]["vocals"]["onsets"]
other_onsets = data["stems"]["other"]["onsets"]  # synth/piano/melody

# Per-stem energy (beat-indexed)
bass_stem_e = data["stems"]["bass"]["energy"]
drum_stem_e = data["stems"]["drums"]["energy"]
other_stem_e = data["stems"]["other"]["energy"]

BAR_MS = bpm_to_ms(BPM, 4)   # ~2087ms
BEAT_MS = bpm_to_ms(BPM, 1)  # ~522ms

# =============================================================================
# HELPER: Find beat index closest to a timestamp
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

def bars_between(t_start, t_end):
    """Number of bars between two timestamps."""
    return (t_end - t_start) / (BAR_MS / 1000)

def onsets_in_range(onset_list, t_start, t_end):
    """Get onsets falling within a time range."""
    lo = bisect.bisect_left(onset_list, t_start)
    hi = bisect.bisect_right(onset_list, t_end)
    return onset_list[lo:hi]

def avg_energy(energy_arr, t_start, t_end):
    """Average energy between two timestamps."""
    i_start = beat_at(t_start)
    i_end = beat_at(t_end)
    if i_start >= i_end:
        return 0.0
    return sum(energy_arr[i_start:i_end]) / (i_end - i_start)

def peak_energy(energy_arr, t_start, t_end):
    """Peak energy between two timestamps."""
    i_start = beat_at(t_start)
    i_end = beat_at(t_end)
    if i_start >= i_end:
        return 0.0
    return max(energy_arr[i_start:i_end])

# =============================================================================
# COLOR PALETTES — segment-driven
# =============================================================================

# False calm (intros 1-2)
CALM_BLUE = (40, 80, 180)
CALM_TEAL = (20, 100, 140)

# Corruption (intro 3)
SICK_GREEN = (60, 140, 20)
SICK_AMBER = (180, 100, 10)
BRUISE_PURPLE = (90, 10, 120)

# Solo / aggressive
BLOOD_RED = (180, 0, 0)
DEEP_RED = (120, 0, 10)
VOID_BLUE = (0, 10, 80)
POISON_GREEN = (0, 100, 20)
COLD_WHITE = (200, 200, 220)
VIOLET = (100, 0, 180)
DARK_CYAN = (0, 80, 100)

# Break
EERIE_DIM = (10, 5, 30)

# Outro
DEAD_BLUE = (15, 30, 60)
DEAD_TEAL = (8, 40, 50)

NOTHING = (0, 0, 0)

# Segment-to-palette mapping: each segment gets a primary and accent color
# plus matching color wheel values for movers
SEGMENT_PALETTES = {
    0:  {"rgb1": CALM_BLUE,    "rgb2": CALM_TEAL,     "bsw": BSW_BLUE,   "sharpy": SHARPY_BLUE,   "prof": PROF_BLUE,   "halo": H_BLU},
    1:  {"rgb1": CALM_BLUE,    "rgb2": CALM_TEAL,     "bsw": BSW_BLUE,   "sharpy": SHARPY_BLUE,   "prof": PROF_BLUE,   "halo": H_BLU},
    2:  {"rgb1": CALM_TEAL,    "rgb2": SICK_GREEN,    "bsw": BSW_TEAL,   "sharpy": SHARPY_TEAL,   "prof": PROF_TEAL,   "halo": H_CYN},
    3:  {"rgb1": SICK_GREEN,   "rgb2": BRUISE_PURPLE, "bsw": BSW_GREEN,  "sharpy": SHARPY_GREEN,  "prof": PROF_GREEN,  "halo": H_GRN},
    4:  {"rgb1": BLOOD_RED,    "rgb2": DEEP_RED,      "bsw": BSW_RED,    "sharpy": SHARPY_RED,    "prof": PROF_RED,    "halo": H_RED},
    5:  {"rgb1": VIOLET,       "rgb2": BLOOD_RED,     "bsw": BSW_MAG,    "sharpy": SHARPY_PURPLE, "prof": PROF_PINK,   "halo": H_PNK},
    6:  {"rgb1": COLD_WHITE,   "rgb2": BLOOD_RED,     "bsw": BSW_WHITE,  "sharpy": SHARPY_WHITE,  "prof": PROF_WHITE,  "halo": H_RGB},
    7:  {"rgb1": DARK_CYAN,    "rgb2": VOID_BLUE,     "bsw": BSW_TEAL,   "sharpy": SHARPY_TEAL,   "prof": PROF_TEAL,   "halo": H_CYN},
    8:  {"rgb1": EERIE_DIM,    "rgb2": NOTHING,       "bsw": BSW_BLUE,   "sharpy": SHARPY_BLUE,   "prof": PROF_BLUE,   "halo": H_OFF},
    9:  {"rgb1": DEEP_RED,     "rgb2": POISON_GREEN,  "bsw": BSW_RED,    "sharpy": SHARPY_RED,    "prof": PROF_RED,    "halo": H_RED},
    10: {"rgb1": VIOLET,       "rgb2": DARK_CYAN,     "bsw": BSW_MAG,    "sharpy": SHARPY_PURPLE, "prof": PROF_PINK,   "halo": H_PNK},
    11: {"rgb1": BLOOD_RED,    "rgb2": VIOLET,        "bsw": BSW_RED,    "sharpy": SHARPY_RED,    "prof": PROF_RED,    "halo": H_RED},
    12: {"rgb1": COLD_WHITE,   "rgb2": BLOOD_RED,     "bsw": BSW_WHITE,  "sharpy": SHARPY_WHITE,  "prof": PROF_WHITE,  "halo": H_RGB},
    13: {"rgb1": DEAD_BLUE,    "rgb2": DEAD_TEAL,     "bsw": BSW_BLUE,   "sharpy": SHARPY_BLUE,   "prof": PROF_BLUE,   "halo": H_BLU},
}

# =============================================================================
# MOVER POSITIONS
# =============================================================================

S_C = {"pan": 153, "tilt": 0}
B_C = {"pan": 7,   "tilt": 19}
P_C = {"pan": 0,   "tilt": 123}

# Position vocabulary for reactive movement
MOVER_POSITIONS = [
    # (sharpy, bsw, profile) — various configurations
    ({"pan": 153, "tilt": 0},   {"pan": 7,   "tilt": 19},  {"pan": 0,   "tilt": 123}),  # 0: center
    ({"pan": 220, "tilt": 15},  {"pan": 80,  "tilt": 30},  {"pan": 60,  "tilt": 100}),  # 1: spread left
    ({"pan": 80,  "tilt": 15},  {"pan": 200, "tilt": 5},   {"pan": 200, "tilt": 100}),  # 2: spread right
    ({"pan": 80,  "tilt": 10},  {"pan": 200, "tilt": 10},  {"pan": 180, "tilt": 100}),  # 3: cross
    ({"pan": 220, "tilt": 20},  {"pan": 80,  "tilt": 30},  {"pan": 50,  "tilt": 90}),   # 4: wide
    ({"pan": 153, "tilt": 40},  {"pan": 7,   "tilt": 50},  {"pan": 0,   "tilt": 80}),   # 5: high
    ({"pan": 153, "tilt": 245}, {"pan": 7,   "tilt": 5},   {"pan": 0,   "tilt": 160}),  # 6: low/audience
    ({"pan": 130, "tilt": 20},  {"pan": 40,  "tilt": 10},  {"pan": 35,  "tilt": 110}),  # 7: tight cluster
    ({"pan": 200, "tilt": 30},  {"pan": 200, "tilt": 25},  {"pan": 200, "tilt": 95}),   # 8: all right
    ({"pan": 100, "tilt": 30},  {"pan": 100, "tilt": 25},  {"pan": 100, "tilt": 95}),   # 9: all left
]

# =============================================================================
# SCENE GENERATION ENGINE
# =============================================================================

scenes = []
folder = "Acid Rain"

# Always scene 0 = blackout
scenes.append(scene("Blackout", *blackout_all(), path=folder))

def get_segment_index(t):
    """Which segment does timestamp t fall in?"""
    for i, seg in enumerate(segments):
        if seg["start"] <= t < seg["end"]:
            return i
    return len(segments) - 1

def energy_to_dim(e, low=30, high=255):
    """Map energy (0-1) to dimmer value."""
    return int(low + (high - low) * min(1.0, max(0.0, e)))

def energy_to_master(e, low=20, high=255):
    """Map energy (0-1) to master value for static fixtures."""
    return int(low + (high - low) * min(1.0, max(0.0, e)))

def pick_position(beat_idx, energy_val):
    """Pick a mover position based on beat index and energy.
    Higher energy = more extreme positions. Beat index adds variety."""
    if energy_val < 0.15:
        # Low energy: center or tight
        return MOVER_POSITIONS[beat_idx % 2 * 7]  # alternates 0, 7
    elif energy_val < 0.4:
        # Medium: spread or cross
        options = [1, 2, 3, 7]
        return MOVER_POSITIONS[options[beat_idx % len(options)]]
    elif energy_val < 0.7:
        # High: wide, high/low
        options = [4, 5, 6, 3, 8, 9]
        return MOVER_POSITIONS[options[beat_idx % len(options)]]
    else:
        # Peak: extreme positions
        options = [4, 6, 8, 9, 5, 3]
        return MOVER_POSITIONS[options[beat_idx % len(options)]]

def make_reactive_scene(name, beat_idx, seg_idx, is_accent=False,
                         strobe_movers=False, lasers=False,
                         prism=False, gobo=False):
    """Generate a scene reactive to the analysis data at a given beat.

    Reads energy/dynamics at beat_idx and segment palette at seg_idx to
    determine colors, intensity, positions, and effects.
    """
    pal = SEGMENT_PALETTES.get(seg_idx, SEGMENT_PALETTES[0])

    # Energy at this beat
    rms = e_rms[beat_idx] if beat_idx < len(e_rms) else 0
    sub = e_sub[beat_idx] if beat_idx < len(e_sub) else 0
    bass_e = e_bass[beat_idx] if beat_idx < len(e_bass) else 0
    high_e = e_high[beat_idx] if beat_idx < len(e_high) else 0
    flux_v = float(flux[beat_idx]) if beat_idx < len(flux) else 0

    # Dimmer from energy
    mover_dim = energy_to_dim(rms, low=40, high=255)
    par_master = energy_to_master(rms, low=20, high=255)

    # Position from energy + beat variety
    s_pos, b_pos, p_pos = pick_position(beat_idx, rms)

    # Frost: inverse of energy (more energy = less frost = sharper beams)
    frost_val = int(200 * (1.0 - min(1.0, rms)))

    # Effects
    prism_val = 128 if prism or rms > 0.7 else 0
    prism_rot = 200 if prism_val > 0 else 0
    gobo_val = BSW_G1_3 if gobo or (rms > 0.5 and beat_idx % 8 < 4) else 0

    # Strobe on accent beats
    s_strobe = SHARPY_STROBE_FAST if strobe_movers else SHARPY_OPEN
    b_shutter = BSW_SHUT_STROBE_FAST if strobe_movers else BSW_SHUT_OPEN

    # NI3K
    ni_r, ni_g, ni_b = pal["rgb1"]
    ni_dim = energy_to_dim(rms, low=10, high=255)
    halo = pal["halo"]

    # Lasers only at peak moments
    laser_r = LASER_ON if lasers else LASER_OFF
    laser_g = LASER_ON if lasers else LASER_OFF
    laser_b = LASER_ON if lasers else LASER_OFF

    # 4BAR: alternate primary/accent on beat parity
    if is_accent:
        bar_fix = fourbar_solid(*COLD_WHITE, master=255)
        m1_fix = miss1(*COLD_WHITE, master=255)
        m2_fix = miss2(*COLD_WHITE, master=255)
    elif beat_idx % 2 == 0:
        bar_fix = fourbar_pairs(pal["rgb1"][0], pal["rgb1"][1], pal["rgb1"][2],
                                pal["rgb2"][0], pal["rgb2"][1], pal["rgb2"][2],
                                master=par_master)
        m1_fix = miss1(*pal["rgb1"], master=par_master)
        m2_fix = miss2(*pal["rgb2"], master=par_master)
    else:
        bar_fix = fourbar_pairs(pal["rgb2"][0], pal["rgb2"][1], pal["rgb2"][2],
                                pal["rgb1"][0], pal["rgb1"][1], pal["rgb1"][2],
                                master=par_master)
        m1_fix = miss1(*pal["rgb2"], master=par_master)
        m2_fix = miss2(*pal["rgb1"], master=par_master)

    return scene(name,
        sharpy(pan=s_pos["pan"], tilt=s_pos["tilt"],
               strobe=s_strobe, dim=mover_dim, frost=frost_val,
               colormacro=pal["sharpy"],
               prism1=prism_val, p1r=prism_rot,
               gobo=gobo_val, focus=128),
        bsw(pan=b_pos["pan"], tilt=b_pos["tilt"],
            color=pal["bsw"], shutter=b_shutter, dim=mover_dim,
            frost=min(255, frost_val), prism=prism_val, prot=prism_rot,
            gobo1=gobo_val, focus=128),
        profile(pan=p_pos["pan"], tilt=p_pos["tilt"],
                color=pal["prof"], dim=mover_dim,
                prism=prism_val // 2, focus=128),
        bar_fix, m1_fix, m2_fix,
        ni3k(pan=128, t1=64, t2=64, t3=64,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, rl=laser_r, gl=laser_g, bl=laser_b,
             dim=ni_dim, strobe=0),
        path=folder)


def make_onset_scene(name, onset_time, seg_idx, fixture_focus="other"):
    """Generate a scene triggered by an individual onset (synth note, bass hit).

    Lighter than a full reactive scene — used for individual note triggers
    in quiet sections.
    """
    pal = SEGMENT_PALETTES.get(seg_idx, SEGMENT_PALETTES[0])
    bi = beat_at(onset_time)
    rms = e_rms[bi] if bi < len(e_rms) else 0

    # For quiet sections, use single fixtures with punchy colors
    dim = energy_to_dim(max(0.3, rms), low=80, high=255)

    # Cycle through position vocabulary based on onset index
    pos_idx = hash(str(onset_time)) % len(MOVER_POSITIONS)
    s_pos, b_pos, p_pos = MOVER_POSITIONS[pos_idx]

    if fixture_focus == "bass":
        # Bass hit: sub-bass reaction — all movers converge, red flash
        return scene(name,
            sharpy(pan=S_C["pan"], tilt=S_C["tilt"],
                   strobe=SHARPY_OPEN, dim=dim,
                   colormacro=pal["sharpy"], focus=128),
            bsw(pan=B_C["pan"], tilt=B_C["tilt"],
                color=pal["bsw"], shutter=BSW_SHUT_OPEN, dim=dim,
                focus=128),
            profile(pan=P_C["pan"], tilt=P_C["tilt"],
                    color=pal["prof"], dim=dim, focus=128),
            fourbar_solid(*pal["rgb1"], master=energy_to_master(max(0.4, rms))),
            *miss_both(*pal["rgb1"], master=energy_to_master(max(0.3, rms))),
            ni3k(pan=128, t1=64, t2=64, t3=64,
                 r=pal["rgb1"][0], g=pal["rgb1"][1], b=pal["rgb1"][2],
                 halo=pal["halo"], dim=dim, strobe=0),
            path=folder)
    else:
        # Melodic onset: single mover spot + par accent
        # Rotate which mover is the "lead" based on onset position
        onset_mod = hash(str(onset_time)) % 3
        s_dim = dim if onset_mod == 0 else 0
        b_dim = dim if onset_mod == 1 else 0
        p_dim = dim if onset_mod == 2 else 0

        # The non-lead fixtures stay dark or very dim
        return scene(name,
            sharpy(pan=s_pos["pan"], tilt=s_pos["tilt"],
                   strobe=SHARPY_OPEN, dim=s_dim,
                   colormacro=pal["sharpy"], frost=60, focus=128),
            bsw(pan=b_pos["pan"], tilt=b_pos["tilt"],
                color=pal["bsw"], shutter=BSW_SHUT_OPEN, dim=b_dim,
                frost=80, focus=128),
            profile(pan=p_pos["pan"], tilt=p_pos["tilt"],
                    color=pal["prof"], dim=p_dim, focus=128),
            fourbar(pal["rgb1"][0] if onset_mod == 0 else 0,
                    pal["rgb1"][1] if onset_mod == 0 else 0,
                    pal["rgb1"][2] if onset_mod == 0 else 0,
                    pal["rgb1"][0] if onset_mod == 1 else 0,
                    pal["rgb1"][1] if onset_mod == 1 else 0,
                    pal["rgb1"][2] if onset_mod == 1 else 0,
                    pal["rgb1"][0] if onset_mod == 2 else 0,
                    pal["rgb1"][1] if onset_mod == 2 else 0,
                    pal["rgb1"][2] if onset_mod == 2 else 0,
                    pal["rgb2"][0], pal["rgb2"][1], pal["rgb2"][2],
                    master=energy_to_master(max(0.3, rms))),
            miss1(*pal["rgb2"] if onset_mod % 2 == 0 else NOTHING,
                  master=60),
            miss2(*pal["rgb2"] if onset_mod % 2 == 1 else NOTHING,
                  master=60),
            ni3k(pan=128, t1=64, t2=64, t3=64,
                 r=pal["rgb1"][0] // 4, g=pal["rgb1"][1] // 4,
                 b=pal["rgb1"][2] // 4,
                 halo=pal["halo"], dim=dim // 3, strobe=0),
            path=folder)


# =============================================================================
# BUILD SHOW: Walk through segments and generate scenes + chaser steps
# =============================================================================

steps = []  # (scene_id, (fade_ms, hold_ms))

# Track scene creation to avoid duplicates for reused looks
scene_cache = {}

def get_or_create_scene(key, create_fn):
    """Cache scenes by key to avoid duplicates."""
    if key not in scene_cache:
        sc = create_fn()
        scene_cache[key] = len(scenes)
        scenes.append(sc)
    return scene_cache[key]


def process_segment(seg_idx, seg):
    """Generate scenes and chaser steps for one segment."""
    t_start = seg["start"]
    t_end = seg["end"]
    label = seg["label"]
    duration = t_end - t_start
    n_bars = bars_between(t_start, t_end)

    if duration < 0.1:
        return  # Skip zero-length segments

    seg_rms = avg_energy(e_rms, t_start, t_end)
    seg_sub = avg_energy(e_sub, t_start, t_end)
    seg_peak = peak_energy(e_rms, t_start, t_end)

    # Get onsets in this segment
    seg_bass_onsets = onsets_in_range(bass_onsets, t_start, t_end)
    seg_other_onsets = onsets_in_range(other_onsets, t_start, t_end)
    seg_drum_onsets = onsets_in_range(drum_onsets, t_start, t_end)

    print(f"  Seg {seg_idx:2d} [{t_start:6.1f}–{t_end:6.1f}] {label:8s} "
          f"| {n_bars:5.1f} bars | rms={seg_rms:.2f} peak={seg_peak:.2f} "
          f"| bass={len(seg_bass_onsets)} drum={len(seg_drum_onsets)} "
          f"other={len(seg_other_onsets)}")

    # =========================================================================
    # STRATEGY per segment type
    # =========================================================================

    if label == "intro" and seg_rms < 0.2:
        # --- QUIET INTRO: individual synth onsets trigger lights ---
        _build_sparse_section(seg_idx, t_start, t_end, seg_other_onsets,
                              seg_bass_onsets)

    elif label == "intro":
        # --- BUILDING INTRO: bar-level looks with onset accents ---
        _build_building_section(seg_idx, t_start, t_end, seg_bass_onsets,
                                seg_other_onsets, n_bars)

    elif label == "break":
        # --- BREAK: sparse, eerie, individual triggers ---
        _build_sparse_section(seg_idx, t_start, t_end, seg_other_onsets,
                              seg_bass_onsets, eerie=True)

    elif label == "chorus":
        # --- CHORUS: maximum reactivity, strobes on bass, prisms ---
        _build_peak_section(seg_idx, t_start, t_end, seg_bass_onsets,
                            seg_drum_onsets, n_bars)

    elif label == "solo":
        # --- SOLO: melodic reactivity, bass triggers, movement ---
        _build_melodic_section(seg_idx, t_start, t_end, seg_bass_onsets,
                               seg_other_onsets, n_bars)

    elif label in ("outro", "end"):
        # --- OUTRO: fading, returning to calm ---
        _build_outro_section(seg_idx, t_start, t_end, seg_other_onsets, n_bars)

    else:
        # Fallback: treat as solo
        _build_melodic_section(seg_idx, t_start, t_end, seg_bass_onsets,
                               seg_other_onsets, n_bars)


def _build_sparse_section(seg_idx, t_start, t_end, melody_onsets, bass_hits,
                           eerie=False):
    """Sparse section: individual onsets fire individual fixtures.

    Each synth/piano note gets its own scene with a single fixture lit.
    Bass hits get a converge-center reaction.
    """
    # Combine and sort all onsets
    events = [(t, "melody") for t in melody_onsets]
    events += [(t, "bass") for t in bass_hits]
    events.sort(key=lambda x: x[0])

    if not events:
        # No onsets at all — hold blackout or near-blackout
        sid = get_or_create_scene(f"sparse_dark_{seg_idx}", lambda:
            make_reactive_scene(f"Sparse Dark {seg_idx}",
                                beat_at((t_start + t_end) / 2), seg_idx))
        bars = bars_between(t_start, t_end)
        steps.append((sid, smooth(BPM, max(1, bars))))
        return

    # Walk through events, creating scenes for each
    prev_time = t_start
    for i, (t, etype) in enumerate(events):
        # Gap before this onset: hold darkness or previous scene
        gap = t - prev_time
        if gap > 0.3:  # More than ~half a beat of silence
            dark_sid = get_or_create_scene(
                f"dark_{seg_idx}_{i}", lambda:
                scene(f"Dark Gap {seg_idx}-{i}",
                      sharpy(pan=S_C["pan"], tilt=S_C["tilt"],
                             strobe=SHARPY_OPEN, dim=0),
                      bsw(pan=B_C["pan"], tilt=B_C["tilt"],
                          shutter=BSW_SHUT_OPEN, dim=0),
                      profile(pan=P_C["pan"], tilt=P_C["tilt"], dim=0),
                      fourbar_solid(*NOTHING),
                      *miss_both(*NOTHING),
                      ni3k(pan=128, r=0, g=0, b=0,
                           halo=H_OFF if not eerie else H_BLU,
                           dim=10 if eerie else 0, strobe=0),
                      path=folder))
            gap_ms = int(gap * 1000)
            steps.append((dark_sid, (0, gap_ms)))

        # The onset itself: create a triggered scene
        onset_key = f"onset_{seg_idx}_{etype}_{i}"
        focus = "bass" if etype == "bass" else "other"
        onset_sid = get_or_create_scene(onset_key, lambda:
            make_onset_scene(f"Hit {seg_idx}-{i} ({etype})",
                             t, seg_idx, fixture_focus=focus))

        # Hold for ~1 beat or until next event
        if i + 1 < len(events):
            hold_ms = int((events[i + 1][0] - t) * 1000)
        else:
            hold_ms = int((t_end - t) * 1000)
        hold_ms = max(100, min(hold_ms, BEAT_MS * 4))

        steps.append((onset_sid, (50, hold_ms - 50)))
        prev_time = t + hold_ms / 1000


def _build_building_section(seg_idx, t_start, t_end, bass_hits,
                             melody_onsets, n_bars):
    """Building section: bar-level looks that evolve with energy.

    Every 2 bars, create a new scene based on the energy at that point.
    Bass hits within the section get snap reactions.
    """
    bar_dur = BAR_MS / 1000  # seconds per bar
    t = t_start

    step_num = 0
    while t < t_end - 0.5:
        bi = beat_at(t)
        # Check for bass hits in the next 2 bars
        next_t = min(t + bar_dur * 2, t_end)
        hits_here = onsets_in_range(bass_hits, t, next_t)

        if hits_here:
            # Split: smooth lead-in, snap on bass hit, continue
            hit_t = hits_here[0]
            pre_gap = hit_t - t

            if pre_gap > 0.5:
                # Smooth scene before the hit
                pre_sid = get_or_create_scene(
                    f"build_pre_{seg_idx}_{step_num}", lambda:
                    make_reactive_scene(f"Build {seg_idx}-{step_num}",
                                        bi, seg_idx))
                steps.append((pre_sid, (int(pre_gap * 500), int(pre_gap * 500))))

            # Snap on the bass hit
            hit_bi = beat_at(hit_t)
            hit_sid = get_or_create_scene(
                f"build_hit_{seg_idx}_{step_num}", lambda:
                make_reactive_scene(f"Build Hit {seg_idx}-{step_num}",
                                    hit_bi, seg_idx, is_accent=True))
            post_gap = next_t - hit_t
            steps.append((hit_sid, (0, int(post_gap * 1000))))
        else:
            # No bass hit: smooth crossfade over 2 bars
            sid = get_or_create_scene(
                f"build_{seg_idx}_{step_num}", lambda:
                make_reactive_scene(f"Build {seg_idx}-{step_num}",
                                    bi, seg_idx))
            bars_here = bars_between(t, next_t)
            steps.append((sid, smooth(BPM, max(1, bars_here))))

        t = next_t
        step_num += 1


def _build_melodic_section(seg_idx, t_start, t_end, bass_hits,
                            melody_onsets, n_bars):
    """Melodic solo section: movers react to melody, bass hits get snaps.

    Scenes change every 1-2 bars. Bass hits within get instant color flash.
    Melody density modulates movement complexity.
    """
    bar_dur = BAR_MS / 1000
    # Determine step size from energy: higher energy = faster changes
    seg_rms = avg_energy(e_rms, t_start, t_end)
    step_bars = 2 if seg_rms < 0.5 else 1.5 if seg_rms < 0.7 else 1

    t = t_start
    step_num = 0

    while t < t_end - 0.3:
        bi = beat_at(t)
        next_t = min(t + bar_dur * step_bars, t_end)
        hits_here = onsets_in_range(bass_hits, t, next_t)

        # Determine if this is a high-energy moment
        local_peak = peak_energy(e_rms, t, next_t)
        use_prism = local_peak > 0.65
        use_gobo = local_peak > 0.5

        if hits_here and len(hits_here) > 0:
            hit_t = hits_here[0]
            pre_gap = hit_t - t

            # Scene before bass hit
            if pre_gap > 0.4:
                pre_sid = get_or_create_scene(
                    f"solo_pre_{seg_idx}_{step_num}", lambda:
                    make_reactive_scene(f"Solo {seg_idx}-{step_num}",
                                        bi, seg_idx,
                                        prism=use_prism, gobo=use_gobo))
                steps.append((pre_sid, smooth(BPM, max(0.5, bars_between(t, hit_t)))))

            # SNAP on bass hit
            hit_bi = beat_at(hit_t)
            hit_sid = get_or_create_scene(
                f"solo_hit_{seg_idx}_{step_num}", lambda:
                make_reactive_scene(f"Solo Hit {seg_idx}-{step_num}",
                                    hit_bi, seg_idx,
                                    is_accent=True,
                                    strobe_movers=(local_peak > 0.7),
                                    prism=use_prism))
            post_dur = next_t - hit_t
            steps.append((hit_sid, (0, int(post_dur * 1000))))
        else:
            # Smooth evolution
            sid = get_or_create_scene(
                f"solo_{seg_idx}_{step_num}", lambda:
                make_reactive_scene(f"Solo {seg_idx}-{step_num}",
                                    bi, seg_idx,
                                    prism=use_prism, gobo=use_gobo))
            bars_here = bars_between(t, next_t)
            steps.append((sid, smooth(BPM, max(0.5, bars_here))))

        t = next_t
        step_num += 1


def _build_peak_section(seg_idx, t_start, t_end, bass_hits,
                         drum_hits, n_bars):
    """Peak/chorus section: maximum reactivity.

    Every bass hit = strobe snap. Every 2 beats = position change.
    Prisms and gobos always on. Lasers for the biggest moments.
    """
    bar_dur = BAR_MS / 1000
    beat_dur = BEAT_MS / 1000

    # For chorus, step every beat for maximum reactivity
    t = t_start
    step_num = 0

    while t < t_end - 0.2:
        bi = beat_at(t)
        next_t = min(t + beat_dur * 2, t_end)  # 2-beat steps

        local_peak = peak_energy(e_rms, t, next_t)
        local_sub = peak_energy(e_sub, t, next_t)
        has_bass = len(onsets_in_range(bass_hits, t, next_t)) > 0
        use_lasers = local_sub > 0.8

        if has_bass:
            # STROBE SNAP on bass hit
            sid = get_or_create_scene(
                f"peak_hit_{seg_idx}_{step_num}", lambda:
                make_reactive_scene(f"Peak Hit {seg_idx}-{step_num}",
                                    bi, seg_idx,
                                    is_accent=True,
                                    strobe_movers=True,
                                    lasers=use_lasers,
                                    prism=True, gobo=True))
            dur_ms = int((next_t - t) * 1000)
            steps.append((sid, (0, dur_ms)))
        else:
            # Intense look without strobe
            sid = get_or_create_scene(
                f"peak_{seg_idx}_{step_num}", lambda:
                make_reactive_scene(f"Peak {seg_idx}-{step_num}",
                                    bi, seg_idx,
                                    lasers=use_lasers,
                                    prism=True, gobo=True))
            dur_ms = int((next_t - t) * 1000)
            steps.append((sid, (100, dur_ms - 100)))

        t = next_t
        step_num += 1


def _build_outro_section(seg_idx, t_start, t_end, melody_onsets, n_bars):
    """Outro: fading back to calm. Energy-driven dimming.

    Smooth crossfades getting progressively darker. Individual melody onsets
    get gentle single-fixture reactions.
    """
    bar_dur = BAR_MS / 1000
    t = t_start
    step_num = 0

    # Divide into 3-bar chunks, each progressively darker
    chunk_bars = 3
    while t < t_end - 0.3:
        bi = beat_at(t)
        next_t = min(t + bar_dur * chunk_bars, t_end)

        # Force progressively lower dimmer
        progress = (t - t_start) / max(1, t_end - t_start)  # 0.0 → 1.0
        forced_dim = int(120 * (1.0 - progress))

        pal = SEGMENT_PALETTES.get(seg_idx, SEGMENT_PALETTES[13])
        s_pos, b_pos, p_pos = MOVER_POSITIONS[0]  # center

        sid = get_or_create_scene(
            f"outro_{seg_idx}_{step_num}", lambda:
            scene(f"Outro {seg_idx}-{step_num}",
                  sharpy(pan=s_pos["pan"], tilt=s_pos["tilt"],
                         strobe=SHARPY_OPEN, dim=forced_dim,
                         frost=200, colormacro=pal["sharpy"], focus=128),
                  bsw(pan=b_pos["pan"], tilt=b_pos["tilt"],
                      color=pal["bsw"], shutter=BSW_SHUT_OPEN,
                      dim=forced_dim, frost=200, focus=128),
                  profile(pan=p_pos["pan"], tilt=p_pos["tilt"],
                          color=pal["prof"], dim=forced_dim // 2, focus=128),
                  fourbar_solid(*pal["rgb1"], master=forced_dim // 2),
                  *miss_both(*pal["rgb2"], master=forced_dim // 3),
                  ni3k(pan=128, r=pal["rgb1"][0] // 4,
                       g=pal["rgb1"][1] // 4, b=pal["rgb1"][2] // 4,
                       halo=H_BLU if progress < 0.5 else H_OFF,
                       dim=forced_dim // 2, strobe=0),
                  path=folder))

        bars_here = bars_between(t, next_t)
        steps.append((sid, smooth(BPM, max(1, bars_here))))

        t = next_t
        step_num += 1

    # Final blackout
    steps.append((0, smooth(BPM, 2)))


# =============================================================================
# MAIN: Process all segments
# =============================================================================

print(f"Generating show from analysis data...")
print(f"  BPM: {BPM}, Beats: {len(beats)}, Segments: {len(segments)}")
print(f"  Bass onsets: {len(bass_onsets)}, Drum onsets: {len(drum_onsets)}")
print(f"  Vocal onsets: {len(vocal_onsets)}, Other onsets: {len(other_onsets)}")
print()

for i, seg in enumerate(segments):
    process_segment(i, seg)

# =============================================================================
# BUILD CHASER AND WRITE
# =============================================================================

print(f"\nTotal scenes: {len(scenes)}")
print(f"Total chaser steps: {len(steps)}")

# Verify timing
total_ms = sum(fi + ho for _, (fi, ho) in steps)
print(f"Total duration: {total_ms/1000:.1f}s (target: ~263s)")

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Acid Rain", scene_ids, timing,
                           run_order="SingleShot", path=folder)

# VC buttons
vc_buttons = [
    {"caption": "▶ ACID RAIN", "vc_id": 0, "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#880000", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace(os.path.join(VENUE_DIR, "shows", "Lorn - Acid Rain (Skeler Remix).qxw"),
                scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
