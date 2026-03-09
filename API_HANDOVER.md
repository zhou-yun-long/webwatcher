# API / Integration Handover

## 1. 接口概览
| 接口名称 | 方法 | 路径 | 用途 | 鉴权 | 负责人/模块 |
|---|---|---|---|---|---|
| CLI: init | CLI command | `python app.py init` | 初始化数据库 | 无 | `app.py` / `storage.py` |
| CLI: add | CLI command | `python app.py add ...` | 添加监控任务 | 无 | `app.py` / `storage.py` |
| CLI: list | CLI command | `python app.py list` | 查看监控任务 | 无 | `app.py` / `storage.py` |
| CLI: check | CLI command | `python app.py check` | 执行检查与变化检测 | 无 | `app.py` / `watcher.py` |
| CLI: events | CLI command | `python app.py events --limit N` | 查看变化事件 | 无 | `app.py` / `storage.py` |
| CLI: config-show | CLI command | `python app.py config-show` | 查看当前解析后的配置 | 无 | `app.py` / `config.py` |
| Feishu webhook notify | Outbound HTTP POST | `FEISHU_WEBHOOK_URL` | 页面变化后发送飞书文本通知 | webhook URL 持有即视为授权 | `notifier.py` |

## 2. 基础信息
- 服务名称：WebWatcher
- Base URL：无固定对外 HTTP API Base URL
- 环境：本地运行 / Docker 运行
- 文档来源：代码扫描 + README + 配置文件 + 人工整理
- 版本：`0.3.0`

## 3. 鉴权方式
- WebWatcher 自身对外不提供 HTTP API，因此不存在统一的服务端鉴权层。
- 唯一明确的外部集成点是飞书 webhook：
  - 鉴权类型：通过 webhook URL 持有来完成
  - 请求头要求：默认 `requests.post(..., json=payload)`，无额外签名逻辑
  - 签名算法：当前仓库未实现自定义签名
  - token 获取方式：由使用方在飞书侧创建机器人 webhook 后填入配置
  - 过期处理：未在代码中单独实现，需要人工更新 webhook

## 4. 通用请求约定
- 对外 HTTP API：无
- 对内交互方式：CLI 命令
- 数据持久化：SQLite
- 外呼方式：HTTP POST 到飞书 webhook
- 超时建议：
  - 页面抓取默认 timeout 来自配置，默认 20 秒
  - webhook POST 在 `notifier.py` 中 timeout 为 10 秒
- 重试策略：当前仓库未实现通用重试机制

## 5. 通用响应格式
当前项目没有统一的 HTTP JSON 响应封装，因为它不是 Web API 服务。

CLI 输出以终端文本为主，例如：

```text
数据库已初始化: /path/to/webwatcher.sqlite3
```

或：

```text
[CHANGED] Example Home [mode=playwright] -> 检测到页面内容变化
```

飞书 webhook 发送时使用的 payload 格式为：

```json
{
  "msg_type": "text",
  "content": {
    "text": "[WebWatcher] 页面变化..."
  }
}
```

## 6. 错误码约定
项目内部未维护统一错误码表。

| 错误来源 | 含义 | 处理建议 |
|---|---|---|
| Python exception | 运行期异常 | 直接查看终端输出和 traceback |
| requests HTTP error | 静态抓取或 webhook 失败 | 检查目标 URL / 网络 / webhook 是否有效 |
| Playwright runtime error | 动态页面抓取失败 | 检查浏览器依赖、页面加载、selector、等待参数 |
| `selector not found` | CSS selector 未匹配到内容 | 检查页面结构是否变化，或改 selector |
| config parse error | 配置文件格式错误 | 检查 `webwatcher.json` 是否为合法 JSON 对象 |

## 7. 接口详情

## CLI: init
- 用途：初始化 SQLite 数据库及 schema
- 请求方法：CLI command
- 请求地址：`python app.py init`
- 所属模块：初始化 / 存储
- 是否需要鉴权：否
- 调用方：开发者 / 运维 / 定时任务环境
- 被调用方：`storage.init_db()`

### 请求头
不适用。

### Query 参数
不适用。

### Body 参数
不适用。

### 响应示例
```text
数据库已初始化: /root/.openclaw/workspace/projects/webwatcher/data/webwatcher.sqlite3
```

### 字段说明
无结构化返回字段。

### 错误码
无统一错误码；失败时依赖 Python 异常。

### 注意事项
- 会按当前配置文件解析数据库路径
- 如果 `WEBWATCHER_CONFIG` 指向其他配置文件，数据库位置也会变化

## CLI: add
- 用途：添加监控任务
- 请求方法：CLI command
- 请求地址：`python app.py add --url <URL> --name <NAME> [options]`
- 所属模块：CLI / 存储
- 是否需要鉴权：否
- 调用方：开发者 / 运维
- 被调用方：`storage.add_monitor()`

