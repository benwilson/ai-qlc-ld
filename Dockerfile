FROM python:3.11-slim

# System dependencies (cmake + ninja for NATTEN source build)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        build-essential \
        cmake \
        ninja-build \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# PyTorch 2.2.0 CPU — official aarch64 wheels are CPU-only by default on PyPI
RUN pip install --no-cache-dir torch==2.2.0 torchaudio==2.2.0

# Pin numpy<2 — PyTorch 2.2.0 and NATTEN 0.15.1 were compiled against NumPy 1.x
RUN pip install --no-cache-dir "numpy<2"

# NATTEN 0.15.1 from source (CPU kernels only, matches allin1's API)
# Enable O3 optimization and OpenMP for the C++ extension build
ENV CFLAGS="-O3 -fopenmp" CXXFLAGS="-O3 -fopenmp"
RUN pip install --no-cache-dir natten==0.15.1

# madmom from git (required by allin1, PyPI version is outdated)
RUN pip install --no-cache-dir \
    git+https://github.com/CPJKU/madmom

# allin1
RUN pip install --no-cache-dir allin1

# librosa 0.10.2 for feature extraction (onset detection, spectral analysis, energy)
# Pinned to 0.10.2 — last release before 0.11.0 which targets NumPy 2.x.
# 0.10.2 works with our numpy<2 pin. soundfile is the backend for audio loading.
RUN pip install --no-cache-dir "librosa==0.10.2" soundfile

# Pre-cache the demucs model (~80MB) so it doesn't download on every run
RUN python -c "from demucs.pretrained import get_model; get_model('htdemucs')"

# Copy the analysis pipeline script
COPY pipeline.py /usr/local/bin/pipeline.py
COPY extract_features.py /usr/local/bin/extract_features.py

# Tune threading — use all available cores (override at runtime with -e if needed)
ENV OMP_NUM_THREADS=8
ENV MKL_NUM_THREADS=8
ENV OPENBLAS_NUM_THREADS=1

# Working directory
WORKDIR /workspace

ENTRYPOINT ["python3", "/usr/local/bin/pipeline.py"]
CMD ["--help"]
