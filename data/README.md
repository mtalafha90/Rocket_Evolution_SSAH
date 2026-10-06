# Teaching dataset: fictional launch attempts

**Author/instructor: Dr. Mohammed Hussin Talafha**  
Prepared for *Predicting Rocket Launch Delays*, SSAH, 7 October 2026.

## Provenance

`synthetic_launch_attempts.csv` is generated entirely by
[`../scripts/generate_data.py`](../scripts/generate_data.py), with NumPy's
`default_rng(2026)`. It contains **960 simulated first attempts**, spaced 8 hours
apart from 1 January 2024 at 08:00 UTC. These timestamps are artificial ordering
markers, not historical launch records. No information was scraped from launch operators.
The dataset and generator are covered by the repository MIT licence.

Each row belongs to a different fictional mission; rescheduled attempts are not
included. Forecasts and technical status are assumed available exactly one hour
before the original scheduled launch. Outcomes are recorded six hours after that
schedule, before the next row's prediction time.

## Target and data dictionary

`delayed = 1` if `scrubbed == 1` OR `actual_delay_minutes > 15`; otherwise 0.
Exactly 15 minutes counts as 0. A scrub cancels this attempt, with no actual liftoff
time, so `actual_delay_minutes` is missing. Scrubs remain in the classification task.
All labels are complete. This dataset is not a regression benchmark for delay duration.

| Column | Type / units | Definition | Modelling role |
|---|---|---|---|
| `mission_id` | String | Unique `SIM-xxxx` identifier | Audit only |
| `scheduled_launch_utc` | UTC timestamp | Original scheduled liftoff | Chronological split only |
| `prediction_time_utc` | UTC timestamp | Original schedule minus 60 min | Availability audit only |
| `launch_pad` | Category | Coastal Pad / Inland Pad; both fictional | Pre-launch input |
| `vehicle` | Category | Aster-1 / Lyra-2 / Vela-3; all fictional | Pre-launch input |
| `forecast_wind_kmh` | km/h | Wind forecast for the launch window, issued by T−60 | Pre-launch input |
| `forecast_rain_pct` | 0–100% | Forecast chance of rain in that window | Pre-launch input |
| `forecast_lightning_pct` | 0–100% | Forecast chance of lightning in that window | Pre-launch input |
| `forecast_cloud_pct` | 0–100% | Forecast cloud-cover fraction, not rain probability | Pre-launch input |
| `temperature_c` | °C | Forecast temperature for that window | Pre-launch input |
| `open_technical_items` | Integer, 0–5 | Unresolved checklist items at T−60 | Pre-launch input |
| `actual_delay_minutes` | Minutes; blank for scrub | Nonnegative realised delay; 0–15 or 16–180 | **Post-event: exclude** |
| `scrubbed` | 0/1 | Attempt ultimately cancelled | **Post-event: exclude** |
| `delayed` | 0/1 | Classification outcome defined above | **Target, never input** |
| `outcome_recorded_utc` | UTC timestamp | Original schedule plus 6 h | **Post-event: exclude** |

Blank numeric forecasts represent missing information, not zero-valued weather.
Missingness is introduced independently at approximately 3.5% per weather column.
Notebook pipelines learn median replacements using **training rows only**.

## How the simulator works

A latent storminess variable generates correlated weather forecasts. Wind, rain,
lightning, cloud cover, checklist items, pad and vehicle contribute to an invented
logistic score. An unobserved random term and a Bernoulli draw prevent outcomes from
being completely predictable. Temperature has no direct term in the score but is
correlated with storminess. The score and its underlying probability are deliberately
not exported as learner inputs.

With `W` = wind in km/h, `R` = rain percentage, `L` = lightning percentage, `C` = cloud
percentage, `T` = technical item count, the invented score is:

```text
z = -3.4 + 0.07 max(W-20, 0) + 0.024 R + 0.032 L + 0.75 T
    + 0.012 max(C-60, 0) + 0.30 I(vehicle=Lyra-2)
    + 0.15 I(pad=Coastal Pad) + Normal(0, 0.45)
p = 1 / (1 + exp(-z))
delayed ~ Bernoulli(p)
```

Here `I(...)` is 1 when its condition is true and 0 otherwise. Conditional on a
positive label, an attempt is scrubbed with probability 0.15; other positive rows
receive a delay between 16 and 180 minutes. Negative rows receive 0–15 minutes.
Missing forecast entries are added after the outcomes are generated. All numbers
above are teaching choices, **not empirically estimated coefficients or launch rules**.

## Reproduction and split

From the repository root, with the pinned environment installed:

```bash
python scripts/generate_data.py
```

This intentionally overwrites the bundled CSV with the same deterministic data.
The validator compares the generated and committed tables.

| Split | Ordered rows (1-based) | Count | Permitted use |
|---|---|---:|---|
| Train | 1–576 | 576 | Exploration, preprocessing fit, model fit |
| Validation | 577–768 | 192 | Model selection and threshold selection |
| Test | 769–960 | 192 | Final score after choices are fixed |

## Interpretation limits

Performance describes recovery of this simulator's relationships. It says nothing
quantitative about real launch-delay rates, vehicle quality or launch safety.
The simulator does not model real schedule revisions, repeated attempts, seasonality,
operational rules, upper-atmosphere winds, mission constraints or forecast calibration.
The artificial chronology illustrates the evaluation workflow but does not by itself
simulate operational drift. Model probabilities are not verified against real outcomes.

Real work would require versioned schedule/forecast snapshots with known availability,
consistent attempt definitions, linked mission IDs, grouped chronological splits,
and evaluation on subsequent real attempts. NOAA/NASA weather observations collected
after the prediction time would not be substitutes for forecasts available beforehand.
