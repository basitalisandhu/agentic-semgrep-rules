# Writing rules for this pack

This guide covers the conventions behind the pack and the Semgrep behaviours that cost time while building it. Read it before adding or changing a rule. The pull request checklist is in [CONTRIBUTING.md](../CONTRIBUTING.md).

## 1. Decide what the rule is about

Each rule answers one question with one CWE:

| Family | Question | Mode |
|---|---|---|
| `llm-output-to-*` | Does text the model produced reach a dangerous sink? | taint |
| `user-input-in-system-prompt` | Does untrusted input reach the system prompt? | taint |
| `*-tool-param-to-*` | Does a model-filled tool argument reach a dangerous sink? | taint |
| flag and constructor rules (`langchain-allow-dangerous-*`, `torch-load-*`, `fastmcp-*`) | Is a dangerous option enabled or a dangerous component used? | pattern |
| secrets rules | Is a credential in source, on a command line or in a log? | regex, pattern, taint |

If your idea does not fit a family, it may still be a good rule, but ask whether a developer can act on the finding and whether the pattern is specific to agent code. "max_tokens is not set" was rejected for this reason: too common, too rarely a security problem.

## 2. Sources

### Model output (Python and JS)

The source list is identical in every `llm-output-to-*` rule of a language. It has three parts:

1. Vendor SDK calls, matched as a whole call with `exact: true`.
2. Framework calls (`invoke`, `run`, `predict`, `stream`, `kickoff`) restricted with `metavariable-regex` to receivers whose name contains `agent`, `chain`, `llm`, `model`, `graph`, `runnable`, `executor`, `crew`, `pipeline`, `chat`, `assistant`, `bot` or `completion`, or is exactly `app` or `workflow`. Without this restriction `subprocess.run(...)` and `thread.run()` would be sources.
3. Response shapes unique to model SDKs (`$R.choices[0].message.content`, `$R.output_text`, `$R.content[0].text`), so that a response passed through a function parameter is still recognised.

When you add a provider, add it to every rule in the family for that language and copy the fixture line into one rule's fixture.

### Tool parameters

Parameters of functions registered as tools are sources. The decorator forms covered are listed in `agent-tool-param-to-shell.yaml` (Python) and `mcp-tool-param-to-shell.yaml` (JS). Python excludes `self`, `ctx` and `context`. JS handles destructured (`({ command })`), renamed (`({ path: target })`) and positional (`(args) => args.command`) handlers.

### Untrusted input for prompt injection

Request objects (`request.args`, `req.body`, `await request.json()`), route handler parameters (FastAPI style decorators, Hono context), CLI arguments and chat framework handlers. Keep this list to things that are user-controlled by construction.

## 3. Sinks

Point `focus-metavariable` at the argument that must be tainted. A sink such as `subprocess.run($CMD, ..., shell=True, ...)` with focus on `$CMD` reports only when the command is tainted, not when the model output is in `cwd=`.

Model-chosen *values* inside a safe structure are not findings: `subprocess.run(["wc", "-l", filename])` and `cur.execute("... WHERE x = ?", (value,))` must stay clean. When the sink argument is a list or a parameter tuple the taint is in a sub-expression that is not the focused argument, which is what makes this work.

## 4. Sanitizers

Add the mitigations a careful developer writes, and add an `ok` fixture line for each one:

- Shell: `shlex.quote`, numeric casts, allowlist membership checks (`if x not in ALLOWED: raise`).
- Paths: `os.path.basename`, `secure_filename`, `path.basename`, containment checks (`if not p.is_relative_to(BASE)`, `if (!resolved.startsWith(BASE))`).
- URLs: `encodeURIComponent`, `urllib.parse.quote`, a `validate_url` helper.
- HTML: `bleach.clean`, `nh3.clean`, `DOMPurify.sanitize`, `html.escape`.
- Secrets: `bool(...)`, `len(...)`, masked slices.

Conditional sanitizers use the pattern-inside idiom:

```yaml
pattern-sanitizers:
  - patterns:
      - pattern-inside: |
          if not $P.is_relative_to(...):
            ...
          ...
      - pattern: $P
```

