from datetime import datetime

from fetcher import fetch_and_hash, summarize_change
from notifier import send_feishu_text
from storage import add_event, list_monitors, update_monitor_state


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def run_checks() -> list[dict]:
    results = []
    monitors = list_monitors()

    for monitor in monitors:
        checked_at = now_iso()
        try:
            _text, new_hash = fetch_and_hash(monitor.url)
            changed = monitor.last_hash != new_hash
            summary = summarize_change(monitor.last_hash, new_hash)

            if changed:
                add_event(
                    monitor_id=monitor.id,
                    old_hash=monitor.last_hash,
                    new_hash=new_hash,
                    changed_at=checked_at,
                    summary=summary,
                )
                send_feishu_text(
                    f"[WebWatcher] 页面变化\n名称: {monitor.name}\nURL: {monitor.url}\n时间: {checked_at}\n说明: {summary}"
                )

            update_monitor_state(monitor.id, new_hash, checked_at)
            results.append(
                {
                    "monitor_id": monitor.id,
                    "name": monitor.name,
                    "url": monitor.url,
                    "changed": changed,
                    "summary": summary,
                }
            )
        except Exception as exc:
            results.append(
                {
                    "monitor_id": monitor.id,
                    "name": monitor.name,
                    "url": monitor.url,
                    "changed": False,
                    "summary": f"检查失败: {exc}",
                }
            )

    return results
