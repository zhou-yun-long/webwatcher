from dataclasses import dataclass
from typing import Optional


@dataclass
class Monitor:
    id: int
    name: str
    url: str
    interval_seconds: int
    selector: Optional[str]
    noise_rules: Optional[str]
    fetch_mode: Optional[str]
    wait_for_selector: Optional[str]
    wait_after_load_ms: int
    last_hash: Optional[str]
    last_checked_at: Optional[str]
    created_at: str


@dataclass
class Event:
    id: int
    monitor_id: int
    old_hash: Optional[str]
    new_hash: str
    changed_at: str
    summary: str
