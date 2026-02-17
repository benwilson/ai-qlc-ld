#!/usr/bin/env python3
"""
Show Generator: Damian Marley - Welcome To Jamrock (Explicit) (v2)
===================================================================
BPM: 77 | Duration: ~3:33 | Genre: Reggae / Dancehall

v2 Changes from v1:
  - ALL positions now use hardware-verified focus positions from focus-positions.md
  - 7-tuple format: (sharpy_pan, sharpy_tilt, bsw_pan, bsw_tilt, prof_pan, prof_tilt, ni3k_pan)
  - SL=DSL=USL and SR=DSR=USR (room too small for depth difference on sides)
  - Added verified specials: DJ Booth, Disco Ball, Center Ceiling, Cross (X)
  - NI3K pan in tuple for consistency (NI3K is OFF for this show)
  - Drift sequences redesigned to feature specials:
    * DJ Booth in intro and outro (intimate, performer-focused)
    * Center Ceiling in chorus drift (dramatic upward beams)
    * Cross (X) in chorus for beam crossing effects
    * Disco Ball in verses for atmosphere

Creative Direction:
  - RASTA PALETTE: Red, Gold (yellow), Green — cycling through pars and movers
  - Movers: PULSE to bass — snap bright on bass onset, smooth fade-down on next beat
  - Pars: chase on every beat — one par lit cycling R/G/Y through 4BAR + Missyees
  - NI3K: OFF (clean mover + par look)
  - Split chaser architecture: separate mover chaser (smooth fades) and par chaser
    (instant snaps), bundled in a QLC+ Collection for one-button playback

Technical approach:
  Movers and pars need different FadeIn timing, so they run as two parallel chasers:
    - Mover chaser: FadeIn=0 on bass hits (snap bright), FadeIn=BEAT_MS on non-bass
      beats (smooth crossfade = pulse decay back to dim). Positions drift smoothly.
    - Par chaser: FadeIn=0 on every beat (crisp chase pattern).
  Both chasers are bundled in a Collection triggered by one VC button.

Song Structure (from allin1 analysis):
  0:00 - 0:29  verse     (~38 beats)  "Siren Intro + Verse 1" — dark, building
  0:29 - 0:45  verse     (~19 beats)  "Verse 2" — established groove
  0:45 - 1:08  verse     (~31 beats)  "Verse 3" — building intensity
  1:08 - 1:22  chorus    (~18 beats)  "Chorus 1" — WELCOME TO JAMROCK
  1:22 - 2:00  verse     (~47 beats)  "Verse 4" — pull back, longest section
  2:00 - 2:25  verse     (~33 beats)  "Verse 5" — rebuilding
  2:25 - 2:49  chorus    (~30 beats)  "Chorus 2" — big energy
  2:49 - 3:03  chorus    (~17 beats)  "Chorus 3" — peak
  3:03 - 3:28  outro     (~33 beats)  "Outro" — winding down
  3:28 - 3:33  end       (~4 beats)   "Final" — snap to black
"""

import os
import sys
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENUE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(VENUE_DIR))
sys.path.insert(0, PROJECT_ROOT)
from showlib import *

BPM = 77
BEAT_MS = bpm_to_ms(BPM, 1)  # ~779ms

# =============================================================================
# LOAD ANALYSIS DATA
# =============================================================================

with open(os.path.join(PROJECT_ROOT, "songs-data",
          "Damian Marley - Welcome To Jamrock (Explicit).json")) as f:
    analysis = json.load(f)

beats = analysis["beats"]
bass_onsets = analysis["stems"]["bass"]["onsets"]

# Quantize bass onsets to nearest beat index
bass_beat_set = set()
for onset in bass_onsets:
    best_idx = 0
    best_dist = abs(beats[0] - onset)
    for i, b in enumerate(beats):
        d = abs(b - onset)
        if d < best_dist:
            best_dist = d
            best_idx = i
    if best_dist < (BEAT_MS / 1000) * 0.5:
        bass_beat_set.add(best_idx)

print(f"Beats: {len(beats)}, Bass onsets: {len(bass_onsets)}, "
      f"Bass beats (quantized): {len(bass_beat_set)}")

