# AGMH Examples

These examples start from the same baseline:

1. AGMH is installed.
2. The `agmh` command works.
3. No source tokens, destination tokens, webhooks, or config files have been created yet.

Use the smallest example that matches your goal. If the scenario only needs public source data, it uses no source token. If it needs private or membership-level access, it uses a token. If the scenario has no destination, it does not configure one.

## Quick Terms

| Term | Meaning |
| --- | --- |
| Visitor | A user running AGMH without authentication. |
| Download | A normal `git clone`; files are directly visible in the target directory. |
| Local mirror | A bare `git clone --mirror`; useful for pushing to another forge. |
| Full mirror | Discover, mirror locally, create destination repositories, then push. |
| Watching | Poll sources and run an action when AGMH sees a supported source update. |

## Example Index

| Example | Scenario | Main Features |
| --- | --- | --- |
| [01 Visitor Discover GitHub Organization](01-visitor-discover-github-hackerschoice.md) | Visitor discovers public repositories from `hackerschoice` on GitHub. | No token, no config, `discover` |
| [02 Discover Own Public GitHub Profile](02-extencil-discover-own-github-profile.md) | `extencil` discovers public repositories from the `extencil` GitHub profile. | No token, CLI-only |
| [03 Local Mirror a GitHub Organization as a Member](03-extencil-local-mirror-haltman-github-org.md) | `extencil` mirrors `haltman-io` locally as a GitHub organization member. | GitHub source token, local bare mirrors |
| [04 GitHub Organization to Codeberg Mirror](04-skyperthc-github-to-codeberg-hackerschoice-mirror.md) | `skyperthc` mirrors `hackerschoice` from GitHub to Codeberg. | GitHub source token, Codeberg destination token |
| [05 Discover a GitHub Organization as a Member](05-extencil-discover-haltman-github-org.md) | `extencil` discovers `haltman-io` with member-level GitHub access. | GitHub token, discover |
| [06 Watch GitHub Organization and Download Updates](06-jiab77-watch-hackerschoice-download.md) | `jiab77` watches `hackerschoice` and downloads source files on updates. | Watching, GitHub token, download action |
| [07 Download Public GitHub Organization](07-extencil-download-hackerschoice-github.md) | `extencil` downloads public repositories from `hackerschoice`. | No token, normal clones |
| [08 Download Public GitHub Organization with Telegram Finish Notice](08-extencil-download-hackerschoice-telegram-finish.md) | `extencil` downloads `hackerschoice` and sends Telegram finish notifications. | Telegram webhook, download |
| [09 Visitor Watches GitHub User with Discord Notifications](09-visitor-watch-extencil-discord-all-events.md) | Visitor watches `extencil` and sends Discord notifications for all AGMH events. | Discord webhook, no token |
| [10 Watch Own GitHub Profile and Mirror to Three Forges](10-jiab77-watch-own-github-mirror-to-gitlab-codeberg-sourcehut.md) | `jiab77` mirrors own GitHub profile to GitLab, Codeberg, and SourceHut. | Watching, multiple destinations, portable mirrors |
| [11 Discover Another GitHub User](11-skyperthc-discover-vanhauser-thc-github.md) | `skyperthc` discovers public repositories from `vanhauser-thc`. | No token, discover |
| [12 Watch Two GitHub Sources and Mirror to GitLab](12-skyperthc-watch-two-github-sources-to-gitlab.md) | `skyperthc` watches personal and organization GitHub sources and mirrors to GitLab. | Multiple sources, GitLab destination |
| [13 Watch GitHub Organization, Download Updates, Notify Telegram](13-skyperthc-watch-phrackzine-download-telegram.md) | `skyperthc` watches `phrackzine`, downloads updates, and notifies Telegram. | Watching, Telegram, download |
| [14 Download a Public GitLab Group](14-public-gitlab-group-download.md) | Visitor downloads public repositories from a GitLab group. | GitLab source, no token |
| [15 Mirror a GitLab Group to GitHub](15-gitlab-group-to-github-private-mirror.md) | A GitLab group member mirrors a group to a GitHub organization. | GitLab source token, GitHub destination token |
| [16 Discover and Download Codeberg Repositories](16-codeberg-public-discover-and-download.md) | Visitor discovers and downloads public Codeberg repositories. | Forgejo/Codeberg source |
| [17 Download a Bitbucket Workspace](17-bitbucket-workspace-download.md) | A Bitbucket user downloads a workspace with an API token. | Bitbucket source token |
| [18 Two-Step Local Mirror then Remote Mirror](18-two-step-local-mirror-then-remote-mirror.md) | Run local mirror first, then push later from local state. | Resume state, remote-mirror |
| [19 Discord Thread Notifications](19-discord-thread-notifications.md) | Send AGMH notifications into a specific Discord thread. | Discord webhook thread ID |
| [20 Dry Run and State Audit](20-dry-run-and-state-audit.md) | Validate a mirror plan before mutating local or remote state. | `--dry-run`, `state`, audit |
| [21 Mirror to a Generic Git VPS Destination](21-generic-git-vps-destination.md) | Mirror repositories to existing bare Git repositories on a VPS over SSH. | Generic Git destination, SSH, portable mirrors |
| [22 GitHub User to Custom Forgejo Mirror](22-extencil-github-to-irchaos-forgejo-mirror.md) | `extencil` mirrors the GitHub profile to the IRChaos Forgejo instance. | Custom Forgejo destination, explicit API base, portable mirrors |
| [Shared Token and Webhook Reference](shared-token-and-webhook-reference.md) | Common token and webhook setup notes used by examples. | Provider references |
| [Example Template](EXAMPLE_TEMPLATE.md) | Template for contributing new examples. | Reproducible structure |
