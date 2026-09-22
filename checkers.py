"""Pluggable slot checkers."""
from __future__ import annotations
import requests


class SlotResult:
    def __init__(self, post: str, available: bool, detail: str = "", dates: list | None = None):
        self.post = post
        self.available = available
        self.detail = detail
        self.dates = dates or []

    def key(self) -> str:
        return f"{self.post}:{','.join(sorted(self.dates))}"


class BaseChecker:
    """Subclass and implement check(post) for login-walled sites."""

    def check(self, post: str) -> SlotResult:  # pragma: no cover
        raise NotImplementedError


class HttpJsonChecker(BaseChecker):
    """Example checker hitting a JSON endpoint.

    config per post: {"url": "...", "available_key": "slots",
                      "dates_key": "dates"}
    """

    def __init__(self, post_config: dict):
        self.cfg = post_config

    def check(self, post: str) -> SlotResult:
        cfg = self.cfg.get(post, {})
        url = cfg.get("url", "")
        if not url:
            return SlotResult(post, False, "no url configured")
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            data = r.json()
        except Exception as e:  # network/parse failure = unknown, not available
            return SlotResult(post, False, f"check failed: {e}")
        dates = data.get(self.cfg.get("dates_key", "dates"), []) or []
        available = bool(dates) or bool(data.get(self.cfg.get("available_key", "slots")))
        return SlotResult(post, available, detail=f"http {r.status_code}", dates=list(dates))
