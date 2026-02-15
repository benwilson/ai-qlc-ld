#!/bin/bash
# Analyze audio files in songs/ using the allin1 Docker image.
# Results are written to songs-data/ as JSON files.
#
# Usage:
#   ./analyze.sh                       # analyze all songs without existing results
#   ./analyze.sh "specific file.flac"  # analyze one file (even if results exist)
#
# The Docker image is built automatically on first run.

set -euo pipefail

IMAGE="allin1"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
SONGS_DIR="$BASE_DIR/songs"
DATA_DIR="$BASE_DIR/songs-data"

# Require Docker
if ! command -v docker &>/dev/null; then
    echo "Error: docker is not installed or not in PATH." >&2
    exit 1
fi

# Build image if it doesn't exist
if ! docker image inspect "$IMAGE" &>/dev/null; then
    echo "Image '$IMAGE' not found — building (this may take a few minutes)..."
    docker build -t "$IMAGE" "$BASE_DIR"
fi

mkdir -p "$DATA_DIR"

if [ $# -gt 0 ]; then
    # Analyze specific file(s)
    FILES=()
    for f in "$@"; do
        FILES+=("/workspace/songs/$f")
    done
    docker run --rm \
        -v "$SONGS_DIR:/workspace/songs:ro" \
        -v "$DATA_DIR:/workspace/songs-data" \
        "$IMAGE" \
        "${FILES[@]}" \
        -o /workspace/songs-data \
        -d cpu
else
    # Analyze songs that don't already have results
    FILES=()
    SKIPPED=0
    for f in "$SONGS_DIR"/*; do
        [ -f "$f" ] || continue
        BASENAME="$(basename "$f")"
        # allin1 outputs JSON named after the input file (without extension)
        STEM="${BASENAME%.*}"
        if [ -f "$DATA_DIR/${STEM}.json" ]; then
            SKIPPED=$((SKIPPED + 1))
            continue
        fi
        FILES+=("/workspace/songs/$BASENAME")
    done

    if [ $SKIPPED -gt 0 ]; then
        echo "Skipping $SKIPPED file(s) with existing results."
    fi

    if [ ${#FILES[@]} -eq 0 ]; then
        echo "Nothing to analyze — all songs already have results."
        exit 0
    fi

    echo "Analyzing ${#FILES[@]} file(s)..."
    docker run --rm \
        -v "$SONGS_DIR:/workspace/songs:ro" \
        -v "$DATA_DIR:/workspace/songs-data" \
        "$IMAGE" \
        "${FILES[@]}" \
        -o /workspace/songs-data \
        -d cpu
fi

echo "Done. Results in songs-data/"
