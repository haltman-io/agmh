# AGMH

[![PyPI](https://img.shields.io/pypi/v/agmh.svg)](https://pypi.org/project/agmh/)
[![Python](https://img.shields.io/pypi/pyversions/agmh.svg)](https://pypi.org/project/agmh/)
[![CI](https://github.com/haltman-io/agmh/actions/workflows/ci.yml/badge.svg)](https://github.com/haltman-io/agmh/actions/workflows/ci.yml)
[![Release](https://github.com/haltman-io/agmh/actions/workflows/release-please.yml/badge.svg)](https://github.com/haltman-io/agmh/actions/workflows/release-please.yml)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](LICENSE)

AGMH means **ANTI GITHUB & MICROSOFT HYSTERIA**.

AGMH is a Python CLI for local Git repository backups and cross-forge mirroring.
It discovers repositories from supported source accounts, organizations, groups,
namespaces, or workspaces; downloads source files with regular `git clone`;
stores local Git mirrors when needed; and can push those mirrors to GitHub,
GitLab, Forgejo/Codeberg, Bitbucket, SourceHut, or compatible Git remotes.

Package: [agmh on PyPI](https://pypi.org/project/agmh/)

Repository: [haltman-io/agmh](https://github.com/haltman-io/agmh)

> [!IMPORTANT]
> The complete technical documentation is in the GitHub Wiki:
> [AGMH Complete Guide](https://github.com/haltman-io/agmh/wiki/AGMH-COMPLETE-GUIDE).
>
> This README is intentionally short. It is for people who need to install AGMH,
> configure tokens, and run the most common mirror workflows quickly.

The primary command is:

```bash
agmh
```

The legacy typo `aghm` was removed. AGMH intentionally uses `agmh` for commands,
default config files, state directories, logs, and generated marker files.

## What AGMH Does

- Downloads repositories as normal working trees with `git clone`.
- Backs up repositories locally as bare mirrors with `git clone --mirror`.
- Discovers repositories from GitHub, GitLab, Forgejo/Gitea, Codeberg,
  Bitbucket, and SourceHut.
- Pushes mirrors to GitHub, GitLab, Forgejo/Gitea, Codeberg, Bitbucket,
  SourceHut, or custom Git remotes.
- Supports simple `download` runs, local mirror backups, remote-only mirror
  publishing, full mirror runs, and polling with `watching`.
- Uses environment variables for tokens.
- Keeps resumable state in `.agmh/state.json`.
- Writes logs under `.agmh/logs/`.

## What AGMH Does Not Do

AGMH mirrors Git repositories. It does not migrate issues, pull requests, merge
requests, reviews, discussions, releases, CI configuration, project boards,
branch protection rules, repository permissions, organization members, or forge
secrets.

## Install

Install from PyPI:

```bash
python3 -m pip install -U pip
python3 -m pip install "agmh[tui]"
```

Check it:

```bash
agmh --help
agmh run --help
```

Ubuntu packages you probably need:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git ca-certificates openssh-client
```

Optional:

```bash
sudo apt install -y git-lfs curl
```

## Tokens

Use environment variables. Do not paste tokens into config files, shell history,
logs, issues, or pull requests.

Common environment names:

```bash
export GITHUB_TOKEN="source_github_token_here"
export GITHUB_DEST_TOKEN="destination_github_token_here"
export GITLAB_TOKEN="gitlab_token_here"
export CODEBERG_TOKEN="codeberg_or_forgejo_token_here"
export BITBUCKET_TOKEN="bitbucket_app_password_or_token_here"
export SOURCEHUT_TOKEN="sourcehut_token_here"
```

Where to create tokens:

- GitHub: https://github.com/settings/tokens
- GitLab: https://gitlab.com/-/user_settings/personal_access_tokens
- Codeberg: https://codeberg.org/user/settings/applications
- Bitbucket app passwords: https://bitbucket.org/account/settings/app-passwords/
- SourceHut OAuth tokens: https://meta.sr.ht/oauth

Token requirements depend on the provider, but the practical rule is simple:

- Source token: must be able to read every repository you want to back up.
- Destination token: must be able to create repositories and push Git refs in
  the destination account, organization, group, namespace, or workspace.

For private repositories, make sure the token has private repository access. For
organizations with SSO or extra approval rules, authorize the token for that
organization before running AGMH.

## Quick Start

Create a config:

```bash
agmh init-config --path agmh.config.toml
```

Create a source list:

```bash
cat > sources.txt <<'EOF'
https://github.com/YOUR_USER_OR_ORG/
EOF
```

Run a dry-run:

```bash
agmh run --config agmh.config.toml --dry-run --verbose
```

Run it for real:

```bash
agmh run --config agmh.config.toml --verbose
```

Check state:

```bash
agmh state --config agmh.config.toml
```

## Common Commands

### Back Up My GitHub Locally Only

This runs regular `git clone` operations so repository files are directly
available under `--local-dir`. It does not create remote repositories and does
not push anywhere.

```bash
export GITHUB_TOKEN="..."

agmh download \
  --source https://github.com/YOUR_USER_OR_ORG/ \
  --github-token env:GITHUB_TOKEN \
  --local-dir backups \
  --verbose
```

Result:

```text
backups/github/YOUR_USER_OR_ORG/REPOSITORY_NAME/
.agmh/state.json
.agmh/logs/
```

### Mirror My GitHub to GitLab

Use a GitHub token that can read the source and a GitLab token that can create
projects and push to the destination namespace.

```bash
export GITHUB_TOKEN="..."
export GITLAB_TOKEN="..."

agmh run \
  --source https://github.com/YOUR_USER_OR_ORG/ \
  --github-token env:GITHUB_TOKEN \
  --destination https://gitlab.com/YOUR_GITLAB_NAMESPACE \
  --destination-token gitlab:env:GITLAB_TOKEN \
  --verbose
```

The destination URL is the namespace/group/user where AGMH should create
repositories. It is not an individual repository URL.

### Mirror My GitHub to Another GitHub Account or Organization

Use separate tokens if the source and destination accounts are different.

```bash
export GITHUB_TOKEN="..."
export GITHUB_DEST_TOKEN="..."

agmh run \
  --source https://github.com/SOURCE_USER_OR_ORG/ \
  --github-token env:GITHUB_TOKEN \
  --destination https://github.com/DESTINATION_USER_OR_ORG \
  --destination-token github:env:GITHUB_DEST_TOKEN \
  --verbose
```

### Mirror GitLab to GitHub

```bash
export GITLAB_SOURCE_TOKEN="..."
export GITHUB_DEST_TOKEN="..."

agmh run \
  --source https://gitlab.com/SOURCE_GROUP_OR_USER/ \
  --source-token gitlab:env:GITLAB_SOURCE_TOKEN \
  --destination https://github.com/DESTINATION_USER_OR_ORG \
  --destination-token github:env:GITHUB_DEST_TOKEN \
  --verbose
```

### Mirror Codeberg or Forgejo to GitLab

```bash
export CODEBERG_SOURCE_TOKEN="..."
export GITLAB_TOKEN="..."

agmh run \
  --source https://codeberg.org/SOURCE_USER_OR_ORG/ \
  --source-token forgejo:YOUR_CODEBERG_USERNAME:env:CODEBERG_SOURCE_TOKEN \
  --destination https://gitlab.com/DESTINATION_NAMESPACE \
  --destination-token gitlab:env:GITLAB_TOKEN \
  --verbose
```

### Mirror Bitbucket to GitHub

```bash
export BITBUCKET_TOKEN="..."
export GITHUB_DEST_TOKEN="..."

agmh run \
  --source https://bitbucket.org/SOURCE_WORKSPACE/ \
  --source-token bitbucket:YOUR_BITBUCKET_USERNAME_OR_EMAIL:env:BITBUCKET_TOKEN \
  --destination https://github.com/DESTINATION_USER_OR_ORG \
  --destination-token github:env:GITHUB_DEST_TOKEN \
  --verbose
```

### Push Existing Local Mirrors Later

First, create local mirrors:

```bash
export GITHUB_TOKEN="..."

agmh local-mirror \
  --source https://github.com/YOUR_USER_OR_ORG/ \
  --github-token env:GITHUB_TOKEN \
  --local-dir backups \
  --verbose
```

Later, push those local mirrors:

```bash
export GITLAB_TOKEN="..."

agmh remote-mirror \
  --config agmh.config.toml \
  --destination https://gitlab.com/DESTINATION_NAMESPACE \
  --destination-token gitlab:env:GITLAB_TOKEN \
  --verbose
```

### Force Destination Visibility

Mirror source visibility:

```bash
agmh remote-mirror --config agmh.config.toml --destination-visibility mirror
```

Force everything private:

```bash
agmh remote-mirror --config agmh.config.toml --destination-visibility private
```

Force everything public:

```bash
agmh remote-mirror --config agmh.config.toml --destination-visibility public
```

Use `public` only after reviewing the repositories. AGMH cannot know your
disclosure policy.

### Disable the Marker Commit

By default, AGMH can add `agmh.txt` before remote mirroring. If you want a mirror
without that repository content change, set:

```toml
[backup]
marker_enabled = false
```

### Watch for Updates

```bash
agmh watching \
  --config agmh.config.toml \
  --watch-interval 300 \
  --watch-action full \
  --verbose
```

Watching mode uses polling. It is not an inbound webhook server.

## Examples

Detailed usage examples live in [`examples/`](examples/). Each example starts
from a clean install where `agmh` works but no tokens, webhooks, destinations,
or config files exist yet.

| Example | Description |
| --- | --- |
| [Visitor discover GitHub organization](examples/01-visitor-discover-github-hackerschoice.md) | Discover public repositories from `hackerschoice` without authentication. |
| [Discover own public GitHub profile](examples/02-extencil-discover-own-github-profile.md) | Run public-only discovery for `extencil`. |
| [Local mirror GitHub organization as a member](examples/03-extencil-local-mirror-haltman-github-org.md) | Use a GitHub token to create local bare mirrors for `haltman-io`. |
| [Mirror GitHub organization to Codeberg](examples/04-skyperthc-github-to-codeberg-hackerschoice-mirror.md) | Mirror `hackerschoice` from GitHub to Codeberg with source and destination tokens. |
| [Discover GitHub organization as a member](examples/05-extencil-discover-haltman-github-org.md) | Discover `haltman-io` with member-level GitHub access. |
| [Watch GitHub organization and download updates](examples/06-jiab77-watch-hackerschoice-download.md) | Watch `hackerschoice` and download working trees when updates are detected. |
| [Download public GitHub organization](examples/07-extencil-download-hackerschoice-github.md) | Download public `hackerschoice` repositories with normal `git clone`. |
| [Download GitHub organization with Telegram finish notice](examples/08-extencil-download-hackerschoice-telegram-finish.md) | Download public repositories and notify Telegram when AGMH finishes. |
| [Visitor watch with Discord notifications](examples/09-visitor-watch-extencil-discord-all-events.md) | Watch public `extencil` repositories and notify Discord for all supported events. |
| [Watch own GitHub profile and mirror to three forges](examples/10-jiab77-watch-own-github-mirror-to-gitlab-codeberg-sourcehut.md) | Mirror a GitHub profile to GitLab, Codeberg, and SourceHut. |
| [Discover another GitHub user](examples/11-skyperthc-discover-vanhauser-thc-github.md) | Discover public repositories from `vanhauser-thc`. |
| [Watch two GitHub sources and mirror to GitLab](examples/12-skyperthc-watch-two-github-sources-to-gitlab.md) | Watch a personal profile and organization, then mirror both to GitLab. |
| [Watch GitHub organization, download, notify Telegram](examples/13-skyperthc-watch-phrackzine-download-telegram.md) | Watch `phrackzine`, download updates, and notify Telegram. |
| [Download a public GitLab group](examples/14-public-gitlab-group-download.md) | Download public GitLab group repositories as working trees. |
| [Mirror GitLab group to GitHub as private](examples/15-gitlab-group-to-github-private-mirror.md) | Mirror a GitLab group to private GitHub repositories. |
| [Discover and download Codeberg repositories](examples/16-codeberg-public-discover-and-download.md) | Use Forgejo/Codeberg source support for public repositories. |
| [Download a Bitbucket workspace](examples/17-bitbucket-workspace-download.md) | Download Bitbucket workspace repositories with an API token. |
| [Two-step local mirror then remote mirror](examples/18-two-step-local-mirror-then-remote-mirror.md) | Create local mirrors first, then push them later. |
| [Discord thread notifications](examples/19-discord-thread-notifications.md) | Send AGMH notifications to a specific Discord thread. |
| [Dry run and state audit](examples/20-dry-run-and-state-audit.md) | Validate mirror plans with `--dry-run` and inspect AGMH state. |
| [Shared token and webhook reference](examples/shared-token-and-webhook-reference.md) | Common credential setup notes used by the examples. |

## Quick Config Example

This is enough for a common GitHub to GitLab mirror:

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
url = "https://gitlab.com/YOUR_GITLAB_NAMESPACE"
platform = "gitlab"
tokens = [{ env = "GITLAB_TOKEN", name = "gitlab-destination" }]
visibility = "mirror"
push_mode = "mirror"
```

`sources.txt`:

```text
https://github.com/YOUR_USER_OR_ORG/
```

## When You Need More Than This README

Read the complete guide:

https://github.com/haltman-io/agmh/wiki/AGMH-COMPLETE-GUIDE

It covers:

- every supported source and destination provider;
- full TOML reference;
- local mirror, remote mirror, and watching mode details;
- webhook notifications for generic endpoints, Discord, and Telegram;
- marker commit behavior;
- visibility rules;
- push modes;
- Git LFS;
- proxy and TLS options;
- state, logs, resume, and troubleshooting.

## Security Notes

- Prefer environment variables for secrets.
- Do not commit `.agmh/`, `backups/`, `agmh.config.toml`, `sources.txt`,
  `destinations.txt`, tokens, logs, or private config files.
- Rotate tokens if they were ever printed or pasted in the wrong place.
- Use `--insecure` only for controlled troubleshooting. It disables TLS
  verification.

Security reports: email `root@haltman.io`. Do not open a public issue for
private vulnerability details.

## Project Background

### Risk Model

This tool exists because important work should not depend on a single platform
remaining available, cooperative, or operational forever.

AGMH was built after past platform access incidents made us reassess the risk of
being locked out of a large technology platform without enough time to preserve
our work or coordinate with the people closest to a project. The risk is similar
to an abrupt offboarding process where access is disabled so quickly that a
person cannot even send a final email to close colleagues.

For software projects, that access risk is broader than any single account or
provider. A team can lose continuity because of enforcement actions, sanctions,
provider policy changes, operational outages, service degradation, acquisition
risk, or a platform eventually disappearing. The critical issue is
centralization: if repository history, issues, branches, tags, release metadata,
and collaboration context all live in one place, a disruption in that place can
have a large impact on the surrounding ecosystem.

This is not a personal fight with GitHub. It is a risk-management and business
continuity problem. AGMH provides a practical way to keep local mirrors, move
repositories between forges, preserve Git history, and maintain high
availability of project information when a centralized platform becomes
unavailable or unsuitable.

AGMH is produced by **Haltman.IO** and released freely so others can protect
their own work.

This tool has already been used to back up repositories from `@extencil` and
`@haltman-io` to GitLab, Codeberg, and SourceHut successfully.

### Continuity Incident Timeline

AGMH was used to move the work of `@extencil` and `@haltman-io` away from a
single forge dependency and into independent mirrors:

- GitLab: https://gitlab.com/extencil
- Codeberg: https://codeberg.org/extencil
- SourceHut: https://git.sr.ht/~extencil
- GitLab: https://gitlab.com/haltman-io
- Codeberg: https://codeberg.org/haltman

The account access incident that reinforced this risk model followed this
timeline:

| Event | Time |
| --- | --- |
| Account suspended/banned by platform enforcement | Monday, 2026-06-08, around 04:00 `America/Sao_Paulo` (`UTC-03:00`), approximately 2026-06-08 07:00 UTC |
| Review ticket opened | 2026-06-08 07:59 UTC, 2026-06-08 04:59 `America/Sao_Paulo` |
| Priority follow-up sent by our side | 2026-06-11 16:47 UTC, 2026-06-11 13:47 `America/Sao_Paulo` |
| Case reviewed and reverted by GitHub | 2026-06-12 11:19 UTC, 2026-06-12 08:19 `America/Sao_Paulo` |

The incident would have been significantly more damaging without continuity
procedures already in place. When Haltman.IO created its GitHub organization,
other Haltman.IO members were assigned as organization owners. That avoided a
complete lockout scenario.

Someone who is not part of an organization, or who is not an organization owner
or repository administrator, cannot reliably operate that organization. They
cannot recover organization-level access, manage owners and teams, change
organization settings, manage repository permissions, configure secrets,
webhooks, deploy keys, branch protection, or security settings, create or
transfer repositories, publish releases, or consistently triage and merge work
across the organization.

This matters because the affected work is operational, not cosmetic. Haltman.IO
voluntarily sustains email-forwarding infrastructure associated with The
Hacker's Choice, in collaboration with Phrack, Eurocompton, team-teso, Antisec,
pwnbuffer, and other groups connected to cybersecurity research. A complete
organization lockout would have affected the ability to manage the many
repositories behind that email-forwarding stack.

That impact is not about minor product changes or visual polish. It affects the
ability to coordinate proper vulnerability disclosure for people who self-host
the email-forwarding stack, publish fixes, document operational changes, and
credit researchers correctly when they report vulnerabilities.

It also affects our internal service expectations. There is no legal or
commercial SLA: we do not sell this work, and the output is public work for the
public. Still, we prefer to respond to issues and pull requests quickly. Acting
like a large platform with effectively unbounded response times is neither our
role nor consistent with Haltman.IO's operating values.

### Haltman.IO

Haltman is a group of Brazilian hackers. Friends for over a decade, building
public, privacy-first infrastructure and free software.

We build, break, audit, and publish.

We do not sell platforms. We do not run franchises.

We do not ask permission.

Haltman.IO links:

- Website: https://haltman.io/
- Alternate website: https://haltman.org/
- Contact: root@haltman.io, root@haltman.org
- Join Haltman.IO: https://haltman.io/join/
- Telegram group: https://t.me/haltman_group

### Operating Values

| Doctrine | Value |
| --- | --- |
| 01 Independence | We answer to no one. No board. No investors. No sponsors. Our independence guarantees our freedom. |
| 02 Transparency | Every tool is open source. Every decision is visible. No back rooms. No hidden agendas. |
| 03 Public Output | We publish. We document. We release. Our work speaks for itself. Not our marketing. |
| 04 No Hierarchy | Flat structure. No leaders. No bosses. No titles. No org charts. Respect is earned by output. |
| 05 Mutual Aid | When one of us needs help, the others show up. No invoices. No politics. Just engineering. |
| 06 No Compromise | We do not water down our principles for comfort, profit, or acceptance. Those who trade freedom for security end up with neither. |

## Project Files

- [CHANGELOG.md](CHANGELOG.md): release notes and pending changes.
- [SECURITY.md](SECURITY.md): private vulnerability reporting policy.
- [CONTRIBUTING.md](CONTRIBUTING.md): development setup and contribution checks.
- [RELEASING.md](RELEASING.md): Release Please and PyPI publishing process.
- [SUPPORT.md](SUPPORT.md): support paths for bugs, questions, and security reports.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): collaboration expectations.
- [MAINTAINERS.md](MAINTAINERS.md): maintainer and security contact information.
- [.github/CODEOWNERS](.github/CODEOWNERS): default review ownership.

## References

- Complete documentation: https://github.com/haltman-io/agmh/wiki/AGMH-COMPLETE-GUIDE
- AGMH on PyPI: https://pypi.org/project/agmh/
- AGMH repository: https://github.com/haltman-io/agmh
- GitHub personal access tokens: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- GitLab personal access tokens: https://docs.gitlab.com/user/profile/personal_access_tokens/
- Codeberg access tokens: https://docs.codeberg.org/advanced/access-token/
- Bitbucket app passwords: https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/
- SourceHut OAuth: https://man.sr.ht/meta.sr.ht/oauth.md
- Unlicense: https://unlicense.org/

## License

AGMH is released under the **Unlicense**.

This means the project is dedicated to the public domain to the fullest extent
possible. See:

- https://unlicense.org/
- [LICENSE](LICENSE)

## Author

Author: **extencil** <extencil@segfault.net>

Repository: [haltman-io/agmh](https://github.com/haltman-io/agmh)

Produced by **Haltman.IO**.
