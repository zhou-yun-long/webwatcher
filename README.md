# WebWatcher

Minimal open-source website change monitor built with Python + SQLite.

给一个 URL，WebWatcher 会抓取页面文本、生成内容哈希，并在页面发生变化时记录事件。这个版本专注于 **简单、可运行、适合开源首发**。

## Why WebWatcher?

很多人并不需要一个复杂的大监控平台，他们只想要：

- 监控一个网页有没有变
- 知道什么时候变了
- 后续能接消息通知
- 能自己部署、自己改

WebWatcher 就是这个基础版。

## Features

- Add monitor tasks from CLI
- Fetch webpage text content
- Detect changes with SHA-256 hash
- Store monitor state in SQLite
- Record change events
- Run manual checks
- List monitors and events
- Optional Feishu webhook notifications
- Optional CSS selector monitoring
- Optional noise filtering rules for unstable content
- Optional Playwright mode for JavaScript-rendered pages
- JSON config file support for database / fetch / notifications

## Demo Flow

```bash
cp webwatcher.example.json webwatcher.json
python app.py init
python app.py add --url https://example.com --interval 600 --name "Example Home"
python app.py add --url https://news.ycombinator.com --selector '.titleline' --interval 600 --name "HN Titles"
python app.py add --url https://example.com --selector 'h1' --noise-rules ignore_digits,ignore_dates --interval 600 --name "Stable Example"
python app.py add --url https://example.com --fetch-mode playwright --wait-for-selector '#app' --wait-after-load-ms 1500 --name "Dynamic Example"
python app.py config-show
python app.py check
python app.py list
python app.py events
```

## Project Structure

```text
webwatcher/
  app.py
  config.py           # Config loader
  watcher.py          # Check workflow
  storage.py          # SQLite storage
  fetcher.py          # Web fetching and cleanup
  notifier.py         # Feishu notification
  models.py           # Data models
  requirements.txt
  webwatcher.example.json
  Dockerfile
  docker-compose.yml
  .gitignore
  LICENSE
  README.md
```

## Quick Start

### 1) Install dependencies

If your system supports virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

If not, you can still install directly in a disposable environment.

### 2) Create config file

```bash
cp webwatcher.example.json webwatcher.json
```

Default config path:
- `./webwatcher.json`

You can also override it with environment variable:

```bash
export WEBWATCHER_CONFIG=/path/to/webwatcher.json
```

### 3) Initialize database

```bash
python app.py init
```

### 4) Add a monitor

```bash
python app.py add --url https://example.com --interval 600 --name "Example Home"
```

Monitor a specific page section with CSS selector:

```bash
python app.py add --url https://news.ycombinator.com --selector '.titleline' --interval 600 --name "HN Titles"
```

Reduce false positives with noise filtering:

```bash
python app.py add --url https://example.com --selector 'h1' --noise-rules ignore_digits,ignore_dates --interval 600 --name "Stable Example"
```

Monitor JavaScript-rendered content with Playwright:

```bash
python app.py add \
  --url https://example.com/dashboard \
  --name "Dynamic Example" \
  --fetch-mode playwright \
  --wait-for-selector '#app' \
  --wait-after-load-ms 1500
```

### 5) Show current config

```bash
python app.py config-show
```

### 6) Run a check

```bash
python app.py check
```

### 7) Show monitor list

```bash
python app.py list
```

### 8) Show recent events

```bash
python app.py events --limit 20
```

## Config File

Example:

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
- `database.path`: SQLite file path
- `fetch.timeout`: default fetch timeout in seconds
- `fetch.mode`: `static` or `playwright`
- `fetch.wait_for_selector`: default Playwright wait selector
- `fetch.wait_after_load_ms`: default extra wait time after page load
- `notifications.feishu_webhook_url`: Feishu bot webhook URL

Environment override:
- `FEISHU_WEBHOOK_URL` overrides config file webhook
- `WEBWATCHER_CONFIG` overrides config file path

## Feishu Notification

Set a Feishu bot webhook in either:
- `webwatcher.json` → `notifications.feishu_webhook_url`
- or environment variable `FEISHU_WEBHOOK_URL`

Then run checks as usual:

```bash
python app.py check
```

When a monitor changes, WebWatcher will send a simple text alert to Feishu.

## CLI Commands

### Initialize database

```bash
python app.py init
```

### Add monitor

```bash
python app.py add --url <URL> --interval 600 --name "Monitor Name"
```

### Add selector-based monitor

```bash
python app.py add --url <URL> --selector '.content' --interval 600 --name "Monitor Name"
```

### Add noise filtering rules

```bash
python app.py add --url <URL> --selector '.content' --noise-rules ignore_digits,ignore_dates --interval 600 --name "Monitor Name"
```

### Add Playwright-based monitor

```bash
python app.py add --url <URL> --name "Monitor Name" --fetch-mode playwright --wait-for-selector '.ready'
```

### Show current config

```bash
python app.py config-show
```

Supported fetch modes:
- `static`
- `playwright`

Supported noise rules:
- `ignore_digits`
- `ignore_dates`
- `regex:<pattern>`

### Run checks

```bash
python app.py check
```

### List monitors

```bash
python app.py list
```

### List events

```bash
python app.py events --limit 20
```

## What this version does NOT include

- User accounts
- Multi-tenant SaaS
- Payments
- Telegram / email notifications
- Web dashboard

Those are intentional follow-up versions.

## Roadmap

### v0.3
- Playwright support for dynamic pages ✅
- Docker / Compose ✅
- Config file support ✅

### v0.4
- Better release packaging
- Web dashboard
- Multi-user auth
- Multi-channel notifications
- AI-generated change summary

## Monetization Ideas

- Hosted SaaS version
- Team notifications and collaboration
- Advanced rules / selector mode / screenshots
- AI summary and change classification
- Custom monitoring solutions for businesses

## Good first open-source release because

- Easy to understand in 1 minute
- Solves a real problem
- Has a clean MVP boundary
- Easy to demo
- Easy to expand into a product

## License

MIT
