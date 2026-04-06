# WebWatcher v0.4.0

WebWatcher v0.4.0 improves signal quality by reducing false positives from unstable page content, while keeping the project small, local-first, and easy to deploy.

## Highlights

- Added **noise filtering rules** for unstable page content
- Added **`--noise-rules` CLI support** and monitor storage support
- Reduced false positives from digits, dates, and regex-matched noise
- Kept support for **CSS selector-based monitoring**
- Kept support for **Playwright-based monitoring** on JavaScript-rendered pages
- Kept support for **JSON config files**, **SQLite history**, and **Feishu webhook notifications**
- Kept support for **Docker** and **docker-compose** deployment

## Why this release matters

A lot of webpage monitoring noise comes from unstable fragments such as dates, counters, or rotating values.

This release makes WebWatcher more practical for real-world use by letting you filter those noisy changes before they trigger unnecessary diffs and alerts.

You can now more reliably:
- watch a whole page
- monitor only part of a page
- reduce noisy diffs from unstable content
- support JS-rendered pages
- keep local history in SQLite
- send alerts to Feishu
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
  --url https://example.com \
  --selector 'h1' \
  --noise-rules ignore_digits,ignore_dates \
  --name "Stable Example"

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

This project is still intentionally small.
There is no user system, no SaaS panel, and no heavy web dashboard.

If you use Playwright mode, install browser binaries first:

```bash
python -m playwright install chromium
```
