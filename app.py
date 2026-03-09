import argparse
import json
from datetime import datetime

from config import get_config_path, load_config
from storage import add_monitor, get_db_path, init_db, list_events, list_monitors
from watcher import run_checks


def cmd_init(_args):
    init_db()
    print(f"数据库已初始化: {get_db_path()}")


def cmd_add(args):
    monitor_id = add_monitor(
        name=args.name,
        url=args.url,
        interval_seconds=args.interval,
        created_at=datetime.now().isoformat(timespec="seconds"),
        selector=args.selector,
        noise_rules=args.noise_rules,
        fetch_mode=args.fetch_mode,
        wait_for_selector=args.wait_for_selector,
        wait_after_load_ms=args.wait_after_load_ms,
    )
    print(f"已添加监控 #{monitor_id}: {args.name} -> {args.url}")


def cmd_list(_args):
    monitors = list_monitors()
    if not monitors:
        print("暂无监控任务")
        return

    for item in monitors:
        print(
            f"[{item.id}] {item.name}\n"
            f"  URL: {item.url}\n"
            f"  Fetch Mode: {item.fetch_mode or 'static'}\n"
            f"  Selector: {item.selector or '-'}\n"
            f"  Wait For: {item.wait_for_selector or '-'}\n"
            f"  Wait After Load: {item.wait_after_load_ms or 0}ms\n"
            f"  Noise Rules: {item.noise_rules or '-'}\n"
            f"  Interval: {item.interval_seconds}s\n"
            f"  Last Checked: {item.last_checked_at or '-'}\n"
            f"  Last Hash: {(item.last_hash[:12] + '...') if item.last_hash else '-'}\n"
        )


def cmd_check(_args):
    results = run_checks()
    if not results:
        print("没有可检查的监控任务")
        return

    for item in results:
        status = "CHANGED" if item["changed"] else "OK"
        mode_suffix = f" [mode={item['fetch_mode']}]" if item.get("fetch_mode") else ""
        selector_suffix = f" [selector={item['selector']}]" if item.get("selector") else ""
        wait_suffix = f" [wait_for={item['wait_for_selector']}]" if item.get("wait_for_selector") else ""
        noise_suffix = f" [noise={item['noise_rules']}]" if item.get("noise_rules") else ""
        print(f"[{status}] {item['name']}{mode_suffix}{selector_suffix}{wait_suffix}{noise_suffix} -> {item['summary']}")


def cmd_events(args):
    events = list_events(limit=args.limit)
    if not events:
        print("暂无变化事件")
        return

    for event in events:
        print(
            f"[{event.id}] monitor={event.monitor_id} at {event.changed_at}\n"
            f"  summary: {event.summary}\n"
            f"  old: {(event.old_hash[:12] + '...') if event.old_hash else '-'}\n"
            f"  new: {event.new_hash[:12]}...\n"
        )


def cmd_config_show(_args):
    config = load_config()
    print(json.dumps(config, ensure_ascii=False, indent=2))
    print(f"\nConfig Path: {get_config_path()}")
    print(f"Database Path: {get_db_path()}")


def build_parser():
    parser = argparse.ArgumentParser(description="WebWatcher CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="初始化数据库")
    init_parser.set_defaults(func=cmd_init)

    add_parser = subparsers.add_parser("add", help="添加监控")
    add_parser.add_argument("--url", required=True, help="监控 URL")
    add_parser.add_argument("--name", required=True, help="监控名称")
    add_parser.add_argument("--interval", type=int, default=600, help="检查间隔（秒）")
    add_parser.add_argument("--selector", help="可选：只监控匹配的 CSS selector 内容")
    add_parser.add_argument(
        "--noise-rules",
        help="可选：噪声过滤规则，逗号分隔，如 ignore_digits,ignore_dates 或 regex:<pattern>",
    )
    add_parser.add_argument(
        "--fetch-mode",
        choices=["static", "playwright"],
        default="static",
        help="抓取模式：static（默认）或 playwright（适合 JS 动态页面）",
    )
    add_parser.add_argument(
        "--wait-for-selector",
        help="仅 Playwright 模式可选：等待某个 selector 出现后再提取内容",
    )
    add_parser.add_argument(
        "--wait-after-load-ms",
        type=int,
        default=0,
        help="仅 Playwright 模式可选：页面加载后额外等待毫秒数",
    )
    add_parser.set_defaults(func=cmd_add)

    list_parser = subparsers.add_parser("list", help="查看监控")
    list_parser.set_defaults(func=cmd_list)

    check_parser = subparsers.add_parser("check", help="执行检查")
    check_parser.set_defaults(func=cmd_check)

    events_parser = subparsers.add_parser("events", help="查看变化事件")
    events_parser.add_argument("--limit", type=int, default=20, help="返回条数")
    events_parser.set_defaults(func=cmd_events)

    config_parser = subparsers.add_parser("config-show", help="查看当前配置")
    config_parser.set_defaults(func=cmd_config_show)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
