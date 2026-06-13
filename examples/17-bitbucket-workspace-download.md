# Download a Bitbucket Workspace

## Scenario

A Bitbucket user wants to download repositories from a Bitbucket workspace.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No Bitbucket token or config file exists yet.

## Minimum Assumptions

1. The workspace may require authentication.
2. Use a Bitbucket API token.
3. No destination is required.
4. Use `download` for directly visible source files.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `BITBUCKET_TOKEN` | Yes | Reads repositories from the Bitbucket workspace. |

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Create a Bitbucket API token for the Bitbucket user.
2. Export it as `BITBUCKET_TOKEN`.
3. Run `download` with `--source-token`.
4. Inspect working trees under `backups/bitbucket/`.

## Commands

```bash
export BITBUCKET_TOKEN="paste_bitbucket_api_token_here"

agmh download \
  --source https://bitbucket.org/example-workspace/ \
  --source-token bitbucket:you@example.com:env:BITBUCKET_TOKEN \
  --local-dir backups \
  --verbose
```

## Expected Result

AGMH downloads repositories visible to the Bitbucket credential as working trees.