### 请求头
不适用。

### Query 参数
不适用。

### Body 参数
命令行参数：
- `--url`：监控 URL，必填
- `--name`：监控名称，必填
- `--interval`：检查间隔秒数，默认 600
- `--selector`：可选，CSS selector
- `--noise-rules`：可选，噪声过滤规则
- `--fetch-mode`：`static` 或 `playwright`
- `--wait-for-selector`：Playwright 模式可选
- `--wait-after-load-ms`：Playwright 模式可选

### 响应示例
```text
已添加监控 #1: Example Home -> https://example.com
```

### 字段说明
无结构化返回字段。

### 错误码
无统一错误码；参数错误由 argparse 抛出。

### 注意事项
- `--selector` 不稳定时容易导致误报或抓取失败
- 对 JS 动态页面应优先尝试 `--fetch-mode playwright`

## CLI: list
- 用途：查看监控任务清单
- 请求方法：CLI command
- 请求地址：`python app.py list`
- 所属模块：CLI / 存储
- 是否需要鉴权：否
- 调用方：开发者 / 运维
- 被调用方：`storage.list_monitors()`

### 响应示例
```text
[1] Example Home
  URL: https://example.com
  Fetch Mode: static
  Selector: -
```

### 注意事项
- 输出是面向人工阅读的终端文本，不是 JSON

## CLI: check
- 用途：执行所有监控项的检查，比较哈希并在变化时记录事件/发送通知
- 请求方法：CLI command
- 请求地址：`python app.py check`
- 所属模块：CLI / 检查流程
- 是否需要鉴权：否
- 调用方：开发者 / 运维 / 定时任务
- 被调用方：`watcher.run_checks()`

### 响应示例
```text
[OK] Example Home [mode=static] -> 内容无变化
[CHANGED] Dynamic Example [mode=playwright] -> 检测到页面内容变化
```

### 注意事项
- 如果配置了飞书 webhook，变化发生时会额外发通知
- 若抓取失败，会输出 `检查失败: ...`

## CLI: events
- 用途：查看最近变化事件
- 请求方法：CLI command
- 请求地址：`python app.py events --limit 20`
- 所属模块：CLI / 存储
- 是否需要鉴权：否

### 响应示例
```text
[1] monitor=1 at 2026-03-09T12:00:00
  summary: 检测到页面内容变化
  old: abcdef123456...
  new: 7890abcd1234...
```

## CLI: config-show
- 用途：查看当前解析后的配置和数据库路径
- 请求方法：CLI command
- 请求地址：`python app.py config-show`
- 所属模块：CLI / 配置
- 是否需要鉴权：否

### 响应示例
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

### 注意事项
- 输出里可能包含 webhook 地址，分享时要注意脱敏

## Feishu webhook notify
- 用途：页面变化后向飞书发送文本通知
- 请求方法：HTTP POST
- 请求地址：`FEISHU_WEBHOOK_URL`
- 所属模块：通知
- 是否需要鉴权：由 webhook URL 持有控制
- 调用方：`watcher.py`
- 被调用方：飞书机器人 webhook

### 请求头
默认由 `requests` 根据 JSON 发送，通常等价于：

```json
{
  "Content-Type": "application/json"
}
```

### Body 参数
```json
{
  "msg_type": "text",
  "content": {
    "text": "[WebWatcher] 页面变化\n名称: Example Home\nURL: https://example.com\n说明: 检测到页面内容变化"
  }
}
```

### 响应示例
飞书 webhook 成功响应未在仓库中封装保存，当前逻辑只检查 HTTP 是否报错。

### 错误码
| 错误来源 | 含义 | 处理建议 |
|---|---|---|
| HTTP 非 2xx | webhook 发送失败 | 检查 webhook 是否失效、网络是否正常 |
| requests timeout | 发送超时 | 检查网络或下游可用性 |

### 注意事项
- 当前仅支持纯文本通知
- 未实现签名、重试、消息去重

## 8. 回调 / 异步通知（如有）
- 当前项目没有“接收入站回调”的 HTTP endpoint。
- 唯一异步相关行为是：变化后向飞书发起单向 webhook POST。
- 因此：
  - 回调地址：无
  - 回调方法：无
  - 验签方式：无
  - 重试策略：未实现
  - 幂等要求：未显式实现
  - 失败补偿：未实现

## 9. 待确认项
- 当前项目未来是否会扩展成真正的 HTTP API 服务
- 是否需要把 CLI 输出再封装成机器可读 JSON，以便对接自动化系统
- 飞书 webhook 是否需要补签名、重试、限流和失败补偿
- 若未来增加 Web dashboard，届时 API_HANDOVER 结构需重写为真正的 REST/HTTP 接口文档
