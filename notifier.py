import requests

from config import get_feishu_webhook_url


def send_feishu_text(text: str) -> bool:
    webhook = get_feishu_webhook_url()
    if not webhook:
        return False

    payload = {
        "msg_type": "text",
        "content": {
            "text": text,
        },
    }
    response = requests.post(webhook, json=payload, timeout=10)
    response.raise_for_status()
    return True
