# Watch GitHub Organization, Download Updates, Notify Telegram

## Scenario

The GitHub user `skyperthc` wants to watch the GitHub organization `phrackzine`, download source files when AGMH detects supported updates, and notify Telegram when the workflow starts and finishes.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token, Telegram credentials, or config file exists yet.

## Minimum Assumptions

1. The scenario does not say `skyperthc` is a `phrackzine` member.
2. Only public repositories are in scope.
3. No GitHub token is required.
4. Telegram requires a bot token and chat ID.
5. Use `watching` with action `download`.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Yes | Sends Telegram notifications. |
| `TELEGRAM_CHAT_ID` | Yes | Selects the Telegram chat. |

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
events = ["start", "finish", "watch_update", "local_saved", "error"]

[[webhooks]]
name = "telegram-watch-download"
platform = "telegram"
bot_token_env = "TELEGRAM_BOT_TOKEN"
chat_id_env = "TELEGRAM_CHAT_ID"
events = ["start", "finish", "watch_update", "local_saved", "error"]
```

Create `sources.txt`:

```text
https://github.com/phrackzine/
```

## Algorithm

1. Create a Telegram bot with BotFather.
2. Add the bot to the target chat and get the chat ID.
3. Export Telegram credentials.
4. Create the minimal config and `sources.txt`.
5. Run one watch cycle to test.
6. Run continuously after the notification flow is verified.

## Commands

```bash
export TELEGRAM_BOT_TOKEN="paste_telegram_bot_token_here"
export TELEGRAM_CHAT_ID="paste_telegram_chat_id_here"

agmh watching --config agmh.config.toml --watch-once --verbose
agmh watching --config agmh.config.toml --verbose
```

## Expected Result

AGMH watches `phrackzine`, downloads changed repositories as working trees, and sends Telegram notifications for startup, detected updates, saved local downloads, errors, and finish events.

