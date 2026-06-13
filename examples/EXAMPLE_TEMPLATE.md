# Example Title

## Scenario

Describe the exact user, source, destination, and desired AGMH action.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No source tokens, destination tokens, webhooks, or config files exist yet.

## Minimum Assumptions

1. State whether the user is a visitor or authenticated user.
2. State whether private repositories are in scope.
3. State whether a destination is required.
4. State whether notifications are required.

## Required Credentials

List only credentials required by this scenario.

| Credential | Required | Why |
| --- | --- | --- |
| `EXAMPLE_TOKEN` | Yes/No | Explain why. |

## Minimal Configuration

If the scenario does not need a config file, write:

```text
No config file is required for this example.
```

If a config file is required, show the minimal `agmh.config.toml`.

```toml
mode = "download"
sources_file = "sources.txt"
```

## Algorithm

1. Create only the tokens required by the scenario.
2. Export each token as an environment variable.
3. Create the minimal config only if needed.
4. Run the AGMH command.
5. Inspect the expected output path.
6. Inspect state with `agmh state --config agmh.config.toml` if a config file was used.

## Commands

```bash
agmh --help
```

## Expected Result

Describe the local paths, remote repositories, notifications, and state entries the user should expect.

## Notes

Add only details that are specific to this example.

