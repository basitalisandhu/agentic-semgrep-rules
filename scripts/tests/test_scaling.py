"""Scaling checks: ten times the input must take roughly ten times as long, not a hundred.

1. The whole pack scans the fixture tree copied once and ten times (needs `semgrep` on PATH;
   skipped otherwise). Measured on 1.181.0: 44 files 1.8s, 440 files 4.7s, most of it start-up.
2. `check_metadata.py` lints the rules tree and a tree with ten copies of every rule.
The ratio of the two timings (best of three for the second) must stay under 30.
"""
from __future__ import annotations

import io
import pathlib
import shutil
import subprocess
import sys
import time
from contextlib import redirect_stdout

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_metadata  # noqa: E402

LIMIT = 30


def _copies(dest: pathlib.Path, source: pathlib.Path, n: int) -> pathlib.Path:
    for i in range(n):
        shutil.copytree(source, dest / f"copy{i}")
    for fixed in dest.rglob("*.fixed.*"):
        fixed.unlink()
    return dest


@pytest.mark.skipif(shutil.which("semgrep") is None, reason="semgrep is not on PATH")
def test_pack_scan_time_stays_near_linear(tmp_path):
    (tmp_path / ".semgrepignore").write_text(".git/\n")
    timings = []
    for n in (1, 10):
        target = _copies(tmp_path / f"x{n}", ROOT / "tests", n)
        start = time.perf_counter()
        proc = subprocess.run(
            ["semgrep", "--config", str(ROOT / "rules"), "--metrics=off", "--disable-version-check",
             "--json", "--quiet", target.name],
            cwd=tmp_path, capture_output=True, text=True, timeout=600,
        )
        timings.append(time.perf_counter() - start)
        assert proc.returncode in (0, 1), proc.stderr[-1000:]
    assert timings[1] / timings[0] < LIMIT, f"1x {timings[0]:.2f}s, 10x {timings[1]:.2f}s"


def test_metadata_lint_time_stays_near_linear(tmp_path):
    def best(rules: pathlib.Path) -> float:
        times = []
        for _ in range(3):
            start = time.perf_counter()
            with redirect_stdout(io.StringIO()):
                check_metadata.main(["check_metadata.py", str(rules)])
            times.append(time.perf_counter() - start)
        return max(min(times), 1e-3)

    small = best(ROOT / "rules")
    big = tmp_path / "rules"
    for path in sorted((ROOT / "rules").rglob("*.yaml")):
        for i in range(10):
            dest = big / path.relative_to(ROOT / "rules").parent / f"{path.stem}{i}.yaml"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    assert best(big) / small < LIMIT
