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
            _text, new_hash = fetch_and_hash(
                monitor.url,
                selector=monitor.selector,
                noise_rules=monitor.noise_rules,
                fetch_mode=monitor.fetch_mode or "static",
                wait_for_selector=monitor.wait_for_selector,
                wait_after_load_ms=monitor.wait_after_load_ms or 0,
            )
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
                selector_line = f"\nSelector: {monitor.selector}" if monitor.selector else ""
                noise_line = f"\nNoise Rules: {monitor.noise_rules}" if monitor.noise_rules else ""
                mode_line = f"\nFetch Mode: {monitor.fetch_mode or 'static'}"
                wait_for_line = f"\nWait For: {monitor.wait_for_selector}" if monitor.wait_for_selector else ""
                wait_after_line = (
                    f"\nWait After Load: {monitor.wait_after_load_ms}ms"
                    if (monitor.wait_after_load_ms or 0) > 0
                    else ""
                )
                send_feishu_text(
                    f"[WebWatcher] 页面变化\n名称: {monitor.name}\nURL: {monitor.url}{mode_line}{selector_line}{wait_for_line}{wait_after_line}{noise_line}\n时间: {checked_at}\n说明: {summary}"
                )

            update_monitor_state(monitor.id, new_hash, checked_at)
            results.append(
                {
                    "monitor_id": monitor.id,
                    "name": monitor.name,
                    "url": monitor.url,
                    "fetch_mode": monitor.fetch_mode or "static",
                    "selector": monitor.selector,
                    "wait_for_selector": monitor.wait_for_selector,
                    "wait_after_load_ms": monitor.wait_after_load_ms or 0,
                    "noise_rules": monitor.noise_rules,
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
                    "fetch_mode": monitor.fetch_mode or "static",
                    "selector": monitor.selector,
                    "wait_for_selector": monitor.wait_for_selector,
                    "wait_after_load_ms": monitor.wait_after_load_ms or 0,
                    "noise_rules": monitor.noise_rules,
                    "changed": False,
                    "summary": f"检查失败: {exc}",
                }
            )

    return results
