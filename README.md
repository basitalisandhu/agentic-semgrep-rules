# agentic-semgrep-rules: Semgrep rules for AI agent code

Semgrep rules for AI agent code: static analysis for LLM applications in Python, TypeScript and JavaScript that finds model output flowing into `exec`, shells, SQL, URLs, file paths and HTML (eval of model output, SSRF through tool URLs), user input written into system prompts, tools that let the model run anything, MCP server security checks (HTTP transports without authentication, servers bound to every interface), leaked provider keys, and unsafe model or config loading. For teams that ship LLM agents, MCP servers and tool-using assistants and want these mistakes caught in a pull request rather than found in an incident.

36 rules (23 Python, 13 TypeScript/JavaScript), every one with a tested fixture, CWE and OWASP LLM Top 10 (2025) mapping, and a message that says what is wrong and how to fix it.

```sh
pip install semgrep
semgrep --config https://raw.githubusercontent.com/basitalisandhu/agentic-semgrep-rules/main/agentic-semgrep-rules.yaml .
```

## When to use this

- **How do I catch eval of model output, or model output reaching a shell, in CI?** The `llm-output-to-*` rules track text returned by the OpenAI, Anthropic, LiteLLM, Ollama, Google GenAI, Vercel AI and LangChain calls into `exec`, `eval`, `subprocess`, `child_process` and the other sinks in the tables below.
- **How do I find MCP servers exposed without auth?** `fastmcp-http-transport-without-auth`, `mcp-http-transport-without-auth` and `fastmcp-bind-all-interfaces` report HTTP transports with no token verifier and servers listening on every interface.
- **Which Semgrep rules cover LangChain, the OpenAI Agents SDK, pydantic-ai, Semantic Kernel, FastMCP or the MCP TypeScript SDK?** The `permissions` rules know those frameworks' tool decorators and the `deserialization` rules know LangChain's dangerous flags; the tables name each rule and the paragraph after them lists the recognised sources.
- **How do I stop an agent tool from turning into SSRF or path traversal?** `llm-output-to-fetch`, `llm-output-to-http-request` and the `*-tool-param-to-file-path` rules report URLs and paths that the model chose.
- **How do I get agent security findings into GitHub code scanning?** The composite action below runs the pack and uploads SARIF.

## Why

Static analysers know that `eval(user_input)` is bad. They do not know that `response.choices[0].message.content` is attacker-controlled the moment the model has read a web page, a PDF or a tool result, or that a function decorated with `@mcp.tool()` receives arguments the model (and therefore a prompt injection) chose. This pack teaches Semgrep those sources and the agent-specific sinks and misconfigurations around them, with precision as the first design goal: a rule that is noisy on real code gets narrowed or removed.

## What it finds

**Model output reaches code or shell execution**

| Rule | Language | Severity | CWE | OWASP LLM Top 10 (2025) | Confidence |
|---|---|---|---|---|---|
| [`llm-output-to-child-process`](rules/javascript/code-execution/llm-output-to-child-process.yaml) | JS/TS | ERROR | CWE-78 | LLM05, LLM06 | HIGH |
| [`llm-output-to-eval-function`](rules/javascript/code-execution/llm-output-to-eval-function.yaml) | JS/TS | ERROR | CWE-95, CWE-94 | LLM05, LLM06 | HIGH |
| [`llm-output-to-exec-eval`](rules/python/code-execution/llm-output-to-exec-eval.yaml) | Python | ERROR | CWE-95, CWE-94 | LLM05, LLM06 | HIGH |
| [`llm-output-to-os-system`](rules/python/code-execution/llm-output-to-os-system.yaml) | Python | ERROR | CWE-78 | LLM05, LLM06 | HIGH |
| [`llm-output-to-subprocess`](rules/python/code-execution/llm-output-to-subprocess.yaml) | Python | ERROR | CWE-78 | LLM05, LLM06 | HIGH |

**Model output reaches injection sinks**

