"""Check the dataset and execute the two notebooks in separate fresh kernels.

Usage: python scripts/validate_workshop.py [--write-executed]
Execution copies are saved to .validation/ (ignored by Git).
"""

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

import nbformat
import numpy as np
import pandas as pd
from nbclient import NotebookClient

from generate_data import make_data


def execute_ipython(source, destination, cwd):
    """Socket-free fallback; called in a new process for each notebook.

    This executes cells with IPython, not a Jupyter kernel or Codespaces browser.
    The default validation engine remains nbclient/Jupyter.
    """
    from contextlib import redirect_stdout, redirect_stderr
    from io import StringIO
    import os
    from IPython.core.displaypub import DisplayPublisher
    from IPython.terminal.interactiveshell import TerminalInteractiveShell
    from IPython.utils.capture import capture_output

    os.chdir(cwd)
    nb = nbformat.read(source, as_version=4)
    shell = TerminalInteractiveShell.instance()
    with capture_output():
        shell.run_line_magic("matplotlib", "inline")
    shell.display_formatter.active_types = [
        "text/plain", "text/html", "image/png", "image/svg+xml",
        "application/vnd.jupyter.widget-view+json",
    ]
    count = 0
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        count += 1
        outputs = []

        class CellStream(StringIO):
            def __init__(self, name):
                super().__init__()
                self.name = name

            def write(self, value):
                if value:
                    if outputs and outputs[-1].output_type == "stream" and outputs[-1].name == self.name:
                        outputs[-1].text += value
                    else:
                        outputs.append(nbformat.v4.new_output("stream", name=self.name, text=value))
                return super().write(value)

        class CellDisplay(DisplayPublisher):
            def publish(self, data, metadata=None, **kwargs):
                outputs.append(nbformat.v4.new_output("display_data", data=data, metadata=metadata or {}))

            def clear_output(self, wait=False):
                outputs.clear()

        old_publisher = shell.display_pub
        shell.display_pub = CellDisplay(shell=shell)
        try:
            with redirect_stdout(CellStream("stdout")), redirect_stderr(CellStream("stderr")):
                result = shell.run_cell(cell.source, store_history=True)
        finally:
            shell.display_pub = old_publisher
        if result.error_before_exec or result.error_in_exec:
            details = "\n".join(o.get("text", "") for o in outputs)
            raise RuntimeError(f"Cell {cell.id} failed: {details}") from (result.error_before_exec or result.error_in_exec)
        cell.execution_count = count
        cell.outputs = outputs
    nbformat.write(nb, destination)


