# Project Handover

## 1. 项目概览
- 项目名称：WebWatcher
- 用途 / 目标：一个轻量、自托管的网页变更监控工具。核心能力是抓取网页文本、记录内容哈希、检测变化，并可通过飞书 webhook 发送提醒。
- 当前状态：已完成开源版 `v0.3.0` 的主要能力收口，可本地运行，也提供 Docker 运行路径。
- 仓库 / 目录：`projects/webwatcher`
- 交接范围：整个 WebWatcher 仓库（CLI、抓取逻辑、存储、配置、Docker、发布材料）

## 2. 当前进展
- 已完成：
  - 基础 CLI：`init` / `add` / `list` / `check` / `events` / `config-show`
  - SQLite 存储监控任务和变化事件
  - 静态网页抓取
  - CSS selector 定向监控
  - noise filtering（`ignore_digits` / `ignore_dates` / `regex:<pattern>`）
  - Playwright 动态页面抓取
  - JSON 配置文件支持（`webwatcher.json`）
  - 飞书 webhook 通知
  - Docker / docker-compose
  - v0.3.0 发布材料（README / release notes / launch 文案 / VERSION）
- 进行中：无明确进行中的功能开发；仓库当前工作树干净。
- 未开始：
  - Web dashboard
  - 多用户 / SaaS 化
  - 多渠道通知（Telegram / email 等）
  - AI 生成变更摘要
- 最近关键改动：
  - `cc38838` Polish release materials for v0.3.0
  - `5a7e43b` Add JSON config file support
  - `9e73bac` Add Playwright support for dynamic pages
  - `4c073d2` Add noise filtering rules for unstable content

## 3. 技术栈与结构
- 主要语言 / 框架：Python 3
- 核心依赖：
  - `requests`
  - `beautifulsoup4`
  - `playwright`
  - `sqlite3`（标准库）
- 关键目录 / 文件：
  - `app.py`：CLI 入口
  - `watcher.py`：执行检查流程
  - `fetcher.py`：静态 / Playwright 抓取与规范化
  - `storage.py`：SQLite schema 与读写
  - `config.py`：配置文件加载
  - `notifier.py`：飞书通知
  - `models.py`：数据模型
  - `webwatcher.example.json`：配置示例
  - `Dockerfile` / `docker-compose.yml`：容器运行路径
- 入口文件 / 服务入口：
  - 本地：`python app.py <command>`
  - Docker：`python app.py check`

## 4. 本地运行
- 环境要求：
  - Python 3.10+（当前 Dockerfile 用的是 Python 3.12）
  - 可安装 Playwright 及 Chromium 浏览器
