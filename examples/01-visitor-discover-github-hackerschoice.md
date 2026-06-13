# Visitor Discover GitHub Organization: hackerschoice

## Scenario

A visitor wants to run `discover` for the public GitHub organization profile `hackerschoice`.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No tokens, destinations, webhooks, or config files exist yet.

## Minimum Assumptions

1. The visitor is unauthenticated.
2. Only public GitHub repositories are in scope.
3. No destination is required.
4. No config file is required.

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Treat the user as a visitor.
2. Do not create a GitHub token.
3. Run `discover` against the GitHub organization URL.
4. Read the repository list printed to stdout.
5. If GitHub rate limits anonymous requests, repeat later or use a GitHub token.

## Commands

```bash
agmh discover \
  --source https://github.com/hackerschoice/
```

Optional JSON output:

```bash
agmh discover \
  --source https://github.com/hackerschoice/ \
  --output hackerschoice-discovery.json
```

## Expected Result

AGMH prints public repositories visible to unauthenticated GitHub API access. No clone, download, mirror, destination repository, or notification is created.