def validate_data(root):
    csv = root / "data/synthetic_launch_attempts.csv"
    frame = pd.read_csv(csv, parse_dates=["scheduled_launch_utc", "prediction_time_utc", "outcome_recorded_utc"])
    expected = make_data()
    pd.testing.assert_frame_equal(frame, expected, check_dtype=False, check_exact=False, rtol=1e-12, atol=1e-12)
    assert frame.shape == (960, 15)
    assert frame.mission_id.is_unique
    assert frame.scheduled_launch_utc.is_monotonic_increasing
    assert frame.scrubbed.isin([0, 1]).all() and frame.delayed.isin([0, 1]).all()
    assert frame.actual_delay_minutes.isna().equals(frame.scrubbed.eq(1))
    assert frame.delayed.equals((frame.scrubbed.eq(1) | frame.actual_delay_minutes.gt(15)).astype(int))
    assert frame.forecast_wind_kmh.dropna().between(0, 85).all()
    assert frame.temperature_c.dropna().between(5, 42).all()
    assert frame.open_technical_items.between(0, 5).all()
    for name in ["forecast_rain_pct", "forecast_lightning_pct", "forecast_cloud_pct"]:
        assert frame[name].dropna().between(0, 100).all()
    for start, end in [(0, 576), (576, 768), (768, 960)]:
        assert frame.iloc[start:end].delayed.nunique() == 2
    for boundary in [576, 768]:
        assert frame.iloc[:boundary].outcome_recorded_utc.max() < frame.iloc[boundary:].prediction_time_utc.min()
    return hashlib.sha256(csv.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-executed", action="store_true", help="Refresh reference outputs in the distributed notebooks.")
    parser.add_argument("--engine", choices=["jupyter", "ipython"], default="jupyter",
                        help="Use isolated IPython processes only when local kernel sockets are unavailable.")
    parser.add_argument("--execute-ipython", nargs=3, metavar=("SOURCE", "DESTINATION", "CWD"), help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.execute_ipython:
        execute_ipython(*args.execute_ipython)
        return
    root = Path(__file__).resolve().parents[1]
    output = root / ".validation"
    output.mkdir(exist_ok=True)
    digest = validate_data(root)
    notebooks = sorted((root / "notebooks").glob("*.ipynb"))
    assert len(notebooks) == 2
    results = []
    for i, path in enumerate(notebooks):
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        assert nb.metadata.workshop.duration_minutes == 60
        assert nb.metadata.authors[0].name == "Dr. Mohammed Hussin Talafha"
        for cell in nb.cells:
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
        start = time.perf_counter()
        # Exercise both supported launch directories and never reuse kernel state.
        cwd = root if i == 0 else root / "notebooks"
        if args.engine == "jupyter":
            client = NotebookClient(nb, timeout=180, kernel_name="python3",
                                    resources={"metadata": {"path": str(cwd)}},
                                    # Output widgets need state while messages are processed.
                                    # Remove live state only after execution for static previews.
                                    allow_errors=False, store_widget_state=True)
            client.execute()
        else:
            subprocess.run([sys.executable, str(Path(__file__).resolve()), "--execute-ipython",
                            str(path), str(output / path.name), str(cwd)], check=True, timeout=180)
            nb = nbformat.read(output / path.name, as_version=4)
        seconds = time.perf_counter() - start
        cells = [c for c in nb.cells if c.cell_type == "code"]
        assert all(c.execution_count is not None for c in cells)
        assert not any(o.output_type == "error" for c in cells for o in c.outputs)
        image_count = sum("image/png" in o.get("data", {}) for c in cells for o in c.outputs)
        assert image_count >= 2, "Expected visible educational figures."
        # Live widget references have no meaning in a static GitHub preview.
        # Keep ordinary text/images and allow users to recreate widgets by rerunning.
        nb.metadata.pop("widgets", None)
        for cell in cells:
            cell.metadata.pop("execution", None)
            for result in cell.outputs:
                result.get("data", {}).pop("application/vnd.jupyter.widget-view+json", None)
            if "widgets" in cell.metadata.get("tags", []):
                cell.outputs = [nbformat.v4.new_output("stream", name="stdout", text=
                    "Interactive controls passed execution. Rerun this cell in Codespaces to display the sliders.\n")]
        nbformat.write(nb, output / path.name)
        if args.write_executed:
            nbformat.write(nb, path)
        result = {"notebook": path.name, "code_cells": len(cells),
                  "figures": image_count, "seconds": round(seconds, 2), "status": "passed", "engine": args.engine,
                  "working_directory": "repository root" if i == 0 else "notebooks/"}
        results.append(result)
        print(json.dumps(result), flush=True)

    # Check the student export produced by a completely independent notebook 02.
    report = json.loads((root / "artifacts/my_workshop_report.json").read_text())
    assert 0.1 <= report["threshold"] <= 0.9
    assert 0 <= report["my_scenario_probability"] <= 1
    assert report["instructor"] == "Dr. Mohammed Hussin Talafha"
    assert np.isfinite(list(report["test_metrics"].values())).all()
    for filename in ["final_test_metrics.csv", "scenario_predictions.csv"]:
        assert not pd.read_csv(root / "artifacts" / filename).empty
    summary = {"python": platform.python_version(), "dataset_sha256": digest,
               "rows": 960, "checks": results, "default_report": report,
               "codespaces_browser_session_tested": False}
    (output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"PASS: dataset, independent {args.engine} execution, figures, widget code and student exports.", flush=True)


if __name__ == "__main__":
    main()
