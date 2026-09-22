"""Notifications: console + generic webhook."""
from __future__ import annotations
import json
import urllib.request


def notify_console(message: str) -> None:
    print(f"[notifier] {message}", flush=True)


def notify_webhook(webhook_url: str, message: str, timeout: int = 15) -> bool:
    if not webhook_url:
        return False
    payload = {"text": message}
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 300
    except Exception as e:
        print(f"[notifier] webhook failed: {e}", flush=True)
        return False


def notify_all(message: str, webhook_url: str = "") -> None:
    notify_console(message)
    if webhook_url:
        notify_webhook(webhook_url, message)
