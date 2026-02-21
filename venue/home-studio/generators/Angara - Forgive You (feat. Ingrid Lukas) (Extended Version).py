#!/usr/bin/env python3
"""
Show Generator: Angara - Forgive You (feat. Ingrid Lukas) (Extended Version)
============================================================================
BPM: 125 | Duration: ~6:13 | Genre: Melodic house / narrative house

Aesthetic: "Narrative house" — water flow, warmth emerging from darkness.
Angara = Siberian river imagery, Ingrid Lukas = dark Rothko canvas.
Midnight blue base with warm amber/gold on vocal. Teal for flow.
Slow, patient unfolding. Tension → euphoric release.

Song Structure (grouped from analysis):
  0:00 - 0:45  INTRO         (24 bars, rms=0.76) Atmospheric, no sub
  0:45 - 1:32  FIRST_CHORUS  (25 bars, rms=0.61) Melody + 16-bar breakdown
  1:32 - 2:33  DROP_1        (33 bars, rms=0.90) First full energy, sub=0.69
  2:33 - 3:37  VALLEY        (25 bars, rms=0.52) Pullback + bridge, emotional low
  3:37 - 5:27  DROP_2        (56 bars, rms=0.89) Sustained peak, the climax
  5:27 - 6:13  OUTRO         (24 bars, rms=0.80) Fading to atmosphere

Movement: Flowing water-like sweeps. 4-8 bar crossfades in quiet sections,
2-bar during drops. No snaps except brief climax strobe.
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

SONG_STEM = "Angara - Forgive You (feat. Ingrid Lukas) (Extended Version)"
BRIEF = require_research_brief(SONG_STEM, project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)
print(f"Research brief OK: {BRIEF['_meta']['brief_json']}")
print(f"Creative thesis: {BRIEF['thesis']}")
DATA_PATH = os.path.join(PROJECT_ROOT, "songs-data", f"{SONG_STEM}.json")

CREATIVE = build_creative_context(BRIEF, song_stem=SONG_STEM)
BRAND_TOKENS = CREATIVE["brand_tokens"]
CREATIVE_DIRECTIVES = CREATIVE["creative_directives"]

with open(DATA_PATH) as f:
    data = json.load(f)

BPM = data["bpm"]  # 125
beats = data["beats"]
downbeats = data["downbeats"]
segments = data["segments"]

e_sub = data["energy"]["sub_bass"]
e_rms = data["energy"]["rms"]
e_high = data["energy"]["high"]

vocal_e = data["stems"]["vocals"]["energy"]
vocal_onsets = data["stems"]["vocals"]["onsets"]
bass_onsets = data["stems"]["bass"]["onsets"]

BAR_MS = bpm_to_ms(BPM, 4)   # 1920ms
BEAT_MS = bpm_to_ms(BPM, 1)  # 480ms

# =============================================================================
# HELPERS
# =============================================================================

def beat_at(t):
    idx = bisect.bisect_left(beats, t)
    if idx == 0:
        return 0
    if idx >= len(beats):
        return len(beats) - 1
    if abs(beats[idx] - t) < abs(beats[idx - 1] - t):
        return idx
    return idx - 1

def avg_energy(energy_arr, t_start, t_end):
    i_start = beat_at(t_start)
    i_end = beat_at(t_end)
    if i_start >= i_end:
        return 0.0
    return sum(energy_arr[i_start:i_end]) / (i_end - i_start)

def segment_at(t):
    for i, seg in enumerate(segments):
        if seg["start"] <= t < seg["end"]:
            return i, seg
    return len(segments) - 1, segments[-1]

def vocal_present(t_start, t_end):
    avg_v = avg_energy(vocal_e, t_start, t_end)
    return avg_v > 0.015

def sub_present(t_start, t_end):
    avg_s = avg_energy(e_sub, t_start, t_end)
    return avg_s > 0.2

def energy_to_dim(e, low=30, high=255):
    return int(low + (high - low) * min(1.0, max(0.0, e)))

# =============================================================================
# PHRASE-AWARE HARD LAYER (anti-overuse, not strict uniqueness)
# =============================================================================

PHRASE_BALANCE_ENABLED = True
PHRASE_TECH_COOLDOWN = 2

PHRASE_USAGE_BY_BUCKET = {}
PHRASE_RECENT_BY_BUCKET = {}
PHRASE_BAR_COUNTS = {}
TECHNIQUE_COUNTS = {}
LAST_TECHNIQUE_PLAN = None

def timing_from_phrase_technique(technique, bars_here):
    bars_here = max(1.0, float(bars_here))
    timing = technique["timing"]
    par_style = str(timing["par_style"])
    par_beats = int(timing["par_beats"])
    relationship = str(technique["relationship"])

    if par_style == "fade":
        return smooth(BPM, bars_here)
    if par_style == "chase":
        if par_beats <= 1 and relationship == "inclusion":
            return snap(BPM, bars_here, fade_ms=60)
        if par_beats <= 2:
            return hold(BPM, bars_here)
        return smooth(BPM, bars_here)
    return smooth(BPM, bars_here)

def phrase_step_timing(t_start, t_end, bars_here):
    global LAST_TECHNIQUE_PLAN
    mid = (t_start + t_end) / 2.0
    seg_idx, seg = segment_at(mid)
    label = seg["label"]

    rms = avg_energy(e_rms, t_start, t_end)
    sub = avg_energy(e_sub, t_start, t_end)
    high = avg_energy(e_high, t_start, t_end)
    progress = min(1.0, max(0.0, mid / max(1.0, beats[-1])))

    phrase = classify_phrase(
        segment_label=label,
        rms=rms,
        sub=sub,
        high=high,
        progress=progress,
        project_root=PROJECT_ROOT,
    )

    usage = PHRASE_USAGE_BY_BUCKET.setdefault(phrase, {}) if PHRASE_BALANCE_ENABLED else None
    recent = PHRASE_RECENT_BY_BUCKET.setdefault(phrase, [])
    global_bar = int(round((t_start * 1000.0) / BAR_MS))

    technique = pick_phrase_technique(
        phrase=phrase,
        segment_index=seg_idx,
        global_bar=global_bar,
        usage=usage,
        recent=recent,
        cooldown=PHRASE_TECH_COOLDOWN,
        previous_plan=LAST_TECHNIQUE_PLAN,
        brand_tokens=BRAND_TOKENS,
        creative_directives=CREATIVE_DIRECTIVES,
        candidate_count=3,
        show_key=SONG_STEM,
        project_root=PROJECT_ROOT,
    )
    LAST_TECHNIQUE_PLAN = technique
    technique_id = technique["id"]
    if usage is not None:
        usage[technique_id] = usage.get(technique_id, 0) + 1
    recent.append(technique_id)
    if len(recent) > 8:
        del recent[:-8]

    PHRASE_BAR_COUNTS[phrase] = PHRASE_BAR_COUNTS.get(phrase, 0) + max(1, int(round(bars_here)))
    TECHNIQUE_COUNTS[technique_id] = TECHNIQUE_COUNTS.get(technique_id, 0) + 1
    return timing_from_phrase_technique(technique, bars_here)

# =============================================================================
# COLOR PALETTE — deep darkness with warm amber reveals
# =============================================================================

# Cold palette (default / instrumental)
MIDNIGHT_BLUE = (15, 25, 70)
OCEAN_TEAL = (20, 100, 120)
DEEP_VIOLET = (50, 20, 90)
NEAR_BLACK = (8, 10, 20)
COLD_WHITE = (200, 210, 230)

# Warm palette (vocal reveals)
WARM_AMBER = (210, 150, 50)
SOFT_GOLD = (190, 160, 80)
PALE_PINK = (200, 120, 140)

NOTHING = (0, 0, 0)

# =============================================================================
# MOVER POSITIONS — loaded from venue focus-positions.md
# =============================================================================

POS = load_focus_position_tuples(project_root=PROJECT_ROOT, venue_dir=VENUE_DIR)

# =============================================================================
# LOGICAL SECTIONS
# =============================================================================

SECTIONS = [
    {"name": "INTRO",        "start": 0.0,    "end": 45.0,   "bars": 24},
    {"name": "FIRST_CHORUS", "start": 45.0,   "end": 92.0,   "bars": 25},
    {"name": "DROP_1",       "start": 92.0,   "end": 153.0,  "bars": 33},
    {"name": "VALLEY",       "start": 153.0,  "end": 217.0,  "bars": 25},
    {"name": "DROP_2",       "start": 217.0,  "end": 327.0,  "bars": 56},
    {"name": "OUTRO",        "start": 327.0,  "end": 373.6,  "bars": 24},
]

# =============================================================================
# SCENE GENERATION
# =============================================================================

scenes = []
folder = "Forgive You"

scenes.append(scene("Blackout", *blackout_all(), path=folder))

steps = []
scene_cache = {}

def get_or_create_scene(key, create_fn):
    if key not in scene_cache:
        sc = create_fn()
        scene_cache[key] = len(scenes)
        scenes.append(sc)
    return scene_cache[key]


def make_full_scene(name, pos_key, energy, frost_val,
                    sharpy_color=SHARPY_BLUE, bsw_color=BSW_TEAL,
                    prof_color=PROF_TEAL,
                    par_rgb=MIDNIGHT_BLUE, miss_rgb=DEEP_VIOLET,
                    ni3k_rgb=MIDNIGHT_BLUE, halo=H_OFF,
                    sharpy_dim=None, bsw_dim=None, prof_dim=None,
                    par_master=None,
                    prism=False, lasers=False,
                    strobe_sharpy=SHARPY_OPEN,
                    shutter_bsw=BSW_SHUT_OPEN,
                    ni3k_tilt=(64, 64, 64)):
    """Build an atmosphere scene. Energy modulates dimmer/frost."""
    p = POS[pos_key]
    sp, st, bp, bt, pp, pt, ni_pan = p

    s_dim = sharpy_dim if sharpy_dim is not None else energy_to_dim(energy, low=40, high=230)
    b_dim = bsw_dim if bsw_dim is not None else energy_to_dim(energy, low=30, high=210)
    p_dim = prof_dim if prof_dim is not None else energy_to_dim(energy * 0.6, low=0, high=160)
    p_mst = par_master if par_master is not None else energy_to_dim(energy, low=15, high=210)

    prism_val = 128 if prism else 0
    prism_rot = 200 if prism else 0

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
            prism=prism_val, prot=prism_rot, focus=128),
        profile(pan=pp, tilt=pt, color=prof_color, dim=p_dim, focus=128),
        fourbar_solid(*par_rgb, master=p_mst),
        miss1(*miss_rgb, master=p_mst // 2),
        miss2(*miss_rgb, master=p_mst // 2),
        ni3k(pan=ni_pan, t1=t1, t2=t2, t3=t3,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, rl=laser_r, gl=laser_g, bl=laser_b,
             dim=ni_dim, strobe=0),
        path=folder)


def make_solo_scene(name, pos_key, active_mover, dim,
                    mover_color_sharpy=SHARPY_BLUE, mover_color_bsw=BSW_TEAL,
                    mover_color_prof=PROF_TEAL, frost=200,
                    ni3k_rgb=NEAR_BLACK, halo=H_OFF,
                    par_rgb=NOTHING, par_master=0):
    """Scene with one active mover, others dark parked at same position."""
    p = POS[pos_key]
    sp, st, bp, bt, pp, pt, ni_pan = p

    ni_r, ni_g, ni_b = ni3k_rgb
    ni_dim = 25 if sum(ni3k_rgb) > 0 else 0

    if active_mover == "sharpy":
        s = sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=dim,
                   frost=frost, colormacro=mover_color_sharpy, focus=128)
        b = dark_bsw(pan=bp, tilt=bt)
        pr = dark_profile(pan=pp, tilt=pt)
    elif active_mover == "bsw":
        s = dark_sharpy(pan=sp, tilt=st)
        b = bsw(pan=bp, tilt=bt, color=mover_color_bsw, shutter=BSW_SHUT_OPEN,
                dim=dim, frost=frost, focus=128)
        pr = dark_profile(pan=pp, tilt=pt)
    elif active_mover == "profile":
        s = dark_sharpy(pan=sp, tilt=st)
        b = dark_bsw(pan=bp, tilt=bt)
        pr = profile(pan=pp, tilt=pt, color=mover_color_prof, dim=dim, focus=128)
    else:
        s = dark_sharpy(pan=sp, tilt=st)
        b = dark_bsw(pan=bp, tilt=bt)
        pr = dark_profile(pan=pp, tilt=pt)

    return scene(name, s, b, pr,
        fourbar_solid(*par_rgb, master=par_master),
        miss1(*NOTHING), miss2(*NOTHING),
        ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
             r=ni_r, g=ni_g, b=ni_b, w=0,
             halo=halo, dim=ni_dim, strobe=0),
        path=folder)


# =============================================================================
# SECTION BUILDERS
# =============================================================================

def build_intro(sec):
    """INTRO (0:00-0:45, 24 bars): Atmospheric, no sub bass.

    Near-dark. Deep midnight blue pars barely visible. Single mover (BSW)
    at center, frosted teal. Gradually add Sharpy, widen positions.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000

    # Phase 1: first 12 bars — single BSW at center, barely visible
    phase1_end = t + bar_dur * 12
    step_num = 0

    while t < phase1_end - 0.5:
        next_t = min(t + bar_dur * 4, phase1_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)

        dim = int(30 + 40 * progress)

        sid = get_or_create_scene(f"intro_solo_{step_num}", lambda:
            make_solo_scene(f"Intro {step_num}", "C",
                active_mover="bsw", dim=dim, frost=220,
                ni3k_rgb=MIDNIGHT_BLUE, halo=H_OFF,
                par_rgb=MIDNIGHT_BLUE if progress > 0.1 else NEAR_BLACK,
                par_master=int(30 * progress + 10)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1

    # Phase 2: bars 12-24 — add Sharpy, widen positions
    positions = ["C", "USC", "SL"]
    while t < t_end - 0.5:
        next_t = min(t + bar_dur * 4, t_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = positions[step_num % len(positions)]

        # Both Sharpy + BSW now, but still dim
        s_dim = int(40 + 60 * progress)
        b_dim = int(50 + 50 * progress)

        # Warm accent if vocal sneaks in during intro
        par_c = WARM_AMBER if has_vocal else MIDNIGHT_BLUE
        miss_c = SOFT_GOLD if has_vocal else DEEP_VIOLET

        sid = get_or_create_scene(f"intro_wide_{step_num}", lambda:
            make_full_scene(f"Intro Wide {step_num}", pos,
                energy=energy * 0.5, frost_val=200,
                par_rgb=par_c, miss_rgb=miss_c,
                ni3k_rgb=MIDNIGHT_BLUE, halo=H_BLU if progress > 0.6 else H_OFF,
                sharpy_dim=s_dim, bsw_dim=b_dim, prof_dim=0,
                par_master=int(40 * progress + 20)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1


def build_first_chorus(sec):
    """FIRST_CHORUS (0:45-1:32, 25 bars): Melody enters, then 16-bar breakdown.

    First 9 bars: melodic, adding warmth. Profile comes on.
    Last 16 bars: breakdown — strip down, build tension with slow dimmer rise.
    """
    t = sec["start"]
    t_end = sec["end"]
    bar_dur = BAR_MS / 1000

    # Phase 1: Melodic chorus (9 bars)
    melody_end = t + bar_dur * 9
    step_num = 0
    sweep = ["C", "SL", "SR"]

    while t < melody_end - 0.5:
        next_t = min(t + bar_dur * 3, melody_end)
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = sweep[step_num % len(sweep)]

        par_c = WARM_AMBER if has_vocal else OCEAN_TEAL
        miss_c = SOFT_GOLD if has_vocal else DEEP_VIOLET

        sid = get_or_create_scene(f"ch1_melody_{step_num}", lambda:
            make_full_scene(f"Chorus 1 Melody {step_num}", pos,
                energy=energy * 0.7, frost_val=180,
                sharpy_color=SHARPY_AMBER if has_vocal else SHARPY_BLUE,
                par_rgb=par_c, miss_rgb=miss_c,
                ni3k_rgb=OCEAN_TEAL, halo=H_BLU,
                prof_dim=energy_to_dim(energy * 0.4, low=0, high=100),
                par_master=energy_to_dim(energy * 0.6, low=20, high=140)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1

    # Phase 2: 16-bar breakdown — strip down, then build tension
    breakdown_positions = ["C", "DSC", "C", "USC"]
    bd_step = 0
    bd_total = t_end - t

    while t < t_end - 0.5:
        next_t = min(t + bar_dur * 4, t_end)
        bd_progress = (t - melody_end) / bd_total  # 0→1 through breakdown
        energy = avg_energy(e_rms, t, next_t)
        pos = breakdown_positions[bd_step % len(breakdown_positions)]

        # Start dark, slowly build tension (dimmer rises toward drop)
        tension_dim = int(20 + 60 * bd_progress)
        frost = int(220 - 30 * bd_progress)

        sid = get_or_create_scene(f"ch1_bd_{bd_step}", lambda:
            make_full_scene(f"Breakdown {bd_step}", pos,
                energy=energy * 0.4, frost_val=frost,
                sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                par_rgb=MIDNIGHT_BLUE, miss_rgb=NEAR_BLACK,
                ni3k_rgb=DEEP_VIOLET, halo=H_OFF,
                sharpy_dim=tension_dim, bsw_dim=int(tension_dim * 0.7),
                prof_dim=0,
                par_master=int(20 + 30 * bd_progress)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        bd_step += 1


def build_drop_1(sec):
    """DROP_1 (1:32-2:33, 33 bars): First full energy, sub bass arrives.

    Flowing L-R sweeps, 2-bar crossfades. First "release" — breathing
    after being underwater. Warm amber on vocal, blue/teal instrumental.
    """
    t = sec["start"]
    t_end = sec["end"]
    bar_dur = BAR_MS / 1000
    step_bars = 2

    # Flowing sweep — water-like arcs
    sweep = ["DSC", "SL", "C", "SR", "DSC", "X", "SL", "DSC",
             "SR", "C", "DSL", "DSC", "USC", "C", "DSR", "DSC", "X"]
    step_num = 0

    while t < t_end - 0.3:
        next_t = min(t + bar_dur * step_bars, t_end)
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        has_sub = sub_present(t, next_t)
        pos = sweep[step_num % len(sweep)]

        frost = int(140 - 70 * energy)
        use_prism = energy > 0.85

        # Color: warm on vocal, cool on instrumental
        if has_vocal:
            s_color = SHARPY_AMBER
            par_c = WARM_AMBER
            miss_c = SOFT_GOLD
        else:
            s_color = SHARPY_BLUE
            par_c = OCEAN_TEAL
            miss_c = MIDNIGHT_BLUE

        # Alternate miss colors every 4 bars
        if (step_num // 2) % 2 == 1 and not has_vocal:
            miss_c = DEEP_VIOLET

        sid = get_or_create_scene(f"drop1_{step_num}", lambda:
            make_full_scene(f"Drop 1 {step_num}", pos,
                energy=energy, frost_val=frost,
                sharpy_color=s_color, bsw_color=BSW_TEAL,
                prof_color=PROF_TEAL,
                par_rgb=par_c, miss_rgb=miss_c,
                ni3k_rgb=OCEAN_TEAL, halo=H_BLU,
                prism=use_prism,
                ni3k_tilt=(64, 64, 64) if not use_prism else (150, 170, 160)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1


def build_valley(sec):
    """VALLEY (2:33-3:37, 25 bars): Pullback + bridge, emotional low point.

    First 12 bars: gradual pullback. Last 13 bars: bridge — near-blackout,
    candlelight warmth, intimate. Like string lights on black.
    """
    t = sec["start"]
    t_end = sec["end"]
    bar_dur = BAR_MS / 1000

    # Phase 1: Pullback (12 bars) — gradually dim everything
    pullback_end = t + bar_dur * 12
    step_num = 0

    while t < pullback_end - 0.5:
        next_t = min(t + bar_dur * 4, pullback_end)
        progress = (t - sec["start"]) / (pullback_end - sec["start"])
        energy = avg_energy(e_rms, t, next_t)

        dim_factor = max(0.1, 1.0 - progress * 0.8)

        sid = get_or_create_scene(f"valley_pull_{step_num}", lambda:
            make_full_scene(f"Valley Pullback {step_num}", "DSC",
                energy=energy * dim_factor, frost_val=int(180 + 40 * progress),
                sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                par_rgb=tuple(int(c * dim_factor) for c in MIDNIGHT_BLUE),
                miss_rgb=tuple(int(c * dim_factor) for c in DEEP_VIOLET),
                ni3k_rgb=tuple(int(c * dim_factor) for c in MIDNIGHT_BLUE),
                halo=H_BLU if progress < 0.5 else H_OFF,
                sharpy_dim=int(120 * dim_factor),
                bsw_dim=int(100 * dim_factor),
                prof_dim=int(40 * dim_factor),
                par_master=int(80 * dim_factor)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1

    # Phase 2: Bridge — the emotional low. Near-blackout with warm candlelight.
    # Single NI3K warm glow + gentle Sharpy amber, like string lights on black
    bridge_positions = ["C", "DJ", "C"]
    bridge_step = 0

    while t < t_end - 0.5:
        next_t = min(t + bar_dur * 4, t_end)
        bridge_progress = (t - pullback_end) / max(1, t_end - pullback_end)
        pos = bridge_positions[bridge_step % len(bridge_positions)]
        has_vocal = vocal_present(t, next_t)

        # Candlelight: very dim warm amber from one fixture
        # Toward end of bridge, start building tension again
        if bridge_progress < 0.7:
            # Pure intimacy — single warm mover
            sid = get_or_create_scene(f"bridge_{bridge_step}", lambda:
                make_solo_scene(f"Bridge {bridge_step}", pos,
                    active_mover="sharpy",
                    dim=int(35 + 20 * bridge_progress),
                    mover_color_sharpy=SHARPY_AMBER if has_vocal else SHARPY_BLUE,
                    frost=220,
                    ni3k_rgb=WARM_AMBER if has_vocal else DEEP_VIOLET,
                    halo=H_OFF,
                    par_rgb=WARM_AMBER if has_vocal else NOTHING,
                    par_master=15 if has_vocal else 0))
        else:
            # Tension building — add BSW, start widening
            sid = get_or_create_scene(f"bridge_build_{bridge_step}", lambda:
                make_full_scene(f"Bridge Build {bridge_step}", pos,
                    energy=0.3 + 0.2 * bridge_progress, frost_val=200,
                    sharpy_color=SHARPY_BLUE, bsw_color=BSW_TEAL,
                    par_rgb=MIDNIGHT_BLUE, miss_rgb=NEAR_BLACK,
                    ni3k_rgb=MIDNIGHT_BLUE, halo=H_OFF,
                    sharpy_dim=int(50 * bridge_progress + 30),
                    bsw_dim=int(40 * bridge_progress),
                    prof_dim=0,
                    par_master=int(30 * bridge_progress)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        bridge_step += 1


def build_drop_2(sec):
    """DROP_2 (3:37-5:27, 56 bars): Sustained peak, the climax.

    Build (first 9 bars): fixtures return one by one.
    Full peak (47 bars): wider positions, warmer than Drop 1.
    "Touching heaven" — NI3K lasers at absolute peak.
    Brief strobe accent at climax only.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000

    # Phase 1: Build (9 bars) — fixtures return one by one
    build_end = t + bar_dur * 9
    step_num = 0
    build_positions = ["C", "SL", "DSC"]

    while t < build_end - 0.5:
        next_t = min(t + bar_dur * 3, build_end)
        build_progress = (t - sec["start"]) / (build_end - sec["start"])
        energy = avg_energy(e_rms, t, next_t)
        pos = build_positions[step_num % len(build_positions)]

        # Add fixtures progressively
        s_dim = int(40 + 120 * build_progress)
        b_dim = int(80 * build_progress) if build_progress > 0.3 else 0
        p_dim = int(60 * build_progress) if build_progress > 0.5 else 0
        p_mst = int(40 + 80 * build_progress)

        p = POS[pos]
        sp, st, bp, bt, pp, pt, ni_pan = p

        sid = get_or_create_scene(f"drop2_build_{step_num}", lambda:
            scene(f"Drop 2 Build {step_num}",
                sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=s_dim,
                       frost=int(200 - 60 * build_progress),
                       colormacro=SHARPY_BLUE, focus=128),
                bsw(pan=bp, tilt=bt, color=BSW_TEAL,
                    shutter=BSW_SHUT_OPEN, dim=b_dim,
                    frost=200, focus=128) if b_dim > 0
                    else dark_bsw(pan=bp, tilt=bt),
                profile(pan=pp, tilt=pt, color=PROF_TEAL,
                        dim=p_dim, focus=128) if p_dim > 0
                    else dark_profile(pan=pp, tilt=pt),
                fourbar_solid(*MIDNIGHT_BLUE, master=p_mst),
                miss1(*DEEP_VIOLET, master=p_mst // 2),
                miss2(*DEEP_VIOLET, master=p_mst // 2),
                ni3k(pan=ni_pan, t1=64, t2=64, t3=64,
                     r=OCEAN_TEAL[0], g=OCEAN_TEAL[1], b=OCEAN_TEAL[2],
                     w=0, halo=H_BLU, dim=int(40 * build_progress), strobe=0),
                path=folder))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1

    # Phase 2: Full peak (47 bars) — the sustained climax
    # Flowing sweep, warmer than Drop 1, "coming home" feeling
    peak_sweep = ["DSC", "X", "SL", "C", "SR", "DSC", "DSL", "C",
                  "DSR", "USC", "X", "DSC", "CEIL", "C", "SL", "DSC",
                  "SR", "X", "C", "DSC", "SL", "USC", "SR", "DSC"]
    peak_step = 0
    step_bars = 2

    # Find the absolute peak for laser/strobe moment
    climax_t = t
    climax_e = 0
    scan = t
    while scan < t_end:
        e = avg_energy(e_rms, scan, min(scan + bar_dur * 2, t_end))
        if e > climax_e:
            climax_e = e
            climax_t = scan
        scan += bar_dur * 2

    while t < t_end - 0.3:
        next_t = min(t + bar_dur * step_bars, t_end)
        progress = (t - build_end) / max(1, t_end - build_end)
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)
        pos = peak_sweep[peak_step % len(peak_sweep)]

        frost = int(120 - 60 * energy)
        is_climax = abs(t - climax_t) < bar_dur * 4

        # Warmer palette than Drop 1 — "coming home"
        if has_vocal or progress > 0.2:
            s_color = SHARPY_AMBER
            par_c = WARM_AMBER
            miss_c = SOFT_GOLD
        else:
            s_color = SHARPY_TEAL
            par_c = OCEAN_TEAL
            miss_c = MIDNIGHT_BLUE

        # At the absolute climax: white, lasers, brief strobe
        if is_climax and energy > 0.85:
            s_color = SHARPY_WHITE
            par_c = COLD_WHITE
            miss_c = COLD_WHITE

        use_prism = energy > 0.8
        use_lasers = is_climax and energy > 0.88
        use_strobe = is_climax and energy > 0.9

        sid = get_or_create_scene(f"drop2_peak_{peak_step}", lambda:
            make_full_scene(f"Drop 2 Peak {peak_step}", pos,
                energy=energy, frost_val=frost,
                sharpy_color=s_color, bsw_color=BSW_TEAL,
                prof_color=PROF_TEAL,
                par_rgb=par_c, miss_rgb=miss_c,
                ni3k_rgb=WARM_AMBER if has_vocal else OCEAN_TEAL,
                halo=H_CYN,
                prism=use_prism, lasers=use_lasers,
                strobe_sharpy=SHARPY_STROBE_MED if use_strobe else SHARPY_OPEN,
                shutter_bsw=BSW_SHUT_STROBE_SLOW if use_strobe else BSW_SHUT_OPEN,
                ni3k_tilt=(150, 170, 160) if use_prism else (64, 64, 64)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        peak_step += 1


def build_outro(sec):
    """OUTRO (5:27-6:13, 24 bars): Fading to atmosphere.

    Return to cool palette. Progressive dimming. Movers converge to center.
    Resolved, peaceful. Warm amber fading to soft blue, then blackout.
    """
    t = sec["start"]
    t_end = sec["end"]
    total_dur = t_end - t
    bar_dur = BAR_MS / 1000
    step_num = 0

    # First 8 bars: still some energy, warm → cool transition
    trans_end = t + bar_dur * 8
    while t < trans_end - 0.5:
        next_t = min(t + bar_dur * 4, trans_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)
        has_vocal = vocal_present(t, next_t)

        # Transition from warm amber back to cool blue
        warm_fade = max(0, 1.0 - progress * 3)
        if warm_fade > 0.3 and has_vocal:
            par_c = WARM_AMBER
            s_color = SHARPY_AMBER
        else:
            par_c = MIDNIGHT_BLUE
            s_color = SHARPY_BLUE

        sid = get_or_create_scene(f"outro_trans_{step_num}", lambda:
            make_full_scene(f"Outro Trans {step_num}", "C",
                energy=energy * (1.0 - progress * 0.5), frost_val=200,
                sharpy_color=s_color, bsw_color=BSW_BLUE,
                par_rgb=par_c, miss_rgb=DEEP_VIOLET,
                ni3k_rgb=MIDNIGHT_BLUE, halo=H_BLU if progress < 0.3 else H_OFF,
                par_master=energy_to_dim(energy * (1.0 - progress), low=15, high=140)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1

    # Last 16 bars: progressive fade to near-blackout
    while t < t_end - 0.5:
        next_t = min(t + bar_dur * 4, t_end)
        progress = (t - sec["start"]) / total_dur
        energy = avg_energy(e_rms, t, next_t)
        dim_factor = max(0.0, 1.0 - progress)

        sid = get_or_create_scene(f"outro_fade_{step_num}", lambda:
            make_full_scene(f"Outro Fade {step_num}", "C",
                energy=energy * dim_factor * 0.5, frost_val=230,
                sharpy_color=SHARPY_BLUE, bsw_color=BSW_BLUE,
                par_rgb=tuple(int(c * dim_factor) for c in MIDNIGHT_BLUE),
                miss_rgb=NOTHING,
                ni3k_rgb=tuple(int(c * dim_factor) for c in DEEP_VIOLET),
                halo=H_OFF,
                sharpy_dim=int(60 * dim_factor),
                bsw_dim=int(40 * dim_factor),
                prof_dim=0,
                par_master=int(40 * dim_factor)))

        bars_here = max(1, (next_t - t) / bar_dur)
        steps.append((sid, phrase_step_timing(t, next_t, bars_here)))
        t = next_t
        step_num += 1

    # Final blackout
    steps.append((0, phrase_step_timing(max(0.0, t_end - bar_dur * 2), t_end, 2)))


# =============================================================================
# MAIN
# =============================================================================

BUILDERS = {
    "INTRO": build_intro,
    "FIRST_CHORUS": build_first_chorus,
    "DROP_1": build_drop_1,
    "VALLEY": build_valley,
    "DROP_2": build_drop_2,
    "OUTRO": build_outro,
}

print(f"Generating show: {SONG_STEM}")
print(f"  BPM: {BPM}, Beats: {len(beats)}, Duration: {beats[-1]:.1f}s")
print()

for sec in SECTIONS:
    print(f"  Building {sec['name']:14s} ({sec['bars']:2d} bars, "
          f"{sec['start']:.1f}s-{sec['end']:.1f}s)")
    BUILDERS[sec["name"]](sec)

print(f"\nTotal scenes: {len(scenes)}")
print(f"Total chaser steps: {len(steps)}")
print(f"Phrase bars: {PHRASE_BAR_COUNTS}")
top_techniques = sorted(TECHNIQUE_COUNTS.items(), key=lambda kv: kv[1], reverse=True)[:8]
print(f"Top technique usage: {top_techniques}")

total_ms = sum(fi + ho for _, (fi, ho) in steps)
print(f"Total duration: {total_ms/1000:.1f}s (target: ~374s)")

scene_ids = [s for s, _ in steps]
timing = [t for _, t in steps]

main_chaser = make_chaser("Forgive You", scene_ids, timing,
                           run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "FORGIVE YOU", "vc_id": 0,
     "func_id": len(scenes),
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#0F1946", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": 0,
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

output_path = os.path.join(VENUE_DIR, "shows", f"{SONG_STEM}.qxw")
write_workspace(output_path, scenes, [main_chaser], bpm=BPM, vc_buttons=vc_buttons)