Any use of `$P` after that guard is considered clean.

## 5. Semgrep behaviours to know (verified on 1.179)

- **`metavariable-regex` is anchored at the start of the matched text.** `regex: API` does not match `"OPENAI_API_KEY"`; `regex: (?i)^.*api.*$` does. Always write regexes with explicit `^` and `$` and `.*` where you mean "contains". The text includes the quotes of a string literal.
- **An unbound metavariable in `metavariable-regex` fails the whole `patterns` group.** If a `pattern-either` has alternatives that do not bind `$METHOD`, put the regex-free alternatives in their own group.
- **Call sources taint their arguments unless `exact: true`.** `pattern: $C.messages.create(...)` as a source made `system="static"` inside the same call count as tainted. Use `exact: true` on every call-based source.
- **`metavariable-pattern` searches inside the bound expression.** `pattern-not: "[...]"` under `metavariable-pattern` did not exclude a list argument, because a sub-expression of the list matched `$ANY`. Use a text regex on the metavariable instead (`regex: (?s)^[^\[(].*$`).
- **`metavariable-regex` does not see call expressions in some positions.** Constraining `$MW` in `$APP.use(..., $MW, ...)` worked for identifiers but not for `requireBearerAuth(...)`. `metavariable-pattern` with `pattern-regex` works for both.
- **`pattern-not-inside` accepts nested `patterns`.** That is how the MCP transport rule excludes routes with auth middleware.
- **A JSX attribute pattern needs the element.** `dangerouslySetInnerHTML={{__html: $X}}` fails to parse; `{ __html: $X }` matches the object in JSX and in `createElement` props.
- **Attribute assignment on an object breaks `...` flow for `pattern-not-inside`.** `mcp.settings.host = "..."` between `FastMCP(...)` and `mcp.run()` makes the auth exclusion miss. Documented inside the rule.
- **YAML quoting.** Patterns that contain `{ key: value }`, `"..." + $X` or `? :` must be quoted, or ruamel reports "mapping values are not allowed in this context".
- **`semgrep --test` reports findings only on annotated lines.** A rule can fire on an unannotated line of any fixture and the suite still passes. `scripts/check_fixtures.py` scans the whole tree with the whole pack and fails on that.
- **Semgrep's default ignore list skips `tests/`.** Scanning fixtures directly needs a project-level `.semgrepignore`; `check_fixtures.py` copies the tree to a temporary directory for that reason.
- **Findings are reported at the focused expression.** Put the `ruleid` comment on the line above the focused argument, not above the start of a multi-line call.

## 6. Precision bar

Before opening a pull request, run the rule against real code (`make smoke SMOKE_PATHS=path`). The bar is: no finding on code a reviewer would call fine. Examples that must stay clean, taken from the fixtures:

- `subprocess.run(["git", "log", "--", name])` with a model-chosen `name`.
- `requests.get("https://api.example.com/search", params={"q": model_output})`.
- `{"role": "user", "content": user_text}`; only the system and developer roles are sinks.
- `print(os.getenv("MODEL_NAME"))`; only names that look like keys, tokens or secrets are sources.
- `torch.load(path, weights_only=True)`, `yaml.safe_load(...)`, `from_pretrained("org/model")`.

## 7. Metadata reference

| Field | Values |
|---|---|
| `category` | `security` |
| `subcategory` | `[vuln]` for an exploitable flow, `[audit]` for a configuration that needs human judgement |
| `cwe` | list of `CWE-<id>: <name>` |
| `owasp` | list of `LLM<nn>:2025 <name>` from the OWASP Top 10 for LLM Applications 2025 |
| `confidence` | HIGH when the pattern is unambiguous, MEDIUM when context can make it safe, LOW when it is a heuristic |
| `likelihood`, `impact` | HIGH, MEDIUM or LOW |
| `technology` | libraries and runtimes the rule understands |
| `references` | real https URLs: the OWASP entry, the CWE page, the library's own security docs |
| `pack.family` | `llm-output-to-sink`, `prompt-injection`, `excessive-agency`, `mcp-exposure`, `secrets`, `model-supply-chain` |

OWASP ids used: LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage.
