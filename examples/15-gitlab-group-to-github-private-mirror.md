# Mirror a GitLab Group to GitHub as Private Repositories

## Scenario

A GitLab group member wants to mirror repositories from a GitLab group to a GitHub organization and force the destination repositories to private.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitLab token, GitHub token, or config file exists yet.

## Minimum Assumptions

1. GitLab membership-level access may matter.
2. GitHub destination creation is required.
3. Use `full` mode because AGMH must discover, mirror locally, create destinations, and push.
4. Force destination visibility to private.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITLAB_SOURCE_TOKEN` | Yes | Reads GitLab source repositories. |
| `GITHUB_DEST_TOKEN` | Yes | Creates and pushes GitHub destination repositories. |

## Minimal Configuration

```bash
agmh init-config --path agmh.config.toml
```

Replace it with:

```toml
mode = "full"

[backup]
local_dir = "backups"
push_mode = "portable-mirror"

[[sources]]
url = "https://gitlab.com/example-group"
platform = "gitlab"
tokens = [{ env = "GITLAB_SOURCE_TOKEN", name = "gitlab-source" }]

[[destinations]]
url = "https://github.com/example-github-org"
platform = "github"
tokens = [{ env = "GITHUB_DEST_TOKEN", name = "github-destination" }]
visibility = "private"
push_mode = "portable-mirror"
```

`sources.txt` is not needed because `[[sources]]` is inline in this example.

## Algorithm

1. Create a GitLab token for the source group.
2. Create a GitHub token that can create repositories in `example-github-org`.
3. Export both tokens.
4. Write the minimal config.
5. Run a dry run.
6. Run the full mirror.
7. Confirm GitHub repositories are private.

## Commands

```bash
export GITLAB_SOURCE_TOKEN="paste_gitlab_source_token_here"
export GITHUB_DEST_TOKEN="paste_github_destination_token_here"

agmh run --config agmh.config.toml --dry-run --verbose
agmh run --config agmh.config.toml --verbose
```

## Expected Result

AGMH mirrors GitLab repositories into local bare mirrors, creates matching private repositories on GitHub, and pushes compatible refs.
