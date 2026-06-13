# Discover GitHub Organization as a Member: extencil and haltman-io

## Scenario

The GitHub user `extencil` is a member of the `haltman-io` organization and wants to run `discover` for that organization.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token or config file exists yet.

## Minimum Assumptions

1. Organization membership may reveal repositories not visible to visitors.
2. Use a GitHub token.
3. No destination is required.
4. No config file is required.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Authenticates as `extencil` for member-level GitHub discovery. |

## Algorithm

1. Create a GitHub token for `extencil`.
2. Export it as `GITHUB_TOKEN`.
3. Run `discover` against `haltman-io`.
4. Save JSON output if you want an audit artifact.

## Commands

```bash
export GITHUB_TOKEN="paste_extencil_github_token_here"

agmh discover \
  --source https://github.com/haltman-io/ \
  --github-token env:GITHUB_TOKEN \
  --output haltman-io-discovery.json
```

## Expected Result

AGMH writes a JSON file with repositories visible to `extencil` through GitHub API access. It does not clone or push anything.

