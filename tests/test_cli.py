# tests/test_cli.py

import sys
import subprocess
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
CLI = ROOT / "cli.py"

def run_cmd(args, extra_env=None):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    result = subprocess.run(
        [sys.executable, str(CLI)] + args,
        capture_output=True,
        text=True,
        env=env,
        timeout=5,
    )
    return result

def test_amortize_exit_zero():
    res = run_cmd(["amortize", "-P", "1000", "-r", "0.05", "-y", "1", "-k", "4"])
    assert res.returncode == 0
    assert "Period" in res.stdout
    # check that it printed 4 lines of data
    assert len(res.stdout.strip().splitlines()) == 1 + 4  # header + 4 rows

def test_metrics_exit_zero():
    res = run_cmd(["metrics", "-P", "1000", "-r", "0.05", "-y", "1"])
    assert res.returncode == 0
    # should print at least total_interest
    assert "total_interest" in res.stdout

def test_plot_exit_zero():
    # Use a non‐interactive backend to avoid GUI popups
    res = run_cmd(
        ["plot", "balance", "-P", "1000", "-r", "0.05", "-y", "1"],
        extra_env={"MPLBACKEND": "Agg"}
    )
    assert res.returncode == 0
    # It shouldn’t print anything to stdout
    assert res.stdout == ""
    # And stderr should be empty
    assert res.stderr == ""