| Rule | Language | Severity | CWE | OWASP LLM Top 10 (2025) | Confidence |
|---|---|---|---|---|---|
| [`llm-output-to-fetch`](rules/javascript/injection/llm-output-to-fetch.yaml) | JS/TS | WARNING | CWE-918 | LLM05, LLM06 | MEDIUM |
| [`llm-output-to-file-path`](rules/javascript/injection/llm-output-to-file-path.yaml) | JS/TS | WARNING | CWE-22 | LLM05, LLM06 | MEDIUM |
| [`llm-output-to-innerhtml`](rules/javascript/injection/llm-output-to-innerhtml.yaml) | JS/TS | WARNING | CWE-79 | LLM05 | MEDIUM |
| [`llm-output-to-sql`](rules/javascript/injection/llm-output-to-sql.yaml) | JS/TS | ERROR | CWE-89 | LLM05, LLM06 | HIGH |
| [`llm-output-to-file-path`](rules/python/injection/llm-output-to-file-path.yaml) | Python | WARNING | CWE-22 | LLM05, LLM06 | MEDIUM |
| [`llm-output-to-html`](rules/python/injection/llm-output-to-html.yaml) | Python | WARNING | CWE-79 | LLM05 | MEDIUM |
| [`llm-output-to-http-request`](rules/python/injection/llm-output-to-http-request.yaml) | Python | WARNING | CWE-918 | LLM05, LLM06 | MEDIUM |
| [`llm-output-to-sql`](rules/python/injection/llm-output-to-sql.yaml) | Python | ERROR | CWE-89 | LLM05, LLM06 | HIGH |

**Prompt injection**

| Rule | Language | Severity | CWE | OWASP LLM Top 10 (2025) | Confidence |
|---|---|---|---|---|---|
| [`user-input-in-system-prompt`](rules/javascript/prompt-injection/user-input-in-system-prompt.yaml) | JS/TS | WARNING | CWE-1427, CWE-74 | LLM01, LLM07 | MEDIUM |
| [`user-input-in-system-prompt`](rules/python/prompt-injection/user-input-in-system-prompt.yaml) | Python | WARNING | CWE-1427, CWE-74 | LLM01, LLM07 | MEDIUM |

**Over-broad tools and permissions**

| Rule | Language | Severity | CWE | OWASP LLM Top 10 (2025) | Confidence |
|---|---|---|---|---|---|
| [`mcp-tool-param-to-file-path`](rules/javascript/permissions/mcp-tool-param-to-file-path.yaml) | JS/TS | WARNING | CWE-22 | LLM06, LLM05 | MEDIUM |
| [`mcp-tool-param-to-shell`](rules/javascript/permissions/mcp-tool-param-to-shell.yaml) | JS/TS | ERROR | CWE-78 | LLM06, LLM05 | HIGH |
| [`agent-tool-param-to-file-path`](rules/python/permissions/agent-tool-param-to-file-path.yaml) | Python | WARNING | CWE-22 | LLM06, LLM05 | MEDIUM |
| [`agent-tool-param-to-shell`](rules/python/permissions/agent-tool-param-to-shell.yaml) | Python | ERROR | CWE-78 | LLM06, LLM05 | HIGH |
| [`langchain-allow-dangerous-code`](rules/python/permissions/langchain-allow-dangerous-code.yaml) | Python | WARNING | CWE-94 | LLM06 | HIGH |
| [`langchain-allow-dangerous-requests`](rules/python/permissions/langchain-allow-dangerous-requests.yaml) | Python | WARNING | CWE-918 | LLM06 | HIGH |
| [`langchain-dangerous-tools`](rules/python/permissions/langchain-dangerous-tools.yaml) | Python | WARNING | CWE-250, CWE-94 | LLM06, LLM05 | HIGH |

**Exposed MCP servers**

| Rule | Language | Severity | CWE | OWASP LLM Top 10 (2025) | Confidence |
|---|---|---|---|---|---|
| [`mcp-http-transport-without-auth`](rules/javascript/mcp/mcp-http-transport-without-auth.yaml) | JS/TS | WARNING | CWE-306 | LLM06 | MEDIUM |
| [`fastmcp-bind-all-interfaces`](rules/python/mcp/fastmcp-bind-all-interfaces.yaml) | Python | WARNING | CWE-1327 | LLM06 | HIGH |
| [`fastmcp-http-transport-without-auth`](rules/python/mcp/fastmcp-http-transport-without-auth.yaml) | Python | WARNING | CWE-306 | LLM06 | MEDIUM |

**Secrets**

