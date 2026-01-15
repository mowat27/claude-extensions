#!/usr/bin/env python3
"""Post messages to Slack via incoming webhook."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def post_to_slack(message: str, title: str | None = None, channel: str | None = None) -> dict:
    """Post a message to Slack webhook."""
    webhook_url = os.environ.get("PW_SPARK_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("PW_SPARK_WEBHOOK_URL environment variable not set")

    # Use provided channel or fall back to env var
    channel = channel or os.environ.get("PW_SPARK_CHANNEL")

    blocks = []

    if title:
        blocks.append({
            "type": "header",
            "text": {"type": "plain_text", "text": title, "emoji": True}
        })

    # Split long messages into multiple sections (Slack limit: 3000 chars per block)
    max_len = 2900
    chunks = [message[i:i+max_len] for i in range(0, len(message), max_len)]

    for chunk in chunks:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": chunk}
        })

    payload = {"blocks": blocks}

    # Fallback text for notifications
    payload["text"] = title or message[:100]

    if channel:
        payload["channel"] = channel

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            return {"ok": True, "status": response.status}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": e.read().decode()}


def main():
    parser = argparse.ArgumentParser(description="Post to Slack webhook")
    parser.add_argument("message", nargs="?", help="Message to post (or pipe via stdin)")
    parser.add_argument("--title", "-t", help="Header title for the message")
    parser.add_argument("--channel", "-c", help="Override channel (default: PW_SPARK_CHANNEL env var)")
    args = parser.parse_args()

    # Get message from arg or stdin
    if args.message:
        message = args.message
    elif not sys.stdin.isatty():
        message = sys.stdin.read().strip()
    else:
        parser.error("No message provided. Pass as argument or pipe via stdin.")

    result = post_to_slack(message, title=args.title, channel=args.channel)

    if result["ok"]:
        print("Posted to Slack")
    else:
        print(f"Failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
