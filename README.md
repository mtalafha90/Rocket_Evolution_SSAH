# Predicting Rocket Launch Delays

**Prepared and presented by Dr. Mohammed Hussin Talafha**  
Postdoctoral Research Fellow · University of Sharjah  
**الدكتور محمد حسين طلافحة — التنبؤ بتأخيرات إطلاق الصواريخ**

Rocket Revolution · World Space Week 2026 · SSAH  
**Wednesday, 7 October 2026 · 11:00–13:00 UAE time (UTC+4)**

Two guided, one-hour Jupyter notebooks for a hands-on introduction to machine learning.
Make a prediction, run a cell, change an input, and explain the result. Each notebook
includes the instructor's name, learning objectives, a 60-minute schedule, working
code, exercises, hints, charts, and an exit ticket.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/mtalafha90/Rocket_Evolution_SSAH?quickstart=1)

| Session | Notebook | What participants build |
|---|---|---|
| 11:00–12:00 · 60 min | [01 — Launch-delay detectives](notebooks/01_launch_delay_detectives.ipynb) | Data exploration, a majority baseline and an interpretable decision tree |
| 12:00–13:00 · 60 min | [02 — From predictions to decisions](notebooks/02_launch_delay_decisions.ipynb) | Model comparison, threshold selection, a final test and an interactive scenario panel |

## Start in Codespaces

**Before the workshop:** bring a laptop, sign in to GitHub, confirm that Codespaces
is available for your account, and create the environment at least 10 minutes early.
Initial setup needs internet access to install Python packages and editor extensions.
A CPU Codespace with 2 cores and 4 GB RAM is sufficient for these small exercises; no GPU is needed.

1. Click **Open in GitHub Codespaces** above. Alternatively, use **Code → Codespaces → Create codespace on main**.
2. Wait for the setup command to finish. It creates `.venv`, installs `requirements.txt`,
   and registers the **Python (Rocket Workshop)** kernel.
3. Open `notebooks/01_launch_delay_detectives.ipynb`.
4. Click **Select Kernel** at the top right, then **Python (Rocket Workshop)**.
   If needed, choose **Select Another Kernel → Jupyter Kernel**, or select `.venv/bin/python` under Python environments.
5. Run the first cell with **Shift+Enter**. Work downward and pause at **YOUR TURN**.
6. At 12:00, open notebook 02 and select the same kernel. It runs independently;
   it does not import code, trained models or variables from notebook 01.

Saved outputs let you preview the notebooks on GitHub. Sliders require a live
Codespace; notebook 02 also provides a plain Python scenario cell with no widgets.
After setup, the exercises load a small local CSV and make **no external data/API calls**.
Codespaces itself still requires a browser connection.

**Save your work:** notebook 02 writes a JSON mini report and two CSVs to `artifacts/`.
Right-click the files in the Explorer to download them before deleting your Codespace.
Stop your Codespace when finished using **Codespaces: Stop Current Codespace** in the
Command Palette, or stop it from [your Codespaces page](https://github.com/codespaces).
Account allowances and billing depend on your GitHub plan.

## The prediction task

At **T−60 minutes**, use available forecasts and technical checklist information to
predict whether a fictional mission's first attempt will **not lift off within
15 minutes after its original scheduled time**. The target is 1 for a delay greater
than 15 minutes or a scrubbed attempt, and 0 otherwise. Exactly 15 minutes is class 0.
This is classification, not a prediction of the exact delay duration.

**All 960 attempts are simulated.** Vehicle names, pad names, weather forecasts and
outcomes are fictional. The simulator is documented and reproducible; its numeric
relationships are not physical launch criteria. Reported scores measure learning
within that simulation and do not validate real launch forecasting or launch clearance.
No real-world accuracy claim is made.

The first 576 attempts are used for training, the next 192 for validation and the last
192 for final testing. Exploration and missing-value imputation use training data;
model and threshold choices use validation; notebook 02 scores the fixed choice on
the test split. Post-event fields are excluded from model inputs.

## Materials

- [`data/README.md`](data/README.md): units, target definition, provenance and limitations.
- [`data/synthetic_launch_attempts.csv`](data/synthetic_launch_attempts.csv): bundled teaching dataset.
- [`docs/INSTRUCTOR_GUIDE.md`](docs/INSTRUCTOR_GUIDE.md): timing, answers, facilitation and fallback plan.
- [`docs/VALIDATION.md`](docs/VALIDATION.md): the execution check and its scope.
- [`scripts/generate_data.py`](scripts/generate_data.py): deterministic dataset generator for instructors.
- [`scripts/validate_workshop.py`](scripts/validate_workshop.py): data checks and fresh-kernel execution of both notebooks.
- [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json): Python 3.12, Python/Jupyter extensions and automatic setup.
- [`requirements.txt`](requirements.txt): pinned direct dependencies used in validation.

The agenda supplies the session title, presenter name and date/time. The agenda PDF
is not required to run the notebooks. Technical background links appear in both notebooks.
The repository's original [MIT licence](LICENSE) is retained.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError` | Select **Python (Rocket Workshop)**. If setup did not finish, run `bash .devcontainer/post-create.sh` in the terminal, then restart the kernel. |
| Kernel is missing | Refresh the editor after setup; use **Select Another Kernel** and choose `.venv/bin/python`. |
| `NameError` after running a later cell | Restart the kernel and run all earlier cells in order. |
| Dataset not found | Open the full repository. Keep the `data/` directory beside `notebooks/`; do not copy only the notebook. |
| Sliders are blank | Run the preceding model cells first; then rerun the widget cell. The ordinary scenario cell provides the same model calculation. |
| Codespaces is unavailable or quota is exhausted | Use a locally prepared Python 3.12 environment below, or work with a partner who has a running environment. |
| Output differs after editing an exercise | Expected: your input/settings changed. Restart and restore the original defaults if you want the reference result. |

## Local alternative and instructor verification

With Python 3.12 installed, clone or download the repository and open its root in VS Code.
Install the Python and Jupyter extensions, then use:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --user --name rocket-workshop --display-name "Python (Rocket Workshop)"
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1` instead.
Select **Python (Rocket Workshop)** in each notebook.

To check both notebooks from fresh kernels, including the optional widget code:

```bash
python scripts/validate_workshop.py
```

The checker writes executed copies and a summary under `.validation/`; it does not
replace the distributed notebooks unless `--write-executed` is explicitly given.
The GitHub Actions workflow runs the same check on pushes and pull requests.
