#!/usr/bin/env python3
"""
Busking workspace generator for Home Studio - Drum & Bass + Aggressive Mood
174 BPM | Complementary color scheme | Hot/intense palette

Run from project root:
    python3 "venue/home-studio/generators/Busking-DnB-Aggressive.py"
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from showlib import *

# =============================================================================
# CONFIGURATION
# =============================================================================
VENUE = "venue/home-studio"
GENRE = "DnB"
MOOD = "Aggressive"
BPM = 174
OUTPUT = f"{VENUE}/shows/Busking-DnB-Aggressive.qxw"

# =============================================================================
# AGGRESSIVE MOOD MODIFIERS (applied to DnB genre)
# =============================================================================
# Color: Hot bias, max saturation, prefer red/white/orange/magenta
# Intensity: 80% base, max contrast, high blackout frequency
# Movement: 1.5x speed, angular/snappy, 0.5x hold
# Effects: Heavy strobe, full lasers, gobos + prism
# Timing: 0.25x fade (near instant), 2x chase speed

# Aggressive timing adjustments
FADE_MULT = 0.25     # Near-instant fades
HOLD_MULT = 0.5      # Half hold times
CHASE_MULT = 0.5     # 2x chase speed (halve the duration)

# =============================================================================
# PARSE FOCUS POSITIONS
# =============================================================================
def parse_focus_positions(venue_dir):
    """Parse focus-positions.md and return dict of position_name -> fixture_values."""
    fp_path = os.path.join(venue_dir, "focus-positions.md")
    with open(fp_path) as f:
        content = f.read()

    positions = {}
    # Split by ### headings
    sections = re.split(r'^### ', content, flags=re.MULTILINE)
    for section in sections[1:]:  # Skip content before first ###
        lines = section.strip().split('\n')
        pos_name = lines[0].strip()

        fixture_vals = {}
        in_table = False
        for line in lines[1:]:
            if line.startswith('|') and 'Fixture' not in line and '---' not in line:
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if len(cells) >= 3:
                    fixture_name = cells[0]
                    pan_str = cells[1].strip()
                    tilt_str = cells[2].strip()

                    pan = int(pan_str) if pan_str.isdigit() else None
                    tilt = int(tilt_str) if tilt_str.isdigit() else None

                    if 'Sharpy' in fixture_name:
                        fixture_vals['sharpy'] = {'pan': pan, 'tilt': tilt}
                    elif 'BSW' in fixture_name:
                        fixture_vals['bsw'] = {'pan': pan, 'tilt': tilt}
                    elif 'Profile' in fixture_name:
                        fixture_vals['profile'] = {'pan': pan, 'tilt': tilt}
                    elif 'NI3K' in fixture_name:
                        fixture_vals['ni3k'] = {'pan': pan}

        if fixture_vals:
            positions[pos_name] = fixture_vals

    return positions

POSITIONS = parse_focus_positions(VENUE)

# =============================================================================
# ARGB COLOR HELPER
# =============================================================================
def argb(r, g, b):
    """Convert RGB to QLC+ signed ARGB integer."""
    val = (0xFF << 24) | (r << 16) | (g << 8) | b
    if val >= 0x80000000:
        val -= 0x100000000
    return val

# Color constants for VC buttons
VC_RED = argb(255, 0, 0)
VC_WHITE = argb(255, 255, 255)
VC_AMBER = argb(255, 128, 0)
VC_BLUE = argb(0, 0, 255)
VC_CYAN = argb(0, 255, 255)
VC_PURPLE = argb(128, 0, 255)
VC_YELLOW = argb(255, 255, 0)
VC_GREEN = argb(0, 255, 0)
VC_ORANGE = argb(255, 140, 0)
VC_DARK_RED = argb(139, 0, 0)
VC_GREY = argb(68, 68, 68)
VC_DARK_GREY = argb(40, 40, 40)
VC_BLACK = argb(0, 0, 0)

# =============================================================================
# LAYER 1: COLOR PALETTE
# Aggressive DnB: Hot bias, complementary pairs, max saturation
# Selected pairs: Classic DnB, Blood Moon, Whiteout, Fire & Ice
# =============================================================================
all_scenes = []

def add_scene(name, *fixtures, path="Busking"):
    s = scene(name, *fixtures, path=path)
    all_scenes.append(s)
    return len(all_scenes) - 1  # Return scene index as function ID

# --- Two-Color Pair: Classic DnB (Red movers / Blue pars) ---
s_classic_a = add_scene("Classic DnB A",
    sharpy(colormacro=SHARPY_RED),
    bsw(color=BSW_RED),
    profile(color=PROF_RED),
    fourbar_solid(0, 0, 255),
    miss_both(0, 0, 255),
    ni3k(r=255, g=0, b=0, halo=H_RED),
    path="Busking/Colors")

s_classic_b = add_scene("Classic DnB B",
    sharpy(colormacro=SHARPY_BLUE),
    bsw(color=BSW_BLUE),
    profile(color=PROF_BLUE),
    fourbar_solid(255, 0, 0),
    miss_both(255, 0, 0),
    ni3k(r=0, g=0, b=255, halo=H_BLU),
    path="Busking/Colors")

# --- Two-Color Pair: Blood Moon (Red movers / Amber pars) ---
s_blood_a = add_scene("Blood Moon A",
    sharpy(colormacro=SHARPY_RED),
    bsw(color=BSW_RED),
    profile(color=PROF_RED),
    fourbar_solid(255, 128, 0),
    miss_both(255, 128, 0),
    ni3k(r=255, g=0, b=0, halo=H_RED),
    path="Busking/Colors")

s_blood_b = add_scene("Blood Moon B",
    sharpy(colormacro=SHARPY_AMBER),
    bsw(color=BSW_ORANGE),
    profile(color=PROF_ORANGE),
    fourbar_solid(255, 0, 0),
    miss_both(255, 0, 0),
    ni3k(r=255, g=128, b=0, halo=H_YEL),
    path="Busking/Colors")

# --- Two-Color Pair: Whiteout (White movers / Red pars) ---
s_white_a = add_scene("Whiteout A",
    sharpy(colormacro=SHARPY_WHITE),
    bsw(color=BSW_WHITE),
    profile(color=PROF_WHITE),
    fourbar_solid(255, 0, 0),
    miss_both(255, 0, 0),
    ni3k(r=255, g=255, b=255, halo=H_RGB),
    path="Busking/Colors")

s_white_b = add_scene("Whiteout B",
    sharpy(colormacro=SHARPY_RED),
    bsw(color=BSW_RED),
    profile(color=PROF_RED),
    fourbar_solid(255, 255, 255),
    miss_both(255, 255, 255),
    ni3k(r=255, g=0, b=0, halo=H_RED),
    path="Busking/Colors")

# --- Two-Color Pair: Fire & Ice (Red movers / Cyan pars) ---
s_fire_a = add_scene("Fire & Ice A",
    sharpy(colormacro=SHARPY_RED),
    bsw(color=BSW_RED),
    profile(color=PROF_RED),
    fourbar_solid(0, 255, 255),
    miss_both(0, 255, 255),
    ni3k(r=255, g=0, b=0, halo=H_RED),
    path="Busking/Colors")

s_fire_b = add_scene("Fire & Ice B",
    sharpy(colormacro=SHARPY_TEAL),
    bsw(color=BSW_TEAL),
    profile(color=PROF_TEAL),
    fourbar_solid(255, 0, 0),
    miss_both(255, 0, 0),
    ni3k(r=0, g=255, b=255, halo=H_CYN),
    path="Busking/Colors")

# --- Single-Color Washes ---
s_all_white = add_scene("ALL WHITE",
    sharpy(colormacro=SHARPY_WHITE),
    bsw(color=BSW_WHITE),
    profile(color=PROF_WHITE),
    fourbar_solid(255, 255, 255),
    miss_both(255, 255, 255),
    ni3k(r=255, g=255, b=255, w=255, halo=H_RGB),
    path="Busking/Colors")

s_all_red = add_scene("ALL RED",
    sharpy(colormacro=SHARPY_RED),
    bsw(color=BSW_RED),
    profile(color=PROF_RED),
    fourbar_solid(255, 0, 0),
    miss_both(255, 0, 0),
    ni3k(r=255, g=0, b=0, halo=H_RED),
    path="Busking/Colors")

# =============================================================================
# LAYER 2: POSITION PRESETS (movers only — pan/tilt, safe defaults)
# =============================================================================
def pos_scene(name, pos_key, path="Busking/Positions"):
    """Create a scene with mover pan/tilt from focus-positions data."""
    pos = POSITIONS.get(pos_key, POSITIONS.get("Center (C)", {}))
    fixtures = []

    s = pos.get('sharpy', {})
    if s.get('pan') is not None:
        fixtures.append(sharpy(pan=s['pan'], tilt=s.get('tilt', 0)))

    b = pos.get('bsw', {})
    if b.get('pan') is not None:
        fixtures.append(bsw(pan=b['pan'], tilt=b.get('tilt', 19)))

    p = pos.get('profile', {})
    if p.get('pan') is not None:
        fixtures.append(profile(pan=p['pan'], tilt=p.get('tilt', 123)))

    n = pos.get('ni3k', {})
    if n.get('pan') is not None:
        fixtures.append(ni3k(pan=n['pan']))

    return add_scene(name, *fixtures, path=path)

# Area positions
s_pos_c = pos_scene("POS: Center", "Center (C)")
s_pos_dsc = pos_scene("POS: DSC", "Downstage Center (DSC)")
s_pos_usc = pos_scene("POS: USC", "Upstage Center (USC)")
s_pos_sl = pos_scene("POS: SL", "Stage Left (SL)")
s_pos_sr = pos_scene("POS: SR", "Stage Right (SR)")
s_pos_dsl = pos_scene("POS: DSL", "Downstage Left (DSL)")
s_pos_dsr = pos_scene("POS: DSR", "Downstage Right (DSR)")
s_pos_usl = pos_scene("POS: USL", "Upstage Left (USL)")
s_pos_usr = pos_scene("POS: USR", "Upstage Right (USR)")

# Specials
s_pos_dj = pos_scene("POS: DJ Booth", "DJ Booth")
s_pos_dance = pos_scene("POS: Dance Floor", "Dance Floor")
s_pos_ceil = pos_scene("POS: Ceiling", "Center Ceiling")

# Effects
s_pos_blinder = pos_scene("POS: Blinder", "Audience Blinder")
s_pos_sweep_l = pos_scene("POS: Sweep Far L", "Sweep Far Left")
s_pos_sweep_r = pos_scene("POS: Sweep Far R", "Sweep Far Right")

# =============================================================================
# LAYER 3: MOVEMENT CHASERS
# Aggressive mood: 1.5x speed, angular movement
# =============================================================================

# LR Sweep: Far Left → SL → C → SR → Far Right (PingPong, aggressive speed)
sweep_lr_scenes = [s_pos_sweep_l, s_pos_sl, s_pos_c, s_pos_sr, s_pos_sweep_r]
# At 174 BPM, 1-bar smooth = 1379ms. Aggressive 1.5x speed = ~920ms per step
sweep_ms = int(bpm_to_ms(BPM, 4) * CHASE_MULT)  # 2-bar smooth at 2x speed = 1-bar
sweep_timing = [(sweep_ms, 0)] * len(sweep_lr_scenes)

# RL Sweep (reverse)
sweep_rl_scenes = list(reversed(sweep_lr_scenes))

# Narrow LR: SL → C → SR (tight, fast)
narrow_scenes = [s_pos_sl, s_pos_c, s_pos_sr]
narrow_ms = int(bpm_to_ms(BPM, 2) * CHASE_MULT)  # 1-beat smooth at aggressive speed
narrow_timing = [(narrow_ms, 0)] * len(narrow_scenes)

# Cross: USL → DSR, USR → DSL alternating
cross_scenes = [s_pos_usl, s_pos_dsr, s_pos_usr, s_pos_dsl]
cross_ms = int(bpm_to_ms(BPM, 2) * CHASE_MULT)
cross_timing = [(cross_ms, 0)] * len(cross_scenes)

# Front-Back: DSC → C → USC
fb_scenes = [s_pos_dsc, s_pos_c, s_pos_usc]
fb_ms = int(bpm_to_ms(BPM, 4) * CHASE_MULT)
fb_timing = [(fb_ms, 0)] * len(fb_scenes)

# Beat snap sweep: SL → C → SR with instant snaps (aggressive angular movement)
snap_scenes = [s_pos_sl, s_pos_c, s_pos_sr, s_pos_c]
snap_ms = int(bpm_to_ms(BPM, 1))  # 1 beat per position
snap_timing = [(50, snap_ms - 50)] * len(snap_scenes)  # Near-instant fade

# =============================================================================
# LAYER 4: STROBE & FLASH
# Aggressive: Heavy strobe is the primary effect
# =============================================================================

# Strobe All — fast strobe on every fixture
s_strobe_all = add_scene("STROBE ALL",
    sharpy(strobe=SHARPY_STROBE_FAST),
    bsw(shutter=BSW_SHUT_STROBE_FAST),
    profile(strobe=128),
    fourbar_solid(255, 255, 255, strobe=200),
    miss_both(255, 255, 255, strobe=200),
    ni3k(r=255, g=255, b=255, strobe=200),
    path="Busking/Strobes")

# Strobe Movers only
s_strobe_movers = add_scene("STROBE MOVERS",
    sharpy(strobe=SHARPY_STROBE_FAST),
    bsw(shutter=BSW_SHUT_STROBE_FAST),
    profile(strobe=128),
    path="Busking/Strobes")

# Strobe Pars only
s_strobe_pars = add_scene("STROBE PARS",
    fourbar_solid(255, 255, 255, strobe=200),
    miss_both(255, 255, 255, strobe=200),
    ni3k(strobe=200),
    path="Busking/Strobes")

# Flash White — momentary full white all fixtures
s_flash_white = add_scene("FLASH WHITE",
    sharpy(colormacro=SHARPY_WHITE, dim=255),
    bsw(color=BSW_WHITE, dim=255),
    profile(color=PROF_WHITE, dim=255),
    fourbar_solid(255, 255, 255),
    miss_both(255, 255, 255),
    ni3k(r=255, g=255, b=255, w=255, halo=H_RGB),
    path="Busking/Strobes")

# =============================================================================
# LAYER 5: SPECIAL MOMENTS
# =============================================================================

# BLACKOUT
s_blackout = add_scene("BLACKOUT", *blackout_all(), path="Busking/Specials")

# WHITEOUT — all fixtures full white + strobe
s_whiteout = add_scene("WHITEOUT",
    sharpy(colormacro=SHARPY_WHITE, dim=255, strobe=SHARPY_STROBE_FAST),
    bsw(color=BSW_WHITE, dim=255, shutter=BSW_SHUT_STROBE_FAST),
    profile(color=PROF_WHITE, dim=255, strobe=128),
    fourbar_solid(255, 255, 255, strobe=200),
    miss_both(255, 255, 255, strobe=200),
    ni3k(r=255, g=255, b=255, w=255, strobe=200, halo=H_RGB,
         rl=LASER_ON, gl=LASER_ON, bl=LASER_ON),
    path="Busking/Specials")

# LASERS ON
s_lasers_on = add_scene("LASERS ON",
    ni3k(rl=LASER_ON, gl=LASER_ON, bl=LASER_ON, dim=0, r=0, g=0, b=0, halo=H_OFF),
    path="Busking/Specials")

# LASERS STROBE
s_lasers_strobe = add_scene("LASERS STROBE",
    ni3k(rl=LASER_STROBE_FAST, gl=LASER_STROBE_FAST, bl=LASER_STROBE_FAST,
         dim=0, r=0, g=0, b=0, halo=H_OFF),
    path="Busking/Specials")

# LASERS OFF
s_lasers_off = add_scene("LASERS OFF",
    ni3k(rl=LASER_OFF, gl=LASER_OFF, bl=LASER_OFF),
    path="Busking/Specials")

# PRISM CHAOS — all movers: prism on + rotation, gobo on
s_prism_chaos = add_scene("PRISM CHAOS",
    sharpy(prism1=128, p1r=200, prism2=128, p2r=200, gobo=30),
    bsw(prism=200, prot=160, gobo1=BSW_G1_3),
    profile(prism=200, gobo=30),
    path="Busking/Specials")

# GOBO TEXTURE — movers with gobos, no prism
s_gobo_texture = add_scene("GOBO TEXTURE",
    sharpy(gobo=30),
    bsw(gobo1=BSW_G1_2, gobo2=BSW_G2_3),
    profile(gobo=20, gobo1=20),
    path="Busking/Specials")

# OPEN BEAM — clean movers, no gobo/prism/frost
s_open_beam = add_scene("OPEN BEAM",
    sharpy(gobo=0, prism1=0, prism2=0, frost=0),
    bsw(gobo1=0, gobo2=0, prism=0, frost=0),
    profile(gobo=0, gobo1=0, prism=0),
    path="Busking/Specials")

# NI3K SPIN — NI3K heads in fast rotation
s_ni3k_spin = add_scene("NI3K SPIN",
    ni3k(t1=180, t2=220, t3=160, moteff=100, effspd=200),
    path="Busking/Specials")

# HOME — center position, red, full intensity (aggressive home state)
s_home = add_scene("HOME",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED),
    bsw(pan=177, tilt=19, color=BSW_RED),
    profile(pan=0, tilt=123, color=PROF_RED),
    fourbar_solid(255, 0, 0),
    miss_both(255, 0, 0),
    ni3k(pan=128, r=255, g=0, b=0, halo=H_RED),
    path="Busking/Specials")

# MOOD: AGGRESSIVE LOW — single fixture, tight red beam
s_mood_low = add_scene("AGGR LOW",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=200),
    bsw(dim=0),
    profile(dim=0),
    fourbar_solid(0, 0, 0),
    miss_both(0, 0, 0),
    ni3k(dim=0, r=0, g=0, b=0, halo=H_OFF),
    path="Busking/Mood")

# MOOD: AGGRESSIVE MID — movers + pars, snappy
s_mood_mid = add_scene("AGGR MID",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=255),
    bsw(pan=177, tilt=19, color=BSW_RED, dim=255),
    profile(dim=0),
    fourbar_solid(255, 0, 0),
    miss_both(0, 0, 0),
    ni3k(r=255, g=0, b=0, dim=200, halo=H_RED),
    path="Busking/Mood")

# MOOD: AGGRESSIVE HIGH — full rig blast
s_mood_high = add_scene("AGGR HIGH",
    sharpy(pan=153, tilt=0, colormacro=SHARPY_RED, dim=255,
           prism1=128, p1r=200, gobo=30),
    bsw(pan=177, tilt=19, color=BSW_RED, dim=255,
        prism=200, prot=160, gobo1=BSW_G1_3),
    profile(pan=0, tilt=123, color=PROF_RED, dim=255, prism=200),
    fourbar_solid(255, 0, 0),
    miss_both(255, 0, 0),
    ni3k(r=255, g=0, b=0, dim=255, halo=H_RED,
         rl=LASER_ON, gl=LASER_ON, bl=LASER_ON,
         t1=180, t2=220, t3=160),
    path="Busking/Mood")

# =============================================================================
# BUILD CHASERS
# =============================================================================
all_chasers = []
chaser_base_id = len(all_scenes)

def add_chaser(name, scene_ids, timing, run_order="Loop", path="Busking/Movement"):
    ch = make_chaser(name, scene_ids, timing, run_order=run_order, path=path)
    all_chasers.append(ch)
    return chaser_base_id + len(all_chasers) - 1

# Color pair chasers (2-step loop for tap-swap)
ch_classic = add_chaser("Classic DnB", [s_classic_a, s_classic_b],
    [(0, 60000), (0, 60000)], run_order="Loop", path="Busking/Colors")

ch_blood = add_chaser("Blood Moon", [s_blood_a, s_blood_b],
    [(0, 60000), (0, 60000)], run_order="Loop", path="Busking/Colors")

ch_whiteout_pair = add_chaser("Whiteout", [s_white_a, s_white_b],
    [(0, 60000), (0, 60000)], run_order="Loop", path="Busking/Colors")

ch_fire = add_chaser("Fire & Ice", [s_fire_a, s_fire_b],
    [(0, 60000), (0, 60000)], run_order="Loop", path="Busking/Colors")

# Movement chasers
ch_lr_sweep = add_chaser("LR SWEEP", sweep_lr_scenes, sweep_timing,
    run_order="PingPong")

ch_rl_sweep = add_chaser("RL SWEEP", sweep_rl_scenes, sweep_timing,
    run_order="PingPong")

ch_narrow = add_chaser("NARROW LR", narrow_scenes, narrow_timing,
    run_order="PingPong")

ch_cross = add_chaser("CROSS", cross_scenes, cross_timing,
    run_order="Loop")

ch_front_back = add_chaser("FRONT-BACK", fb_scenes, fb_timing,
    run_order="PingPong")

ch_beat_snap = add_chaser("BEAT SNAP", snap_scenes, snap_timing,
    run_order="Loop")

# =============================================================================
# VIRTUAL CONSOLE LAYOUT — Direct XML Generation
# =============================================================================
def generate_vc_xml():
    """Generate the complete Virtual Console XML section."""
    lines = []
    def L(s): lines.append(s)

    vc_id = 0

    def next_vc_id():
        nonlocal vc_id
        vid = vc_id
        vc_id += 1
        return vid

    # Main frame
    L(' <VirtualConsole>')
    L('  <Frame Caption="">')
    L('   <Appearance>')
    L('    <FrameStyle>None</FrameStyle>')
    L('    <ForegroundColor>Default</ForegroundColor>')
    L('    <BackgroundColor>Default</BackgroundColor>')
    L('    <BackgroundImage>None</BackgroundImage>')
    L('    <Font>Default</Font>')
    L('   </Appearance>')

    # =============================================
    # COLUMN 1: COLORS (Solo Frame) — X=10, W=260
    # =============================================
    colors_frame_id = next_vc_id()
    L(f'   <SoloFrame Caption="COLORS" ID="{colors_frame_id}">')
    L(f'    <WindowState Visible="True" X="10" Y="10" Width="260" Height="520"/>')
    L('    <Appearance>')
    L('     <BackgroundColor>Default</BackgroundColor>')
    L('    </Appearance>')
    L('    <AllowChildren>True</AllowChildren>')
    L('    <AllowResize>True</AllowResize>')
    L('    <ShowHeader>True</ShowHeader>')
    L('    <ShowEnableButton>True</ShowEnableButton>')
    L('    <Collapsed>False</Collapsed>')
    L('    <Disabled>False</Disabled>')

    # Color pair buttons (each triggers a 2-step chaser)
    color_buttons = [
        ("CLASSIC DnB", ch_classic, VC_RED),
        ("BLOOD MOON", ch_blood, VC_DARK_RED),
        ("WHITEOUT", ch_whiteout_pair, VC_WHITE),
        ("FIRE & ICE", ch_fire, VC_ORANGE),
    ]
    by = 30
    for label, func_id, color in color_buttons:
        bid = next_vc_id()
        L(f'    <Button Caption="{xml_escape(label)}" ID="{bid}" Icon="">')
        L(f'     <WindowState Visible="True" X="10" Y="{by}" Width="240" Height="55"/>')
        L('     <Appearance>')
        L(f'      <BackgroundColor>{color}</BackgroundColor>')
        L('     </Appearance>')
        L(f'     <Function ID="{func_id}"/>')
        L('     <Action>Toggle</Action>')
        L('    </Button>')
        by += 65

    # Single-color wash buttons
    wash_buttons = [
        ("ALL WHITE", s_all_white, VC_WHITE),
        ("ALL RED", s_all_red, VC_RED),
    ]
    by += 10
    for label, func_id, color in wash_buttons:
        bid = next_vc_id()
        L(f'    <Button Caption="{xml_escape(label)}" ID="{bid}" Icon="">')
        L(f'     <WindowState Visible="True" X="10" Y="{by}" Width="240" Height="50"/>')
        L('     <Appearance>')
        L(f'      <BackgroundColor>{color}</BackgroundColor>')
        L('     </Appearance>')
        L(f'     <Function ID="{func_id}"/>')
        L('     <Action>Toggle</Action>')
        L('    </Button>')
        by += 60

    L('   </SoloFrame>')

    # =============================================
    # COLUMN 2: POSITIONS (Solo Frame) — X=280, W=230
    # =============================================
    pos_frame_id = next_vc_id()
    L(f'   <SoloFrame Caption="POSITIONS" ID="{pos_frame_id}">')
    L(f'    <WindowState Visible="True" X="280" Y="10" Width="230" Height="700"/>')
    L('    <Appearance>')
    L('     <BackgroundColor>Default</BackgroundColor>')
    L('    </Appearance>')
    L('    <AllowChildren>True</AllowChildren>')
    L('    <AllowResize>True</AllowResize>')
    L('    <ShowHeader>True</ShowHeader>')
    L('    <ShowEnableButton>True</ShowEnableButton>')
    L('    <Collapsed>False</Collapsed>')
    L('    <Disabled>False</Disabled>')

    pos_buttons = [
        ("CENTER", s_pos_c),
        ("DSC", s_pos_dsc),
        ("USC", s_pos_usc),
        ("SL", s_pos_sl),
        ("SR", s_pos_sr),
        ("DSL", s_pos_dsl),
        ("DSR", s_pos_dsr),
        ("USL", s_pos_usl),
        ("USR", s_pos_usr),
        ("DJ BOOTH", s_pos_dj),
        ("DANCE FLR", s_pos_dance),
        ("CEILING", s_pos_ceil),
    ]
    by = 30
    for label, func_id in pos_buttons:
        bid = next_vc_id()
        L(f'    <Button Caption="{xml_escape(label)}" ID="{bid}" Icon="">')
        L(f'     <WindowState Visible="True" X="10" Y="{by}" Width="210" Height="45"/>')
        L('     <Appearance>')
        L(f'      <BackgroundColor>{VC_GREY}</BackgroundColor>')
        L('     </Appearance>')
        L(f'     <Function ID="{func_id}"/>')
        L('     <Action>Toggle</Action>')
        L('    </Button>')
        by += 52

    L('   </SoloFrame>')

    # =============================================
    # COLUMN 3: MOVEMENT + STROBES — X=520, W=240
    # =============================================
    move_frame_id = next_vc_id()
    L(f'   <Frame Caption="MOVEMENT" ID="{move_frame_id}">')
    L(f'    <WindowState Visible="True" X="520" Y="10" Width="240" Height="420"/>')
    L('    <Appearance>')
    L('     <BackgroundColor>Default</BackgroundColor>')
    L('    </Appearance>')
    L('    <AllowChildren>True</AllowChildren>')
    L('    <AllowResize>True</AllowResize>')
    L('    <ShowHeader>True</ShowHeader>')
    L('    <ShowEnableButton>True</ShowEnableButton>')
    L('    <Collapsed>False</Collapsed>')
    L('    <Disabled>False</Disabled>')

    move_buttons = [
        ("LR SWEEP", ch_lr_sweep, VC_GREY),
        ("RL SWEEP", ch_rl_sweep, VC_GREY),
        ("NARROW LR", ch_narrow, VC_GREY),
        ("CROSS", ch_cross, VC_GREY),
        ("FRONT-BACK", ch_front_back, VC_GREY),
        ("BEAT SNAP", ch_beat_snap, VC_ORANGE),
    ]
    by = 30
    for label, func_id, color in move_buttons:
        bid = next_vc_id()
        L(f'    <Button Caption="{xml_escape(label)}" ID="{bid}" Icon="">')
        L(f'     <WindowState Visible="True" X="10" Y="{by}" Width="220" Height="50"/>')
        L('     <Appearance>')
        L(f'      <BackgroundColor>{color}</BackgroundColor>')
        L('     </Appearance>')
        L(f'     <Function ID="{func_id}"/>')
        L('     <Action>Toggle</Action>')
        L('    </Button>')
        by += 58

    L('   </Frame>')

    # Strobe frame
    strobe_frame_id = next_vc_id()
    L(f'   <Frame Caption="STROBES" ID="{strobe_frame_id}">')
    L(f'    <WindowState Visible="True" X="520" Y="440" Width="240" Height="310"/>')
    L('    <Appearance>')
    L('     <BackgroundColor>Default</BackgroundColor>')
    L('    </Appearance>')
    L('    <AllowChildren>True</AllowChildren>')
    L('    <AllowResize>True</AllowResize>')
    L('    <ShowHeader>True</ShowHeader>')
    L('    <ShowEnableButton>True</ShowEnableButton>')
    L('    <Collapsed>False</Collapsed>')
    L('    <Disabled>False</Disabled>')

    strobe_buttons = [
        ("STROBE ALL", s_strobe_all, VC_YELLOW, "Flash"),
        ("STROBE MOVERS", s_strobe_movers, VC_YELLOW, "Flash"),
        ("STROBE PARS", s_strobe_pars, VC_YELLOW, "Flash"),
        ("FLASH WHITE", s_flash_white, VC_WHITE, "Flash"),
    ]
    by = 30
    for label, func_id, color, action in strobe_buttons:
        bid = next_vc_id()
        L(f'    <Button Caption="{xml_escape(label)}" ID="{bid}" Icon="">')
        L(f'     <WindowState Visible="True" X="10" Y="{by}" Width="220" Height="55"/>')
        L('     <Appearance>')
        L(f'      <BackgroundColor>{color}</BackgroundColor>')
        L('     </Appearance>')
        L(f'     <Function ID="{func_id}"/>')
        L(f'     <Action>{action}</Action>')
        L('    </Button>')
        by += 62

    L('   </Frame>')

    # =============================================
    # COLUMN 4: SPECIALS — X=770, W=240
    # =============================================
    special_frame_id = next_vc_id()
    L(f'   <Frame Caption="SPECIALS" ID="{special_frame_id}">')
    L(f'    <WindowState Visible="True" X="770" Y="10" Width="240" Height="750"/>')
    L('    <Appearance>')
    L('     <BackgroundColor>Default</BackgroundColor>')
    L('    </Appearance>')
    L('    <AllowChildren>True</AllowChildren>')
    L('    <AllowResize>True</AllowResize>')
    L('    <ShowHeader>True</ShowHeader>')
    L('    <ShowEnableButton>True</ShowEnableButton>')
    L('    <Collapsed>False</Collapsed>')
    L('    <Disabled>False</Disabled>')

    special_buttons = [
        ("BLACKOUT", s_blackout, VC_RED, "Toggle"),
        ("WHITEOUT", s_whiteout, VC_WHITE, "Flash"),
        ("HOME", s_home, VC_ORANGE, "Toggle"),
        ("LASERS ON", s_lasers_on, VC_GREEN, "Toggle"),
        ("LASERS STROBE", s_lasers_strobe, VC_GREEN, "Flash"),
        ("LASERS OFF", s_lasers_off, VC_DARK_GREY, "Toggle"),
        ("PRISM CHAOS", s_prism_chaos, VC_ORANGE, "Toggle"),
        ("GOBO TEXTURE", s_gobo_texture, VC_ORANGE, "Toggle"),
        ("OPEN BEAM", s_open_beam, VC_GREY, "Toggle"),
        ("NI3K SPIN", s_ni3k_spin, VC_PURPLE, "Toggle"),
    ]
    by = 30
    for label, func_id, color, action in special_buttons:
        bid = next_vc_id()
        L(f'    <Button Caption="{xml_escape(label)}" ID="{bid}" Icon="">')
        L(f'     <WindowState Visible="True" X="10" Y="{by}" Width="220" Height="60"/>')
        L('     <Appearance>')
        L(f'      <BackgroundColor>{color}</BackgroundColor>')
        L('     </Appearance>')
        L(f'     <Function ID="{func_id}"/>')
        L(f'     <Action>{action}</Action>')
        L('    </Button>')
        by += 68

    L('   </Frame>')

    # =============================================
    # COLUMN 5: MOOD — X=1020, W=200
    # =============================================
    mood_frame_id = next_vc_id()
    L(f'   <Frame Caption="MOOD" ID="{mood_frame_id}">')
    L(f'    <WindowState Visible="True" X="1020" Y="10" Width="200" Height="260"/>')
    L('    <Appearance>')
    L('     <BackgroundColor>Default</BackgroundColor>')
    L('    </Appearance>')
    L('    <AllowChildren>True</AllowChildren>')
    L('    <AllowResize>True</AllowResize>')
    L('    <ShowHeader>True</ShowHeader>')
    L('    <ShowEnableButton>True</ShowEnableButton>')
    L('    <Collapsed>False</Collapsed>')
    L('    <Disabled>False</Disabled>')

    mood_buttons = [
        ("AGGR LOW", s_mood_low, VC_DARK_RED, "Toggle"),
        ("AGGR MID", s_mood_mid, VC_RED, "Toggle"),
        ("AGGR HIGH", s_mood_high, VC_RED, "Toggle"),
    ]
    by = 30
    for label, func_id, color, action in mood_buttons:
        bid = next_vc_id()
        L(f'    <Button Caption="{xml_escape(label)}" ID="{bid}" Icon="">')
        L(f'     <WindowState Visible="True" X="10" Y="{by}" Width="180" Height="60"/>')
        L('     <Appearance>')
        L(f'      <BackgroundColor>{color}</BackgroundColor>')
        L('     </Appearance>')
        L(f'     <Function ID="{func_id}"/>')
        L(f'     <Action>{action}</Action>')
        L('    </Button>')
        by += 68

    L('   </Frame>')

    # =============================================
    # INTENSITY SLIDERS — Bottom row Y=770
    # =============================================
    # Movers slider
    slider_id = next_vc_id()
    L(f'   <Slider Caption="MOVERS" ID="{slider_id}" WidgetStyle="Slider" InvertedAppearance="false">')
    L(f'    <WindowState Visible="True" X="10" Y="770" Width="120" Height="300"/>')
    L('    <SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None" Monitor="false">Level</SliderMode>')
    L('    <Level LowLimit="0" HighLimit="255" Value="255">')
    L(f'     <Channel Fixture="{FX_SHARPY}">7</Channel>')   # Sharpy dimmer
    L(f'     <Channel Fixture="{FX_BSW}">17</Channel>')     # BSW dimmer
    L(f'     <Channel Fixture="{FX_PROFILE}">0</Channel>')  # Profile dimmer
    L('    </Level>')
    L('   </Slider>')

    # Pars slider
    slider_id = next_vc_id()
    L(f'   <Slider Caption="PARS" ID="{slider_id}" WidgetStyle="Slider" InvertedAppearance="false">')
    L(f'    <WindowState Visible="True" X="140" Y="770" Width="120" Height="300"/>')
    L('    <SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None" Monitor="false">Level</SliderMode>')
    L('    <Level LowLimit="0" HighLimit="255" Value="255">')
    L(f'     <Channel Fixture="{FX_4BAR}">1</Channel>')    # 4BAR master
    L(f'     <Channel Fixture="{FX_MISS1}">0</Channel>')   # Missyee 1 master
    L(f'     <Channel Fixture="{FX_MISS2}">0</Channel>')   # Missyee 2 master
    L('    </Level>')
    L('   </Slider>')

    # NI3K slider
    slider_id = next_vc_id()
    L(f'   <Slider Caption="NI3K" ID="{slider_id}" WidgetStyle="Slider" InvertedAppearance="false">')
    L(f'    <WindowState Visible="True" X="270" Y="770" Width="120" Height="300"/>')
    L('    <SliderMode ValueDisplayStyle="Exact" ClickAndGoType="None" Monitor="false">Level</SliderMode>')
    L('    <Level LowLimit="0" HighLimit="255" Value="255">')
    L(f'     <Channel Fixture="{FX_NI3K}">5</Channel>')    # NI3K dimmer
    L('    </Level>')
    L('   </Slider>')

    # Close main frame
    L('  </Frame>')
    L('  <Properties>')
    L('   <Size Width="1920" Height="1080"/>')
    L('   <GrandMaster ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal"/>')
    L('  </Properties>')
    L(' </VirtualConsole>')

    return '\n'.join(lines)

# =============================================================================
# WRITE WORKSPACE (custom to support Solo Frames, Sliders)
# =============================================================================
def xml_escape(s):
    """Escape special XML characters."""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def write_busking_workspace():
    """Write complete busking workspace with custom VC layout."""
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
    L(f'   <BeatGenerator BeatType="Internal" BPM="{BPM}"/>')
    L('   <Universe Name="Universe 1" ID="0">')
    L('    <Output Plugin="ArtNet" UID="10.0.0.7" Line="0"/>')
    L('   </Universe>')
    L('  </InputOutputMap>')

    # Fixtures (in ID order)
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
    for sid, sc in enumerate(all_scenes):
        L(f'  <Function ID="{sid}" Type="Scene" Name="{xml_escape(sc["name"])}" Path="{xml_escape(sc["path"])}">')
        L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        for fid, channels in sc["fixtures"]:
            val_str = ','.join(f'{ch},{val}' for ch, val in channels)
            L(f'   <FixtureVal ID="{fid}">{val_str}</FixtureVal>')
        L('  </Function>')

    # Chasers
    for i, ch in enumerate(all_chasers):
        cid = chaser_base_id + i
        L(f'  <Function ID="{cid}" Type="Chaser" Name="{xml_escape(ch["name"])}" Path="{xml_escape(ch["path"])}">')
        L('   <Speed FadeIn="0" FadeOut="0" Duration="0"/>')
        L('   <Direction>Forward</Direction>')
        L(f'   <RunOrder>{ch["run_order"]}</RunOrder>')
        L('   <SpeedModes FadeIn="PerStep" FadeOut="Default" Duration="PerStep"/>')
        for step_num, (scene_id, (fi, ho)) in enumerate(zip(ch["scene_ids"], ch["timing"])):
            L(f'   <Step Number="{step_num}" FadeIn="{fi}" Hold="{ho}" FadeOut="0">{scene_id}</Step>')
        L('  </Function>')

    L(' </Engine>')

    # Virtual Console (custom layout)
    L(generate_vc_xml())

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

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Wrote {OUTPUT}")
    print(f"  Scenes: {len(all_scenes)}")
    print(f"  Chasers: {len(all_chasers)}")
    total_funcs = len(all_scenes) + len(all_chasers)
    print(f"  Total functions: {total_funcs}")

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    write_busking_workspace()
