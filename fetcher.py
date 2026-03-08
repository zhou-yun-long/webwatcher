import hashlib
import re
from typing import Tuple

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": "WebWatcher/0.1 (+https://github.com/yourname/webwatcher)"
}


def fetch_text(url: str, timeout: int = 20) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text("\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_and_hash(url: str) -> Tuple[str, str]:
    text = fetch_text(url)
    digest = hash_text(text)
    return text, digest


def summarize_change(old_hash: str | None, new_hash: str) -> str:
    if not old_hash:
        return "首次抓取，已建立基线"
    if old_hash != new_hash:
        return "检测到页面内容变化"
    return "内容无变化"
