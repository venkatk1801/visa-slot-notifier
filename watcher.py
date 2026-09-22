#!/usr/bin/env python3
"""Poll loop for visa slot watching."""
import argparse
import json
import os
import time
from datetime import datetime, timezone

import yaml

from checkers import HttpJsonChecker
from notifier import notify_all

STATE_FILE = ".slots_seen.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def run_once(config, checker):
    state = load_state()
    found = []
    for post in config.get("posts", []):
        result = checker.check(post)
        key = result.key()
        if result.available and state.get(post) != key:
            found.append(result)
            state[post] = key
            msg = f"SLOT OPEN at {post}: {', '.join(result.dates) or result.detail}"
            notify_all(msg, config.get("webhook_url", ""))
        elif not result.available:
            print(f"[{datetime.now(timezone.utc):%H:%M:%SZ}] {post}: none ({result.detail})",
                  flush=True)
    save_state(state)
    return found


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="config.yaml")
    p.add_argument("--once", action="store_true")
    args = p.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    checker = HttpJsonChecker(config.get("checker_config", {}))
    interval = int(config.get("poll_interval_seconds", 600))

    if args.once:
        run_once(config, checker)
        return

    print(f"watching {len(config.get('posts', []))} posts every {interval}s", flush=True)
    while True:
        try:
            run_once(config, checker)
        except Exception as e:
            print(f"[watcher] loop error: {e}", flush=True)
        time.sleep(interval)


if __name__ == "__main__":
    main()
