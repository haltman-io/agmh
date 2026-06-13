# Discover Own Public GitHub Profile: extencil

## Scenario

The GitHub user `extencil` wants to discover repositories from the `extencil` GitHub profile.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No tokens or config files exist yet.

## Minimum Assumptions

1. The scenario does not mention private repositories.
2. Use the minimum path: public-only discovery.
3. No token is required.
4. No destination is required.

## Minimal Configuration

```text
No config file is required for this example.
```

## Algorithm

1. Do not create a token yet.
2. Run `discover` against `https://github.com/extencil/`.
3. Review the public repository list.
4. If `extencil` later wants private repositories, create a GitHub token and rerun with `--github-token env:GITHUB_TOKEN`.

## Commands

```bash
agmh discover \
  --source https://github.com/extencil/
```

Optional authenticated version:

```bash
export GITHUB_TOKEN="paste_github_token_here"

agmh discover \
  --source https://github.com/extencil/ \
  --github-token env:GITHUB_TOKEN
```

## Expected Result

Without a token, AGMH discovers only public repositories. With a token for `extencil`, AGMH can also discover accessible private repositories when GitHub returns them for that account.

