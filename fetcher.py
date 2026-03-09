import hashlib
import re
from typing import Tuple

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": "WebWatcher/0.3 (+https://github.com/yourname/webwatcher)"
}


def _cleanup_html_text(html: str, selector: str | None = None) -> str:
    soup = BeautifulSoup(html, "html.parser")

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


def fetch_text_static(url: str, timeout: int = 20, selector: str | None = None) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return _cleanup_html_text(response.text, selector=selector)


def fetch_text_playwright(
    url: str,
    timeout: int = 20,
    selector: str | None = None,
    wait_for_selector: str | None = None,
    wait_after_load_ms: int = 0,
) -> str:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise RuntimeError(
            "Playwright is not available. Install dependencies with `pip install -r requirements.txt` "
            "and browser binaries with `python -m playwright install chromium`."
        ) from exc

    timeout_ms = max(timeout, 1) * 1000

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.set_extra_http_headers(DEFAULT_HEADERS)
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)

            try:
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
            except PlaywrightTimeoutError:
                pass

            if wait_for_selector:
                page.locator(wait_for_selector).first.wait_for(state="visible", timeout=timeout_ms)

            if wait_after_load_ms > 0:
                page.wait_for_timeout(wait_after_load_ms)

            if selector:
                locator = page.locator(selector)
                count = locator.count()
                if count == 0:
                    raise ValueError(f"selector not found: {selector}")
                text = "\n".join(locator.all_inner_texts())
            else:
                text = page.locator("body").inner_text(timeout=timeout_ms)

            text = re.sub(r"\n+", "\n", text)
            text = re.sub(r"[ \t]+", " ", text)
            return text.strip()
        finally:
            browser.close()


def fetch_text(
    url: str,
    timeout: int = 20,
    selector: str | None = None,
    fetch_mode: str = "static",
    wait_for_selector: str | None = None,
    wait_after_load_ms: int = 0,
) -> str:
    if fetch_mode == "playwright":
        return fetch_text_playwright(
            url,
            timeout=timeout,
            selector=selector,
            wait_for_selector=wait_for_selector,
            wait_after_load_ms=wait_after_load_ms,
        )
    return fetch_text_static(url, timeout=timeout, selector=selector)


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


def fetch_and_hash(
    url: str,
    selector: str | None = None,
    noise_rules: str | None = None,
    fetch_mode: str = "static",
    wait_for_selector: str | None = None,
    wait_after_load_ms: int = 0,
) -> Tuple[str, str]:
    raw_text = fetch_text(
        url,
        selector=selector,
        fetch_mode=fetch_mode,
        wait_for_selector=wait_for_selector,
        wait_after_load_ms=wait_after_load_ms,
    )
    text = normalize_text(raw_text, noise_rules=noise_rules)
    digest = hash_text(text)
    return text, digest


def summarize_change(old_hash: str | None, new_hash: str) -> str:
    if not old_hash:
        return "首次抓取，已建立基线"
    if old_hash != new_hash:
        return "检测到页面内容变化"
    return "内容无变化"