# =============================================================================
# RASTA PALETTE
# =============================================================================

RASTA_RED  = (255, 0, 0)
RASTA_GOLD = (255, 200, 0)
RASTA_GRN  = (0, 255, 0)

RASTA_3 = [RASTA_RED, RASTA_GOLD, RASTA_GRN]

BSW_RASTA = {
    RASTA_RED: BSW_RED, RASTA_GOLD: BSW_YELLOW, RASTA_GRN: BSW_GREEN,
}
SHARPY_RASTA = {
    RASTA_RED: SHARPY_RED, RASTA_GOLD: SHARPY_YELLOW, RASTA_GRN: SHARPY_GREEN,
}
PROF_RASTA = {
    RASTA_RED: PROF_RED, RASTA_GOLD: PROF_YELLOW, RASTA_GRN: PROF_GREEN,
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
}

# v2: Drift sequences redesigned with specials
DRIFT_INTRO   = ["C", "SL", "DJ", "SR", "C"]                            # DJ Booth for performer focus
DRIFT_VERSE   = ["C", "SL", "SR", "DSC", "C", "DISCO", "USR", "C"]     # Disco Ball for atmosphere
DRIFT_CHORUS  = ["DSC", "SL", "SR", "X", "CEIL", "C", "DSC", "SL"]     # Cross + Ceiling for drama
DRIFT_OUTRO   = ["C", "SL", "DJ", "SR", "C", "USC", "C"]               # DJ Booth for intimate wind-down

# =============================================================================
# SCENE BUILDING WITH DEDUP — SEPARATE MOVER AND PAR TRACKS
# =============================================================================

folder = "Welcome To Jamrock"

# All scenes go into one list, but we track mover vs par scenes separately
scenes = []
scene_cache = {}
dedup_hits = 0

# Separate step lists for the two chasers
mover_steps = []   # (scene_idx, (FadeIn, Hold))
par_steps = []     # (scene_idx, (FadeIn, Hold))


def add_scene(name, *fixtures):
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


# =============================================================================
# FIXTURE BUILDERS
# =============================================================================

def mk_movers(pos_key, color, dim=255, frost=0, focus=128,
              prism_s=0, p1r_s=0, prism_b=0, prot_b=0, prism_p=0,
              gobo_b=0, gobo_p=0):
    """Build all 3 movers from position key + Rasta color. Uses 7-tuple positions.
    Always uses open shutter — dimmer controls the pulse."""
    sp, st, bp, bt, pp, pt, _ni = POS[pos_key]
    bsw_c = BSW_RASTA.get(color, BSW_WHITE)
    sharpy_c = SHARPY_RASTA.get(color, SHARPY_WHITE)
    prof_c = PROF_RASTA.get(color, PROF_WHITE)
    s = sharpy(pan=sp, tilt=st, strobe=SHARPY_OPEN, dim=dim,
               frost=frost, focus=focus, prism1=prism_s, p1r=p1r_s,
               colormacro=sharpy_c)
    b = bsw(pan=bp, tilt=bt, color=bsw_c, shutter=BSW_SHUT_OPEN,
            dim=dim, prism=prism_b, prot=prot_b, focus=focus,
            gobo1=gobo_b)
    p = profile(pan=pp, tilt=pt, dim=dim, prism=prism_p, focus=focus,
                color=prof_c, gobo=gobo_p)
    return s, b, p


def par_chase_beat(beat_idx, color, master=255):
    """4BAR: one par lit per beat, cycling R/G/Y. Missyees alternate."""
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


def ni3k_off():
    """NI3K completely dark."""
    return ni3k(dim=0, r=0, g=0, b=0, w=0, halo=H_OFF,
                rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF)


# =============================================================================
# SECTION MAPPING
# =============================================================================

section_bounds = [
    ("intro",   0.0,    29.3),
    ("verse2",  29.3,   44.9),
    ("verse3",  44.9,   68.4),
    ("chorus1", 68.4,   82.5),
    ("verse4",  82.5,   120.0),
    ("verse5",  120.0,  145.1),
    ("chorus2", 145.1,  169.3),
    ("chorus3", 169.3,  182.6),
    ("outro",   182.6,  207.7),
    ("end",     207.7,  213.3),
]

