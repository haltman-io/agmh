# Download Public GitHub Organization: extencil and hackerschoice

## Scenario

The GitHub user `extencil` wants to download all public repositories from `hackerschoice` on GitHub.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token or config file exists yet.

## Minimum Assumptions

1. `extencil` is not described as a `hackerschoice` member.
2. Only public repositories are in scope.
3. No destination is required.
4. Use `download`, not `local-mirror`, because source files should be directly visible.

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Do not create a token.
2. Run `agmh download` against the GitHub organization URL.
3. Inspect the output directory.
4. If GitHub anonymous rate limits the run, add a GitHub token later.

## Commands

```bash
agmh download \
  --source https://github.com/hackerschoice/ \
  --local-dir backups \
  --verbose
```

## Expected Result

AGMH creates normal working tree clones:

```text
backups/github/hackerschoice/repository-name/
backups/github/hackerschoice/repository-name/.git/
```

Files are directly visible inside each repository directory.

