#!/usr/bin/env python3
"""Check that every rule in the pack carries the metadata this project requires.

Usage: python3 scripts/check_metadata.py rules

Exit code 1 if any rule is missing a field or uses an unexpected value.
"""
from __future__ import annotations

import pathlib
import re
import sys

import yaml

REQUIRED_TOP = ["id", "languages", "severity", "message", "metadata"]
REQUIRED_META = [
    "category",
    "subcategory",
    "cwe",
    "owasp",
    "confidence",
    "likelihood",
    "impact",
    "technology",
    "references",
]
LEVELS = {"LOW", "MEDIUM", "HIGH"}
SEVERITIES = {"INFO", "WARNING", "ERROR"}
CWE_RE = re.compile(r"^CWE-\d+: .+")
OWASP_RE = re.compile(r"^LLM(0[1-9]|10):2025 .+")
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def check_rule(path: pathlib.Path, rule: dict) -> list[str]:
    problems: list[str] = []
    for key in REQUIRED_TOP:
        if key not in rule:
            problems.append(f"missing top-level '{key}'")
    rid = rule.get("id", "")
    if not ID_RE.match(rid):
        problems.append(f"id '{rid}' is not kebab-case")
    if rid and path.stem != rid:
        problems.append(f"file name '{path.name}' does not match id '{rid}'")
    if rule.get("severity") not in SEVERITIES:
        problems.append(f"severity must be one of {sorted(SEVERITIES)}")
    message = rule.get("message", "")
    if len(message) < 80:
        problems.append("message is too short to explain the finding and the fix")
    meta = rule.get("metadata") or {}
    for key in REQUIRED_META:
        if key not in meta:
            problems.append(f"missing metadata.{key}")
    if meta.get("category") != "security":
        problems.append("metadata.category must be 'security'")
    for cwe in meta.get("cwe", []):
        if not CWE_RE.match(str(cwe)):
            problems.append(f"cwe entry '{cwe}' must look like 'CWE-78: ...'")
    for owasp in meta.get("owasp", []):
        if not OWASP_RE.match(str(owasp)):
            problems.append(f"owasp entry '{owasp}' must look like 'LLM05:2025 ...'")
    for level_key in ("confidence", "likelihood", "impact"):
        if meta.get(level_key) not in LEVELS:
            problems.append(f"metadata.{level_key} must be one of {sorted(LEVELS)}")
    refs = meta.get("references", [])
    if not refs or not all(str(r).startswith("https://") for r in refs):
        problems.append("metadata.references must be a non-empty list of https URLs")
    lang_dir = path.parts[path.parts.index("rules") + 1] if "rules" in path.parts else ""
    langs = set(rule.get("languages", []))
    if lang_dir == "python" and langs != {"python"}:
        problems.append("rules under rules/python must declare languages: [python]")
    if lang_dir == "javascript" and not langs <= {"javascript", "typescript"}:
        problems.append("rules under rules/javascript must declare javascript and/or typescript")
    return problems


def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[1] if len(argv) > 1 else "rules")
    files = sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml"))
    failures = 0
    count = 0
    for path in files:
        data = yaml.safe_load(path.read_text())
        for rule in data.get("rules", []):
            count += 1
            problems = check_rule(path, rule)
            for problem in problems:
                failures += 1
                print(f"{path}: {rule.get('id', '?')}: {problem}")
    print(f"checked {count} rules in {len(files)} files, {failures} problems")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
