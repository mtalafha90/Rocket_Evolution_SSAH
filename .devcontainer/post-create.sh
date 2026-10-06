#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
python -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
.venv/bin/python -m ipykernel install --user --name rocket-workshop --display-name "Python (Rocket Workshop)"
printf '\nReady: open notebook 01 and select Python (Rocket Workshop).\n'
