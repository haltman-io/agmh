# Download a Public GitLab Group

## Scenario

A visitor wants to download public repositories from a GitLab group.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitLab token or config file exists yet.

## Minimum Assumptions

1. The user is a visitor.
2. Only public repositories are in scope.
3. No destination is required.
4. Use `download` because the user wants directly visible source files.

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Choose the public GitLab group URL.
2. Do not create a token.
3. Run `agmh download`.
4. Inspect the working tree directories under `backups/gitlab/`.

## Commands

```bash
agmh download \
  --source https://gitlab.com/example-group/ \
  --local-dir backups \
  --verbose
```

If the group requires authentication, create a GitLab token and use:

```bash
export GITLAB_TOKEN="paste_gitlab_token_here"

agmh download \
  --source https://gitlab.com/example-group/ \
  --source-token gitlab:env:GITLAB_TOKEN \
  --local-dir backups \
  --verbose
```

## Expected Result

AGMH downloads public GitLab repositories as normal working trees. If the group requires authentication, add a GitLab token and rerun with `--source-token gitlab:env:GITLAB_TOKEN`.
