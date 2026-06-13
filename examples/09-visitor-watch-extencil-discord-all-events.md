# Visitor Watches GitHub User with Discord Notifications

## Scenario

A visitor wants to watch the public GitHub profile `extencil` and notify Discord for every AGMH event the tool supports.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token, Discord webhook, or config file exists yet.

## Minimum Assumptions

1. The user is a visitor.
2. Only public repositories are in scope.
3. No destination is required.
4. Use `download` as the watch action so AGMH has a useful action that does not need destinations.
5. Discord notification requires a config file.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `DISCORD_WEBHOOK_URL` | Yes | Lets AGMH send Discord messages. |

## Minimal Configuration

```bash
agmh init-config --path agmh.config.toml
```

Replace it with:

```toml
mode = "watching"
sources_file = "sources.txt"

[backup]
local_dir = "backups"

[watch]
interval_seconds = 300
action = "download"
initial_run = true
once = false

[notifications]
enabled = true
events = ["*"]

[[webhooks]]
name = "discord-all-events"
platform = "discord"
url_env = "DISCORD_WEBHOOK_URL"
events = ["*"]
```

Create `sources.txt`:

```text
https://github.com/extencil/
```

## Algorithm

1. Create a Discord webhook in the target channel.
2. Export the webhook URL.
3. Create the minimal config and `sources.txt`.
4. Run one watch cycle to test.
5. Run continuously after the test succeeds.

## Commands

```bash
export DISCORD_WEBHOOK_URL="paste_discord_webhook_url_here"

agmh watching --config agmh.config.toml --watch-once --verbose
agmh watching --config agmh.config.toml --verbose
```

## Expected Result

AGMH sends Discord notifications for supported events such as `start`, `finish`, `local_saved`, `watch_check`, `watch_update`, `watch_none`, and `error`.

