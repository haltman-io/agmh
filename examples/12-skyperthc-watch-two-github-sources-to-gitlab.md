# Watch Two GitHub Sources and Mirror to GitLab

## Scenario

The GitHub user `skyperthc` wants to watch both the personal GitHub profile `skyperthc` and the organization `hackerschoice`. When AGMH detects a supported update, it should mirror to the `hackerschoice` namespace on GitLab.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No source token, destination token, or config file exists yet.

## Minimum Assumptions

1. `skyperthc` owns or can access both GitHub sources.
2. Use one GitHub source token.
3. Use one GitLab destination token.
4. Use `watching` with action `full`.
5. Use `portable-mirror` for compatibility.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads both GitHub sources. |
| `GITLAB_TOKEN` | Yes | Creates and pushes repositories under `hackerschoice` on GitLab. |

## Minimal Configuration

```bash
agmh init-config --path agmh.config.toml
```

Replace it with:

```toml
mode = "watching"
sources_file = "sources.txt"

[github]
tokens = [{ env = "GITHUB_TOKEN", name = "github-source" }]

[backup]
local_dir = "backups"
push_mode = "portable-mirror"

[watch]
interval_seconds = 300
action = "full"
initial_run = true
once = false

[[destinations]]
url = "https://gitlab.com/hackerschoice"
platform = "gitlab"
tokens = [{ env = "GITLAB_TOKEN", name = "gitlab-destination" }]
visibility = "mirror"
push_mode = "portable-mirror"
```

Create `sources.txt`:

```text
https://github.com/skyperthc/
https://github.com/hackerschoice/
```

## Algorithm

1. Create and export the GitHub source token.
2. Create and export the GitLab destination token.
3. Create the config and source file.
4. Run one watch cycle.
5. Review created GitLab repositories.
6. Run continuously after the first cycle is correct.

## Commands

```bash
export GITHUB_TOKEN="paste_skyperthc_github_token_here"
export GITLAB_TOKEN="paste_gitlab_token_here"

agmh watching --config agmh.config.toml --watch-once --verbose
agmh watching --config agmh.config.toml --verbose
```

## Expected Result

AGMH watches both GitHub sources and mirrors changed repositories to the GitLab `hackerschoice` namespace.

