FROM --platform=linux/amd64 python:3.11-slim

# System dependencies (cmake + ninja for NATTEN source build)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        build-essential \
        cmake \
        ninja-build \
    && rm -rf /var/lib/apt/lists/*

# PyTorch 2.2.0 CPU
RUN pip install --no-cache-dir \
    torch==2.2.0+cpu \
    torchaudio==2.2.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Pin numpy<2 — PyTorch 2.2.0 and NATTEN 0.15.1 were compiled against NumPy 1.x
RUN pip install --no-cache-dir "numpy<2"

# NATTEN 0.15.1 from source (CPU kernels only, matches allin1's API)
RUN pip install --no-cache-dir natten==0.15.1

# madmom from git (required by allin1, PyPI version is outdated)
RUN pip install --no-cache-dir \
    git+https://github.com/CPJKU/madmom

# allin1
RUN pip install --no-cache-dir allin1

# Working directory
WORKDIR /workspace

ENTRYPOINT ["allin1"]
CMD ["--help"]
