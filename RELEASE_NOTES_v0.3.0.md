# WebWatcher v0.3.0

WebWatcher v0.3.0 turns the project from a basic MVP into a more practical self-hosted monitoring tool.

## Highlights

- Added **CSS selector-based monitoring**
- Added **noise filtering** for unstable page content
- Added **Playwright-based monitoring** for JavaScript-rendered pages
- Added **JSON config file support**
- Added **Feishu webhook notifications**
- Added **Dockerfile** and **docker-compose** support
- Improved README and launch materials for release

## Why this release matters

This version is now good enough to cover a lot of real-world monitoring cases without introducing a heavy architecture.

You can:
- watch a whole page
- monitor only part of a page
- reduce noisy diffs
- support JS-rendered pages
- keep local history in SQLite
- plug notifications into Feishu
- deploy locally or with Docker

## Example

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
cp webwatcher.example.json webwatcher.json
python app.py init

python app.py add \
  --url https://example.com/dashboard \
  --name "Dynamic Example" \
  --fetch-mode playwright \
  --wait-for-selector '#app' \
  --wait-after-load-ms 1500

python app.py check
```

## Good fit for

- job page monitoring
- announcement pages
- docs / changelog updates
- competitor pages
- rankings / listings
- simple internal dashboards

## Notes

This is still intentionally small.
There is no user system, no SaaS panel, and no heavy web dashboard yet.

If you use Playwright mode, install browser binaries first:

```bash
python -m playwright install chromium
```
