# Discover and Download Public Codeberg Repositories

## Scenario

A visitor wants to discover and download public repositories from a Codeberg profile.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No Codeberg token or config file exists yet.

## Minimum Assumptions

1. The user is a visitor.
2. Only public repositories are in scope.
3. No destination is required.
4. Codeberg uses AGMH's Forgejo source support.

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Run `discover` first.
2. Review the public repository list.
3. Run `download` if the list is correct.
4. Inspect working trees under `backups/forgejo/`.

## Commands

```bash
agmh discover \
  --source https://codeberg.org/example-user/

agmh download \
  --source https://codeberg.org/example-user/ \
  --local-dir backups \
  --verbose
```

## Expected Result

AGMH discovers and downloads public repositories from Codeberg. No destination repository is created.

