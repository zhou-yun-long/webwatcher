import argparse
from datetime import datetime

from storage import add_monitor, init_db, list_events, list_monitors
from watcher import run_checks


def cmd_init(_args):
    init_db()
    print("数据库已初始化")


def cmd_add(args):
    monitor_id = add_monitor(
        name=args.name,
        url=args.url,
        interval_seconds=args.interval,
        created_at=datetime.now().isoformat(timespec="seconds"),
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
        print(f"[{status}] {item['name']} -> {item['summary']}")


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


def build_parser():
    parser = argparse.ArgumentParser(description="WebWatcher CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="初始化数据库")
    init_parser.set_defaults(func=cmd_init)

    add_parser = subparsers.add_parser("add", help="添加监控")
    add_parser.add_argument("--url", required=True, help="监控 URL")
    add_parser.add_argument("--name", required=True, help="监控名称")
    add_parser.add_argument("--interval", type=int, default=600, help="检查间隔（秒）")
    add_parser.set_defaults(func=cmd_add)

    list_parser = subparsers.add_parser("list", help="查看监控")
    list_parser.set_defaults(func=cmd_list)

    check_parser = subparsers.add_parser("check", help="执行检查")
    check_parser.set_defaults(func=cmd_check)

    events_parser = subparsers.add_parser("events", help="查看变化事件")
    events_parser.add_argument("--limit", type=int, default=20, help="返回条数")
    events_parser.set_defaults(func=cmd_events)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
