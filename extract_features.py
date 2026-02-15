#!/usr/bin/env python3
"""
Audio Feature Extraction for Lighting Show Generation
======================================================
Runs on demucs-separated stems (bass, drums, vocals, other) and the original
mix to extract energy envelopes and onset timestamps per stem.

Designed for electronic music (house, DnB, dubstep) — frequency bands and
onset sensitivity are tuned for these genres.

Usage:
    python3 extract_features.py "songs/Artist - Track.flac" \
        --demix-dir demix \
        --allin1-json "songs-data/Artist - Track.json" \
        --output "songs-data/Artist - Track.json"

Input:
    - Original audio file (for full-mix analysis)
    - Demucs stems in demix/htdemucs/<stem_name>/{bass,drums,vocals,other}.wav
    - allin1 JSON (for beat timestamps to align energy envelopes)

Output:
    Extends the allin1 JSON with:
    - stems.{bass,drums,vocals,other}.energy   — per-beat energy (0.0–1.0)
    - stems.{bass,drums,vocals,other}.onsets    — onset timestamps (seconds)
    - energy.{sub_bass,bass,low_mid,mid,high}   — per-beat frequency band energy
    - energy.rms                                — per-beat overall loudness
    - dynamics.spectral_centroid                 — per-beat brightness (Hz)
    - dynamics.spectral_flux                    — per-beat spectral change rate
    - dynamics.onset_strength                   — per-beat onset strength (0.0–1.0)
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import librosa


# =============================================================================
# CONFIGURATION — tuned for electronic music
# =============================================================================

# Sample rate for all analysis (22050 is librosa default, good balance of
# frequency resolution and speed)
SR = 22050

# Frequency bands (Hz) for energy decomposition
# Sub-bass: the "feel it in your chest" range — drops live here
# Bass: wobble bass, reese bass, basslines above sub territory
# Low-mid: upper bass harmonics, low synth body
# Mid: lead synths, vocals, snares
# High: hi-hats, cymbals, risers, white noise
FREQ_BANDS = {
    "sub_bass": (20, 80),
    "bass": (80, 250),
    "low_mid": (250, 500),
    "mid": (500, 2000),
    "high": (2000, 11025),  # Nyquist at 22050 SR
}

# Onset detection parameters per stem — different instruments need different
# sensitivity. These were tuned for electronic music where bass hits are
# sustained (need higher delta threshold) and melodic elements are more
# transient.
ONSET_PARAMS = {
    "bass": {
        "onset_detect_method": "energy",  # energy works best for sustained bass
        "delta": 0.15,                    # moderate threshold — bass is sustained
        "wait": 4,                        # min frames between onsets (~93ms at default hop)
    },
    "drums": {
        "onset_detect_method": "spectral_flux",  # transient-sensitive
        "delta": 0.10,                            # lower threshold — catch ghost notes
        "wait": 2,                                # drums can be fast (DnB!)
    },
    "vocals": {
        "onset_detect_method": "energy",
        "delta": 0.20,                    # higher threshold — avoid breath noise
        "wait": 6,                        # vocal phrases, not syllables
    },
    "other": {
        "onset_detect_method": "spectral_flux",  # catches synth attacks, piano notes
        "delta": 0.12,                            # sensitive — this is our "melodic hits" stem
        "wait": 2,                                # individual notes in arpeggios
    },
}

# Names of demucs htdemucs stems
STEM_NAMES = ["bass", "drums", "vocals", "other"]


# =============================================================================
# AUDIO LOADING
# =============================================================================

def load_audio(path: str, sr: int = SR) -> np.ndarray:
    """Load audio file as mono waveform."""
    y, _ = librosa.load(path, sr=sr, mono=True)
    return y


# =============================================================================
# ENERGY ENVELOPE EXTRACTION
# =============================================================================

def rms_at_beats(y: np.ndarray, beat_times: list, sr: int = SR,
                 window_sec: float = 0.05) -> np.ndarray:
    """Compute RMS energy centered at each beat timestamp.

    Args:
        y: Audio waveform
        beat_times: List of beat timestamps in seconds
        sr: Sample rate
        window_sec: Window size in seconds around each beat

    Returns:
        Array of RMS values, one per beat
    """
    window_samples = int(window_sec * sr)
    rms_values = []
    for t in beat_times:
        center = int(t * sr)
        start = max(0, center - window_samples)
        end = min(len(y), center + window_samples)
        segment = y[start:end]
        if len(segment) == 0:
            rms_values.append(0.0)
        else:
            rms_values.append(float(np.sqrt(np.mean(segment ** 2))))
    return np.array(rms_values)


def bandpass_energy_at_beats(y: np.ndarray, beat_times: list,
                             freq_low: float, freq_high: float,
                             sr: int = SR) -> np.ndarray:
    """Compute energy in a frequency band at each beat.

    Uses STFT to isolate the frequency band, then measures energy at each
    beat timestamp.

    Args:
        y: Audio waveform
        beat_times: Beat timestamps in seconds
        freq_low: Lower frequency bound (Hz)
        freq_high: Upper frequency bound (Hz)
        sr: Sample rate

    Returns:
        Array of energy values, one per beat
    """
    # Compute STFT
    n_fft = 2048
    hop_length = 512
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))

    # Frequency bins
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    band_mask = (freqs >= freq_low) & (freqs <= freq_high)

    # Energy in band over time
    band_energy = np.sum(S[band_mask, :] ** 2, axis=0)
    band_energy = np.sqrt(band_energy)  # RMS-like

    # Sample at beat positions
    beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=hop_length)
    beat_frames = np.clip(beat_frames, 0, len(band_energy) - 1)

    return band_energy[beat_frames]


def normalize_0_1(arr: np.ndarray) -> list:
    """Normalize array to 0.0–1.0 range. Returns plain list for JSON."""
    if len(arr) == 0:
        return []
    arr = arr.astype(float)
    mn, mx = arr.min(), arr.max()
    if mx - mn < 1e-10:
        return [0.0] * len(arr)
    normalized = (arr - mn) / (mx - mn)
    return [round(float(x), 4) for x in normalized]


# =============================================================================
# ONSET DETECTION
# =============================================================================

def detect_onsets(y: np.ndarray, sr: int = SR,
                  method: str = "spectral_flux",
                  delta: float = 0.1,
                  wait: int = 3) -> list:
    """Detect note/hit onsets in an audio signal.

    Args:
        y: Audio waveform
        sr: Sample rate
        method: Detection method — "energy" or "spectral_flux"
        delta: Onset detection threshold (higher = fewer onsets)
        wait: Minimum frames between consecutive onsets

    Returns:
        List of onset timestamps in seconds
    """
    if np.max(np.abs(y)) < 1e-6:
        return []  # Silent stem

    # Compute onset strength envelope
    hop_length = 512

    if method == "energy":
        # Compute RMS envelope directly — librosa.onset.onset_strength passes
        # sr= to the feature function, but rms() doesn't accept it.
        rms_env = librosa.feature.rms(y=y, hop_length=hop_length)[0]
        # Differentiate to get onset-like envelope (energy increases = onsets)
        onset_env = np.diff(rms_env, prepend=0)
        onset_env = np.maximum(onset_env, 0)  # Only positive changes (attacks)
    else:  # spectral_flux (default)
        onset_env = librosa.onset.onset_strength(
            y=y, sr=sr, hop_length=hop_length
        )

    # Peak-pick onsets
    onsets = librosa.onset.onset_detect(
        y=y, sr=sr, hop_length=hop_length,
        onset_envelope=onset_env,
        delta=delta,
        wait=wait,
        units="time"
    )

    return [round(float(t), 4) for t in onsets]


# =============================================================================
# SPECTRAL FEATURES
# =============================================================================

def spectral_centroid_at_beats(y: np.ndarray, beat_times: list,
                                sr: int = SR) -> list:
    """Compute spectral centroid (brightness) at each beat.

    Returns Hz values — higher = brighter. A rising centroid over multiple
    beats usually indicates a filter sweep or riser.
    """
    hop_length = 512
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=hop_length)
    beat_frames = np.clip(beat_frames, 0, len(centroid) - 1)
    return [round(float(centroid[f]), 1) for f in beat_frames]


def spectral_flux_at_beats(y: np.ndarray, beat_times: list,
                            sr: int = SR) -> np.ndarray:
    """Compute spectral flux (rate of spectral change) at each beat.

    High flux = lots of new transient energy (hits, impacts).
    Low flux = sustained sounds (pads, drones).
    """
    hop_length = 512
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=hop_length)
    beat_frames = np.clip(beat_frames, 0, len(onset_env) - 1)
    return onset_env[beat_frames]


def onset_strength_at_beats(y: np.ndarray, beat_times: list,
                             sr: int = SR) -> np.ndarray:
    """Compute onset strength at each beat — how 'impactful' that beat is.

    This measures transient energy right at each beat position. High values
    mean a strong hit landed on that beat (kick, snare, bass drop).
    """
    hop_length = 512
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    beat_frames = librosa.time_to_frames(beat_times, sr=sr, hop_length=hop_length)
    beat_frames = np.clip(beat_frames, 0, len(onset_env) - 1)
    return onset_env[beat_frames]


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def find_stems(demix_dir: str, audio_path: str) -> dict:
    """Locate demucs stem WAV files.

    Demucs saves stems to: <demix_dir>/htdemucs/<filename_without_ext>/

    Returns dict of stem_name -> path, or empty dict if not found.
    """
    audio_name = Path(audio_path).stem
    stem_dir = Path(demix_dir) / "htdemucs" / audio_name

    if not stem_dir.exists():
        # Try without path prefix (demucs sometimes strips directory)
        # Also handle case where the audio was in a subdirectory
        candidates = list(Path(demix_dir).glob(f"htdemucs/*"))
        for candidate in candidates:
            if candidate.is_dir() and audio_name in candidate.name:
                stem_dir = candidate
                break

    stems = {}
    for name in STEM_NAMES:
        stem_path = stem_dir / f"{name}.wav"
        if stem_path.exists():
            stems[name] = str(stem_path)

    return stems


def extract_all(audio_path: str, demix_dir: str, allin1_json: str) -> dict:
    """Run the full feature extraction pipeline.

    Args:
        audio_path: Path to original audio file
        demix_dir: Path to demucs output directory
        allin1_json: Path to allin1 analysis JSON

    Returns:
        Extended analysis dict with all new features
    """
    # Load allin1 results
    with open(allin1_json) as f:
        data = json.load(f)

    beats = data["beats"]
    if len(beats) == 0:
        print("WARNING: No beats found in allin1 output. Skipping feature extraction.")
        return data

    print(f"  Extracting features for {len(beats)} beats...")

    # Load original mix
    print("  Loading mix...")
    y_mix = load_audio(audio_path)

    # --- Frequency band energy from full mix ---
    print("  Computing frequency band energy...")
    energy = {}
    for band_name, (f_low, f_high) in FREQ_BANDS.items():
        raw = bandpass_energy_at_beats(y_mix, beats, f_low, f_high)
        energy[band_name] = normalize_0_1(raw)

    # Overall RMS
    rms_raw = rms_at_beats(y_mix, beats)
    energy["rms"] = normalize_0_1(rms_raw)

    data["energy"] = energy

    # --- Spectral dynamics from full mix ---
    print("  Computing spectral dynamics...")
    dynamics = {}
    dynamics["spectral_centroid"] = spectral_centroid_at_beats(y_mix, beats)

    flux_raw = spectral_flux_at_beats(y_mix, beats)
    dynamics["spectral_flux"] = normalize_0_1(flux_raw)

    strength_raw = onset_strength_at_beats(y_mix, beats)
    dynamics["onset_strength"] = normalize_0_1(strength_raw)

    data["dynamics"] = dynamics

    # --- Per-stem analysis ---
    stems = find_stems(demix_dir, audio_path)
    if not stems:
        print(f"  WARNING: No demucs stems found in {demix_dir}. "
              f"Skipping stem analysis.")
        print(f"  (Expected stems in: {demix_dir}/htdemucs/{Path(audio_path).stem}/)")
        data["stems"] = {}
        return data

    print(f"  Found stems: {list(stems.keys())}")
    stem_data = {}

    for stem_name, stem_path in stems.items():
        print(f"  Processing {stem_name} stem...")
        y_stem = load_audio(stem_path)

        # Energy envelope at beats
        stem_rms = rms_at_beats(y_stem, beats)
        stem_energy = normalize_0_1(stem_rms)

        # Onset detection with stem-specific parameters
        params = ONSET_PARAMS.get(stem_name, ONSET_PARAMS["other"])
        onsets = detect_onsets(
            y_stem,
            method=params["onset_detect_method"],
            delta=params["delta"],
            wait=params["wait"],
        )

        stem_data[stem_name] = {
            "energy": stem_energy,
            "onsets": onsets,
            "onset_count": len(onsets),
        }

        print(f"    Energy range: {min(stem_energy):.3f} – {max(stem_energy):.3f}, "
              f"Onsets: {len(onsets)}")

    data["stems"] = stem_data

    # --- Summary stats for quick reference ---
    data["feature_summary"] = {
        "total_beats": len(beats),
        "duration_sec": round(beats[-1] - beats[0], 2) if len(beats) > 1 else 0,
        "stem_onset_counts": {
            name: stem_data[name]["onset_count"]
            for name in stem_data
        },
        "energy_bands": list(FREQ_BANDS.keys()),
    }

    return data


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Extract lighting-relevant audio features from demucs stems"
    )
    parser.add_argument("audio", help="Path to original audio file")
    parser.add_argument("--demix-dir", default="demix",
                        help="Demucs output directory (default: demix)")
    parser.add_argument("--allin1-json", required=True,
                        help="Path to allin1 analysis JSON")
    parser.add_argument("--output", required=True,
                        help="Output JSON path (will overwrite allin1 JSON if same path)")

    args = parser.parse_args()

    if not Path(args.audio).exists():
        print(f"ERROR: Audio file not found: {args.audio}")
        sys.exit(1)
    if not Path(args.allin1_json).exists():
        print(f"ERROR: allin1 JSON not found: {args.allin1_json}")
        sys.exit(1)

    print(f"Extracting features: {args.audio}")
    result = extract_all(args.audio, args.demix_dir, args.allin1_json)

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Wrote {args.output}")
    summary = result.get("feature_summary", {})
    print(f"  Beats: {summary.get('total_beats', '?')}, "
          f"Duration: {summary.get('duration_sec', '?')}s")
    for stem, count in summary.get("stem_onset_counts", {}).items():
        print(f"  {stem} onsets: {count}")


if __name__ == "__main__":
    main()
