"""Generate fictional launch attempts for teaching, never for operations.

Run from any directory: python scripts/generate_data.py
This script is for instructors; learners use the committed CSV.
"""

from pathlib import Path

import numpy as np
import pandas as pd


def make_data(n=960, seed=2026):
    """Return one pre-launch snapshot and eventual outcome per fictional mission."""
    rng = np.random.default_rng(seed)
    scheduled = pd.date_range("2024-01-01 08:00", periods=n, freq="8h", tz="UTC")
    pad = rng.choice(["Coastal Pad", "Inland Pad"], n)
    vehicle = rng.choice(["Aster-1", "Lyra-2", "Vela-3"], n)
    storminess = rng.beta(2, 4, n)
    wind = np.round(np.clip(rng.normal(22 + 20 * storminess + 5 * (pad == "Coastal Pad"), 12), 0, 85), 1)
    rain = np.round(np.clip(100 * storminess + rng.normal(0, 12, n), 0, 100), 1)
    lightning = np.round(np.clip(60 * storminess + rng.normal(0, 14, n), 0, 100), 1)
    cloud = np.round(np.clip(25 + 70 * storminess + rng.normal(0, 15, n), 0, 100), 1)
    temperature = np.round(np.clip(rng.normal(27 - 5 * storminess, 6, n), 5, 42), 1)
    technical = np.minimum(rng.poisson(0.65, n), 5)

    # Invented teaching relationships, NOT launch criteria or fitted physics.
    score = (
        -3.4 + 0.07 * np.maximum(wind - 20, 0) + 0.024 * rain
        + 0.032 * lightning + 0.75 * technical
        + 0.012 * np.maximum(cloud - 60, 0)
        + 0.3 * (vehicle == "Lyra-2") + 0.15 * (pad == "Coastal Pad")
        + rng.normal(0, 0.45, n)  # Unobserved influences: outcomes remain uncertain.
    )
    probability = 1 / (1 + np.exp(-score))
    delayed = (rng.random(n) < probability).astype(int)
    scrubbed = ((delayed == 1) & (rng.random(n) < 0.15)).astype(int)
    delay_minutes = np.where(
        delayed == 1,
        np.clip(16 + rng.gamma(2, 23, n), 16, 180),
        rng.integers(0, 16, n),
    ).astype(float)
    delay_minutes[scrubbed == 1] = np.nan
    data = pd.DataFrame({
        "mission_id": [f"SIM-{i:04d}" for i in range(1, n + 1)],
        "scheduled_launch_utc": scheduled,
        "prediction_time_utc": scheduled - pd.Timedelta(hours=1),
        "launch_pad": pad,
        "vehicle": vehicle,
        "forecast_wind_kmh": wind,
        "forecast_rain_pct": rain,
        "forecast_lightning_pct": lightning,
        "forecast_cloud_pct": cloud,
        "temperature_c": temperature,
        "open_technical_items": technical,
        "actual_delay_minutes": np.round(delay_minutes, 1),
        "scrubbed": scrubbed,
        "delayed": delayed,
        "outcome_recorded_utc": scheduled + pd.Timedelta(hours=6),
    })
    # Missing forecast values emulate incomplete records; labels are not missing.
    for column in ["forecast_wind_kmh", "forecast_rain_pct", "forecast_lightning_pct", "forecast_cloud_pct", "temperature_c"]:
        data.loc[rng.random(n) < 0.035, column] = np.nan
    return data


if __name__ == "__main__":
    destination = Path(__file__).resolve().parents[1] / "data" / "synthetic_launch_attempts.csv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    data = make_data()
    data.to_csv(destination, index=False, float_format="%.1f", lineterminator="\n")
    print(f"Wrote {len(data)} fictional attempts to {destination}")
