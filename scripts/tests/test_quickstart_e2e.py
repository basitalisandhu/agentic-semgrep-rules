"""End-to-end: install Semgrep in a fresh venv and run the README quick start and Example.

The quick start runs the single-file bundle on a project; here the bundle is the committed
agentic-semgrep-rules.yaml (the README's URL serves the same file from main) and the project
holds the fixture the README output comes from, saved as agent.py (the bundle sits in the
working directory, so rule ids carry no path prefix, as with the URL). The rule id and the three
code lines of the README excerpt must appear in the output. The Example section's MCP tool
must be reported by `--config rules` from a clone. Installing Semgrep needs the network, so
this runs only when SEMGREP_E2E=1; CI sets it in the quickstart job.
"""
from __future__ import annotations

import os
import pathlib
import re
import shutil
import subprocess
import venv

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
README = (ROOT / "README.md").read_text(encoding="utf-8")
VERSION = os.environ.get("SEMGREP_VERSION", "1.181.0")
pytestmark = pytest.mark.skipif(os.environ.get("SEMGREP_E2E") != "1", reason="set SEMGREP_E2E=1 to run")


@pytest.fixture(scope="module")
def semgrep(tmp_path_factory) -> pathlib.Path:
    env_dir = tmp_path_factory.mktemp("venv")
    venv.create(env_dir, with_pip=True)
    bin_dir = env_dir / ("Scripts" if os.name == "nt" else "bin")
    subprocess.run([str(bin_dir / "python"), "-m", "pip", "install", "-q", f"semgrep=={VERSION}"],
                   check=True, capture_output=True)
    return bin_dir / "semgrep"


def _run(semgrep: pathlib.Path, config: str, cwd: pathlib.Path, target: str = ".") -> str:
    proc = subprocess.run([str(semgrep), "--config", config, "--metrics=off", "--disable-version-check", target],
                          cwd=cwd, capture_output=True, text=True, timeout=600)
    assert proc.returncode == 0, proc.stderr[-2000:]
    return proc.stdout


def test_readme_quick_start(semgrep, tmp_path):
    first = README[: README.index("## When to use this")]
    command = re.search(r"```sh\npip install semgrep\n(semgrep --config \S+ \.)\n```", first).group(1)
    assert command.split()[2].endswith("/main/agentic-semgrep-rules.yaml")
    fixture = re.search(r"the file is \[`(tests/[^`]+)`\]", first).group(1)
    excerpt = re.search(r"```text\n(.*?)```", first, re.S).group(1)
    project = tmp_path / "project"
    project.mkdir()
    shutil.copy(ROOT / fixture, project / "agent.py")
    # A local config file's directory becomes a rule id prefix; from the working directory there is
    # none, which matches what the README's URL form prints.
    shutil.copy(ROOT / "agentic-semgrep-rules.yaml", tmp_path / "agentic-semgrep-rules.yaml")
    out = _run(semgrep, "agentic-semgrep-rules.yaml", tmp_path, "project")
    lines = {line.strip() for line in out.splitlines()}
    wanted = [line.strip() for line in excerpt.splitlines() if "┆" in line and "---" not in line]
    wanted.append(next(line.strip() for line in excerpt.splitlines() if "❯" in line))
    assert len(wanted) == 4 and [w for w in wanted if w not in lines] == []


def test_readme_example_from_a_clone(semgrep, tmp_path):
    section = README[README.index("## Example"):]
    code = re.search(r"```python\n(.*?)```", section, re.S).group(1)
    rule = re.search(r"```text\n(\S+)", section).group(1)
    project = tmp_path / "project"
    project.mkdir()
    (project / "server.py").write_text("import subprocess\n" + code, encoding="utf-8")
    shutil.copytree(ROOT / "rules", tmp_path / "rules")
    out = _run(semgrep, "../rules", project)
    assert rule.split(".", 1)[1] in out
