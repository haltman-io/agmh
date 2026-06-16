# Mirror GitHub User to a Custom Forgejo Instance: extencil and IRChaosClub

## Scenario

The GitHub user `extencil` wants to mirror the `extencil` GitHub profile to the
custom Forgejo instance at `git.irchaos.club`.

IRChaosClub is a trusted DFIR-focused community, and `extencil` has been invited to
test the instance by mirroring the GitHub profile into the `extencil` namespace
there.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No source token, destination token, or config file exists yet.
4. The `extencil` account or namespace already exists on `git.irchaos.club`.

## Minimum Assumptions

1. The source is the authenticated user's own GitHub profile.
2. Private GitHub repositories may be in scope, so a GitHub source token is used.
3. The destination is a custom Forgejo instance, not Codeberg.
4. The destination token can create repositories and push Git refs under `extencil`.
5. Use `portable-mirror` so AGMH pushes branches and tags without GitHub-specific refs.
6. Disable the marker commit so the test mirror does not add AGMH content to the repositories.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads repositories available to `extencil` on GitHub. |
| `IRCHAOSCLUB_TOKEN` | Yes | Creates and pushes repositories under `extencil` on `git.irchaos.club`. |

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
marker_enabled = false
push_mode = "portable-mirror"

[[destinations]]
url = "https://git.irchaos.club/extencil"
platform = "forgejo"
api_base = "https://git.irchaos.club/api/v1"
tokens = [{ env = "IRCHAOSCLUB_TOKEN", name = "irchaosclub-destination", username = "extencil" }]
visibility = "mirror"
push_mode = "portable-mirror"
```

Create `sources.txt`:

```text
https://github.com/extencil
```

## Algorithm

1. Create the GitHub source token for `extencil`.
2. Create the Forgejo access token on `git.irchaos.club`.
3. Export both tokens.
4. Write the minimal config and `sources.txt`.
5. Run a dry run first to verify the source, destination, and repository plan.
6. Run the full mirror workflow.
7. Inspect the mirrored repositories on `git.irchaos.club/extencil` and AGMH state.

## Commands

```bash
export GITHUB_TOKEN="paste_extencil_github_token_here"
export IRCHAOSCLUB_TOKEN="paste_irchaosclub_forgejo_token_here"

agmh run --config agmh.config.toml --dry-run --verbose
agmh run --config agmh.config.toml --verbose
agmh state --config agmh.config.toml
```

## Expected Result

AGMH discovers repositories from `https://github.com/extencil`, creates or
updates local bare mirrors under `backups/github/extencil/`, creates missing
Forgejo repositories under `https://git.irchaos.club/extencil`, and pushes
portable mirror refs to the IRChaosClub Forgejo instance.

Because this custom host is not automatically inferred as Codeberg, Forgejo, or
Gitea from the hostname, the destination uses explicit `platform = "forgejo"`
and `api_base = "https://git.irchaos.club/api/v1"`.
