# Launch data: column guide

The notebooks use `synthetic_launch_attempts.csv`, which is already included.
**One row = one fictional mission's first launch attempt.** All 960 records are
simulated, including the vehicle names, pad names, forecasts, and outcomes.

## What are we predicting?

At **T−60 minutes** (one hour before the original schedule), predict:

- **1 — Delayed / scrubbed:** liftoff is more than 15 minutes late, or this attempt is cancelled.
- **0 — Within 15 minutes:** liftoff is no more than 15 minutes late, including exactly 15 minutes.

A scrub has no liftoff time, so its `actual_delay_minutes` is blank while `delayed` is 1.
An unknown weather value is also blank; it does **not** mean zero.

## Inputs available before launch

| Column | Meaning | Units / values |
|---|---|---|
| `forecast_wind_kmh` | Wind forecast for the launch window | km/h |
| `forecast_rain_pct` | Forecast chance of rain | 0–100% |
| `forecast_lightning_pct` | Forecast chance of lightning | 0–100% |
| `forecast_cloud_pct` | Forecast fraction of sky covered by cloud | 0–100% |
| `temperature_c` | Forecast temperature | °C |
| `open_technical_items` | Unresolved checklist items at T−60 | Integer, 0–5 |
| `launch_pad` | Fictional launch location | Coastal Pad / Inland Pad |
| `vehicle` | Fictional rocket | Aster-1 / Lyra-2 / Vela-3 |

Notebook 01 uses wind, rain, lightning, and technical items. Notebook 02 uses all eight inputs.
Missing numeric inputs are filled with medians learned from **training rows only**.

## Other columns — keep these out of the model inputs

| Column | Meaning | Use |
|---|---|---|
| `mission_id` | Unique `SIM-xxxx` identifier | Check that missions do not repeat |
| `scheduled_launch_utc` | Original scheduled liftoff | Sort attempts before splitting |
| `prediction_time_utc` | Schedule minus 60 minutes | Check when inputs must be available |
| `actual_delay_minutes` | Delay measured after the attempt | **Future information** |
| `scrubbed` | 1 if the attempt was cancelled, otherwise 0 | **Future information** |
| `outcome_recorded_utc` | Schedule plus 6 hours | **Future information** |
| `delayed` | The 0/1 outcome defined above | **Target to predict** |

## Three data splits

| Split | Ordered rows | Purpose |
|---|---|---|
| Training | First 576 | Explore the data and fit models |
| Validation | Next 192 | Choose the model and alert threshold |
| Test | Last 192 | Evaluate after those choices are fixed |

Artificial schedules start on 1 January 2024 at 08:00 UTC, eight hours apart.
Each outcome is recorded before the next row's prediction time. These timestamps
illustrate chronological evaluation; they are not historical launch records.

<details>
<summary>Optional: where the simulated records come from</summary>

[`scripts/generate_data.py`](../scripts/generate_data.py) creates the records with
NumPy's `default_rng(2026)`. A shared storminess variable creates related weather
forecasts. Wind, rain, lightning, cloud, technical items, pad, and vehicle feed an
invented logistic score. Random noise and a random draw determine the outcome, so
similar inputs can still produce different results. Temperature is related to
storminess but has no direct term in the score.

Of attempts assigned a positive label, 15% are randomly scrubbed; the others receive
a delay of 16–180 minutes. Negative labels receive 0–15 minutes. About 3.5% of values
in each weather column are then made missing, independently. The hidden score and
its underlying probability are not included as inputs.

From the repository root, `python scripts/generate_data.py` recreates and overwrites
the CSV with the same records. You do not need to run it during the workshop.

</details>

**What the results mean:** scores measure performance on this simulation only.
They do not establish real launch-delay rates, vehicle quality, or launch safety.
Real forecasting needs historical schedule and forecast snapshots available at the
prediction time, linked rescheduled attempts, and evaluation on later real missions.

[Back to the workshop](../README.md)
