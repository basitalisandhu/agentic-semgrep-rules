# Security policy

## Scope

This repository contains static analysis rules, test fixtures and a GitHub composite action. It does not run in production and holds no secrets. Security-relevant problems here are:

- A rule that misses a pattern it claims to detect (false negative) or reports safe code (false positive) in a way that could mislead a security review.
- The composite action or workflows executing untrusted input, leaking tokens, or escalating permissions.
- Fixtures that contain real credentials. Fixtures must only contain synthetic keys that match the detection regexes.

## Reporting

Please report vulnerabilities privately through GitHub's private vulnerability reporting on this repository (Security tab, "Report a vulnerability"). If that is not available, open an issue titled "Security contact request" without details and a maintainer will reply with a private channel.

You can expect an acknowledgement within 72 hours and a fix or a public statement within 14 days for confirmed issues. Credit is given in the release notes unless you prefer otherwise.

## Supported versions

Only the latest tagged release and the `main` branch receive fixes.

## Safe use of this pack

- Pin the action and the Semgrep version in CI (`basitalisandhu/agentic-semgrep-rules@v1.0.0`, `semgrep-version: 1.179.0`) rather than tracking `main` if you need reproducible scans.
- The action needs `security-events: write` only when `upload-sarif` is true. Use `contents: read` otherwise.
- Findings are advice, not proof. A clean scan does not mean an agent is safe; see the sibling projects in the README for runtime controls.
