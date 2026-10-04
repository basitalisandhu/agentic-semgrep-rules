#!/usr/bin/env python3
"""Audit the fixtures: every finding must sit on a line annotated with 'ruleid: <id>'.

`semgrep --test` only checks annotated lines, so a rule that fires on an unannotated line of a
fixture (its own or another rule's) would pass the test suite while still being a false positive.
This script scans the whole fixture tree with the whole pack and fails on any such finding.

The fixture tree is copied to a temporary directory first because Semgrep's default ignore list
skips directories named tests/ when no project-level .semgrepignore is found.

Usage: python3 scripts/check_fixtures.py [--report] [--config PATH]

--config defaults to the rules/ directory; pass agentic-semgrep-rules.yaml to audit the
single-file bundle with the same fixtures.
"""
from __future__ import annotations

import collections
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ANNOTATION = re.compile(r"(#|//)\s*ruleid:\s*([a-z0-9-]+)")


def main(argv: list[str]) -> int:
    report = "--report" in argv
    config = pathlib.Path(argv[argv.index("--config") + 1]) if "--config" in argv else ROOT / "rules"
    with tempfile.TemporaryDirectory() as tmp:
        work = pathlib.Path(tmp)
        if config.is_dir():
            shutil.copytree(config, work / "rules")
        else:
            shutil.copy(config, work / "rules.yaml")
        shutil.copytree(ROOT / "tests", work / "tests")
        (work / ".semgrepignore").write_text(".git/\n")
        cmd = [
            "semgrep", "--config", "rules" if config.is_dir() else "rules.yaml",
            "--metrics=off", "--disable-version-check", "--json", "--quiet", "tests",
        ]
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
        if proc.returncode not in (0, 1):
            print(proc.stderr)
            return proc.returncode
        data = json.loads(proc.stdout)
        if data.get("errors"):
            for err in data["errors"]:
                print("semgrep error:", err.get("message", err))
            return 1
        findings = collections.defaultdict(set)
        for result in data["results"]:
            rule_id = result["check_id"].split(".")[-1]
            findings[(rule_id, result["path"])].add(result["start"]["line"])
        expected_total = 0
        for fixture in (work / "tests").rglob("*"):
            if fixture.is_file():
                expected_total += len(ANNOTATION.findall(fixture.read_text()))
        unannotated = 0
        per_rule: collections.Counter[str] = collections.Counter()
        for (rule_id, path), lines in sorted(findings.items()):
            source = (work / path).read_text().splitlines()
            expected = {
                i + 2 for i, line in enumerate(source)
                if (m := ANNOTATION.search(line)) and m.group(2) == rule_id
            }
            per_rule[rule_id] += len(lines)
            for line in sorted(lines - expected):
                unannotated += 1
                print(f"UNANNOTATED {rule_id} {path}:{line}: {source[line - 1].strip()}")
        total = len(data["results"])
        if report:
            for rule_id, count in sorted(per_rule.items()):
                print(f"{rule_id}: {count}")
        print(
            f"fixture audit: {total} findings, {expected_total} ruleid annotations, "
            f"{unannotated} findings on unannotated lines, "
            f"{len(data['paths']['scanned'])} files scanned"
        )
        if unannotated or total != expected_total:
            return 1
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
