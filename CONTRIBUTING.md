# Contributing

Thank you for helping make agent code safer. This document is the rule authoring standard and the pull request checklist. Everything here is enforced by `make test` and `make validate`, which CI runs on every pull request.

## Ground rules

- Precision beats coverage. A rule that is noisy on real code will be narrowed or removed, even if it catches more. If you cannot make a pattern precise, document the limitation in a comment inside the rule and keep the confidence at MEDIUM or LOW.
- One problem per rule. Separate rules for separate CWEs, even when the sinks look similar, so SARIF consumers and triage queues can treat them differently.
- Every rule is tested. No rule lands without a fixture that has at least two `ruleid` lines and at least two `ok` lines that look like the mitigated code a developer would actually write.
- Messages explain the fix. Write the message for the developer who sees it in a pull request annotation: what flows where, why it matters in an agent, and what to do instead.

## Layout

```text
rules/<language>/<category>/<rule-id>.yaml
tests/<language>/<category>/<rule-id>.<py|ts|tsx|js>
```

`<language>` is `python` or `javascript` (the latter covers TypeScript too). Categories in use: `code-execution`, `injection`, `prompt-injection`, `permissions`, `mcp`, `secrets`, `deserialization`. Add a category only if none of these fits.

Rule ids are kebab-case and equal to the file name. A Python and a JavaScript rule may share an id when they detect the same problem; Semgrep prefixes ids with the path so they stay distinct, and the single-file bundle (`scripts/bundle.py`) prefixes them with `<language>.<category>.` for the same reason.

A rule may have several fixtures: `<rule-id>.ts` and `<rule-id>.js`, or `<rule-id>-<variant>.py` for a scenario that needs its own file (for example "auth configured at module level").

## Rule anatomy

```yaml
rules:
  - id: llm-output-to-example
    languages: [python]
    severity: ERROR            # ERROR: exploitable with high confidence. WARNING: needs context. INFO: hygiene.
    message: >-
      What flows into what, why it matters for an agent, and how to fix it.
    mode: taint                # taint for data-flow rules; omit for pattern rules
    pattern-sources: [...]
    pattern-sanitizers: [...]
    pattern-sinks: [...]
    metadata:
      category: security
      subcategory: [vuln]      # vuln | audit
      cwe:
        - "CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')"
      owasp:
        - "LLM05:2025 Improper Output Handling"
      confidence: HIGH         # HIGH | MEDIUM | LOW
      likelihood: HIGH
      impact: HIGH
      technology: [python, openai, langchain, agent]
      references:
        - https://cwe.mitre.org/data/definitions/78.html
      hisar:
        pack: agentic-semgrep-rules
        family: llm-output-to-sink
```

`scripts/check_metadata.py` enforces the required fields, the CWE and OWASP formats, the id and file-name match, and the language declaration per directory.

### Sources

Model output sources are shared across the `llm-output-to-*` rules. If you add a provider or framework, add it to every rule in the family in both languages, and add a fixture line for it in at least one rule per language. Tool-parameter sources are shared across the `*-tool-param-to-*` rules in the same way.

Keep call-based sources `exact: true`. Without it Semgrep treats every sub-expression of the matched call as tainted, including the arguments you passed in, which produced false positives on `messages.create(system=...)` during development.

### Sinks

Use `focus-metavariable` to point at the exact argument that must be tainted. Group sink alternatives so that any `metavariable-regex` in the group always has its metavariable bound; an unbound metavariable makes the whole group fail silently.

### Sanitizers

Add the sanitizers a careful developer would use (allowlist checks, `shlex.quote`, `path.basename`, `int()`, `DOMPurify.sanitize`), and add an `ok` fixture line for each one. Do not add broad sanitizers such as `str()` or `.strip()`.

## Pull request checklist

- [ ] Rule file at `rules/<language>/<category>/<rule-id>.yaml`, id equals file name, kebab-case.
- [ ] Fixture at `tests/<language>/<category>/<rule-id>.<ext>` with `ruleid` and `ok` annotations, including the mitigated form from the message.
- [ ] `make test` passes: `semgrep --test` reports all tests passed and `scripts/check_fixtures.py` reports zero findings on unannotated lines.
- [ ] `make validate` passes.
- [ ] The rule was run against at least one real codebase (`make smoke SMOKE_PATHS=path/to/code`) and any findings are documented in the PR as true or false positives. False positives were fixed before opening the PR.
- [ ] Message says what, why and how to fix. No jargon without explanation.
- [ ] Metadata complete: correct CWE ids, OWASP LLM Top 10 2025 ids, confidence, likelihood, impact, technology, real reference URLs.
- [ ] README table regenerated if a rule was added, renamed or removed (`python3 scripts/check_metadata.py rules` lists the rules; the table lives in README.md).
- [ ] `python3 scripts/bundle.py` was run and the regenerated `agentic-semgrep-rules.yaml` is committed (CI checks it).
- [ ] CHANGELOG.md updated under Unreleased.
- [ ] No em-dashes, no model names or product identifiers in prose. Library and SDK names that a rule detects are fine.

## Reporting false positives

Open an issue with the rule id, the code snippet (redacted if needed), and what makes it safe. Narrowing the rule, adding a sanitizer, or adding a negative fixture are all welcome pull requests.

## Licence

By contributing you agree that your contribution is licensed under the MIT licence of this repository.
