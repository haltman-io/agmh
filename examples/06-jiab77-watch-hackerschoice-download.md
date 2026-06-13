# Watch GitHub Organization and Download Updates: jiab77 and hackerschoice

## Scenario

The GitHub user `jiab77` is a member of `hackerschoice` and wants AGMH to watch that GitHub organization and download source files when updates are detected.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token or config file exists yet.

## Minimum Assumptions

1. Membership-level repositories may matter.
2. Use a GitHub source token.
3. No destination is required.
4. Use `watching` with action `download`, because the desired result is normal source files.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads repositories available to `jiab77` as a `hackerschoice` member. |

## Minimal Configuration

Create a starter file:

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

[watch]
interval_seconds = 300
action = "download"
initial_run = true
once = false
```

Create `sources.txt`:

```text
https://github.com/hackerschoice/
```

## Algorithm

1. Create the GitHub token for `jiab77`.
2. Export it.
3. Create `agmh.config.toml` and `sources.txt`.
4. Run one poll cycle with `--watch-once` to verify behavior.
5. Remove `--watch-once` when ready to keep the watcher running.
6. Inspect downloaded working trees under `backups/github/hackerschoice/`.

## Commands

```bash
export GITHUB_TOKEN="paste_jiab77_github_token_here"

agmh watching --config agmh.config.toml --watch-once --verbose
agmh watching --config agmh.config.toml --verbose
```

## Expected Result

AGMH polls GitHub, detects first-seen or updated repositories, and runs normal `git clone` or `git pull --ff-only` into working tree directories.

