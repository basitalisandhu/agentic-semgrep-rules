# Good first issues

Issues the maintainer intends to open under the `good first issue` label, written out so
they can be filed in one sitting. Each one is self-contained and has acceptance criteria
that `make test` and `make validate` can check. Read [CONTRIBUTING.md](../CONTRIBUTING.md)
and [rule-writing.md](rule-writing.md) first: every rule change needs `ruleid` and `ok`
fixture lines, complete metadata, a regenerated bundle (`make bundle`) and a CHANGELOG
entry under Unreleased.

## 1. Autofix for `yaml-unsafe-load`

**Context.** `rules/python/deserialization/yaml-unsafe-load.yaml` reports `yaml.load(x)`
and the explicit `Loader=yaml.Loader`, `UnsafeLoader` and `FullLoader` forms. The safe
replacement is always `yaml.safe_load(x)`, so this is the simplest rule to give a `fix:`.
The Roadmap lists autofix for the flag-based rules; this is the first.

**Acceptance criteria.**

- The rule gains `fix: yaml.safe_load($DATA)`.
- A fixture `tests/python/deserialization/yaml-unsafe-load.fixed.py` holds the expected
  result of applying the fix to `yaml-unsafe-load.py`, and `semgrep --test` reports the
  fix test as passed (today it prints "No tests for fixes found").
- `make test`, `make validate` and `make bundle` pass; CHANGELOG updated.

## 2. Autofix for `torch-load-without-weights-only`

**Context.** `rules/python/deserialization/torch-load-without-weights-only.yaml` reports
`torch.load(...)` without `weights_only=True`. For the plain `torch.load($PATH)` and
`torch.load($PATH, map_location=$LOC)` forms the fix is mechanical.

**Acceptance criteria.**

- Split the rule's patterns so that the two forms above carry a `fix:` that appends
  `weights_only=True`; other forms (extra keyword arguments, `torch.jit.load`) keep
  reporting without a fix.
- `tests/python/deserialization/torch-load-without-weights-only.fixed.py` added and
  `semgrep --test` reports the fix test as passed.
- The message still says that PyTorch 2.6 and later default to `weights_only=True`.
- `make test`, `make validate` and `make bundle` pass; CHANGELOG updated.

## 3. Fixture lines for Semantic Kernel and pydantic-ai tool decorators

**Context.** `agent-tool-param-to-shell` and `agent-tool-param-to-file-path` list
`@kernel_function` (Semantic Kernel) and `@agent.tool_plain` (pydantic-ai) as sources,
but `tests/python/permissions/` has no `kernel_function` line, so a regression in those
patterns would pass the suite.

**Acceptance criteria.**

- Each of the two fixtures gains one `ruleid` function per decorator (shell command
  reaching `subprocess.run(..., shell=True)` or a path reaching `open()`), and one `ok`
  function per decorator using the mitigated form named in the rule message.
- `make test` passes with the finding count in `scripts/check_fixtures.py` output
  raised by exactly the number of new `ruleid` lines.
- `make bundle` run if any rule text changed.

## 4. Enforce the `metadata.masoon` block in the metadata lint

**Context.** Every rule carries `metadata.masoon.pack` and `metadata.masoon.family`
(see the rule anatomy in CONTRIBUTING.md), and SARIF consumers group on `family`, but
`scripts/check_metadata.py` does not check the block, so a new rule can omit it.

**Acceptance criteria.**

- `check_metadata.py` fails when `metadata.masoon` is missing, when `pack` is not
  `agentic-semgrep-rules`, or when `family` is not one of the values currently in use
  (collect them with `grep -h "family:" rules/*/*/*.yaml | sort -u` and list them in
  the script).
- A unit test under `scripts/` or `tests/` (plain `python3 -m pytest` or a `__main__`
  self-test) covers one passing and one failing rule dict.
- `python3 scripts/check_metadata.py rules` still reports 0 problems.

## 5. New rule: model output reaching an HTTP redirect

**Context.** The `llm-output-to-*` family covers shells, SQL, HTTP requests, file paths
and HTML, but not open redirects (CWE-601): a model-chosen URL passed to Flask
`redirect()`, Django `HttpResponseRedirect()` or Express `res.redirect()` sends the user
wherever the content the model read told it to.

**Acceptance criteria.**

- `rules/python/injection/llm-output-to-redirect.yaml` and
  `rules/javascript/injection/llm-output-to-redirect.yaml`, taint mode, reusing the
  exact source list of the sibling `llm-output-to-http-request` and `llm-output-to-fetch`
  rules (copy it; the family shares sources).
- Sinks: `redirect($URL)`, `HttpResponseRedirect($URL)`, `$RES.redirect($URL)`,
  `$RES.redirect($STATUS, $URL)`; sanitizers: an allowlist check or `urlparse`-based
  host validation, with an `ok` line for each.
- Fixtures with at least two `ruleid` and two `ok` lines per language; metadata with
  `CWE-601: URL Redirection to Untrusted Site ('Open Redirect')`, `LLM05:2025 Improper
  Output Handling`, confidence MEDIUM.
- README "What it finds" table row under "Model output reaches injection sinks", rule
  count in the README, `docs/smoke-test.md` header and `repos-meta` description updated
  from 36 to 38, `make bundle`, CHANGELOG.

## 6. ESM and CommonJS fixtures for `llm-output-to-child-process`

**Context.** The JavaScript fixtures are `.ts`, `.tsx` and `.js`. Node projects also
ship `.mjs` and `.cjs` files; Semgrep parses them as JavaScript, but nothing in the
suite proves the `import`/`require` forms of `child_process` are both recognised.

**Acceptance criteria.**

- `tests/javascript/code-execution/llm-output-to-child-process.mjs` (ESM `import`) and
  `.cjs` (`require`) each with one `ruleid` and one `ok` line.
- `semgrep --test` picks both up (it pairs fixtures with the rule by file stem) and
  `scripts/check_fixtures.py` scans 42 files instead of 40.
- `.pre-commit-hooks.yaml` `types_or` extended if pre-commit's `javascript` type does
  not already cover `.mjs` and `.cjs` (check the identify library's extension list and
  say which in the pull request).
