#!/usr/bin/env python3
"""Check that every rule in the pack carries the metadata this project requires.

Usage: python3 scripts/check_metadata.py rules

Exit code 1 if any rule is missing a field or uses an unexpected value, 2 if a rule file
cannot be read or parsed (the message names the file).
"""
from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _ruleio import RuleFileError, load_rules  # noqa: E402

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


def check_fixture_cases(path: pathlib.Path, rid: str) -> list[str]:
    """Every rule needs at least one positive (ruleid) and one negative (ok) fixture line."""
    if "rules" not in path.parts or not rid:
        return []
    idx = path.parts.index("rules")
    tests_dir = pathlib.Path(*path.parts[:idx], "tests", *path.parts[idx + 1 : -1])
    text = "".join(
        f.read_text(encoding="utf-8", errors="replace")
        for f in sorted(tests_dir.glob(f"{path.stem}*"))
        if f.is_file() and f.suffix not in {".yaml", ".yml"}
    )
    word = re.escape(rid)
    problems = []
    if not re.search(rf"ruleid:[^\n]*\b{word}\b", text):
        problems.append(f"no positive fixture ('ruleid: {rid}') under {tests_dir}")
    if not re.search(rf"\bok:[^\n]*\b{word}\b", text):
        problems.append(f"no negative fixture ('ok: {rid}') under {tests_dir}")
    return problems


def _strings(value) -> list:
    """A list-valued field as a list; a scalar counts as one entry, anything else as none."""
    if isinstance(value, list):
        return value
    return [] if value is None or isinstance(value, dict) else [value]


def check_types(rule: dict) -> list[str]:
    """Fields whose type would make the other checks meaningless."""
    problems = []
    for key, kind in (("id", str), ("message", str), ("severity", str), ("languages", list), ("metadata", dict)):
        if key in rule and not isinstance(rule[key], kind):
            problems.append(f"'{key}' must be a {kind.__name__.replace('str', 'string').replace('dict', 'mapping')}")
    meta = rule.get("metadata")
    if isinstance(meta, dict):
        for key in ("cwe", "owasp", "references", "technology", "subcategory"):
            if key in meta and not isinstance(meta[key], list):
                problems.append(f"metadata.{key} must be a list")
    return problems


def check_rule(path: pathlib.Path, rule: dict) -> list[str]:
    problems: list[str] = []
    for key in REQUIRED_TOP:
        if key not in rule:
            problems.append(f"missing top-level '{key}'")
    type_problems = check_types(rule)
    if type_problems:
        return problems + type_problems
    rid = rule.get("id", "")
    if not ID_RE.match(rid):
        problems.append(f"id '{rid}' is not kebab-case")
    if rid and path.stem != rid:
        problems.append(f"file name '{path.name}' does not match id '{rid}'")
    if str(rule.get("severity")) not in SEVERITIES:
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
    for cwe in _strings(meta.get("cwe")):
        if not CWE_RE.match(str(cwe)):
            problems.append(f"cwe entry '{cwe}' must look like 'CWE-78: ...'")
    for owasp in _strings(meta.get("owasp")):
        if not OWASP_RE.match(str(owasp)):
            problems.append(f"owasp entry '{owasp}' must look like 'LLM05:2025 ...'")
    for level_key in ("confidence", "likelihood", "impact"):
        if str(meta.get(level_key)) not in LEVELS:
            problems.append(f"metadata.{level_key} must be one of {sorted(LEVELS)}")
    refs = meta.get("references", [])
    if not refs or not all(str(r).startswith("https://") for r in refs):
        problems.append("metadata.references must be a non-empty list of https URLs")
    levels = {str(meta.get(k)) for k in ("confidence", "likelihood", "impact")}
    if rule.get("severity") == "ERROR" and levels != {"HIGH"}:
        problems.append("severity ERROR needs confidence, likelihood and impact all HIGH")
    if rule.get("severity") != "ERROR" and levels == {"HIGH"}:
        problems.append("confidence, likelihood and impact are all HIGH, so severity must be ERROR")
    problems.extend(check_fixture_cases(path, rid))
    lang_dir = path.parts[path.parts.index("rules") + 1] if "rules" in path.parts else ""
    langs = {str(x) for x in rule.get("languages", [])}
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
    unreadable = 0
    for path in files:
        try:
            rules = load_rules(path)
        except RuleFileError as exc:
            print(f"error: {exc}")
            unreadable += 1
            continue
        for rule in rules:
            count += 1
            problems = check_rule(path, rule)
            for problem in problems:
                failures += 1
                print(f"{path}: {rule.get('id', '?')}: {problem}")
    print(f"checked {count} rules in {len(files)} files, {failures} problems")
    if unreadable:
        print(f"{unreadable} file(s) could not be read")
        return 2
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
