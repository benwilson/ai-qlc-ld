# allin1 Docker Image

Dockerized build of [all-in-one](https://github.com/mir-aidj/all-in-one) (allin1), a music structure analysis tool that extracts BPM, beat positions, downbeats, and song segment boundaries from audio files.

## Tested Hardware

- Apple M1 Pro (10-core, 16GB) — MacBook Pro 18,3
- Docker Desktop for Mac (Apple Silicon, native ARM64 — no Rosetta)

Should also work on x86_64 Linux. Not tested with GPU; this is a CPU-only build.

## What It Does

Analyzes audio files and outputs JSON with:

- **BPM** — detected tempo
- **Beats** — timestamp of every beat
- **Downbeats** — timestamp of every bar start (beat 1)
- **Beat positions** — which beat in the bar (1, 2, 3, 4)
- **Segments** — song structure sections with start/end times and labels (intro, verse, chorus, solo, break, outro, etc.)

The analysis pipeline runs [Hybrid Transformer Demucs](https://github.com/facebookresearch/demucs) (htdemucs) for source separation, then the all-in-one model for structure analysis — all CPU-only.

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
```

The wrapper script (`analyze.sh`) auto-builds the image on first run, skips songs that already have results, and requires Docker to be installed.

## Output Format

One JSON file per input track in the output directory:

```json
{
  "path": "/workspace/songs/Artist - Title.flac",
  "bpm": 115,
  "beats": [0.03, 0.55, 1.06, ...],
  "downbeats": [0.03, 2.12, 4.15, ...],
  "beat_positions": [1, 2, 3, 4, 1, 2, 3, 4, ...],
  "segments": [
    {"start": 0.0, "end": 18.62, "label": "intro"},
    {"start": 18.62, "end": 55.86, "label": "verse"},
    ...
  ]
}
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

## Image Size

Approximately 4 GB due to PyTorch, demucs model, and NATTEN compiled extensions.

## License

This Docker image packages [all-in-one](https://github.com/mir-aidj/all-in-one) (MIT License) and [Demucs](https://github.com/facebookresearch/demucs) (MIT License).
