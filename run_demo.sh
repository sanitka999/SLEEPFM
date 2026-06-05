#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
SleepFM demo helper

Usage:
  ./run_demo.sh check       Check Python version, imports, demo files, checkpoints
  ./run_demo.sh synthetic   Create a minimal synthetic HDF5 input
  ./run_demo.sh notebook    Print and run the notebook command when available
  ./run_demo.sh help        Show this help

Recommended setup:
  conda env create -f env.yml
  conda activate sleepfm_env

CPU-only setup:
  python3.10 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements-cpu.txt
EOF
}

command_name="${1:-check}"

case "${command_name}" in
  check)
    python scripts/check_environment.py
    ;;
  synthetic)
    python scripts/create_synthetic_hdf5.py
    ;;
  notebook)
    if command -v jupyter >/dev/null 2>&1; then
      cd notebooks
      jupyter notebook demo.ipynb
    else
      echo "jupyter is not installed. Install dependencies first, then run:"
      echo "  cd notebooks && jupyter notebook demo.ipynb"
      exit 1
    fi
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    usage
    exit 2
    ;;
esac
