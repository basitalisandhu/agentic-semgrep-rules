"""Seeded fuzz tests for the repository scripts that read rule files.

`check_metadata.py` and `bundle.py` read every rules/**/*.yaml. A damaged rule file (not UTF-8,
invalid or deeply nested YAML, a top level without `rules`, a rule that is not a mapping, fields
of the wrong type) must give exit code 1 or 2 and a message naming the file, never a traceback.
Each test runs under an alarm so a hang fails instead of stalling CI.

Run: python3 -m pytest -q scripts/tests
"""
from __future__ import annotations

import copy
import io
import pathlib
import random
import shutil
import signal
import sys
from contextlib import redirect_stdout

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import bundle  # noqa: E402
import check_metadata  # noqa: E402

SEED = 20261028
SECONDS = 60
RULE_FILES = sorted((ROOT / "rules").rglob("*.yaml"))
JUNK = [None, 5, True, "", 1.5, [], {}, ["x"], {"x": 1}, [None], "x" * 2000]


@pytest.fixture(autouse=True)
def _alarm():
    if not hasattr(signal, "SIGALRM"):  # pragma: no cover - Windows
        yield
        return

    def fail(signum, frame):
        raise TimeoutError(f"test ran longer than {SECONDS}s")

    old = signal.signal(signal.SIGALRM, fail)
    signal.alarm(SECONDS)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def _paths(value, prefix=()):
    if prefix:
        yield prefix
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _paths(item, prefix + (key,))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from _paths(item, prefix + (i,))


def _damage(rng: random.Random, doc):
    path = rng.choice(list(_paths(doc)))
    parent = doc
    for key in path[:-1]:
        parent = parent[key]
    if rng.random() < 0.3:
        del parent[path[-1]]
    else:
        parent[path[-1]] = copy.deepcopy(rng.choice(JUNK))
    return doc


def _tree(tmp: pathlib.Path, rel: pathlib.Path, content: bytes) -> pathlib.Path:
    rules = tmp / "rules"
    if rules.exists():
        shutil.rmtree(rules)
    target = rules / rel
    target.parent.mkdir(parents=True)
    target.write_bytes(content)
    return rules


def _run(fn, argv):
    out = io.StringIO()
    with redirect_stdout(out):
        rc = fn(argv)
    return rc, out.getvalue()


def test_damaged_rules_never_crash_the_scripts(tmp_path, monkeypatch):
    rng = random.Random(SEED)
    for _ in range(200):
        source = rng.choice(RULE_FILES)
        doc = _damage(rng, yaml.safe_load(source.read_text(encoding="utf-8")))
        rules = _tree(tmp_path, source.relative_to(ROOT / "rules"), yaml.safe_dump(doc).encode())
        rc, _ = _run(check_metadata.main, ["check_metadata.py", str(rules)])
        assert rc in (0, 1, 2)
        monkeypatch.setattr(bundle, "RULES", rules)
        rc, _ = _run(bundle.main, ["--out", str(tmp_path / "bundle.yaml")])
        assert rc in (0, 2)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (b"\xff\xfe", "not UTF-8"),
        (b"rules: [" + b"[" * 100_000, "invalid YAML"),
        (b"rules: [unclosed\n", "invalid YAML"),
        (b"- just a list\n", "expected a mapping with a 'rules' list"),
        (b"rules: [5]\n", "rules[0] is not a mapping"),
        (b"", "expected a mapping with a 'rules' list"),
    ],
)
def test_unreadable_rule_files_exit_2_naming_the_file(content, message, tmp_path, monkeypatch):
    rel = pathlib.Path("python/injection/broken-rule.yaml")
    rules = _tree(tmp_path, rel, content)
    rc, out = _run(check_metadata.main, ["check_metadata.py", str(rules)])
    assert rc == 2 and str(rules / rel) in out and message in out
    monkeypatch.setattr(bundle, "RULES", rules)
    rc, out = _run(bundle.main, ["--out", str(tmp_path / "bundle.yaml")])
    assert rc == 2 and str(rules / rel) in out and message in out


def test_wrong_types_are_lint_problems_not_crashes(tmp_path):
    doc = yaml.safe_load(RULE_FILES[0].read_text(encoding="utf-8"))
    doc["rules"][0]["message"] = 7
    doc["rules"][0]["metadata"]["cwe"] = {"CWE-1": "x"}
    rules = _tree(tmp_path, RULE_FILES[0].relative_to(ROOT / "rules"), yaml.safe_dump(doc).encode())
    rc, out = _run(check_metadata.main, ["check_metadata.py", str(rules)])
    assert rc == 1 and "'message' must be a string" in out and "metadata.cwe must be a list" in out


def test_option_without_a_value_is_a_usage_error(tmp_path):
    import check_fixtures

    assert _run(check_fixtures.main, ["--config"])[0] == 2
    assert _run(check_fixtures.main, ["--config", str(tmp_path / "missing")])[0] == 2
    assert _run(bundle.main, ["--out"])[0] == 2
