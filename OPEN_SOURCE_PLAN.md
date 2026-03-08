# WebWatcher 开源发布计划

## 定位

WebWatcher 是一个极简网页变更监控工具：
- 给一个 URL
- 定时抓取文本
- 检测变化
- 记录事件

它不是大而全监控平台，而是一个非常适合开源首发的基础版项目。

## 首发卖点

- 简单直接，5 分钟可跑
- 使用真实场景明确
- CLI 版本非常适合开发者
- 后续可扩展到通知、动态抓取、SaaS

## 首发 README 标题建议

- WebWatcher — Minimal open-source website change monitor
- WebWatcher — Track webpage changes with Python + SQLite
- WebWatcher — Simple webpage monitoring CLI

## GitHub 首发建议

1. 仓库名不要太花：`webwatcher`
2. README 第一屏要放：
   - 一句话介绍
   - 3 步快速开始
   - CLI 示例
3. 补一张运行截图
4. 发首个 release：`v0.1.0`
5. 在 issue 里放 roadmap

## 下一个最值得做的功能

1. Feishu webhook 通知
2. CSS selector 监控
3. 忽略无意义波动
4. Playwright 支持动态网页
5. Docker Compose 部署

## 变现思路

### 1. 托管版
- 用户不用自己部署
- 适合非技术用户

### 2. 企业通知插件
- 飞书/企业微信/钉钉
- Slack/Telegram

### 3. 高级规则
- 页面区域监控
- 截图对比
- AI 变化摘要
- 多账号协作

### 4. 定制服务
- 帮客户接入特定网站
- 帮客户做定制监控与告警
