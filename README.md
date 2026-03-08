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

## Demo Flow

```bash
python app.py init
python app.py add --url https://example.com --interval 600 --name "Example Home"
python app.py check
python app.py list
python app.py events
```

## Project Structure

```text
webwatcher/
  app.py              # CLI entry
  watcher.py          # Check workflow
  storage.py          # SQLite storage
  fetcher.py          # Web fetching and cleanup
  notifier.py         # Feishu notification
  models.py           # Data models
  requirements.txt
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
```

If not, you can still install directly in a disposable environment.

### 2) Initialize database

```bash
python app.py init
```

### 3) Add a monitor

```bash
python app.py add --url https://example.com --interval 600 --name "Example Home"
```

### 4) Run a check

```bash
python app.py check
```

### 5) Show monitor list

```bash
python app.py list
```

### 6) Show recent events

```bash
python app.py events --limit 20
```

## Feishu Notification

Set a Feishu bot webhook in environment variables:

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxxx"
```

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
- Playwright rendering for JS-heavy pages
- CSS selector mode
- Docker deployment
- Web dashboard

Those are intentional follow-up versions.

## Roadmap

### v0.2
- Feishu webhook notification ✅
- CSS selector extraction
- Noise filtering

### v0.3
- Playwright support for dynamic pages
- Docker / Compose
- Config file support

### v0.4
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
