# Watch Own GitHub Profile and Mirror to GitLab, Codeberg, and SourceHut

## Scenario

The GitHub user `jiab77` wants to watch the `jiab77` GitHub profile and automatically mirror compatible repositories to profiles or namespaces on GitLab, Codeberg, and SourceHut.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No source token, destination tokens, SSH config, or config file exists yet.

## Minimum Assumptions

1. This is the user's own GitHub profile, so private repositories may be in scope.
2. Use a GitHub source token.
3. Use destination tokens for GitLab, Codeberg, and SourceHut.
4. Use `portable-mirror` because it is more compatible across forges.
5. SourceHut push is configured through SSH.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads repositories available to `jiab77`. |
| `GITLAB_TOKEN` | Yes | Creates and pushes GitLab repositories. |
| `CODEBERG_TOKEN` | Yes | Creates and pushes Codeberg repositories. |
| `SOURCEHUT_TOKEN` | Yes | Creates SourceHut repositories through the API. |
| SSH key | Yes for SourceHut push | Pushes to `git@git.sr.ht`. |

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

[git]
ssh_identity_file = "/home/jiab77/.ssh/sourcehut_ed25519"
ssh_batch_mode = true
ssh_strict_host_key_checking = "accept-new"

[[destinations]]
url = "https://gitlab.com/jiab77"
platform = "gitlab"
tokens = [{ env = "GITLAB_TOKEN", name = "gitlab-destination" }]
visibility = "mirror"
push_mode = "portable-mirror"

[[destinations]]
url = "https://codeberg.org/jiab77"
platform = "forgejo"
tokens = [{ env = "CODEBERG_TOKEN", name = "codeberg-destination", username = "jiab77" }]
visibility = "mirror"
push_mode = "portable-mirror"

[[destinations]]
url = "https://git.sr.ht/~jiab77"
platform = "sourcehut"
tokens = [{ env = "SOURCEHUT_TOKEN", name = "sourcehut-destination" }]
visibility = "mirror"
push_mode = "portable-mirror"
```

Create `sources.txt`:

```text
https://github.com/jiab77/
```

## Algorithm

1. Create the GitHub source token.
2. Create GitLab, Codeberg, and SourceHut destination tokens.
3. Add the SSH public key to SourceHut.
4. Export all token environment variables.
5. Write `agmh.config.toml` and `sources.txt`.
6. Run one watch cycle with `--watch-once`.
7. Run the watcher continuously under a process manager when the test succeeds.

## Commands

```bash
export GITHUB_TOKEN="paste_github_token_here"
export GITLAB_TOKEN="paste_gitlab_token_here"
export CODEBERG_TOKEN="paste_codeberg_token_here"
export SOURCEHUT_TOKEN="paste_sourcehut_token_here"

agmh watching --config agmh.config.toml --watch-once --verbose
agmh watching --config agmh.config.toml --verbose
```

## Expected Result

AGMH creates local bare mirrors, creates missing destination repositories, and pushes compatible branch and tag refs to GitLab, Codeberg, and SourceHut.

