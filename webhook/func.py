import json
import requests

from django.conf import settings


def mark_as_read(message_id):
    res = requests.post(
        url=settings.WA_ENDPOINT,
        headers=settings.WA_HEADER,
        data=json.dumps({"messaging_product": "whatsapp", "status": "read",
                         "message_id": message_id})
    )
    return res.status_code


def send_selection_msg(to):
    res = requests.post(
        url=settings.WA_ENDPOINT,
        headers=settings.WA_HEADER,
        data=json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": settings.INTERACTIVE_MSG_BODY
        }))
    return res.json()


def send_message(message, to):
    res = requests.post(
        url=settings.WA_ENDPOINT,
        headers=settings.WA_HEADER,
        data=json.dumps(
            {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {
                    "body": message,
                }
            }
        ))
    return res.json()
