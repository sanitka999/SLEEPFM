#!/usr/bin/env python3
"""Create a minimal synthetic SleepFM-style HDF5 input file.

The generated file is for format smoke tests only. It is not physiological data.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import h5py
import numpy as np


CHANNELS = {
    "C3": 8.0,
    "Nasal": 0.2,
    "ECG": 1.3,
    "Chin": 13.0,
}


def make_signal(seconds: int, sample_rate: int, frequency: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n_samples = seconds * sample_rate
    t = np.arange(n_samples, dtype=np.float32) / sample_rate
    signal = np.sin(2 * np.pi * frequency * t)
    signal += 0.05 * rng.standard_normal(n_samples)
    signal = (signal - signal.mean()) / max(signal.std(), 1e-6)
    return signal.astype("float16")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="notebooks/demo_data/synthetic_minimal.hdf5",
        help="Output HDF5 path.",
    )
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--sample-rate", type=int, default=128)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    samples_per_chunk = 5 * 60 * args.sample_rate
    with h5py.File(output, "w") as hdf:
        for idx, (channel, frequency) in enumerate(CHANNELS.items()):
            signal = make_signal(args.seconds, args.sample_rate, frequency, seed=idx)
            hdf.create_dataset(
                channel,
                data=signal,
                dtype="float16",
                chunks=(min(samples_per_chunk, signal.shape[0]),),
                compression="gzip",
            )

    print(f"Wrote synthetic HDF5 input: {output}")
    print("Channels:", ", ".join(CHANNELS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
