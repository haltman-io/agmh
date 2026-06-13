# Discover Another GitHub User: skyperthc and vanhauser-thc

## Scenario

The GitHub user `skyperthc` wants to run `discover` for the public GitHub user profile `vanhauser-thc`.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token or config file exists yet.

## Minimum Assumptions

1. `skyperthc` is not described as the owner of `vanhauser-thc`.
2. Only public repositories are in scope.
3. No source token is required.
4. No destination is required.

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Do not create a token.
2. Run `discover` against `https://github.com/vanhauser-thc/`.
3. Save JSON if the output will be reviewed later.

## Commands

```bash
agmh discover \
  --source https://github.com/vanhauser-thc/ \
  --output vanhauser-thc-discovery.json
```

## Expected Result

AGMH discovers public repositories for `vanhauser-thc`. It does not discover private repositories because the user is not authenticated for that profile.

