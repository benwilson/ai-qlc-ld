#!/bin/bash
# Run all project tests (used by local checks and CI).
set -euo pipefail

python3 -m unittest discover -s tests -p "test_*.py" -q
