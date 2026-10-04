# Smoke test report

Date: 2026-10-03. Semgrep 1.179.0. Pack: 36 rules (23 Python, 13 TypeScript/JavaScript).

## Method

1. `semgrep --test --config rules tests`: every rule's fixture, with `ruleid` lines that must be reported and `ok` lines that must not.
2. `scripts/check_fixtures.py`: the whole fixture tree scanned with the whole pack; any finding on a line not annotated for that rule fails. This catches a rule firing on another rule's fixture, which `--test` does not.
3. `semgrep --config rules --metrics=off` against real code from a public sibling repository, [agent-threat-model](https://github.com/basitalisandhu/agent-threat-model), as a false-positive check.

## Results

### Fixture suite

```text
36/36: All tests passed
fixture audit: 175 findings, 175 ruleid annotations, 0 findings on unannotated lines, 40 files scanned
```

### Real code

| Target | Files scanned | Findings |
|---|---|---|
| `agent-threat-model` (Python CLI, package, scripts and tests) | 21 | 0 |

No findings on 21 real files.

## Tuning done during the smoke test

The fixture audit (step 2) surfaced two cross-fixture problems that `--test` alone had passed:

- `llm-output-to-sql` (Python) fired on `subprocess.run(...)` lines in the subprocess fixture because the sink list contained `$DB.run($QUERY, ...)`. The `run` sink was removed; `execute`, `executemany`, `executescript`, `mogrify`, `exec_driver_sql`, `text`, `read_sql`, `raw` and `sql` remain.
- `fastmcp-http-transport-without-auth` fired on the `fastmcp-bind-all-interfaces` fixture, which was correct behaviour (those servers had no auth). The fixture now configures `auth=` and `token_verifier=` so each fixture exercises only its own rule.

Earlier, during development, these false positives were removed before the smoke test:

- `llm-output-to-html` (Python) matched `st.write(...)` through a generic `$RESP.write($HTML)` sink. Removed.
- `llm-output-to-file-path` (Python) flagged `(BASE / model_output).resolve()` before a containment check. The `$BASE / $PATH` sink was replaced with `Path` method sinks (`read_text`, `write_text`, `open`, `unlink`, ...), which sit after the check.
- `llm-output-to-subprocess` (Python) flagged `subprocess.run(["wc", "-l", filename])`. The string-command sink now requires the command text not to start with `[` or `(`.
- `llm-output-to-innerhtml` (JS) dropped `$EL.append/prepend/after/before` and `$RES.send` as sinks; they are not HTML-specific.
- `llm-output-to-sql` (JS) dropped `$DB.get/all/run/exec` (Map.get, app.run).
- `llm-api-key-logged` (JS) no longer treats `process.env.NODE_ENV` as a secret: `process.env` is a source only when passed whole to a logging call.
- `mcp-http-transport-without-auth` (JS) no longer counts `cors()` as authentication middleware.

## Known limitations

- Taint tracking is intraprocedural. Model output passed through a helper function is tracked only when the parameter is used in a recognised response shape (`.choices[0].message.content`, `.output_text`, `.content[0].text`).
- `fastmcp-http-transport-without-auth`: an attribute assignment on the server object between construction and `run()` (for example `mcp.settings.host = ...`) defeats the auth exclusion, so such a server can be reported even with `auth=` configured.
- `torch-load-without-weights-only` reports plain `torch.load(path)` although PyTorch 2.6 and later default to `weights_only=True`; the rule cannot see the installed version, and the message says so.
- `semgrep --validate` fetches the registry's rule-lint metachecks from semgrep.dev; it could not run in the sandbox used for this report (egress blocked). Rule syntax was validated by the test suite and the full scans (semgrep-core rejects invalid rules at load time), and CI runs `--validate` with network access.

## Reproduce

```sh
make test
make smoke SMOKE_PATHS="path/to/your/code"
```
