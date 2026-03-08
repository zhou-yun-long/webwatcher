import os
import requests


FEISHU_WEBHOOK_ENV = "FEISHU_WEBHOOK_URL"


def send_feishu_text(text: str) -> bool:
    webhook = os.getenv(FEISHU_WEBHOOK_ENV)
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
