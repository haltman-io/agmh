# Dry Run and State Audit

## Scenario

A user wants to validate a mirror plan before allowing AGMH to clone, create repositories, or push.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No tokens or config file exists yet.

## Minimum Assumptions

1. The source is GitHub.
2. The destination is GitLab.
3. The user has tokens but wants a safe plan first.
4. Use `--dry-run` before the real run.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads source repositories. |
| `GITLAB_TOKEN` | Yes | Validates destination configuration and later pushes. |

## Minimal Configuration

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
url = "https://gitlab.com/example-mirror"
platform = "gitlab"
tokens = [{ env = "GITLAB_TOKEN", name = "gitlab-destination" }]
visibility = "private"
push_mode = "portable-mirror"
```

Create `sources.txt`:

```text
https://github.com/example-org/
```

## Algorithm

1. Create and export source and destination tokens.
2. Write the minimal config.
3. Run `discover` to inspect source scope.
4. Run `agmh run --dry-run`.
5. Review logs under `.agmh/logs/`.
6. Run for real only after the plan is correct.
7. Use `agmh state` after the real run.

## Commands

```bash
export GITHUB_TOKEN="paste_github_token_here"
export GITLAB_TOKEN="paste_gitlab_token_here"

agmh discover --config agmh.config.toml --output discovery.json
agmh run --config agmh.config.toml --dry-run --verbose
agmh run --config agmh.config.toml --verbose
agmh state --config agmh.config.toml
```

## Expected Result

The dry run prints planned Git and API actions without performing the main mutations. The real run creates state that can be audited with `agmh state`.