- 安装步骤：
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  python -m playwright install chromium
  cp webwatcher.example.json webwatcher.json
  ```
- 初始化数据库：
  ```bash
  python app.py init
  ```
- 添加监控项：
  ```bash
  python app.py add --url https://example.com --name "Example Home"
  ```
- 执行检查：
  ```bash
  python app.py check
  ```
- 查看监控：
  ```bash
  python app.py list
  python app.py events --limit 20
  python app.py config-show
  ```
- 常见启动问题：
  - 若 Playwright 报缺浏览器，执行：`python -m playwright install chromium`
  - 若飞书通知无效，先检查 `FEISHU_WEBHOOK_URL` 或 `webwatcher.json`
  - 若数据库位置异常，检查 `WEBWATCHER_CONFIG` 是否覆盖了默认配置文件路径

## 5. 配置与环境变量
- 配置文件位置：默认 `./webwatcher.json`
- 配置示例文件：`webwatcher.example.json`
- 支持的关键配置：
  - `database.path`
  - `fetch.timeout`
  - `fetch.mode`
  - `fetch.wait_for_selector`
  - `fetch.wait_after_load_ms`
  - `notifications.feishu_webhook_url`
- 必填环境变量：无严格必填；但如需飞书通知，可使用：
  - `FEISHU_WEBHOOK_URL`
- 可选环境变量：
  - `WEBWATCHER_CONFIG`：覆盖默认配置文件路径
- 开发 / 测试 / 生产差异：当前仓库未显式区分多环境，只通过配置文件路径和环境变量实现差异。
- 密钥 / 敏感信息说明：
  - `webwatcher.json` 不应提交真实 webhook
  - 当前 `.gitignore` 已忽略 `webwatcher.json` 和 `data/`

## 6. 部署与发布
- 当前部署方式：
  - 本地 Python 运行
  - Docker 镜像运行
  - `docker-compose` 单服务方式运行
- Docker 构建：
  ```bash
  docker build -t webwatcher .
  ```
- Docker 运行：
  ```bash
  docker run --rm -v $(pwd):/app -w /app webwatcher python app.py init
  docker run --rm -v $(pwd):/app -w /app webwatcher python app.py check
  ```
- docker-compose：
  ```bash
  docker-compose up --build
  ```
- 发布流程：
  - 已整理 v0.3.0 发布材料
  - 版本文件：`VERSION`
  - release notes：`RELEASE_NOTES_v0.3.0.md`
  - launch 文案：`GITHUB_LAUNCH.md`
- 最近稳定版本：`v0.3.0`
- 回滚方式：当前未定义正式回滚流程；可基于 git tag `v0.3.0` 回退。
- CI/CD 说明：仓库中未看到现成 GitHub Actions / CI workflow。

## 7. 外部依赖
- 数据库：SQLite（本地文件）
- 第三方 API：
  - 飞书机器人 webhook（可选）
- 浏览器依赖：Playwright Chromium（动态页面抓取时需要）
- 队列 / 缓存 / 定时任务：无
- 其他对接系统：无强绑定系统

## 8. 风险与坑
- 已知问题：
  - Docker 路径虽然已补齐，但当前更充分验证的是本机 Python 路径；容器稳定性仍建议再做一次专门验收。
  - `CHANGELOG.md` 当前写法里 `v0.4.0` 放了 noise filtering，但仓库版本文件是 `0.3.0`，版本叙事存在一点轻微不一致，后续最好统一。
- 脆弱模块：
  - Playwright 抓取路径容易受目标页面加载方式、选择器稳定性、浏览器依赖影响
  - noise rules 目前是轻量规则，复杂页面可能仍有误报
- 运行风险：
  - 目标网站结构变化后，selector 监控会直接失效或误报
  - 飞书 webhook 配置不正确时不会发送通知
- 历史坑点 / 暂时规避：
  - 动态页面不能只靠 requests，需要切到 `--fetch-mode playwright`
  - 如果页面文本中含时间、数字等高频变化内容，优先加 `--noise-rules`
  - 项目目录中存在 `webwatcher.sqlite3` 和 `data/webwatcher.sqlite3` 两种数据库路径，接手时要确认当前实际使用的是哪一个

## 9. 待办与建议下一步
- 高优先级：
  - 统一版本叙事（README / CHANGELOG / release notes）
  - 对 Docker + Playwright 运行路径做一次完整验收
  - 增加真实世界页面的回归测试样本
- 中优先级：
  - 增加多渠道通知（Telegram / Email 等）
  - 增加更细的变更摘要能力
  - 设计周期性运行方式（cron/systemd/容器定时）
- 低优先级：
  - Web dashboard
  - 多用户 / SaaS 化
- 推荐接手顺序：
  1. 本地跑通 `init -> add -> check -> list`
  2. 跑通 Playwright 动态抓取
  3. 用真实 webhook 验证通知
  4. 再看 Docker 稳态验收和功能扩展

## 10. 关键文件索引
- README：`README.md`
- 配置文件示例：`webwatcher.example.json`
- 实际配置文件：`webwatcher.json`（本地）
- 数据库：`data/webwatcher.sqlite3` 或 `webwatcher.sqlite3`
- 版本信息：`VERSION`
- 发布说明：`RELEASE_NOTES_v0.3.0.md`
- 变更记录：`CHANGELOG.md`
- Docker：`Dockerfile`, `docker-compose.yml`
- 核心模块：`app.py`, `watcher.py`, `fetcher.py`, `storage.py`, `config.py`, `notifier.py`

## 11. 待确认项
- `CHANGELOG.md` 中 `v0.4.0` 与当前 `VERSION=0.3.0` 的关系是否要重写或拆分
- Docker + Playwright 在干净环境中的完整稳定性是否已达发布标准
- 是否需要为实际部署补一个定时执行方案（cron / systemd / scheduler）
- 是否保留项目根目录下旧的 `webwatcher.sqlite3`
