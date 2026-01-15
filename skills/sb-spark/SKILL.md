---
name: sb-spark
description: Post messages to Slack. Use when user says "make a spark", "spark this", "send a spark", "spark it to Slack", or any request containing "spark" referring to Slack posting.
---

# SB Spark

Post messages to Slack channels via incoming webhooks.

## Setup

1. Create a Slack app at https://api.slack.com/apps
2. Enable "Incoming Webhooks" and add one to your channel
3. Set env vars:
   ```bash
   export PW_SPARK_WEBHOOK_URL="https://hooks.slack.com/services/..."
   export PW_SPARK_CHANNEL="#your-channel"
   ```

## Usage

Post a message using the script:

```bash
python3 ~/.claude/skills/sb-spark/post.py "Your message here"
```

Or pipe content:

```bash
echo "Message content" | python3 ~/.claude/skills/sb-spark/post.py
```

### Formatting Options

```bash
# With custom channel (if webhook allows)
python3 ~/.claude/skills/sb-spark/post.py --channel "#reports" "Message"

# With title block
python3 ~/.claude/skills/sb-spark/post.py --title "CI Report" "Body content"

# Markdown formatting (Slack mrkdwn)
python3 ~/.claude/skills/sb-spark/post.py "*Bold* and _italic_ and \`code\`"
```

### Slack Formatting Reference

- Bold: `*text*`
- Italic: `_text_`
- Code: `` `text` ``
- Code block: ``` ```text``` ```
- Link: `<url|display text>`
- User mention: `<@USER_ID>`
- Channel: `<#CHANNEL_ID>`
- Bullet list: lines starting with `• ` or `- `

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PW_SPARK_WEBHOOK_URL` | Yes | Incoming webhook URL |
| `PW_SPARK_CHANNEL` | No | Default channel (can override with --channel) |
