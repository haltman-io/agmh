# Mirror GitHub Organization to Codeberg: skyperthc and hackerschoice

## Scenario

The GitHub user `skyperthc` owns the GitHub organization `hackerschoice` and wants to mirror that source to the `hackerschoice` profile or organization on Codeberg.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No source token, destination token, or config file exists yet.

## Minimum Assumptions

1. Source ownership means private or member-only source repositories may matter.
2. Codeberg needs an access token to create repositories and push mirrors.
3. A destination is required, so use `agmh run`, not `agmh local-mirror`.
4. `local-mirror` alone cannot push to Codeberg.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads source repositories available to `skyperthc`. |
| `CODEBERG_TOKEN` | Yes | Creates and pushes repositories under `hackerschoice` on Codeberg. |

## Minimal Configuration

Create a starter file:

```bash
agmh init-config --path agmh.config.toml
```

Replace it with:

```toml
mode = "full"
sources_file = "sources.txt"

[github]
tokens = [{ env = "GITHUB_TOKEN", name = "github-source" }]

[backup]
local_dir = "backups"
push_mode = "portable-mirror"

[[destinations]]
url = "https://codeberg.org/hackerschoice"
platform = "forgejo"
tokens = [{ env = "CODEBERG_TOKEN", name = "codeberg-destination", username = "skyperthc" }]
visibility = "mirror"
push_mode = "portable-mirror"
```

Create `sources.txt`:

```text
https://github.com/hackerschoice/
```

## Algorithm

1. Create the GitHub source token for `skyperthc`.
2. Create the Codeberg access token for the Codeberg account that can create repositories under `hackerschoice`.
3. Export both tokens.
4. Write the minimal config and `sources.txt`.
5. Run a dry run first.
6. Run the full mirror workflow.
7. Inspect Codeberg repositories and AGMH state.

## Commands

```bash
export GITHUB_TOKEN="paste_skyperthc_github_token_here"
export CODEBERG_TOKEN="paste_codeberg_token_here"

agmh run --config agmh.config.toml --dry-run --verbose
agmh run --config agmh.config.toml --verbose
agmh state --config agmh.config.toml
```

## Expected Result

AGMH creates local bare mirrors, creates missing Codeberg repositories under `hackerschoice`, and pushes portable mirror refs to Codeberg.

