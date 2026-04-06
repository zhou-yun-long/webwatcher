# WebWatcher

[![CI](https://github.com/zhou-yun-long/webwatcher/actions/workflows/ci.yml/badge.svg)](https://github.com/zhou-yun-long/webwatcher/actions/workflows/ci.yml)
[![Latest Release](https://img.shields.io/github/v/release/zhou-yun-long/webwatcher)](https://github.com/zhou-yun-long/webwatcher/releases)

Track webpage changes with Python + SQLite.

WebWatcher is a minimal open-source website change monitor for people who just want to watch a page, detect updates, and keep a simple local history — without setting up a heavy monitoring platform.

## Why it exists

Most people do **not** need a giant monitoring stack.
They usually just want to:

- watch a webpage for changes
- monitor only part of a page with a CSS selector
- reduce false positives from unstable content
- support JavaScript-rendered pages when needed
- store change history locally
- optionally send change alerts to Feishu

WebWatcher is built for that exact use case.

## Highlights

- Simple CLI workflow
- SQLite storage
- CSS selector-based monitoring
- Noise filtering rules
- Playwright support for dynamic pages
- JSON config file support
- Optional Feishu webhook notifications
- Docker / docker-compose support

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
cp webwatcher.example.json webwatcher.json
python app.py init
python app.py add --url https://example.com --name "Example Home"
python app.py check
```

## Example commands

### Static page

```bash
python app.py add \
  --url https://example.com \
  --name "Example Home"
```

### Partial page monitoring

```bash
python app.py add \
  --url https://news.ycombinator.com \
  --selector '.titleline' \
  --name "HN Titles"
```

### Noise filtering

```bash
python app.py add \
  --url https://example.com \
  --selector 'h1' \
  --noise-rules ignore_digits,ignore_dates \
  --name "Stable Example"
```

### JavaScript-rendered page

```bash
python app.py add \
  --url https://example.com/dashboard \
  --name "Dynamic Example" \
  --fetch-mode playwright \
  --wait-for-selector '#app' \
  --wait-after-load-ms 1500
```

### Common follow-up commands

```bash
python app.py check
python app.py list
python app.py events --limit 20
```

## Good fit for

- job pages
- announcement pages
- docs / changelog pages
- competitor pages
- rankings / listings
- simple internal dashboards

## Install

### Local Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

### Docker

```bash
docker build -t webwatcher .
docker run --rm -v $(pwd):/app -w /app webwatcher python app.py init
docker run --rm -v $(pwd):/app -w /app webwatcher python app.py check
```

## Config

Create a config file:

```bash
cp webwatcher.example.json webwatcher.json
```

Default config path:
- `./webwatcher.json`

Override with environment variable:

```bash
export WEBWATCHER_CONFIG=/path/to/webwatcher.json
```

Example config:

```json
{
  "database": {
    "path": "data/webwatcher.sqlite3"
  },
  "fetch": {
    "timeout": 20,
    "mode": "static",
    "wait_for_selector": null,
    "wait_after_load_ms": 0
  },
  "notifications": {
    "feishu_webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
  }
}
```

Supported config keys:
- `database.path`
- `fetch.timeout`
- `fetch.mode`
- `fetch.wait_for_selector`
- `fetch.wait_after_load_ms`
- `notifications.feishu_webhook_url`

Environment override:
- `FEISHU_WEBHOOK_URL` overrides config file webhook
- `WEBWATCHER_CONFIG` overrides config file path

See current resolved config:

```bash
python app.py config-show
```

## Feishu notification

Set a Feishu bot webhook in either:
- `webwatcher.json` → `notifications.feishu_webhook_url`
- or environment variable `FEISHU_WEBHOOK_URL`

Then run checks as usual:

```bash
python app.py check
```

## CLI

```bash
python app.py init
python app.py add --url <URL> --name "Monitor Name"
python app.py list
python app.py check
python app.py events --limit 20
python app.py config-show
```

### Add monitor options

```bash
python app.py add --url <URL> --interval 600 --name "Monitor Name"
python app.py add --url <URL> --selector '.content' --name "Monitor Name"
python app.py add --url <URL> --selector '.content' --noise-rules ignore_digits,ignore_dates --name "Monitor Name"
python app.py add --url <URL> --fetch-mode playwright --wait-for-selector '.ready' --name "Monitor Name"
```

Supported fetch modes:
- `static`
- `playwright`

Supported noise rules:
- `ignore_digits`
- `ignore_dates`
- `regex:<pattern>`

## What this version does not include

- user accounts
- multi-tenant SaaS
- payments
- Telegram / email notifications
- web dashboard

That is intentional.

## Release status

### v0.4.0
- Noise filtering rules ✅
- `--noise-rules` CLI support ✅
- Reduced false positives from unstable content ✅

### Previously in v0.3.0
- Playwright support for dynamic pages ✅
- Docker / Compose ✅
- Config file support ✅

### Next
- better packaging / release polish
- web dashboard
- multi-user auth
- multi-channel notifications
- AI-generated change summary

## License

MIT
