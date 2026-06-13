# Two-Step Local Mirror then Remote Mirror

## Scenario

A user wants to create local bare mirrors now and push them to GitLab later.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No tokens or config file exists yet.

## Minimum Assumptions

1. The source is GitHub.
2. The destination is GitLab.
3. The first step must not contact the destination.
4. The second step must reuse `.agmh/state.json` and local bare mirrors.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads the source repositories. |
| `GITLAB_TOKEN` | Yes, but only for step two | Creates and pushes GitLab repositories. |

## Minimal Configuration

Create the config before step two:

```bash
agmh init-config --path agmh.config.toml
```

Replace it with:

```toml
mode = "remote"

[backup]
local_dir = "backups"
push_mode = "portable-mirror"

[[destinations]]
url = "https://gitlab.com/example-mirror"
platform = "gitlab"
tokens = [{ env = "GITLAB_TOKEN", name = "gitlab-destination" }]
visibility = "private"
push_mode = "portable-mirror"
```

## Algorithm

1. Create and export the GitHub source token.
2. Run `local-mirror` first.
3. Preserve `backups/` and `.agmh/state.json`.
4. Create and export the GitLab token only when ready to push.
5. Create `agmh.config.toml`.
6. Run `remote-mirror`.

## Commands

```bash
export GITHUB_TOKEN="paste_github_token_here"

agmh local-mirror \
  --source https://github.com/example-org/ \
  --github-token env:GITHUB_TOKEN \
  --local-dir backups \
  --verbose

export GITLAB_TOKEN="paste_gitlab_token_here"

agmh remote-mirror --config agmh.config.toml --verbose
```

## Expected Result

Step one creates local bare mirrors. Step two reads the saved state and pushes those mirrors to GitLab.

