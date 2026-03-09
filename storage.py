import sqlite3
from pathlib import Path
from typing import List

from config import get_database_path
from models import Event, Monitor


DB_PATH = get_database_path()


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS monitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    interval_seconds INTEGER NOT NULL,
    selector TEXT,
    noise_rules TEXT,
    fetch_mode TEXT DEFAULT 'static',
    wait_for_selector TEXT,
    wait_after_load_ms INTEGER DEFAULT 0,
    last_hash TEXT,
    last_checked_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monitor_id INTEGER NOT NULL,
    old_hash TEXT,
    new_hash TEXT NOT NULL,
    changed_at TEXT NOT NULL,
    summary TEXT NOT NULL,
    FOREIGN KEY (monitor_id) REFERENCES monitors(id)
);
"""


def get_db_path() -> Path:
    return get_database_path()


def get_conn() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA_SQL)
        columns = {row['name'] for row in conn.execute("PRAGMA table_info(monitors)").fetchall()}
        if 'selector' not in columns:
            conn.execute("ALTER TABLE monitors ADD COLUMN selector TEXT")
        if 'noise_rules' not in columns:
            conn.execute("ALTER TABLE monitors ADD COLUMN noise_rules TEXT")
        if 'fetch_mode' not in columns:
            conn.execute("ALTER TABLE monitors ADD COLUMN fetch_mode TEXT DEFAULT 'static'")
        if 'wait_for_selector' not in columns:
            conn.execute("ALTER TABLE monitors ADD COLUMN wait_for_selector TEXT")
        if 'wait_after_load_ms' not in columns:
            conn.execute("ALTER TABLE monitors ADD COLUMN wait_after_load_ms INTEGER DEFAULT 0")


def add_monitor(
    name: str,
    url: str,
    interval_seconds: int,
    created_at: str,
    selector: str | None = None,
    noise_rules: str | None = None,
    fetch_mode: str = 'static',
    wait_for_selector: str | None = None,
    wait_after_load_ms: int = 0,
) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO monitors (name, url, interval_seconds, selector, noise_rules, fetch_mode, wait_for_selector, wait_after_load_ms, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, url, interval_seconds, selector, noise_rules, fetch_mode, wait_for_selector, wait_after_load_ms, created_at),
        )
        return int(cursor.lastrowid)


def list_monitors() -> List[Monitor]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, name, url, interval_seconds, selector, noise_rules, fetch_mode, wait_for_selector, wait_after_load_ms, last_hash, last_checked_at, created_at FROM monitors ORDER BY id ASC"
        ).fetchall()
    items = []
    for row in rows:
        data = dict(row)
        data['fetch_mode'] = data.get('fetch_mode') or 'static'
        data['wait_after_load_ms'] = data.get('wait_after_load_ms') or 0
        items.append(Monitor(**data))
    return items


def update_monitor_state(monitor_id: int, new_hash: str, checked_at: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE monitors SET last_hash = ?, last_checked_at = ? WHERE id = ?",
            (new_hash, checked_at, monitor_id),
        )


def add_event(monitor_id: int, old_hash: str | None, new_hash: str, changed_at: str, summary: str) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO events (monitor_id, old_hash, new_hash, changed_at, summary) VALUES (?, ?, ?, ?, ?)",
            (monitor_id, old_hash, new_hash, changed_at, summary),
        )
        return int(cursor.lastrowid)


def list_events(limit: int = 50) -> List[Event]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, monitor_id, old_hash, new_hash, changed_at, summary FROM events ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [Event(**dict(row)) for row in rows]
