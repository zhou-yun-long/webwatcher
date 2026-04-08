# Contributing

Thanks for your interest in WebWatcher.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
cp webwatcher.example.json webwatcher.json
python app.py init
python app.py add --url https://example.com --interval 600 --name "Example Home"
python app.py check
python app.py list
python app.py events --limit 20
```

## Project notes

- SQLite database files are intentionally ignored
- Local config lives in `webwatcher.json` and is ignored by git
- Use `webwatcher.example.json` when documenting config changes
- Playwright is optional at runtime, but needed for dynamic page workflows

## Pull Requests

- Keep changes focused
- Update README when behavior changes
- Update example config or release notes when relevant
- Add clear reproduction steps for bug fixes
