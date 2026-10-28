"""Read rule files for the repository scripts, with one clear error instead of a traceback.

A rule file that cannot be read (not UTF-8, invalid YAML, YAML nested too deeply, a top level
without a `rules` list, or a rule that is not a mapping) raises RuleFileError naming the file.
"""
from __future__ import annotations

import pathlib

import yaml


class RuleFileError(ValueError):
    """A rule file that the scripts cannot use."""


def load_rules(path: pathlib.Path) -> list[dict]:
    try:
        text = path.read_bytes().decode("utf-8")
    except OSError as exc:
        raise RuleFileError(f"{path}: cannot read: {exc.strerror or exc}") from exc
    except UnicodeDecodeError as exc:
        raise RuleFileError(f"{path}: not UTF-8 text (byte {exc.start}); save it as UTF-8") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise RuleFileError(f"{path}: invalid YAML: {' '.join(str(exc).split())}") from exc
    except RecursionError as exc:
        raise RuleFileError(f"{path}: invalid YAML: nested too deeply to read") from exc
    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        raise RuleFileError(f"{path}: expected a mapping with a 'rules' list at the top level")
    for i, rule in enumerate(data["rules"]):
        if not isinstance(rule, dict):
            raise RuleFileError(f"{path}: rules[{i}] is not a mapping")
    return data["rules"]
