# Local Mirror GitHub Organization as a Member: extencil and haltman-io

## Scenario

The GitHub user `extencil` is a member of the GitHub organization `haltman-io` and wants to create local bare mirrors.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token or config file exists yet.

## Minimum Assumptions

1. Membership-level access may matter.
2. A GitHub source token is required.
3. No destination is requested.
4. Use `local-mirror`, not `download`, because the goal is a bare mirror.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Lets AGMH see repositories available to `extencil` as a `haltman-io` member. |

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Create a GitHub token for `extencil` with access to repositories in `haltman-io`.
2. Export the token as `GITHUB_TOKEN`.
3. Run `agmh local-mirror` with the organization URL.
4. Inspect the bare mirrors under `backups/github/haltman-io/*.git`.
5. Keep `.agmh/state.json` if you plan to run `remote-mirror` later.

## Commands

```bash
export GITHUB_TOKEN="paste_extencil_github_token_here"

agmh local-mirror \
  --source https://github.com/haltman-io/ \
  --github-token env:GITHUB_TOKEN \
  --local-dir backups \
  --verbose
```

## Expected Result

AGMH creates bare Git mirrors like:

```text
backups/github/haltman-io/example-repo.git/
.agmh/state.json
.agmh/logs/
```

These paths are mirrors, not normal source directories. They are intended for mirroring workflows and remote pushes.