| Rule | Language | Severity | CWE | OWASP LLM Top 10 (2025) | Confidence |
|---|---|---|---|---|---|
| [`api-key-in-command-line-arg`](rules/javascript/secrets/api-key-in-command-line-arg.yaml) | JS/TS | WARNING | CWE-214 | LLM02 | MEDIUM |
| [`hardcoded-llm-api-key`](rules/javascript/secrets/hardcoded-llm-api-key.yaml) | JS/TS | ERROR | CWE-798 | LLM02 | HIGH |
| [`llm-api-key-logged`](rules/javascript/secrets/llm-api-key-logged.yaml) | JS/TS | WARNING | CWE-532 | LLM02 | MEDIUM |
| [`api-key-in-command-line-arg`](rules/python/secrets/api-key-in-command-line-arg.yaml) | Python | WARNING | CWE-214 | LLM02 | MEDIUM |
| [`hardcoded-llm-api-key`](rules/python/secrets/hardcoded-llm-api-key.yaml) | Python | ERROR | CWE-798 | LLM02 | HIGH |
| [`llm-api-key-logged`](rules/python/secrets/llm-api-key-logged.yaml) | Python | WARNING | CWE-532 | LLM02 | MEDIUM |

**Unsafe model and config loading**

| Rule | Language | Severity | CWE | OWASP LLM Top 10 (2025) | Confidence |
|---|---|---|---|---|---|
| [`langchain-allow-dangerous-deserialization`](rules/python/deserialization/langchain-allow-dangerous-deserialization.yaml) | Python | WARNING | CWE-502 | LLM03 | HIGH |
| [`pickle-load-model-file`](rules/python/deserialization/pickle-load-model-file.yaml) | Python | WARNING | CWE-502 | LLM03, LLM04 | MEDIUM |
| [`torch-load-without-weights-only`](rules/python/deserialization/torch-load-without-weights-only.yaml) | Python | WARNING | CWE-502 | LLM03, LLM04 | MEDIUM |
| [`transformers-trust-remote-code`](rules/python/deserialization/transformers-trust-remote-code.yaml) | Python | WARNING | CWE-829, CWE-94 | LLM03 | HIGH |
| [`yaml-unsafe-load`](rules/python/deserialization/yaml-unsafe-load.yaml) | Python | WARNING | CWE-502 | LLM03 | HIGH |

Rule ids are shared between the Python and JavaScript directories when they detect the same problem; Semgrep prefixes ids with their path (`rules.python.injection.llm-output-to-sql`), so they stay distinct in output and SARIF. The single-file bundle [`agentic-semgrep-rules.yaml`](agentic-semgrep-rules.yaml) prefixes each id with its language and category (`python.injection.llm-output-to-sql`) for the same reason; `python3 scripts/bundle.py` regenerates it and CI fails when it is stale.

Sources recognised by the `llm-output-to-*` rules: the OpenAI (`chat.completions.create`, `responses.create`), Anthropic (`messages.create`), LiteLLM, Ollama and Google GenAI SDK calls, the Vercel AI SDK (`generateText`, `streamText`, `generateObject`), LangChain and LangGraph `invoke`/`run`/`predict`/`stream` on objects named like chains, agents, models or graphs, and response shapes that only model SDKs produce (`.choices[0].message.content`, `.output_text`, `.content[0].text`). Tool-parameter rules recognise FastMCP and the official MCP SDKs, LangChain `@tool` and `DynamicStructuredTool`, OpenAI Agents `@function_tool`, pydantic-ai `@agent.tool_plain`, Semantic Kernel `@kernel_function` and Vercel AI `tool()`.

## Install and run

Semgrep 1.179 or later.

```sh
pip install semgrep

# the single-file bundle, straight from GitHub (Semgrep accepts a URL only for a single file)
semgrep --config https://raw.githubusercontent.com/basitalisandhu/agentic-semgrep-rules/main/agentic-semgrep-rules.yaml .

# or the rules directory from a clone
git clone https://github.com/basitalisandhu/agentic-semgrep-rules
semgrep --config agentic-semgrep-rules/rules .
```

Semgrep registry publication (`semgrep --config p/agentic-semgrep-rules`) is pending; until then use the bundle URL or a clone. Each release also attaches the bundle and a tarball of the `rules` directory to vendor.

### CI (any provider)

```sh
pip install semgrep==1.179.0
semgrep --config https://raw.githubusercontent.com/basitalisandhu/agentic-semgrep-rules/main/agentic-semgrep-rules.yaml \
  --metrics=off --error --severity ERROR .
```

