#!/usr/bin/env python3
"""Check whether the local SleepFM environment can run the demo workflow."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


REQUIRED_MODULES = [
    "pyedflib",
    "h5py",
    "numpy",
    "pandas",
    "scipy",
    "sklearn",
    "torch",
    "mne",
    "tqdm",
    "einops",
    "loguru",
]

EXPECTED_PATHS = [
    "requirements.txt",
    "env.yml",
    "notebooks/demo.ipynb",
    "notebooks/demo_data/demo_psg.csv",
    "notebooks/demo_data/demo_age_gender.csv",
    "notebooks/demo_data/is_event.csv",
    "notebooks/demo_data/time_to_event.csv",
    "sleepfm/configs/channel_groups.json",
    "sleepfm/checkpoints/model_base",
    "sleepfm/checkpoints/model_sleep_staging",
    "sleepfm/checkpoints/model_diagnosis",
]


def module_status(name: str) -> dict[str, str]:
    try:
        module = importlib.import_module(name)
    except Exception as exc:  # pragma: no cover - diagnostic script
        return {"name": name, "status": "missing", "detail": str(exc)}
    version = getattr(module, "__version__", "")
    return {"name": name, "status": "ok", "detail": version}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    print(f"Repository root: {root}")
    print(f"Python: {sys.version.split()[0]}")
    if sys.version_info[:2] != (3, 10):
        print("WARNING: upstream project recommends Python 3.10")

    missing_modules = []
    for status in map(module_status, REQUIRED_MODULES):
        detail = f" ({status['detail']})" if status["detail"] else ""
        print(f"{status['name']}: {status['status']}{detail}")
        if status["status"] != "ok":
            missing_modules.append(status["name"])

    missing_paths = []
    for rel_path in EXPECTED_PATHS:
        exists = (root / rel_path).exists()
        print(f"{rel_path}: {'ok' if exists else 'missing'}")
        if not exists:
            missing_paths.append(rel_path)

    summary = {
        "python": sys.version.split()[0],
        "missing_modules": missing_modules,
        "missing_paths": missing_paths,
    }
    print(json.dumps(summary, indent=2))
    return 1 if missing_modules else 0


if __name__ == "__main__":
    raise SystemExit(main())