def get_section(beat_time):
    for name, start, end in section_bounds:
        if start <= beat_time < end:
            return name
    return "end"


# =============================================================================
# BLACKOUT SCENES (scene 0 = full blackout, 1 = mover blackout, 2 = par blackout)
# =============================================================================

full_bo_idx = add_scene("Blackout", *blackout_all())

mover_bo_idx = add_scene("Mover Blackout",
    sharpy(dim=0, strobe=SHARPY_CLOSED),
    bsw(dim=0, shutter=BSW_SHUT_CLOSED),
    profile(dim=0))

par_bo_idx = add_scene("Par Blackout",
    fourbar_solid(0, 0, 0, master=0),
    miss1(0, 0, 0, master=0),
    miss2(0, 0, 0, master=0),
    ni3k_off())


# =============================================================================
# BUILD SHOW — beat by beat, two parallel tracks
# =============================================================================

section_beat_counts = {}

for bi, bt in enumerate(beats):
    sec = get_section(bt)
    sec_beat = section_beat_counts.get(sec, 0)
    section_beat_counts[sec] = sec_beat + 1

    is_bass = bi in bass_beat_set
    color = RASTA_3[bi % 3]

    # --- Mover drift position (changes every 8 beats) ---
    pos_idx = sec_beat // 8

    if sec == "intro":
        drift = DRIFT_INTRO
    elif sec.startswith("chorus"):
        drift = DRIFT_CHORUS
    elif sec == "outro":
        drift = DRIFT_OUTRO
    else:
        drift = DRIFT_VERSE

    pos_key = drift[pos_idx % len(drift)]

    # --- Section-specific parameters ---
    if sec == "intro":
        par_master = min(80 + sec_beat * 3, 200)
        mover_dim_base = 0
        mover_flash_dim = min(80 + sec_beat * 5, 200)
        frost = 200
        focus = 200
        prism_s = 0; p1r_s = 0; prism_b = 0; prot_b = 0; prism_p = 0
        gobo_b = 0; gobo_p = 0

    elif sec == "verse2":
        par_master = 200
        mover_dim_base = 40
        mover_flash_dim = 220
        frost = 150
        focus = 160
        prism_s = 0; p1r_s = 0; prism_b = 0; prot_b = 0; prism_p = 0
        gobo_b = 0; gobo_p = 0

    elif sec == "verse3":
        par_master = 220
        mover_dim_base = 60
        mover_flash_dim = 240
        frost = 100
        focus = 140
        prism_s = 0; p1r_s = 0; prism_b = 0; prot_b = 0; prism_p = 0
        gobo_b = 0; gobo_p = 0

    elif sec == "chorus1":
        par_master = 255
        mover_dim_base = 80
        mover_flash_dim = 255
        frost = 0
        focus = 128
        prism_s = 0; p1r_s = 0; prism_b = 0; prot_b = 0; prism_p = 0
        gobo_b = BSW_G1_3; gobo_p = 0

    elif sec == "verse4":
        par_master = 180
        mover_dim_base = 50
        mover_flash_dim = 220
        frost = 120
        focus = 160
        prism_s = 0; p1r_s = 0; prism_b = 0; prot_b = 0; prism_p = 0
        gobo_b = 0; gobo_p = 0

    elif sec == "verse5":
        par_master = 220
        mover_dim_base = 70
        mover_flash_dim = 240
        frost = 60
        focus = 140
        prism_s = 0; p1r_s = 0; prism_b = 0; prot_b = 0; prism_p = 0
        gobo_b = 0; gobo_p = 0

    elif sec == "chorus2":
        par_master = 255
        mover_dim_base = 100
        mover_flash_dim = 255
        frost = 0
        focus = 128
        prism_s = 128; p1r_s = 200; prism_b = 80; prot_b = 180; prism_p = 60
        gobo_b = BSW_G1_3; gobo_p = 0

    elif sec == "chorus3":
        par_master = 255
        mover_dim_base = 120
        mover_flash_dim = 255
        frost = 0
        focus = 128
        prism_s = 128; p1r_s = 200; prism_b = 128; prot_b = 200; prism_p = 80
        gobo_b = BSW_G1_5; gobo_p = 0

    elif sec == "outro":
        decay = max(0, sec_beat - 10) * 4
        par_master = max(60, 220 - decay)
        mover_dim_base = max(0, 60 - decay)
        mover_flash_dim = max(80, 200 - decay)
        frost = min(200, 80 + decay * 2)
        focus = 180
        prism_s = 0; p1r_s = 0; prism_b = 0; prot_b = 0; prism_p = 0
        gobo_b = 0; gobo_p = 0

    else:  # "end"
        mover_steps.append((mover_bo_idx, (0, BEAT_MS)))
        par_steps.append((par_bo_idx, (0, BEAT_MS)))
        continue

    # --- MOVER SCENE ---
    if is_bass:
        # Bass hit: snap to bright (FadeIn=0)
        s, b, p = mk_movers(pos_key, color, dim=mover_flash_dim,
                             frost=frost, focus=focus,
                             prism_s=prism_s, p1r_s=p1r_s,
                             prism_b=prism_b, prot_b=prot_b, prism_p=prism_p,
                             gobo_b=gobo_b, gobo_p=gobo_p)
        m_idx = add_scene(f"M-{sec}-{sec_beat+1}-BASS", s, b, p)
        mover_steps.append((m_idx, (0, BEAT_MS)))
    else:
        # Non-bass: smooth crossfade to dim (FadeIn=BEAT_MS, Hold=0)
        # This creates the pulse decay: bright→dim over one beat
        # Also enables smooth position drift between non-bass beats
        s, b, p = mk_movers(pos_key, color, dim=mover_dim_base,
                             frost=frost, focus=focus,
                             prism_s=prism_s, p1r_s=p1r_s,
                             prism_b=prism_b, prot_b=prot_b, prism_p=prism_p,
                             gobo_b=gobo_b, gobo_p=gobo_p)
        m_idx = add_scene(f"M-{sec}-{sec_beat+1}", s, b, p)
        mover_steps.append((m_idx, (BEAT_MS, 0)))

    # --- PAR SCENE (always snap) ---
    fb, m1, m2 = par_chase_beat(bi, color, master=par_master)
    n = ni3k_off()
    p_idx = add_scene(f"P-{sec}-{sec_beat+1}", fb, m1, m2, n)
    par_steps.append((p_idx, (0, BEAT_MS)))


