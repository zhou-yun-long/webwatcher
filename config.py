import json
import os
from pathlib import Path
from typing import Any


CONFIG_ENV = "WEBWATCHER_CONFIG"
DEFAULT_CONFIG_PATH = Path(__file__).parent / "webwatcher.json"


DEFAULT_CONFIG: dict[str, Any] = {
    "database": {
        "path": "webwatcher.sqlite3",
    },
    "fetch": {
        "timeout": 20,
        "mode": "static",
        "wait_for_selector": None,
        "wait_after_load_ms": 0,
    },
    "notifications": {
        "feishu_webhook_url": None,
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def get_config_path() -> Path:
    raw = os.getenv(CONFIG_ENV)
    if raw:
        return Path(raw).expanduser().resolve()
    return DEFAULT_CONFIG_PATH


def load_config() -> dict[str, Any]:
    path = get_config_path()
    config = dict(DEFAULT_CONFIG)
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            loaded = json.load(f)
        if not isinstance(loaded, dict):
            raise ValueError("config file must be a JSON object")
        config = _deep_merge(config, loaded)
    return config


def get_database_path() -> Path:
    config = load_config()
    db_path = config.get("database", {}).get("path") or DEFAULT_CONFIG["database"]["path"]
    path = Path(db_path)
    if not path.is_absolute():
        path = get_config_path().parent / path
    return path.resolve()


def get_fetch_defaults() -> dict[str, Any]:
    config = load_config()
    fetch = config.get("fetch", {})
    defaults = DEFAULT_CONFIG["fetch"]
    return {
        "timeout": fetch.get("timeout", defaults["timeout"]),
        "mode": fetch.get("mode", defaults["mode"]),
        "wait_for_selector": fetch.get("wait_for_selector", defaults["wait_for_selector"]),
        "wait_after_load_ms": fetch.get("wait_after_load_ms", defaults["wait_after_load_ms"]),
    }


def get_feishu_webhook_url() -> str | None:
    env_value = os.getenv("FEISHU_WEBHOOK_URL")
    if env_value:
        return env_value
    config = load_config()
    return config.get("notifications", {}).get("feishu_webhook_url")
