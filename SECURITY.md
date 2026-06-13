# Security Policy

## Reporting A Vulnerability

Do not open a public GitHub issue for security reports.

Send private reports to:

```text
root@haltman.io
```

Use a clear subject such as:

```text
[AGMH SECURITY] short issue summary
```

Include enough detail for maintainers to reproduce and assess the issue:

- Affected AGMH version or commit.
- Operating system, Python version, and install method.
- Minimal configuration needed to reproduce, with secrets removed.
- Exact commands used.
- Expected behavior.
- Actual behavior.
- Logs or stack traces with tokens, webhook URLs, private repository names, and
  other secrets redacted.
- Impact and risk: what an attacker can do, what data can be exposed or
  modified, and what privileges are required.
- Suggested mitigation or patch direction, if you have one.

## Response Expectations

Security reports are triaged privately. The project may ask for more details,
prepare a fix, and publish a public advisory or changelog entry after a patch is
available.

## Public Disclosure

Please do not disclose the vulnerability publicly until maintainers have had a
reasonable chance to validate and fix it.

## Scope

Security-sensitive areas include:

- Token handling and secret redaction.
- Clone and push URL construction.
- Webhook notification payloads.
- Config parsing.
- State files and logs under `.agmh/`.
- Git command execution and SSH configuration.