`--error` makes the command exit non-zero when there are findings; drop `--severity ERROR` to also fail on WARNING-level rules.

### GitHub Action

```yaml
name: agent-security
on: [push, pull_request]
permissions:
  contents: read
  security-events: write
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: basitalisandhu/agentic-semgrep-rules@v1   # or pin a release tag such as v1.0.0
        with:
          severity: ERROR        # fail the job at this level or above (INFO, WARNING, ERROR)
          upload-sarif: "true"   # publish all findings to the Security tab
```

Inputs: `config` (default: the bundled `rules` directory; a path, URL or registry reference), `paths` (default `.`), `severity`, `upload-sarif`, `sarif-file`, `semgrep-version`, `extra-args`. The action installs Semgrep, writes `results.sarif`, uploads it with `github/codeql-action/upload-sarif@v3` and fails the job when findings at or above the threshold exist.

### pre-commit

The hook runs the bundled rules on staged Python, TypeScript and JavaScript files. It needs `semgrep` on your PATH (`pip install semgrep`).

```yaml
repos:
  - repo: https://github.com/basitalisandhu/agentic-semgrep-rules
    rev: v1.0.0
    hooks:
      - id: agentic-semgrep-rules
```

If you already run Semgrep's own hook, point it at the bundle instead:

```yaml
repos:
  - repo: https://github.com/semgrep/pre-commit
    rev: v1.179.0
    hooks:
      - id: semgrep
        args: ["--config", "https://raw.githubusercontent.com/basitalisandhu/agentic-semgrep-rules/main/agentic-semgrep-rules.yaml", "--error", "--metrics=off"]
```

## Example

```python
@mcp.tool()
def run_command(command: str) -> str:
    """Run any shell command."""
    return subprocess.run(command, shell=True, capture_output=True, text=True).stdout
```

```text
rules.python.permissions.agent-tool-param-to-shell
  Tool parameter 'command' is filled in by the model and reaches 'subprocess.run' as a shell
  command or executable. This is an "execute anything" tool: a prompt injection anywhere in the
  agent's context becomes OS command injection on the host running the tool. Replace the free-form
  command with a fixed executable and typed arguments, validate each argument against an allowlist,
  never use shell=True, run with least privilege and a timeout, and require human approval for
  anything with side effects.
```

## Writing a rule

Every rule lives at `rules/<language>/<category>/<rule-id>.yaml` with a fixture at `tests/<language>/<category>/<rule-id>.<ext>` that marks true positives with `# ruleid: <rule-id>` (or `// ruleid:`) on the line above and negative cases with `# ok: <rule-id>`. Rules need `metadata` with `category`, `subcategory`, `cwe`, `owasp`, `confidence`, `likelihood`, `impact`, `technology` and `references`, and a message that names the problem and the fix. Then:

```sh
make test       # semgrep --test on the fixtures, plus an audit for findings on unannotated lines
make validate   # rule syntax and metadata lint, and a check that the single-file bundle is current
make bundle     # regenerate agentic-semgrep-rules.yaml after changing a rule
make smoke      # scan the fixtures and report per-rule counts (add SMOKE_PATHS=... for your own code)
```

[docs/rule-writing.md](docs/rule-writing.md) explains the source and sink conventions, the Semgrep behaviours that bit us while building this pack (anchored `metavariable-regex`, `exact: true` on call sources, YAML quoting of object patterns) and the precision bar a rule has to clear. [CONTRIBUTING.md](CONTRIBUTING.md) has the PR checklist.

## Precision

