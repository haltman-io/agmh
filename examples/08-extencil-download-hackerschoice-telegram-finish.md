# Download Public GitHub Organization and Notify Telegram on Finish

## Scenario

The GitHub user `extencil` wants to download public repositories from `hackerschoice` and send a Telegram notification when AGMH finishes.

## Starting Point

1. AGMH is installed.
2. `agmh --help` works.
3. No GitHub token, Telegram credentials, or config file exists yet.

## Minimum Assumptions

1. `extencil` is not described as a `hackerschoice` member.
2. Only public repositories are in scope.
3. No GitHub token is required.
4. Telegram notification requires a config file.

## Required Credentials

| Credential | Required | Why |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Yes | Lets AGMH send a Telegram message through the bot. |
| `TELEGRAM_CHAT_ID` | Yes | Tells AGMH which chat receives the message. |

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
events = ["finish", "error"]

[[webhooks]]
name = "telegram-finish"
platform = "telegram"
bot_token_env = "TELEGRAM_BOT_TOKEN"
chat_id_env = "TELEGRAM_CHAT_ID"
events = ["finish", "error"]
```

Create `sources.txt`:

```text
https://github.com/hackerschoice/
```

## Algorithm

1. Create a Telegram bot with BotFather.
2. Add the bot to the target chat.
3. Get the chat ID.
4. Export `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
5. Create the minimal config and source file.
6. Run AGMH.
7. Verify the Telegram finish notification.

## Commands

```bash
export TELEGRAM_BOT_TOKEN="paste_telegram_bot_token_here"
export TELEGRAM_CHAT_ID="paste_telegram_chat_id_here"

agmh run --config agmh.config.toml --verbose
```

## Expected Result

AGMH downloads public repositories as working trees and sends a Telegram message when the run finishes or errors.

