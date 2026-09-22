# Visa Slot Notifier

Poll a visa appointment page (or any slot API) and get notified the moment a
slot opens. Built with a pluggable checker interface so you can adapt it to
any country/post without rewriting the loop.

## Quick start

```bash
pip install -r requirements.txt
cp config.example.yaml config.yaml  # fill in your posts + webhook
python watcher.py --config config.yaml --once      # single check
python watcher.py --config config.yaml             # poll loop
```

## How it works

- `watcher.py` — poll loop, state file (`.slots_seen.json`), cooldowns
- `checkers.py` — `BaseChecker` interface + `HttpJsonChecker` example.
  Subclass it for login-walled sites (playwright/selenium) — the loop stays the same.
- `notifier.py` — console + generic webhook (Slack/Discord/ntfy) notifications

## Ethics / ToS

Only poll at a respectful interval (default 10 min, configurable) and follow
the target site's terms. This tool checks availability; it does not auto-book
or bypass CAPTCHAs.
