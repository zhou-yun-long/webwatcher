# GitHub Launch Pack

## Repo name

`webwatcher`

## GitHub description

Minimal open-source website change monitor built with Python and SQLite.

## Suggested topics

- website-monitor
- webpage-monitoring
- change-detection
- python
- sqlite
- cli
- monitoring-tool
- feishu
- open-source
- automation

## Short launch post (CN)

做了一个很小但很实用的开源项目：**WebWatcher**。

它能：
- 监控网页内容变化
- 用哈希判断页面是否更新
- 把变化事件记到 SQLite
- 支持飞书 webhook 通知

我故意把第一版做得很克制：
- 没有大而全后台
- 没有复杂 SaaS 架构
- 先把“网页变化监控”这件事做好

适合拿来监控：
- 招聘页
- 公告页
- 竞品价格页
- 榜单页
- 文档更新

如果你也刚好需要一个简单、可改、可自己部署的基础版，欢迎来看看。

## Short launch post (EN)

Built a small but useful open-source project: **WebWatcher**.

It:
- monitors webpage content changes
- supports CSS selector-based tracking
- detects updates with content hashing
- stores change events in SQLite
- supports Feishu webhook notifications

I intentionally kept v0.1 small and practical.
No huge platform. No overbuilt SaaS layer.
Just a simple, hackable website change monitor.

Good fit for tracking:
- job pages
- announcement pages
- competitor pages
- ranking pages
- documentation updates

If you want a simple self-hosted starting point, take a look.

## README first-screen suggestion

Put these in the first screen of the repo:
1. One-line description
2. 4-line quick start
3. One CLI example
4. Future roadmap

## Next release suggestion

Tag next release as:

`v0.1.0`

Release title:

`WebWatcher v0.1.0 - initial open-source MVP`
