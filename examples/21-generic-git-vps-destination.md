# Mirror to a Generic Git VPS Destination

## Scenario

A GitHub organization member wants to mirror repositories to existing bare Git
repositories on a VPS over SSH. The VPS is not GitLab, Forgejo, Gitea,
SourceHut, or another forge with an API.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No tokens or config file exists yet.
4. The user can SSH to the VPS account that owns the bare repositories.

## Minimum Assumptions

1. The source is GitHub.
2. The destination is a generic SSH Git server.
3. The destination bare repositories already exist.
4. AGMH should not try to create repositories on the VPS.
5. Use `portable-mirror` so AGMH pushes branches and tags without special forge refs.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Reads source repositories. |
| SSH key | Yes | Pushes to the generic Git server. |

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
marker_enabled = false
push_mode = "portable-mirror"

[[destinations]]
platform = "git"
url = "backup-vps"
create = false
push_url_template = "git@backup.example.com:/srv/git/{owner}/{repo}.git"
push_mode = "portable-mirror"

[git]
ssh_identity_file = "/home/user/.ssh/backup_vps_ed25519"
ssh_identities_only = true
ssh_batch_mode = true
ssh_strict_host_key_checking = "accept-new"
```

Create `sources.txt`:

```text
https://github.com/example-org/
```

Prepare matching bare repositories on the VPS before running AGMH:

```bash
ssh git@backup.example.com
mkdir -p /srv/git/example-org
git init --bare /srv/git/example-org/service.git
git init --bare /srv/git/example-org/web.git
exit
```

## Algorithm

1. Create and export the GitHub source token.
2. Add the SSH public key to the VPS account.
3. Create a bare Git repository on the VPS for each source repository AGMH will push.
4. Write the minimal config and `sources.txt`.
5. Run `discover` if you need to confirm the source repository list.
6. Run the full mirror workflow.

## Commands

```bash
export GITHUB_TOKEN="paste_github_token_here"

agmh discover --config agmh.config.toml --output discovery.json
agmh run --config agmh.config.toml --verbose
```

## Expected Result

AGMH creates or updates local bare mirrors under `backups/` and pushes them to
the configured generic Git URL template. For a source repository named
`example-org/service`, the destination push URL is:

```text
git@backup.example.com:/srv/git/example-org/service.git
```

AGMH does not create the destination repository on the VPS. If the bare
repository is missing, the Git push fails and the failure is recorded in state
and logs.