# Final blackout — hold 4 beats
for _ in range(4):
    mover_steps.append((mover_bo_idx, (0, BEAT_MS)))
    par_steps.append((par_bo_idx, (0, BEAT_MS)))


# =============================================================================
# STATS & VERIFICATION
# =============================================================================

# Both chasers should have same step count and total duration
assert len(mover_steps) == len(par_steps), \
    f"Step count mismatch: movers={len(mover_steps)}, pars={len(par_steps)}"

mover_total_ms = sum(fi + ho for _, (fi, ho) in mover_steps)
par_total_ms = sum(fi + ho for _, (fi, ho) in par_steps)

print(f"\nScene dedup: {len(scenes)} unique scenes ({dedup_hits} reuses)")
print(f"Steps per chaser: {len(mover_steps)}")
print(f"Mover chaser duration: {mover_total_ms/1000:.1f}s")
print(f"Par chaser duration: {par_total_ms/1000:.1f}s")
print(f"Target: ~213s")

# Count bass pulse beats
bass_pulse_count = sum(1 for _, (fi, _) in mover_steps if fi == 0 and _ != mover_bo_idx)
smooth_count = sum(1 for _, (fi, ho) in mover_steps if fi > 0)
print(f"Mover snap beats (bass pulses + blackouts): {len(mover_steps) - smooth_count}")
print(f"Mover smooth beats (pulse decay + drift): {smooth_count}")

# Section timing breakdown
print("\nSection beat counts:")
for name, _, _ in section_bounds:
    count = section_beat_counts.get(name, 0)
    ms = count * BEAT_MS
    print(f"  {name:12s}: {count:3d} beats ({ms/1000:.1f}s)")


