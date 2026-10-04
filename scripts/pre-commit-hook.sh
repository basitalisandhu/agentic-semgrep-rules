#!/usr/bin/env sh
# pre-commit entry point for the agentic-semgrep-rules hook (see .pre-commit-hooks.yaml).
# pre-commit runs this script from the user's repository with the staged file names as
# arguments; the rules live next to this script, so resolve them from its own location.
set -eu
here=$(cd "$(dirname "$0")/.." && pwd)
if ! command -v semgrep >/dev/null 2>&1; then
  echo "agentic-semgrep-rules: semgrep is not on PATH (pip install semgrep)" >&2
  exit 1
fi
exec semgrep --config "$here/rules" --metrics=off --disable-version-check --error --quiet "$@"
