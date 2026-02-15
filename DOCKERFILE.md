# Audio Analysis Pipeline Docker Image

Dockerized audio analysis pipeline for lighting show generation. Combines [all-in-one](https://github.com/mir-aidj/all-in-one) (allin1) for structure analysis with [librosa](https://librosa.org/) for feature extraction on [demucs](https://github.com/facebookresearch/demucs)-separated stems.

## Tested Hardware

- Apple M1 Pro (10-core, 16GB) — MacBook Pro 18,3
- Docker Desktop for Mac (Apple Silicon, native ARM64 — no Rosetta)

Should also work on x86_64 Linux. Not tested with GPU; this is a CPU-only build.

## What It Does

The pipeline runs two stages on each audio file:

### Stage 1: allin1 (structure + beats)
- **BPM** — detected tempo
- **Beats** — timestamp of every beat
- **Downbeats** — timestamp of every bar start (beat 1)
- **Beat positions** — which beat in the bar (1, 2, 3, 4)
- **Segments** — song structure sections with start/end times and labels (intro, verse, chorus, solo, break, outro, etc.)
- **Demucs stems** — source separation into bass, drums, vocals, other (saved for Stage 2, then cleaned up)

### Stage 2: Feature extraction (energy + onsets)
- **Per-stem energy envelopes** — RMS energy at each beat for bass, drums, vocals, and other stems (0.0–1.0)
- **Per-stem onset timestamps** — exact time of each note/hit in each stem (seconds)
- **Frequency band energy** — sub-bass (20–80Hz), bass (80–250Hz), low-mid (250–500Hz), mid (500–2kHz), high (2k+) at each beat
- **Overall RMS** — loudness at each beat
- **Spectral centroid** — brightness (Hz) at each beat — rising centroid = filter sweep or riser
- **Spectral flux** — rate of spectral change at each beat — high = transients/impacts, low = sustained sounds
- **Onset strength** — how impactful each beat is (0.0–1.0)

Demucs runs once (via allin1's `keep_byproducts=True`), then stems are reused for feature extraction and cleaned up.

## Quick Start

```bash
docker build -t allin1 .

# Analyze a single file
docker run --rm \
    -v /path/to/songs:/workspace/songs:ro \
    -v /path/to/output:/workspace/songs-data \
    allin1 \
    /workspace/songs/my-track.flac \
    -o /workspace/songs-data \
    -d cpu

# Or use the included wrapper script
./analyze.sh                          # analyze all songs without existing results
./analyze.sh "specific file.flac"     # analyze one file
./analyze.sh --keep-stems "file"      # keep demucs WAV stems after analysis
```

The wrapper script (`analyze.sh`) auto-builds the image on first run, skips songs that already have results, and requires Docker to be installed.

## Output Format

One JSON file per input track in the output directory:

```json
{
  "path": "/workspace/songs/Artist - Title.flac",
  "bpm": 133,
  "beats": [5.86, 6.29, 6.75, ...],
  "downbeats": [7.18, 8.94, 10.75, ...],
  "beat_positions": [2, 3, 4, 1, 2, 3, 4, ...],
  "segments": [
    {"start": 0.0, "end": 14.32, "label": "intro"},
    {"start": 14.32, "end": 28.65, "label": "intro"},
    ...
  ],
  "energy": {
    "sub_bass": [0.0, 0.12, 0.85, ...],
    "bass": [0.0, 0.3, 0.9, ...],
    "low_mid": [0.1, 0.2, 0.4, ...],
    "mid": [0.2, 0.4, 0.6, ...],
    "high": [0.1, 0.3, 0.5, ...],
    "rms": [0.1, 0.4, 0.8, ...]
  },
  "dynamics": {
    "spectral_centroid": [1200.0, 1400.0, ...],
    "spectral_flux": [0.1, 0.8, ...],
    "onset_strength": [0.0, 0.2, 0.9, ...]
  },
  "stems": {
    "bass": {
      "energy": [0.0, 0.1, 0.85, ...],
      "onsets": [28.65, 29.1, 29.55, ...],
      "onset_count": 142
    },
    "drums": {
      "energy": [0.3, 0.8, 0.9, ...],
      "onsets": [5.86, 6.29, 6.75, ...],
      "onset_count": 305
    },
    "vocals": {
      "energy": [0.0, 0.0, 0.1, ...],
      "onsets": [42.98, 43.88, ...],
      "onset_count": 28
    },
    "other": {
      "energy": [0.2, 0.4, 0.1, ...],
      "onsets": [14.32, 14.77, 15.22, ...],
      "onset_count": 186
    }
  },
  "feature_summary": {
    "total_beats": 305,
    "duration_sec": 135.65,
    "stem_onset_counts": {"bass": 142, "drums": 305, "vocals": 28, "other": 186},
    "energy_bands": ["sub_bass", "bass", "low_mid", "mid", "high"]
  }
}
```

### Array Indexing

All arrays in `energy` and `dynamics` are indexed by beat — they have the same length as the `beats` array. `energy.sub_bass[i]` is the sub-bass energy at `beats[i]`.

Stem `onsets` are raw timestamps in seconds (not beat-indexed) — they can fall between beats.

### Using in Show Generators

```python
import json

with open("songs-data/Artist - Track.json") as f:
    data = json.load(f)

# Find the drop: sub-bass goes from near-zero to high
for i, (sb, prev_sb) in enumerate(zip(data["energy"]["sub_bass"][1:],
                                       data["energy"]["sub_bass"])):
    if prev_sb < 0.2 and sb > 0.7:
        print(f"Drop at beat {i+1}, time {data['beats'][i+1]:.2f}s")

# Find piano/synth notes in quiet sections for per-note light triggers
for onset_time in data["stems"]["other"]["onsets"]:
    # Check if this onset is during a low-energy section
    beat_idx = min(range(len(data["beats"])),
                   key=lambda j: abs(data["beats"][j] - onset_time))
    if data["energy"]["rms"][beat_idx] < 0.3:
        print(f"Melodic hit at {onset_time:.2f}s (quiet section)")
```

## Supported Audio Formats

Any format supported by ffmpeg: FLAC, WAV, MP3, OGG, AAC, M4A, etc.

## Build Details

Getting allin1 to run CPU-only in Docker required pinning specific dependency versions. Here's what works and why:

| Package | Version | Why |
|---------|---------|-----|
| Python | 3.11 | Required by NATTEN 0.15.1 (no 3.12 support) |
| PyTorch | 2.2.0 | Official ARM64 CPU wheels on PyPI. Newer versions break NATTEN 0.15.1 compatibility |
| torchaudio | 2.2.0 | Must match PyTorch version |
| NumPy | <2.0 | PyTorch 2.2.0 was compiled against NumPy 1.x. NumPy 2.x causes `RuntimeError: Numpy is not available` at runtime |
| NATTEN | 0.15.1 | Last version with the `natten.functional.natten1dav` / `natten1dqkrpb` API that allin1 imports. Versions 0.17+ reorganized the API and break allin1 |
| madmom | git main | PyPI release is outdated; allin1 requires the current version from source |
| demucs | (via allin1) | htdemucs model is pre-cached in the image (~80MB) to avoid downloading on every run |
| librosa | 0.10.2 | Audio feature extraction. Pinned — last release before 0.11.0 which targets NumPy 2.x |
| soundfile | latest | Backend for librosa's audio loading |
| libsndfile1 | system | C library required by soundfile for reading WAV files |

### Pipeline Scripts

| File | Copied To | Purpose |
|------|-----------|---------|
| `pipeline.py` | `/usr/local/bin/pipeline.py` | Docker entrypoint — orchestrates allin1 + feature extraction |
| `extract_features.py` | `/usr/local/bin/extract_features.py` | Stem energy envelopes + onset detection via librosa |

### NATTEN Build Notes

NATTEN 0.15.1 has no pre-built CPU wheels available (the old wheel server at shi-labs.com has an expired SSL certificate, and whl.natten.org only hosts 0.17.5+). It builds from source using cmake + ninja + build-essential. The Dockerfile sets `CFLAGS="-O3 -fopenmp"` and `CXXFLAGS="-O3 -fopenmp"` for optimized compilation with OpenMP threading.

On ARM64, the source build compiles CPU-only kernels automatically (no CUDA detected). The build takes several minutes but only happens once during `docker build`.

### Threading Configuration

The image sets these environment variables by default:

| Variable | Default | Purpose |
|----------|---------|---------|
| `OMP_NUM_THREADS` | 8 | OpenMP thread count for PyTorch |
| `MKL_NUM_THREADS` | 8 | MKL thread count (x86 only) |
| `OPENBLAS_NUM_THREADS` | 1 | Prevents OpenBLAS/OpenMP conflict that causes hangs |

Override at runtime to match your hardware:

```bash
docker run --rm \
    -e OMP_NUM_THREADS=4 \
    -e MKL_NUM_THREADS=4 \
    ...
```

### Pitfalls We Hit (So You Don't Have To)

1. **NATTEN 0.17.5 crashes on CPU-only PyTorch** — it unconditionally calls `torch.cuda.get_device_capability()` at import time, throwing `AssertionError: Torch not compiled with CUDA enabled`. Use 0.15.1 instead.

2. **NATTEN 0.17.5 breaks allin1's imports** — allin1 imports `natten1dav`, `natten1dqkrpb`, `natten2dav`, `natten2dqkrpb` from `natten.functional`, which were removed in the 0.17.x API reorganization.

3. **PyTorch CPU wheels on ARM** — the `+cpu` suffix used for x86 wheels (e.g., `torch==2.2.0+cpu`) does not exist for ARM64. The default PyPI wheel is already CPU-only on aarch64.

4. **NumPy 2.x incompatibility** — pip will happily install NumPy 2.x, but PyTorch 2.2.0 (compiled against NumPy 1.x) will crash at runtime with `_ARRAY_API not found`. Pin `numpy<2`.

5. **OpenBLAS threading conflict** — without `OPENBLAS_NUM_THREADS=1`, you get `OpenBLAS Warning: Detect OpenMP Loop and this application may hang`. Setting it to 1 lets OpenMP handle parallelism cleanly.

6. **allin1 `keep_byproducts`** — allin1 runs demucs internally and deletes stems by default. Pass `keep_byproducts=True` to the Python API to preserve stems for downstream analysis. This avoids running demucs twice.

7. **librosa `onset_strength` with `feature=rms`** — passing `librosa.feature.rms` as the `feature` argument to `librosa.onset.onset_strength()` fails because `onset_strength` forwards `sr=` to the feature function, but `rms()` doesn't accept `sr`. Workaround: compute the RMS envelope directly with `librosa.feature.rms()`, then differentiate it (`np.diff`) and clamp to positive values to get an onset-like envelope from energy increases.

## Onset Detection Tuning

The onset detection parameters in `extract_features.py` are tuned for electronic music:

| Stem | Method | Delta | Wait | Rationale |
|------|--------|-------|------|-----------|
| bass | energy | 0.15 | 4 (~93ms) | Bass is sustained — energy method avoids false triggers on harmonics |
| drums | spectral_flux | 0.10 | 2 (~46ms) | Drums are transient — low threshold catches ghost notes, short wait handles fast DnB patterns |
| vocals | energy | 0.20 | 6 (~140ms) | Higher threshold avoids breath noise, longer wait groups syllables into phrases |
| other | spectral_flux | 0.12 | 2 (~46ms) | Sensitive to synth attacks and piano notes — this is the "melodic hits" stem |

These can be adjusted in the `ONSET_PARAMS` dict. Lower delta = more onsets detected. Higher wait = more time between consecutive onsets.

## Image Size

Approximately 4.5 GB due to PyTorch, demucs model, NATTEN compiled extensions, and librosa.

## License

This Docker image packages [all-in-one](https://github.com/mir-aidj/all-in-one) (MIT License), [Demucs](https://github.com/facebookresearch/demucs) (MIT License), and [librosa](https://librosa.org/) (ISC License).