# =============================================================================
# CUSTOM WORKSPACE OUTPUT (with Collection support)
# =============================================================================

def write_workspace_with_collection(filename, scenes, mover_chaser, par_chaser, bpm,
                                     collection_name, vc_buttons, artnet_ip="10.0.0.7"):
    """Write QLC+ workspace with two chasers bundled in a Collection."""

    # Function ID assignment:
    # 0..N-1 = scenes
    # N = mover chaser
    # N+1 = par chaser
    # N+2 = collection
    num_scenes = len(scenes)
    mover_chaser_id = num_scenes
    par_chaser_id = num_scenes + 1
    collection_id = num_scenes + 2

    lines = []
    def L(s): lines.append(s)

    L('<?xml version="1.0" encoding="UTF-8"?>')
    L('<!DOCTYPE Workspace>')
    L('<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="VC">')
    L(' <Creator>')
    L('  <Name>Q Light Controller Plus</Name>')
    L('  <Version>5.0.1</Version>')
    L('  <Author>Ben Wilson</Author>')
    L(' </Creator>')
    L(' <Engine>')

    # InputOutputMap
    L('  <InputOutputMap>')
    L(f'   <BeatGenerator BeatType="Internal" BPM="{bpm}"/>')
    L('   <Universe Name="Universe 1" ID="0">')
    L(f'    <Output Plugin="ArtNet" UID="{artnet_ip}" Line="0"/>')
    L('   </Universe>')
    L('  </InputOutputMap>')

    # Fixtures (from showlib FIXTURE_DEFS)
    for fx in FIXTURE_DEFS:
        L('  <Fixture>')
        L(f'   <Manufacturer>{fx["mfr"]}</Manufacturer>')
        L(f'   <Model>{fx["model"]}</Model>')
        L(f'   <Mode>{fx["mode"]}</Mode>')
        L(f'   <ID>{fx["id"]}</ID>')
        L(f'   <Name>{fx["name"]}</Name>')
        L('   <Universe>0</Universe>')
        L(f'   <Address>{fx["addr"]}</Address>')
        L(f'   <Channels>{fx["ch"]}</Channels>')
        L('  </Fixture>')

    # Scenes
    for sid, sc in enumerate(scenes):
        L(f'  <Function ID="{sid}" Type="Scene" Name="{sc["name"]}" Path="{sc["path"]}">')
        L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        for fid, channels in sc["fixtures"]:
            val_str = ','.join(f'{ch},{val}' for ch, val in channels)
            L(f'   <FixtureVal ID="{fid}">{val_str}</FixtureVal>')
        L('  </Function>')

    # Mover Chaser
    mc = mover_chaser
    L(f'  <Function ID="{mover_chaser_id}" Type="Chaser" Name="{mc["name"]}" Path="{mc["path"]}">')
    L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
    L('   <Direction>Forward</Direction>')
    L(f'   <RunOrder>{mc["run_order"]}</RunOrder>')
    L('   <SpeedModes FadeIn="PerStep" FadeOut="Default" Duration="PerStep"/>')
    for step_num, (scene_id, (fi, ho)) in enumerate(zip(mc["scene_ids"], mc["timing"])):
        L(f'   <Step Number="{step_num}" FadeIn="{fi}" Hold="{ho}" FadeOut="0">{scene_id}</Step>')
    L('  </Function>')

    # Par Chaser
    pc = par_chaser
    L(f'  <Function ID="{par_chaser_id}" Type="Chaser" Name="{pc["name"]}" Path="{pc["path"]}">')
    L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
    L('   <Direction>Forward</Direction>')
    L(f'   <RunOrder>{pc["run_order"]}</RunOrder>')
    L('   <SpeedModes FadeIn="PerStep" FadeOut="Default" Duration="PerStep"/>')
    for step_num, (scene_id, (fi, ho)) in enumerate(zip(pc["scene_ids"], pc["timing"])):
        L(f'   <Step Number="{step_num}" FadeIn="{fi}" Hold="{ho}" FadeOut="0">{scene_id}</Step>')
    L('  </Function>')

    # Collection
    L(f'  <Function ID="{collection_id}" Type="Collection" Name="{collection_name}" Path="{folder}">')
    L(f'   <Step Number="0">{mover_chaser_id}</Step>')
    L(f'   <Step Number="1">{par_chaser_id}</Step>')
    L('  </Function>')

    L(' </Engine>')

    # Virtual Console
    L(' <VirtualConsole>')
    L('  <Frame Caption="">')
    L('   <Appearance>')
    L('    <FrameStyle>None</FrameStyle>')
    L('    <ForegroundColor>Default</ForegroundColor>')
    L('    <BackgroundColor>Default</BackgroundColor>')
    L('    <BackgroundImage>None</BackgroundImage>')
    L('    <Font>Default</Font>')
    L('   </Appearance>')

    for btn in vc_buttons:
        func = btn["func_id"]
        # Resolve special IDs
        if func == "COLLECTION":
            func = collection_id
        elif func == "BLACKOUT":
            func = full_bo_idx
        L(f'   <Button Caption="{btn["caption"]}" ID="{btn["vc_id"]}" Icon="">')
        L(f'    <WindowState Visible="True" X="{btn["x"]}" Y="{btn["y"]}" Width="{btn["w"]}" Height="{btn["h"]}"/>')
        L('    <Appearance>')
        L(f'     <BackgroundColor>{btn["color"]}</BackgroundColor>')
        L('    </Appearance>')
        L(f'    <Function ID="{func}"/>')
        L(f'    <Action>{btn.get("action", "Toggle")}</Action>')
        L('   </Button>')

    L('  </Frame>')
    L('  <Properties>')
    L('   <Size Width="1920" Height="1080"/>')
    L('   <GrandMaster ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal"/>')
    L('  </Properties>')
    L(' </VirtualConsole>')

    # Monitor
    L(' <Monitor DisplayMode="0" ShowLabels="0">')
    L('  <Font>Arial,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1</Font>')
    L('  <ChannelStyle>0</ChannelStyle>')
    L('  <ValueStyle>0</ValueStyle>')
    L('  <Grid Width="5" Height="3" Depth="5" Units="0"/>')
    L('  <StageItem>0</StageItem>')
    for fid, x, y_pos, z in STAGE_POSITIONS:
        L(f'  <FxItem ID="{fid}" XPos="{x}" YPos="{y_pos}" ZPos="{z}"/>')
    L(' </Monitor>')
    L('</Workspace>')

    with open(filename, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"\nWrote {filename}")
    print(f"  Scenes: {num_scenes}")
    print(f"  Chasers: 2 (Movers: {len(mc['scene_ids'])} steps, Pars: {len(pc['scene_ids'])} steps)")
    print(f"  Collection: '{collection_name}' (ID {collection_id})")


