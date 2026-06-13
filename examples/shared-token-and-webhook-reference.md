# Shared Token and Webhook Reference

Use this reference when an example requires credentials. Keep credentials in environment variables and do not commit real tokens, webhook URLs, `.agmh/`, `backups/`, `agmh.config.toml`, `sources.txt`, or `destinations.txt`.

## GitHub Source Tokens

1. Use a GitHub personal access token when AGMH must see private repositories, member-only organization repositories, or avoid low anonymous rate limits.
2. For public-only discover or download, do not create a token unless the example says to.
3. Minimum source intent: read repository metadata and clone repositories the account can access.
4. Export it:

```bash
export GITHUB_TOKEN="paste_github_token_here"
```

Reference: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

## GitLab Destination Tokens

1. Use a GitLab token when AGMH must create repositories and push mirrors.
2. Minimum destination intent: API access to create projects in the target namespace and Git write access to push.
3. Export it:

```bash
export GITLAB_TOKEN="paste_gitlab_token_here"
```

Reference: https://docs.gitlab.com/user/profile/personal_access_tokens/

## Codeberg or Forgejo Destination Tokens

1. Use a Codeberg or Forgejo access token when AGMH must create repositories and push mirrors.
2. Minimum destination intent: API write access for repository creation and Git write access for push.
3. For Codeberg, AGMH uses the Forgejo adapter, so `platform = "forgejo"` is correct.
4. Export it:

```bash
export CODEBERG_TOKEN="paste_codeberg_token_here"
```

Reference: https://docs.codeberg.org/advanced/access-token/

## SourceHut Destination Tokens and SSH

1. Use a SourceHut token when AGMH must create repositories through the SourceHut API.
2. SourceHut push is usually best over SSH.
3. Add your SSH public key to SourceHut before running the example.
4. Export the API token:

```bash
export SOURCEHUT_TOKEN="paste_sourcehut_token_here"
```

5. Configure the SSH identity in `[git]` when the default SSH key is not enough.

Reference: https://sourcehut.org/

## Bitbucket Source Tokens

1. Use a Bitbucket API token when a workspace requires authentication or includes private repositories.
2. AGMH accepts Bitbucket credentials as `bitbucket:USERNAME_OR_EMAIL:env:BITBUCKET_TOKEN`.
3. Export it:

```bash
export BITBUCKET_TOKEN="paste_bitbucket_token_here"
```

Reference: https://support.atlassian.com/bitbucket-cloud/docs/api-tokens/

## Discord Webhooks

1. In Discord, create or choose a server channel.
2. Open channel or server integrations and create a webhook for that channel.
3. Copy the webhook URL.
4. Store it in an environment variable:

```bash
export DISCORD_WEBHOOK_URL="paste_discord_webhook_url_here"
```

5. For a specific thread, use `thread_id` in the AGMH webhook config.

References:
- https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
- https://docs.discord.com/developers/resources/webhook

## Telegram Bot Notifications

1. Open Telegram and start a chat with `@BotFather`.
2. Create a bot and copy the bot token.
3. Add the bot to the target chat, group, or channel.
4. Get the target chat ID.
5. Export both values:

```bash
export TELEGRAM_BOT_TOKEN="paste_telegram_bot_token_here"
export TELEGRAM_CHAT_ID="paste_chat_id_here"
```

Reference: https://core.telegram.org/bots/tutorial

