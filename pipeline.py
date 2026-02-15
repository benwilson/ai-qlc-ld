#!/usr/bin/env python3
"""
Unified Analysis Pipeline
=========================
Replaces the raw allin1 CLI entrypoint. Runs:
  1. allin1.analyze() with keep_byproducts=True (saves demucs stems)
  2. extract_features.py on the saved stems

This gives us structure + beats + BPM (from allin1) plus energy envelopes
and onset timestamps per stem (from our extraction) — all in one pass,
one demucs run.

Usage:
    python3 pipeline.py <audio_file> [<audio_file> ...] -o <output_dir> -d cpu

Compatible with the same arguments as the old allin1 CLI for easy migration.
"""

import argparse
import json
import sys
import traceback
from pathlib import Path

# allin1 Python API
import allin1

# Our feature extraction
sys.path.insert(0, "/usr/local/bin")
from extract_features import extract_all


def result_to_dict(result) -> dict:
    """Convert an allin1 AnalysisResult to a JSON-serializable dict.

    allin1.analyze() returns AnalysisResult objects, not dicts. We need to
    convert them to match the JSON format the old CLI produced.
    """
    d = {
        "path": str(result.path),
        "bpm": result.bpm,
        "beats": [round(float(b), 4) for b in result.beats],
        "downbeats": [round(float(b), 4) for b in result.downbeats],
        "beat_positions": [int(bp) for bp in result.beat_positions],
        "segments": [
            {
                "start": round(float(seg.start), 2),
                "end": round(float(seg.end), 2),
                "label": seg.label,
            }
            for seg in result.segments
        ],
    }
    return d


def run_pipeline(audio_paths: list, output_dir: str, device: str = "cpu",
                 demix_dir: str = None, keep_stems: bool = False):
    """Run the full analysis pipeline on one or more audio files.

    Args:
        audio_paths: List of audio file paths
        output_dir: Directory for JSON output
        device: "cpu" or "cuda"
        demix_dir: Where to store demucs stems (default: <output_dir>/demix)
        keep_stems: If True, keep demucs WAV stems after analysis
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if demix_dir is None:
        demix_dir = str(output_dir / "demix")
    demix_path = Path(demix_dir)
    demix_path.mkdir(parents=True, exist_ok=True)

    for audio_path in audio_paths:
        audio_path = Path(audio_path)
        if not audio_path.exists():
            print(f"WARNING: File not found, skipping: {audio_path}")
            continue

        stem_name = audio_path.stem
        output_json = output_dir / f"{stem_name}.json"

        print(f"\n{'='*60}")
        print(f"Processing: {audio_path.name}")
        print(f"{'='*60}")

        # --- Step 1: allin1 analysis with stem preservation ---
        print("\n[1/2] Running allin1 (structure + beats + demucs stems)...")
        try:
            result = allin1.analyze(
                str(audio_path),
                keep_byproducts=True,
                demix_dir=demix_dir,
                device=device,
            )
            # allin1.analyze can return a single result or a list
            if isinstance(result, list):
                result = result[0]

            data = result_to_dict(result)
        except Exception as e:
            print(f"ERROR in allin1 analysis: {e}")
            traceback.print_exc()
            continue

        # Write intermediate allin1 result (so we have something even if
        # feature extraction fails)
        with open(output_json, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  allin1 result: BPM={data['bpm']}, "
              f"beats={len(data['beats'])}, "
              f"segments={len(data['segments'])}")

        # --- Step 2: Feature extraction on stems ---
        print("\n[2/2] Extracting audio features from stems...")
        try:
            enriched = extract_all(
                str(audio_path),
                demix_dir,
                str(output_json),
            )

            with open(output_json, 'w') as f:
                json.dump(enriched, f, indent=2)

            summary = enriched.get("feature_summary", {})
            print(f"\n  Feature extraction complete:")
            for stem, count in summary.get("stem_onset_counts", {}).items():
                print(f"    {stem}: {count} onsets")

        except Exception as e:
            print(f"WARNING: Feature extraction failed: {e}")
            traceback.print_exc()
            print("  (allin1 results were saved successfully)")

        print(f"\nOutput: {output_json}")

    # --- Cleanup: remove stems to save disk space ---
    # Stems can be huge (4x the original file size as WAVs). Remove them
    # after feature extraction unless the user wants to keep them.
    # The JSON has everything we need.
    if keep_stems:
        print(f"\nKeeping demucs stems in {demix_dir}")
    else:
        print(f"\nCleaning up demucs stems in {demix_dir}...")
        try:
            import shutil
            if demix_path.exists():
                shutil.rmtree(demix_path)
                print("  Stems removed.")
        except Exception as e:
            print(f"  WARNING: Could not clean up stems: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze audio: structure + beats + energy + onsets"
    )
    parser.add_argument("audio", nargs="*", help="Audio file(s) to analyze")
    parser.add_argument("-o", "--output-dir", default=".",
                        help="Output directory for JSON results")
    parser.add_argument("-d", "--device", default="cpu",
                        help="Device for inference (cpu or cuda)")
    parser.add_argument("--demix-dir", default=None,
                        help="Directory for demucs stems (default: <output>/demix)")
    parser.add_argument("--keep-stems", action="store_true",
                        help="Keep demucs stems after analysis (warning: large files)")

    args = parser.parse_args()

    if not args.audio:
        parser.print_help()
        sys.exit(0)

    run_pipeline(
        audio_paths=args.audio,
        output_dir=args.output_dir,
        device=args.device,
        demix_dir=args.demix_dir,
        keep_stems=args.keep_stems,
    )


if __name__ == "__main__":
    main()
