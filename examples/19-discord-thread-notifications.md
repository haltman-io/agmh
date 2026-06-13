# Discord Thread Notifications

## Scenario

A user wants AGMH notifications to land inside a specific Discord thread instead of the base channel.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No Discord webhook or config file exists yet.

## Minimum Assumptions

1. The source is public GitHub.
2. Use `download` so no destination token is needed.
3. Discord notification requires a webhook URL and thread ID.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `DISCORD_WEBHOOK_URL` | Yes | Sends messages to Discord. |

## Minimal Configuration

```bash
agmh init-config --path agmh.config.toml
```

Replace it with:

```toml
mode = "download"
sources_file = "sources.txt"

[backup]
local_dir = "backups"

[notifications]
enabled = true
events = ["start", "finish", "local_saved", "error"]

[[webhooks]]
name = "discord-thread"
platform = "discord"
url_env = "DISCORD_WEBHOOK_URL"
thread_id = "123456789012345678"
events = ["start", "finish", "local_saved", "error"]
```

Create `sources.txt`:

```text
https://github.com/example-user/
```

## Algorithm

1. Create a Discord webhook for the target channel.
2. Copy the webhook URL.
3. Copy the Discord thread ID.
4. Export the webhook URL.
5. Put the thread ID in `agmh.config.toml`.
6. Run AGMH.

## Commands

```bash
export DISCORD_WEBHOOK_URL="paste_discord_webhook_url_here"

agmh run --config agmh.config.toml --verbose
```

## Expected Result

AGMH downloads public GitHub repositories and posts selected events into the configured Discord thread.

