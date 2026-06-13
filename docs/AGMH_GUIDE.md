# AGMH Guide

This document is a complete operational guide for AGMH. It is written for users
who are looking for practical answers: what AGMH does, what it does not do,
which scenarios are supported, which limitations matter, how configuration
works, and how to operate it safely.

AGMH is a Python CLI for local Git repository backups and cross-forge mirroring.
Its operational goal is continuity: discover repositories from one or more
sources, download local Git mirrors, and optionally push those mirrors to one or
more destinations.

## Contents

- [Core Concepts](#core-concepts)
- [What AGMH Is](#what-agmh-is)
- [What AGMH Is Not](#what-agmh-is-not)
- [What Is Possible](#what-is-possible)
- [What Is Not Possible](#what-is-not-possible)
- [Supported Platforms](#supported-platforms)
- [Operation Modes](#operation-modes)
- [Installation](#installation)
- [File Layout](#file-layout)
- [Configuration Model](#configuration-model)
- [Tokens and Credentials](#tokens-and-credentials)
- [Sources](#sources)
- [Destinations](#destinations)
- [Scenario Examples](#scenario-examples)
- [Watching Mode](#watching-mode)
- [Notifications and Webhooks](#notifications-and-webhooks)
- [Marker Commit](#marker-commit)
- [Repository Visibility](#repository-visibility)
- [Push Modes](#push-modes)
- [Git LFS](#git-lfs)
- [Proxy, TLS, and Networking](#proxy-tls-and-networking)
- [State, Logs, and Resume](#state-logs-and-resume)
- [Operational Best Practices](#operational-best-practices)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Configuration Quick Reference](#configuration-quick-reference)

## Core Concepts

AGMH uses the following terminology consistently.

| Term | Meaning |
| --- | --- |
| Source | Where AGMH discovers and downloads repositories from. Examples: GitHub user, GitHub organization, GitLab group, Bitbucket workspace. |
| Destination | Where AGMH creates repositories and pushes Git mirrors to. Examples: GitHub organization, GitLab namespace, SourceHut account. |
| Local mirror | Local bare copy created with `git clone --mirror`, usually under `backups/`. |
| Remote mirror | Push of an existing local mirror to a remote destination. |
| Full mode | Complete workflow: discover, download locally, optionally mark, create destination, and push. |
| Local mode | Only download or update local mirrors. |
| Remote mode | Only push existing local mirrors to destinations. |
| Watching mode | Polling loop that detects source updates and runs the configured action. |
| State | Local `.agmh/state.json` file used to resume operations and record completed steps. |
| Marker | Optional file, `agmh.txt` by default, inserted into the default branch before remote mirroring. |

## What AGMH Is

AGMH is:

- A Python command-line tool for Git repository backup and mirroring.
- An operational continuity tool for reducing dependency on a single forge.
- An orchestrator that uses forge APIs to discover and create repositories.
- A controlled wrapper around Git commands such as `clone --mirror`,
  `remote update`, `push --mirror`, `push --all`, and `push --tags`.
- A tool that can run in phases: save locally first, then push to remote
  destinations later when needed.
- A tool that understands sources and destinations across multiple platforms.
- A tool that can run in polling mode to react to future repository updates.
- A tool that attempts to keep configured secrets out of logs and notification
  payloads.

AGMH is designed to be auditable. Configuration is TOML, source and destination
lists can be plain text files, and local state is JSON.

## What AGMH Is Not

AGMH is not:

- A complete replacement for GitHub, GitLab, Bitbucket, Forgejo, or SourceHut.
- A full issue tracker migration tool.
- A migration tool for pull requests, merge requests, reviews, discussions,
  projects, releases, packages, Actions, pipelines, or secrets.
- A forge database backup tool.
- A tool for bypassing permissions, bypassing account restrictions, or
  downloading repositories that the configured token cannot access.
- A bidirectional synchronizer.
- A consensus system between forges.
- An inbound webhook server. AGMH can send outbound webhook notifications, but
  it does not receive HTTP events from platforms.
- A compliance program by itself. It helps keep Git copies, but retention
  policy, governance, and access control remain your responsibility.

## What Is Possible

AGMH can:

- Discover repositories on GitHub, GitLab, Forgejo/Gitea, Codeberg, Bitbucket,
  and SourceHut.
- Read multiple sources from the same file or from `[[sources]]` blocks.
- Use different tokens per platform and per source.
- Download public and private repositories when credentials have access.
- Save local bare mirrors with Git history, branches, tags, and refs exposed by
  the source through Git.
- Update existing local mirrors with `git remote update --prune`.
- Create repositories on GitHub, GitLab, Forgejo/Gitea, Codeberg, Bitbucket, and
  SourceHut.
- Push mirrors to one or more destinations.
- Separate local backup from remote publishing.
- Force destination visibility to `public` or `private`.
- Preserve visibility when the destination platform supports an equivalent
  model.
- Use `portable-mirror` mode to avoid refs that some forges reject.
- Use SSH for clone or push when the platform and configuration allow it.
- Use Git LFS when `backup.lfs = true`.
- Use an HTTP/HTTPS proxy for API calls and Git HTTPS operations.
- Disable TLS verification with `--insecure` when required in controlled
  interception or troubleshooting environments.
- Run dry-run plans without cloning, creating, marking, or pushing.
- Run in watching mode with an infinite polling loop.
- Notify start, finish, errors, local saves, remote saves, watching cycles, and
  detected updates.

## What Is Not Possible

AGMH cannot:

- Restore organization permissions, teams, groups, or owners.
- Migrate issues, pull requests, merge requests, reviews, comments, or
  discussions.
- Migrate GitHub Actions, GitLab CI, Bitbucket Pipelines, or CI secrets.
- Migrate packages, container registries, binary releases, or attached assets.
- Migrate wikis, project boards, branch protection rules, deploy keys, or
  platform webhooks.
- Guarantee that platform-specific refs from one forge will be accepted by
  another forge.
- Preserve GitLab `internal` visibility on platforms that do not have the same
  concept.
- Discover private repositories without valid credentials.
- Download repositories that are inaccessible because of account lockout,
  missing scopes, or platform policy.
- Automatically resolve manual divergence in a destination repository.
- Resolve semantic conflicts between branches that already exist in a
  destination.
- Provide atomic transactions across multiple forges. Each repository and
  destination is processed through separate steps.

## Supported Platforms

### Sources

| Platform | Discovery scope | Private repositories | Notes |
| --- | --- | --- | --- |
| GitHub | User or organization | Yes, with token | Uses the REST API. GitHub Enterprise can use `api_base`. |
| GitLab | User, group, or subgroup | Yes, with token | Groups include subgroups. `internal` is treated as non-public on destinations without that concept. |
| Forgejo/Gitea | User or organization | Yes, with token | Uses an API compatible with `/api/v1`. |
| Codeberg | User or organization | Yes, with token | Uses the Forgejo adapter. |
| Bitbucket | Workspace | Yes, with token | Uses the Bitbucket Cloud 2.0 API. |
| SourceHut | User | Yes, with token | Uses `git.sr.ht` GraphQL. |

### Destinations

| Platform | API create | HTTPS push | SSH push | Notes |
| --- | --- | --- | --- | --- |
| GitHub | Yes | Yes | With custom URL | `mirror` is converted to `portable-mirror` to avoid problematic portable refs. |
| GitLab | Yes | Yes | With custom URL | Invalid names such as `.github` are mapped to names accepted by GitLab. |
| Forgejo/Gitea | Yes | Yes | With custom URL | Same adapter family used for Codeberg. |
| Codeberg | Yes | Yes | With custom URL | `portable-mirror` avoids GitHub-specific special refs. |
| Bitbucket | Yes | Yes | With custom URL | Uses compatible basic/token authentication. |
| SourceHut | Yes | Optional | Yes | SSH push is recommended; `push_url_template` is common. |

## Operation Modes

| Mode | Command | Discovers sources | Updates local mirror | Creates destination | Pushes remote |
| --- | --- | --- | --- | --- | --- |
| Full | `agmh run` | Yes | Yes | Yes | Yes |
| Local | `agmh local-mirror` | Yes | Yes | No | No |
| Remote | `agmh remote-mirror` | No | No | Yes | Yes |
| Watching | `agmh watching` | Yes, by polling | Depends on action | Depends on action | Depends on action |

### Full mode

Use this when you want to run the complete workflow now:

```bash
agmh run --config agmh.config.toml --verbose
```

Full mode:

- discovers repositories from sources;
- clones or updates local mirrors;
- records metadata in state;
- creates a marker commit if enabled;
- creates repositories on destinations;
- pushes branches and tags according to `push_mode`.

### Local mode

Use this when you only want to download everything locally:

```bash
agmh local-mirror --config agmh.config.toml --verbose
```

Equivalent:

```bash
agmh run --config agmh.config.toml --mode local --verbose
```

Local mode does not create marker commits and does not contact any destination.

### Remote mode

Use this when mirrors already exist locally and you want to push them later:

```bash
agmh remote-mirror --config agmh.config.toml --verbose
```

Equivalent:

```bash
agmh run --config agmh.config.toml --mode remote --verbose
```

Remote mode reads `.agmh/state.json` and, when needed, can also scan
`backup.local_dir`. When a local mirror is found without state metadata, source
privacy is unknown; in that case AGMH treats the repository as private by
default.

### Watching mode

Use this when you want AGMH to keep running and react to changes:

```bash
agmh watching --config agmh.config.toml --verbose
```

Watching mode is polling. It is not an HTTP server. It queries source APIs at
configured intervals and compares update fingerprints.

## Installation

### Install from PyPI

```bash
python3 -m pip install -U pip
python3 -m pip install "agmh[tui]"
```

Without the optional TUI dependency:

```bash
python3 -m pip install agmh
```

Verify:

```bash
agmh --help
agmh run --help
```

### Isolated environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install "agmh[tui]"
```

### Development install

```bash
git clone https://github.com/haltman-io/agmh.git
cd agmh
python -m pip install -U pip
python -m pip install -e ".[tui,dev]"
```

### Ubuntu system packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git ca-certificates openssh-client
```

Optional:

```bash
sudo apt install -y git-lfs curl
```

## File Layout

A typical run uses:

```text
agmh.config.toml        main configuration
sources.txt            list of source URLs
destinations.txt       optional list of destination URLs
.agmh/state.json       resumable state
.agmh/logs/            local logs
backups/               local bare mirrors
```

Example mirror layout:

```text
backups/
  github/
    haltman-io/
      agmh.git/
  gitlab/
    example-group/
      service.git/
```

## Configuration Model

AGMH loads configuration in this practical order:

1. Package defaults.
2. TOML values, when `--config` is used.
3. Entries from files such as `sources_file` and `destinations_file`.
4. CLI flags, when provided.

Create an initial config:

```bash
agmh init-config --path agmh.config.toml
```

Minimal example using GitHub as source and GitLab as destination:

```toml
workspace = ".agmh"
mode = "full"
sources_file = "sources.txt"

[github]
tokens = [{ env = "GITHUB_TOKEN", name = "github-source" }]

[backup]
local_dir = "backups"
clone_protocol = "https"
marker_enabled = true
push_mode = "mirror"

[[destinations]]
url = "https://gitlab.com/example-mirror"
platform = "gitlab"
tokens = [{ env = "GITLAB_TOKEN", name = "gitlab-destination" }]
visibility = "mirror"
push_mode = "mirror"
```

`sources.txt`:

```text
https://github.com/haltman-io/
```

## Tokens and Credentials

Never place tokens directly in versioned files. Prefer environment variables.

Example:

```bash
export GITHUB_TOKEN="..."
export GITLAB_TOKEN="..."
export GITHUB_DEST_TOKEN="..."
export CODEBERG_TOKEN="..."
export SOURCEHUT_TOKEN="..."
export BITBUCKET_TOKEN="..."
```

### Token formats in TOML

Token by environment variable:

```toml
tokens = [{ env = "GITHUB_TOKEN", name = "github-source" }]
```

Token with username for platforms that need basic auth:

```toml
tokens = [{ env = "BITBUCKET_TOKEN", username = "you@example.com" }]
```

Inline tokens are supported by the parser, but they are not recommended:

```toml
tokens = [{ token = "do-not-commit-this", name = "temporary" }]
```

### Token formats through CLI

GitHub source:

```bash
agmh run --source https://github.com/haltman-io/ --github-token env:GITHUB_TOKEN
```

Generic source:

```bash
agmh run \
  --source https://gitlab.com/example-group/ \
  --source-token gitlab:env:GITLAB_SOURCE_TOKEN
```

Destination:

```bash
agmh run \
  --destination https://github.com/example-mirror \
  --destination-token github:env:GITHUB_DEST_TOKEN
```

With username:

```bash
agmh run \
  --destination https://bitbucket.org/example-workspace \
  --destination-token bitbucket:you@example.com:env:BITBUCKET_TOKEN
```

### Token rotation

When multiple tokens are configured for a platform, AGMH can rotate between
them during rate limits or recoverable authorization failures.

```toml
[github]
tokens = [
  { env = "GITHUB_TOKEN_1", name = "github-primary" },
  { env = "GITHUB_TOKEN_2", name = "github-secondary" },
]
```

## Sources

Sources can come from a text file:

```toml
sources_file = "sources.txt"
```

```text
https://github.com/haltman-io/
https://gitlab.com/example-group/
https://codeberg.org/example-org/
https://bitbucket.org/example-workspace/
https://git.sr.ht/~example/
```

Or from TOML blocks:

```toml
[[sources]]
url = "https://gitlab.com/example-group"
platform = "gitlab"
tokens = [{ env = "GITLAB_SOURCE_TOKEN", name = "gitlab-source" }]
```

Use `[[sources]]` when:

- the source needs its own token;
- the source is self-hosted;
- you need `api_base`;
- you want to customize watching per source.

### GitHub source

```toml
[[sources]]
url = "https://github.com/haltman-io"
platform = "github"
tokens = [{ env = "GITHUB_TOKEN", name = "github-source" }]
```

GitHub Enterprise:

```toml
[[sources]]
url = "https://github.example.com/platform"
platform = "github"
api_base = "https://github.example.com/api/v3"
tokens = [{ env = "GHE_TOKEN", name = "ghe-source" }]
```

### GitLab source

```toml
[[sources]]
url = "https://gitlab.com/example-group"
platform = "gitlab"
tokens = [{ env = "GITLAB_SOURCE_TOKEN", name = "gitlab-source" }]
```

Self-managed GitLab:

```toml
[[sources]]
url = "https://gitlab.example.net/security"
platform = "gitlab"
api_base = "https://gitlab.example.net/api/v4"
tokens = [{ env = "GITLAB_INTERNAL_TOKEN", name = "gitlab-internal" }]
```

### Forgejo, Gitea, and Codeberg source

```toml
[[sources]]
url = "https://codeberg.org/example-org"
platform = "forgejo"
tokens = [{ env = "CODEBERG_SOURCE_TOKEN", username = "example-user" }]
```

Self-hosted:

```toml
[[sources]]
url = "https://forgejo.example.net/example-org"
platform = "forgejo"
api_base = "https://forgejo.example.net/api/v1"
tokens = [{ env = "FORGEJO_TOKEN", username = "example-user" }]
```

### Bitbucket source

```toml
[[sources]]
url = "https://bitbucket.org/example-workspace"
platform = "bitbucket"
tokens = [{ env = "BITBUCKET_TOKEN", username = "you@example.com" }]
```

### SourceHut source

```toml
[[sources]]
url = "https://git.sr.ht/~example"
platform = "sourcehut"
tokens = [{ env = "SOURCEHUT_TOKEN", name = "sourcehut-source" }]
```

## Destinations

Destinations can be declared in TOML:

```toml
[[destinations]]
url = "https://github.com/example-mirror"
platform = "github"
tokens = [{ env = "GITHUB_DEST_TOKEN", name = "github-destination" }]
visibility = "mirror"
push_mode = "mirror"
```

Or in a text file:

```toml
destinations_file = "destinations.txt"
```

```text
https://github.com/example-mirror
https://gitlab.com/example-mirror
https://codeberg.org/example-mirror
```

Use TOML when the destination needs a token, `api_base`, `push_url_template`,
specific visibility, or a specific push mode.

### GitHub destination

```toml
[[destinations]]
url = "https://github.com/example-mirror"
platform = "github"
tokens = [{ env = "GITHUB_DEST_TOKEN", name = "github-destination" }]
visibility = "mirror"
push_mode = "mirror"
```

GitHub Enterprise:

```toml
[[destinations]]
url = "https://github.example.com/example-mirror"
platform = "github"
api_base = "https://github.example.com/api/v3"
tokens = [{ env = "GHE_DEST_TOKEN", name = "ghe-destination" }]
```

### GitLab destination

```toml
[[destinations]]
url = "https://gitlab.com/example-mirror"
platform = "gitlab"
tokens = [{ env = "GITLAB_TOKEN", name = "gitlab-destination" }]
visibility = "mirror"
push_mode = "mirror"
```

### Forgejo or Codeberg destination

```toml
[[destinations]]
url = "https://codeberg.org/example-mirror"
platform = "forgejo"
tokens = [{ env = "CODEBERG_TOKEN", username = "example-user" }]
visibility = "mirror"
push_mode = "mirror"
```

### Bitbucket destination

```toml
[[destinations]]
url = "https://bitbucket.org/example-workspace"
platform = "bitbucket"
tokens = [{ env = "BITBUCKET_TOKEN", username = "you@example.com" }]
visibility = "private"
push_mode = "portable-mirror"
```

### SourceHut destination

```toml
[[destinations]]
url = "https://git.sr.ht/~example"
platform = "sourcehut"
tokens = [{ env = "SOURCEHUT_TOKEN", name = "sourcehut-destination" }]
visibility = "mirror"
push_mode = "mirror"
push_url_template = "git@git.sr.ht:~{owner}/{repo}"
```

SSH settings:

```toml
[git]
ssh_identity_file = "/home/user/.ssh/sourcehut_ed25519"
ssh_identities_only = true
ssh_batch_mode = true
ssh_strict_host_key_checking = "accept-new"
```

## Scenario Examples

### 1. Local backup of a GitHub organization

Goal: download every accessible repository from a GitHub organization without
pushing to any destination.

```bash
export GITHUB_TOKEN="..."

agmh local-mirror \
  --source https://github.com/haltman-io/ \
  --github-token env:GITHUB_TOKEN \
  --local-dir backups \
  --verbose
```

Expected result:

- mirrors under `backups/github/haltman-io/*.git`;
- state under `.agmh/state.json`;
- no remote repositories created;
- no marker commit.

### 2. GitHub to GitLab in one run

```bash
export GITHUB_TOKEN="..."
export GITLAB_TOKEN="..."

agmh run \
  --source https://github.com/haltman-io/ \
  --github-token env:GITHUB_TOKEN \
  --destination https://gitlab.com/haltman-io-mirror \
  --destination-token gitlab:env:GITLAB_TOKEN \
  --verbose
```

### 3. GitHub to GitHub

```bash
export GITHUB_TOKEN="..."
export GITHUB_DEST_TOKEN="..."

agmh run \
  --source https://github.com/haltman-io/ \
  --github-token env:GITHUB_TOKEN \
  --destination https://github.com/haltman-io-mirror \
  --destination-token github:env:GITHUB_DEST_TOKEN \
  --verbose
```

Use separate tokens when the account that reads the source is not the same
account that creates repositories in the destination.

### 4. GitLab to GitHub

```bash
export GITLAB_SOURCE_TOKEN="..."
export GITHUB_DEST_TOKEN="..."

agmh run \
  --source https://gitlab.com/example-group/ \
  --source-token gitlab:env:GITLAB_SOURCE_TOKEN \
  --destination https://github.com/example-mirror \
  --destination-token github:env:GITHUB_DEST_TOKEN \
  --verbose
```

### 5. Codeberg to GitLab

```bash
export CODEBERG_SOURCE_TOKEN="..."
export GITLAB_TOKEN="..."

agmh run \
  --source https://codeberg.org/example-org/ \
  --source-token forgejo:example-user:env:CODEBERG_SOURCE_TOKEN \
  --destination https://gitlab.com/example-codeberg-mirror \
  --destination-token gitlab:env:GITLAB_TOKEN \
  --verbose
```

### 6. Bitbucket workspace to GitHub

```bash
export BITBUCKET_TOKEN="..."
export GITHUB_DEST_TOKEN="..."

agmh run \
  --source https://bitbucket.org/example-workspace/ \
  --source-token bitbucket:you@example.com:env:BITBUCKET_TOKEN \
  --destination https://github.com/example-bitbucket-mirror \
  --destination-token github:env:GITHUB_DEST_TOKEN \
  --verbose
```

### 7. SourceHut to Forgejo

```bash
export SOURCEHUT_TOKEN="..."
export FORGEJO_TOKEN="..."

agmh run \
  --source https://git.sr.ht/~example/ \
  --source-token sourcehut:env:SOURCEHUT_TOKEN \
  --destination https://forgejo.example.net/example-mirror \
  --destination-token forgejo:example-user:env:FORGEJO_TOKEN \
  --verbose
```

### 8. Local backup first, remote push later

First, download:

```bash
export GITHUB_TOKEN="..."

agmh local-mirror \
  --source https://github.com/haltman-io/ \
  --github-token env:GITHUB_TOKEN \
  --local-dir backups \
  --verbose
```

Then push:

```bash
export GITLAB_TOKEN="..."

agmh remote-mirror \
  --config agmh.config.toml \
  --destination https://gitlab.com/haltman-io-mirror \
  --destination-token gitlab:env:GITLAB_TOKEN \
  --verbose
```

### 9. Push everything as private

```bash
agmh remote-mirror \
  --config agmh.config.toml \
  --destination-visibility private \
  --verbose
```

### 10. Push everything as public

```bash
agmh remote-mirror \
  --config agmh.config.toml \
  --destination-visibility public \
  --verbose
```

Use this mode only after reviewing the risk of making every repository public.

### 11. Preserve source visibility

```bash
agmh remote-mirror \
  --config agmh.config.toml \
  --destination-visibility mirror \
  --verbose
```

### 12. Disable the marker

```toml
[backup]
marker_enabled = false
```

When `marker_enabled = false`, AGMH does not modify repository content before
remote push.

### 13. Use `portable-mirror`

```toml
[backup]
push_mode = "portable-mirror"
```

Or per destination:

```toml
[[destinations]]
url = "https://codeberg.org/example-mirror"
platform = "forgejo"
tokens = [{ env = "CODEBERG_TOKEN", username = "example-user" }]
push_mode = "portable-mirror"
```

This mode pushes branches and tags while avoiding special refs such as
`refs/pull/*`.

### 14. Discover repositories without mirroring

```bash
agmh discover \
  --source https://github.com/haltman-io/ \
  --github-token env:GITHUB_TOKEN \
  --output discovered-repos.json \
  --verbose
```

### 15. Run a dry-run

```bash
agmh run \
  --config agmh.config.toml \
  --dry-run \
  --verbose
```

Dry-run can still call APIs for discovery. It should not create repositories,
clone, create markers, or push.

## Watching Mode

Watching mode runs until interrupted:

```bash
agmh watching --config agmh.config.toml --verbose
```

Global configuration:

```toml
[watch]
interval_seconds = 300
action = "full"
initial_run = true
once = false
```

Per source:

```toml
[[sources]]
url = "https://gitlab.com/example-group"
platform = "gitlab"
tokens = [{ env = "GITLAB_SOURCE_TOKEN", name = "gitlab-source" }]
watch = true
watch_interval_seconds = 120
watch_action = "local"
```

Useful flags:

```bash
agmh watching --config agmh.config.toml --watch-interval 120
agmh watching --config agmh.config.toml --watch-action local
agmh watching --config agmh.config.toml --no-watch-initial-run
agmh watching --config agmh.config.toml --watch-once
```

### Watching actions

| Action | Behavior |
| --- | --- |
| `full` | Download/update locally and push to destinations. |
| `local` | Only download/update locally. |
| `remote` | Push an existing local mirror to destinations. |

### What counts as an update

AGMH uses update metadata exposed by the source API:

- GitHub: `pushed_at` or `updated_at`;
- GitLab: `last_activity_at` or `updated_at`;
- Forgejo/Gitea: `updated_at`;
- Bitbucket: `updated_on`;
- SourceHut: `updated`.

This means watching is only as precise as the platform API. Some platforms may
update those fields with delay.

## Notifications and Webhooks

Notifications are disabled by default.

```toml
[notifications]
enabled = true
events = ["*"]
fail_silently = true
timeout_seconds = 10
```

Supported events:

| Event | When it occurs |
| --- | --- |
| `start` | Start of a run. |
| `finish` | End of a run. |
| `local_saved` | Local mirror saved or updated. |
| `remote_saved` | Repository pushed to a destination. |
| `watch_check` | Watching started checking for updates. |
| `watch_update` | Watching found an update. |
| `watch_none` | Watching found no updates. |
| `error` | Operational error. |

### Generic webhook

```toml
[[webhooks]]
name = "ops-generic"
platform = "generic"
url_env = "AGMH_WEBHOOK_URL"
events = ["*"]

[webhooks.headers]
Authorization = "Bearer ${do-not-hardcode}"
```

For sensitive headers, prefer an intermediary endpoint that injects secrets.
Current header support is literal; do not place secret headers in versioned
files.

### Discord

```toml
[[webhooks]]
name = "ops-discord"
platform = "discord"
url_env = "DISCORD_WEBHOOK_URL"
events = ["start", "finish", "error", "local_saved", "remote_saved"]
username = "AGMH"
thread_id = "123456789012345678"
```

### Telegram

```toml
[[webhooks]]
name = "ops-telegram"
platform = "telegram"
bot_token_env = "TELEGRAM_BOT_TOKEN"
chat_id_env = "TELEGRAM_CHAT_ID"
events = ["start", "finish", "error", "watch_update"]
parse_mode = "HTML"
message_thread_id = 42
```

### Notification security

AGMH sends snapshots without secrets. Even so, review source URLs, destination
URLs, repository names, and metadata before sending notifications to public or
shared channels.

## Marker Commit

By default, before remote mirroring, AGMH creates a file on the default branch:

```text
agmh.txt
```

Typical content:

```text
source_url=https://github.com/example/repo
downloaded_at=2026-06-13T10:00:00Z
marker_created_at=2026-06-13T10:00:10Z
```

Default commit message:

```text
Backuping with AGMH v{version}
```

Configuration:

```toml
[backup]
marker_enabled = true
marker_filename = "agmh.txt"

[git]
author_name = "extencil"
author_email = "extencil@segfault.net"
commit_message = "Backuping with AGMH v{version}"
```

Disable it:

```toml
[backup]
marker_enabled = false
```

When disabled, AGMH does not create an additional commit and does not alter
repository content before remote push.

## Repository Visibility

Per-destination configuration:

```toml
[[destinations]]
visibility = "mirror"
```

Values:

| Value | Effect |
| --- | --- |
| `mirror` | Attempts to use the visibility recorded from the source. |
| `public` | Creates the destination as public. |
| `private` | Creates the destination as private. |
| `unlisted` | Uses unlisted where the platform supports it; otherwise the adapter may fall back to public or private behavior. |

CLI override in remote/watching mode:

```bash
agmh remote-mirror --config agmh.config.toml --destination-visibility private
agmh remote-mirror --config agmh.config.toml --destination-visibility public
agmh remote-mirror --config agmh.config.toml --destination-visibility mirror
```

Notes:

- If the destination already exists, AGMH uses the existing repository as-is.
- Not every platform supports the same visibility levels.
- GitLab `internal` is not preserved as `internal` on forges without that model.
- Remote mode without complete state may treat scanned mirrors as private.

## Push Modes

| Push mode | Approximate Git command | Use case |
| --- | --- | --- |
| `mirror` | `git push --mirror` | Most complete mirror, but may push refs rejected by some forges. |
| `portable-mirror` | branches with prune plus tags | More portable across platforms. Avoids special refs such as `refs/pull/*`. |
| `all` | `git push --all` plus `git push --tags` | Branches and tags, without extra refs. |
| `default` | push only the default branch | Useful for minimal cases. |

GitHub, Forgejo/Codeberg, and Bitbucket convert `mirror` to `portable-mirror`
in some adapters to avoid rejection of special refs.

## Git LFS

AGMH can attempt to fetch LFS objects:

```toml
[backup]
lfs = true
```

Or through CLI:

```bash
agmh run --config agmh.config.toml --lfs
```

Requirements:

- `git-lfs` installed;
- credentials with access to LFS objects;
- working network access to the source.

Limitations:

- AGMH runs `git lfs fetch --all` with `check=false`; LFS failures may not abort
  the entire run.
- The destination also needs to support LFS if you expect LFS objects to be
  preserved there.

## Proxy, TLS, and Networking

Proxy:

```bash
agmh run \
  --config agmh.config.toml \
  --proxy http://127.0.0.1:8080 \
  --verbose
```

TOML configuration:

```toml
proxy = "http://127.0.0.1:8080"
```

Disable TLS verification:

```bash
agmh run --config agmh.config.toml --insecure
```

Or:

```bash
agmh run --config agmh.config.toml -k
```

Use `--insecure` only when you understand the risk. It affects API calls and
Git HTTPS operations.

Timeout and retries:

```bash
agmh run \
  --config agmh.config.toml \
  --request-timeout 5 \
  --max-retries 0 \
  --verbose
```

## State, Logs, and Resume

State:

```text
.agmh/state.json
```

Logs:

```text
.agmh/logs/
```

Show state:

```bash
agmh state --config agmh.config.toml
```

Ignore state:

```bash
agmh run --config agmh.config.toml --no-resume
```

Force steps:

```bash
agmh run --config agmh.config.toml --force
```

Alternative workspace:

```bash
agmh run --config agmh.config.toml --workspace /var/lib/agmh
```

## Operational Best Practices

### Before the first run

1. Create tokens with the smallest sufficient scope.
2. Run `agmh discover`.
3. Run `agmh run --dry-run`.
4. Validate the discovered repository list.
5. Test with a small source.
6. Choose `marker_enabled` intentionally.
7. Choose `visibility` intentionally.
8. Use `portable-mirror` when the destination rejects special refs.

### For recurring jobs

- Use environment variables for secrets.
- Use a fixed workspace.
- Preserve `.agmh/state.json`.
- Write logs to persistent storage.
- Run `watching` under systemd, supervisor, a container, or an equivalent
  service manager.
- Configure notifications for `error`, `finish`, `watch_update`, and
  `watch_none`.
- Avoid `--insecure` in production.

### For incident response

- Prioritize `local-mirror` first when there is a risk of losing access.
- Then run `remote-mirror` to external destinations.
- Use multiple destinations when continuity matters.
- Avoid publishing private repositories by accident; prefer
  `--destination-visibility private`.
- Save logs, state, and sanitized configuration for audit.

## Security

### Secrets

AGMH attempts to remove known secrets from logs, but the operational rule should
be:

- do not paste tokens into flags if the shell records history;
- prefer `env`;
- do not commit a real `agmh.config.toml`;
- do not commit `.agmh/`;
- do not commit `backups/`;
- do not send raw logs to public issues;
- rotate tokens if exposure is suspected.

### Files that normally should not be versioned

```text
agmh.config.toml
sources.txt
destinations.txt
.agmh/
backups/
*.log
```

### Marker

The marker is a real Git change. If you need a mirror without content changes,
disable it:

```toml
[backup]
marker_enabled = false
```

### Accidental publication

Before using:

```bash
--destination-visibility public
```

confirm that every repository can be public. When in doubt, use:

```bash
--destination-visibility private
```

## Troubleshooting

### `No source profiles were provided.`

No source was configured. Fix one of the options:

```bash
agmh run --source https://github.com/haltman-io/
```

or:

```toml
sources_file = "sources.txt"
```

### `No remote destinations were provided.`

Remote mode needs at least one destination:

```bash
agmh remote-mirror \
  --config agmh.config.toml \
  --destination https://gitlab.com/example-mirror \
  --destination-token gitlab:env:GITLAB_TOKEN
```

### `HTTP 401`

Likely causes:

- invalid token;
- expired token;
- token for the wrong platform;
- environment variable not exported;
- insufficient scope.

Check without printing the token value:

```bash
test -n "$GITHUB_TOKEN" && echo "GITHUB_TOKEN is set"
```

### `HTTP 403` or `HTTP 429`

Likely causes:

- rate limit;
- insufficient permission;
- organization policy blocks access;
- token does not have SSO authorization where applicable.

Mitigations:

- add extra tokens;
- increase `rate_limit_sleep_seconds`;
- keep `wait_on_rate_limit = true`;
- reduce external parallelism if you run multiple instances.

### Destination rejects `refs/pull/*`

Use:

```toml
[backup]
push_mode = "portable-mirror"
```

Or per destination:

```toml
[[destinations]]
push_mode = "portable-mirror"
```

### GitLab rejects repository names starting with `.`

AGMH maps GitLab-incompatible names, for example `.github` to `dot-github`.

### SSH `Permission denied (publickey)`

Test manually:

```bash
ssh -T -i ~/.ssh/sourcehut_ed25519 -o IdentitiesOnly=yes git@git.sr.ht
```

Configure:

```toml
[git]
ssh_identity_file = "/home/user/.ssh/sourcehut_ed25519"
ssh_identities_only = true
ssh_strict_host_key_checking = "accept-new"
```

### OpenSSH rejects key permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/sourcehut_ed25519
```

If the key is on a Windows-mounted filesystem, copy it to the Linux filesystem.

### Watching does not detect immediately

Watching depends on source API update fields. Some platforms update those fields
with delay. Lowering `interval_seconds` increases polling frequency, but it does
not remove API-side delay.

### Dry-run appears to make external calls

This is expected for discovery. Dry-run avoids creation, clone, marker, and push
operations, but it can still call APIs to build the plan.

## FAQ

### Does AGMH download private repositories?

Yes, when the configured token has access. Without a token, AGMH only sees what
the platform public API exposes.

### Can AGMH push to more than one destination?

Yes. Configure multiple `[[destinations]]` blocks.

### Can AGMH use a destination platform as a source too?

Yes, as long as that platform is supported as a source. GitHub, GitLab,
Forgejo/Codeberg, Bitbucket, and SourceHut have both source and destination
adapters.

### Does AGMH preserve issues and pull requests?

No. AGMH preserves Git repository data: commits, branches, tags, and refs
accepted by the selected Git operation. Issues, PRs/MRs, reviews, and
collaboration metadata are not migrated.

### Does AGMH preserve releases?

Not as platform release objects. Git tags are preserved according to push mode,
but forge release objects, assets, and release notes are not recreated.

### Does AGMH preserve branch protection?

No. Branch protection is platform configuration and must be recreated by another
process.

### Does AGMH preserve visibility?

It can preserve `public`, `private`, and `unlisted` when the source provides
that information and the destination supports an equivalent model. Use
`visibility = "mirror"`.

### Can I force everything to private?

Yes:

```bash
agmh remote-mirror --config agmh.config.toml --destination-visibility private
```

### Can I force everything to public?

Yes:

```bash
agmh remote-mirror --config agmh.config.toml --destination-visibility public
```

Use this carefully.

### Is the marker required?

No. It is enabled by default, but it can be disabled:

```toml
[backup]
marker_enabled = false
```

### Does local mode create a marker?

No. Local mode only clones or updates local mirrors.

### Does remote mode clone from the source?

No. Remote mode uses existing local mirrors.

### Does full mode always need a destination?

For remote mirroring, yes. If you only want to download locally, use
`local-mirror`.

### Is watching mode a webhook?

No. Watching mode is polling. Webhooks in AGMH are outbound notifications only.

### Can state be deleted?

Yes, but you lose the history of completed steps. AGMH can rebuild part of the
context by scanning local mirrors in some modes, but metadata such as original
visibility can be lost.

### Does AGMH remove repositories from the destination?

AGMH can use `--prune` in `portable-mirror` push mode for Git refs, but it does
not delete entire repositories from the destination.

### Does AGMH overwrite history?

Push modes such as `mirror` and `portable-mirror` can update remote refs to
match the local mirror. This is expected in Git mirroring. Use carefully in
repositories where people work directly on the destination.

### Can I use AGMH from cron?

Yes, but watching mode is usually better under systemd or a supervisor. For
cron, consider `watch-once`, `local-mirror`, or `run` with persistent state.

### Can I use AGMH in CI?

Yes, as long as secrets are configured through CI and workspace/state handling
is planned correctly. For real backups, prefer runners with persistent storage
or publish mirrors to external artifacts.

### Can I use AGMH on Windows?

AGMH is Python and uses Git subprocesses. It should work when Python and Git are
available in `PATH`. The main operational examples use Linux/Ubuntu because
that is the most common environment for automation and servers.

### Can I use AGMH with WSL?

Yes. For SSH, prefer keeping keys inside the WSL Linux filesystem and fixing
permissions with `chmod`.

### Why use `portable-mirror`?

Because `git push --mirror` can try to send platform-specific refs that another
platform rejects. `portable-mirror` preserves branches and tags while avoiding
many of those conflicts.

### What happens if the destination already exists?

By default, `allow_existing = true` lets AGMH continue using the existing
repository. The push can still update refs according to the push mode.

### How do I audit what happened?

Use:

```bash
agmh state --config agmh.config.toml
```

and review:

```text
.agmh/state.json
.agmh/logs/
```

### Is AGMH suitable for long-term backups?

AGMH helps create and update Git mirrors, but long-term backup also requires a
retention policy, redundant storage, periodic verification, access control, and
restore testing.

## Configuration Quick Reference

### Top-level

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `workspace` | path | `.agmh` | State, log, and temporary directory. |
| `mode` | string | `full` | `full`, `local`, `remote`, or `watching`. |
| `dry_run` | bool | `false` | Plans without running main mutations. |
| `verbose` | int | `0` | Initial verbosity. |
| `tui` | bool | `true` | Uses Rich when installed. |
| `proxy` | string | null | HTTP/HTTPS proxy. |
| `insecure_tls` | bool | `false` | Disables TLS verification. |
| `sources_file` | path | null | File with source URLs. |
| `destinations_file` | path | null | File with destination URLs. |

### `[backup]`

| Key | Default | Description |
| --- | --- | --- |
| `local_dir` | `backups` | Directory for local mirrors. |
| `clone_protocol` | `https` | `https` or `ssh`. |
| `include_archived` | `true` | Includes archived repositories. |
| `include_forks` | `true` | Includes forks. |
| `include_private_for_authenticated_user` | `true` | On GitHub, attempts to include private repositories of the authenticated user. |
| `lfs` | `false` | Runs `git lfs fetch --all`. |
| `marker_enabled` | `true` | Creates marker commit before remote mirroring. |
| `marker_filename` | `agmh.txt` | Marker file name. |
| `push_mode` | `mirror` | `mirror`, `portable-mirror`, `all`, or `default`. |

### `[retry]`

| Key | Default | Description |
| --- | --- | --- |
| `max_retries` | `5` | Maximum retry attempts. |
| `base_delay_seconds` | `1.5` | Initial delay. |
| `max_delay_seconds` | `60` | Maximum delay. |
| `request_timeout_seconds` | `15` | Per-request timeout. |
| `rate_limit_sleep_seconds` | `300` | Sleep duration when rate limit does not provide a reset time. |
| `wait_on_rate_limit` | `true` | Waits on rate limits when possible. |

### `[git]`

| Key | Default | Description |
| --- | --- | --- |
| `author_name` | `extencil` | Marker commit author. |
| `author_email` | `extencil@segfault.net` | Marker commit email. |
| `commit_message` | `Backuping with AGMH v{version}` | Marker commit message. |
| `ssh_command` | null | Full `GIT_SSH_COMMAND` override. |
| `ssh_identity_file` | null | SSH private key. |
| `ssh_identities_only` | `true` | Uses `IdentitiesOnly=yes`. |
| `ssh_batch_mode` | `false` | Uses `BatchMode=yes`. |
| `ssh_strict_host_key_checking` | null | `yes`, `no`, or `accept-new`. |

### `[watch]`

| Key | Default | Description |
| --- | --- | --- |
| `interval_seconds` | `300` | Global polling interval. |
| `action` | `full` | `full`, `local`, or `remote`. |
| `initial_run` | `true` | Processes repositories during the first cycle. |
| `once` | `false` | Runs one cycle and exits. |

### `[notifications]`

| Key | Default | Description |
| --- | --- | --- |
| `enabled` | `false` | Enables notifications. |
| `events` | `["*"]` | Globally allowed events. |
| `fail_silently` | `true` | Webhook failure becomes a warning. |
| `timeout_seconds` | `10` | Send timeout. |

### `[[sources]]`

| Key | Description |
| --- | --- |
| `url` | Source URL. |
| `platform` | `github`, `gitlab`, `forgejo`, `bitbucket`, or `sourcehut`. |
| `api_base` | Custom API for enterprise/self-hosted instances. |
| `owner` | Explicit owner/namespace/workspace. |
| `tokens` | Token list. |
| `watch` | Enables this source in watching mode. |
| `watch_interval_seconds` | Source-specific interval. |
| `watch_action` | Source-specific action. |

### `[[destinations]]`

| Key | Description |
| --- | --- |
| `url` | Destination URL. |
| `platform` | `github`, `gitlab`, `forgejo`, `bitbucket`, or `sourcehut`. |
| `api_base` | Custom API. |
| `owner` | Explicit owner/namespace/workspace. |
| `tokens` | Token list. |
| `visibility` | `mirror`, `public`, `private`, or `unlisted`. |
| `push_mode` | `mirror`, `portable-mirror`, `all`, or `default`. |
| `create` | Creates repository through API. |
| `allow_existing` | Continues when the repository already exists. |
| `git_username` | Username for Git HTTPS authentication. |
| `push_url_template` | Custom push URL template. |

## Production Checklist

Before relying on AGMH for operational continuity:

- [ ] Tokens are in environment variables, not files.
- [ ] `agmh discover` returns the expected set.
- [ ] `agmh run --dry-run` has been reviewed.
- [ ] Destination visibility has been chosen intentionally.
- [ ] Marker behavior has been accepted or disabled intentionally.
- [ ] `portable-mirror` has been tested for forges that reject special refs.
- [ ] `.agmh/state.json` and logs are on persistent storage.
- [ ] Local backups are on a volume with enough space.
- [ ] Git LFS has been tested if used by the repositories.
- [ ] Error notifications are configured if the process is recurring.
- [ ] A real restore has been tested for at least one repository.
