# Validation record

**Materials by Dr. Mohammed Hussin Talafha**  
Checked 6 October 2026 for the 7 October workshop.

## GitHub Jupyter execution: passed

[Workflow run 37420774415](https://github.com/mtalafha90/Rocket_Evolution_SSAH/actions/runs/37420774415)
completed successfully for commit `6ba536490d37250d4eada718526309f46676d7ce`.
The clean GitHub runner installed the pinned dependencies and executed **both
notebooks in independent Jupyter kernels**, including widget code, all 22 code cells,
five figures and the student exports. This confirms normal Jupyter execution in
addition to the local IPython checks below.

The first cloud run identified that the checker must retain widget state while
processing widget messages. This was corrected in the validation script; state is
now stripped only after execution when saving static previews. The complete check
then passed. No notebook cells were skipped to achieve the passing result.

## Checks completed locally

- The actual `.devcontainer/post-create.sh` completed successfully in a clean Python
  3.12.14 virtual environment: dependency installation and kernel registration passed.
- `pip check` reported no broken requirements in that environment.
- Both notebooks executed all cells from top to bottom in **separate, fresh IPython
  processes**, with no skipped code cells. Notebook 01 ran from the repository root;
  notebook 02 ran from `notebooks/` to exercise both relative-path cases.
- Notebook 01: **11 code cells**, **2 figures**, about **2.8 seconds** of execution.
- Notebook 02: **11 code cells**, **3 figures**, about **3.4 seconds** of execution.
- The widget construction and its initial prediction callback executed. Static
  notebook outputs replace the live widget reference with a message to rerun the cell.
- The final JSON report and both CSV exports were created and checked.
- The CSV matched the deterministic generator, including labels and missing values.
  All 960 IDs are unique; targets and ranges are valid; split boundaries are time ordered;
  training outcomes are recorded before validation prediction times, and likewise for testing.
- Notebook format, author metadata, 60-minute durations, setup shell syntax and
  devcontainer JSON were checked. The five charts were visually reviewed.

Command used for local execution (this environment blocks Jupyter kernel sockets):

```bash
.venv/bin/python scripts/validate_workshop.py --engine ipython --write-executed
.venv/bin/python -m pip check
```

The standard command, `python scripts/validate_workshop.py`, uses `nbclient` with a
fresh **Jupyter kernel** per notebook. The GitHub workflow runs that standard command
in a clean Python 3.12 runner. See [workflow runs](https://github.com/mtalafha90/Rocket_Evolution_SSAH/actions/workflows/check-notebooks.yml)
for the execution status of a particular commit.

## Default-run reference results

These values apply only to the **bundled simulated data** and original exercise defaults.
They are not measures of real launch forecasting performance.

| Check | Result |
|---|---:|
| Notebook 01 baseline validation accuracy / delay recall | 0.5625 / 0.0000 |
| Notebook 01 tree validation accuracy / delay recall | 0.6406 / 0.5595 |
| Notebook 02 chosen model | Random forest |
| Validation-selected alert threshold | 0.25 |
| Invented cost: missed delay / false alarm | 3 / 1 |
| Final simulated test accuracy | 0.6406 |
| Final simulated test precision / delay recall | 0.5734 / 0.9111 |
| Final simulated test F1 / ROC AUC | 0.7039 / 0.8291 |
| Test delayed/scrubbed attempts | 90 of 192 |
| Delays caught / missed | 82 / 8 |
| Correct no-flags / false alarms | 41 / 61 |
| Model cost / majority-baseline cost | 85 / 270 points |

The threshold was chosen on validation data before testing. Its high delay recall
comes with many false alarms; this is a deliberate discussion point, not a claim
that the chosen cost ratio is appropriate for real operations.

CSV SHA-256:

```text
eb63bcc647952d6ec9b904b3b401526d500fb966f33e63b64dea0efebec1f9d7
```

## Scope

A live GitHub Codespaces browser session and manual slider interaction were not
performed here. The installation script and Python content were tested; the
devcontainer uses the documented `mcr.microsoft.com/devcontainers/python:3.12-bookworm`
image and standard Python/Jupyter extensions. The instructor should open a Codespace
on the venue connection before participants arrive. No real launch data or physical
launch rules were validated. The one-hour timing budgets are teaching plans, not
measured learner completion times.