Every rule ships with positive and negative fixtures and the suite fails on any finding outside an annotated line. The pack was also run against a real Python codebase by the same author ([agent-threat-model](https://github.com/basitalisandhu/agent-threat-model), 21 files) with zero findings; see [docs/smoke-test.md](docs/smoke-test.md). If a rule is noisy on your code, open an issue with the snippet: narrowing a rule is preferred over keeping a noisy one.

## Frequently asked questions

**Are there Semgrep rules for LLM applications and AI agents?**
Yes. This pack has 36 rules, 23 for Python and 13 for TypeScript and JavaScript, each with a tested fixture, a CWE, an OWASP LLM Top 10 (2025) mapping and a message that names the fix. They cover model output reaching `exec`, shells, SQL, HTTP requests, file paths and HTML; user input written into system prompts; tool parameters that reach a shell or a file path; LangChain dangerous-code and dangerous-requests flags; MCP servers without authentication or bound to all interfaces; hard-coded or logged provider keys; and unsafe model and config loading. Run it with `semgrep --config https://raw.githubusercontent.com/basitalisandhu/agentic-semgrep-rules/main/agentic-semgrep-rules.yaml .`

**How do I catch eval of model output or unbounded tool permissions in CI?**
Pin Semgrep and run the bundle with `--error`: `semgrep --config https://raw.githubusercontent.com/basitalisandhu/agentic-semgrep-rules/main/agentic-semgrep-rules.yaml --metrics=off --error --severity ERROR .` exits non-zero when an ERROR-level rule fires (drop `--severity ERROR` to fail on warnings too). On GitHub, use the action `basitalisandhu/agentic-semgrep-rules@v1`, which installs Semgrep, writes `results.sarif`, uploads it to code scanning and fails the job at the severity you choose. A pre-commit hook for staged files is in the "Install and run" section above.

**Which frameworks and SDKs do the rules understand?**
Sources: the OpenAI (`chat.completions.create`, `responses.create`), Anthropic (`messages.create`), LiteLLM, Ollama and Google GenAI SDK calls, the Vercel AI SDK (`generateText`, `streamText`, `generateObject`), LangChain and LangGraph `invoke`, `run`, `predict` and `stream` on chains, agents, models and graphs, and the response shapes only model SDKs produce (`.choices[0].message.content`, `.output_text`, `.content[0].text`). Tool-parameter rules recognise FastMCP and the official MCP SDKs, LangChain `@tool` and `DynamicStructuredTool`, OpenAI Agents `@function_tool`, pydantic-ai `@agent.tool_plain`, Semantic Kernel `@kernel_function` and Vercel AI `tool()`. Go and Java are on the roadmap.

**How noisy are the rules on real code?**
Precision is the first design goal. Every rule ships with positive and negative fixtures, the suite fails on any finding outside an annotated line, and the pack was run against a real Python codebase by the same author ([agent-threat-model](https://github.com/basitalisandhu/agent-threat-model), 21 files) with zero findings ([docs/smoke-test.md](docs/smoke-test.md)). If a rule fires on your code wrongly, open an issue with the snippet: narrowing a rule is preferred over keeping a noisy one.

**Can I use the rules commercially and contribute my own?**
Yes to both. The pack is MIT licensed, so it can be run in commercial CI and vendored into internal rule sets. A contribution is one rule at `rules/<language>/<category>/<rule-id>.yaml` with the required `metadata` block (`category`, `subcategory`, `cwe`, `owasp`, `confidence`, `likelihood`, `impact`, `technology`, `references`) and a fixture at `tests/<language>/<category>/` that marks true positives with `ruleid:` and negatives with `ok:`; `make test`, `make validate` and `make bundle` must pass. [docs/rule-writing.md](docs/rule-writing.md) explains the conventions and the Semgrep behaviours to watch for.

## Roadmap

- Semgrep registry publication (`p/agentic-semgrep-rules`) and an `awesome-semgrep` listing.
- Go and Java coverage for the `llm-output-to-*` family.
- Rules for agent memory and RAG stores (unsanitised retrieval text in prompts, pickle-backed vector stores).
- Secrets in agent configuration files (`.mcp.json`, desktop-client MCP config files, `.env` committed next to agent code) via the generic language.
- Autofix suggestions (`fix:`) for the flag-based rules.
- Cross-file (interprocedural) variants when Semgrep's open-source engine supports them.

## Related projects

More tools by the same author: https://github.com/basitalisandhu

- [ai-agent-incidents](https://github.com/basitalisandhu/ai-agent-incidents): open, structured dataset of publicly documented AI agent security incidents, mapped to OWASP and MITRE ATLAS, with a [browsable site](https://basitalisandhu.github.io/ai-agent-incidents/).
- [agent-threat-model](https://github.com/basitalisandhu/agent-threat-model): CLI that turns a YAML description of an agent system into a STRIDE + OWASP Agentic threat model, control checklist and Mermaid diagram.
- [agent-security-skills](https://github.com/basitalisandhu/agent-security-skills): Claude Code plugin and agentskills-compatible skill pack for agent security reviews: threat modelling, config audits, policy generation, incident lookup.

## Licence

MIT, see [LICENSE](LICENSE). Copyright 2026 Muhammad Basit Ali.
