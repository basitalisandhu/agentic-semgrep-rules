# Publishing to the Semgrep Registry

Checked on 2026-10-16 against the Semgrep documentation and the `semgrep/semgrep-rules` repository. There are two routes; neither can be done from CI without the owner signing in.

## Route 1: publish from your own account (keeps the MIT licence)

Needs a free semgrep.dev account. The rules stay in this repository under MIT.

```sh
pip install semgrep==1.181.0
semgrep login                      # opens a browser; sign in as the owner
git clone https://github.com/basitalisandhu/agentic-semgrep-rules
cd agentic-semgrep-rules
semgrep publish --visibility=unlisted rules/
```

`unlisted` rules can be used by anyone who has the link but are hidden from Registry search. Semgrep uploads the test fixtures next to each rule. `org_private` limits them to your semgrep.dev organisation. The CLI has no self-serve "public" visibility; a public Registry entry or a `p/` pack is curated by Semgrep, so ask in the Semgrep community Slack after publishing unlisted.

## Route 2: contribute rules to `semgrep/semgrep-rules`

This puts rules in the public Registry, but that repository is under the **Semgrep Rules License v1.0**, not MIT, and contributors must sign Semgrep's CLA. Decide that first.

What each rule would need, from the contributing guide and the `semgrep-rule-lints` CI job:

1. One rule per file, with a test file of the same name and the language's extension, at least one `ruleid:` and one `ok:` line. This pack already does this (enforced by `scripts/check_metadata.py`).
2. Path `<language>/<framework>/security/<rule>.yaml`, for example `python/fastmcp/security/fastmcp-bind-all-interfaces.yaml` or `python/lang/security/llm-output-to-exec-eval.yaml`.
3. Metadata: `technology`, `category`, `references`, `cwe`, `owasp`, `confidence`, `subcategory`, `likelihood`, `impact` (all present here), plus `vulnerability_class` (missing here).
4. `owasp` in Registry rules uses the OWASP Top 10 web ids (for example `A03:2021 - Injection`). This pack uses OWASP LLM Top 10 ids; add the matching web id next to them.
5. Open one pull request per rule family, sign the CLA, pass CI and get one maintainer approval.

## Recommendation

Route 1 first: it takes minutes, keeps the licence, and gives a stable `semgrep --config r/...` reference to put in the README. Route 2 only if the wider reach is worth relicensing the contributed copies.