# =============================================================================
# BUILD CHASERS AND WRITE
# =============================================================================

mover_scene_ids = [s for s, _ in mover_steps]
mover_timing = [t for _, t in mover_steps]

par_scene_ids = [s for s, _ in par_steps]
par_timing = [t for _, t in par_steps]

mover_chaser = make_chaser("Jamrock - Movers", mover_scene_ids, mover_timing,
                            run_order="SingleShot", path=folder)

par_chaser = make_chaser("Jamrock - Pars", par_scene_ids, par_timing,
                          run_order="SingleShot", path=folder)

vc_buttons = [
    {"caption": "\u25b6 WELCOME TO JAMROCK", "vc_id": 0, "func_id": "COLLECTION",
     "x": 10, "y": 10, "w": 470, "h": 100,
     "color": "#228B22", "action": "Toggle"},
    {"caption": "BLACKOUT", "vc_id": 1, "func_id": "BLACKOUT",
     "x": 10, "y": 120, "w": 470, "h": 80,
     "color": "#FF0000", "action": "Toggle"},
]

write_workspace_with_collection(
    os.path.join(VENUE_DIR, "shows", "Damian Marley - Welcome To Jamrock (Explicit).qxw"),
    scenes, mover_chaser, par_chaser,
    bpm=BPM,
    collection_name="Welcome To Jamrock",
    vc_buttons=vc_buttons)
