import hashlib
import re
from typing import Tuple

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": "WebWatcher/0.1 (+https://github.com/yourname/webwatcher)"
}


def fetch_text(url: str, timeout: int = 20, selector: str | None = None) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    if selector:
        selected = soup.select(selector)
        if not selected:
            raise ValueError(f"selector not found: {selector}")
        text = "\n".join(node.get_text("\n") for node in selected)
    else:
        text = soup.get_text("\n")

    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def normalize_text(text: str, noise_rules: str | None = None) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    normalized = "\n".join(lines)

    if not noise_rules:
        return normalized

    for rule in [item.strip() for item in noise_rules.split(",") if item.strip()]:
        if rule == "ignore_digits":
            normalized = re.sub(r"\d+", "<NUM>", normalized)
        elif rule == "ignore_dates":
            normalized = re.sub(r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b", "<DATE>", normalized)
            normalized = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\b", "<TIME>", normalized)
        elif rule.startswith("regex:"):
            pattern = rule.split(":", 1)[1]
            normalized = re.sub(pattern, "", normalized)

    normalized = re.sub(r"\n+", "\n", normalized)
    return normalized.strip()


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_and_hash(url: str, selector: str | None = None, noise_rules: str | None = None) -> Tuple[str, str]:
    raw_text = fetch_text(url, selector=selector)
    text = normalize_text(raw_text, noise_rules=noise_rules)
    digest = hash_text(text)
    return text, digest


def summarize_change(old_hash: str | None, new_hash: str) -> str:
    if not old_hash:
        return "首次抓取，已建立基线"
    if old_hash != new_hash:
        return "检测到页面内容变化"
    return "内容无变化"
