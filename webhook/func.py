import json
import requests

from django.conf import settings
from .models import Conversation


def mark_as_read(message_id):
    res = requests.post(
        url=settings.WA_ENDPOINT,
        headers=settings.WA_HEADER,
        data=json.dumps({"messaging_product": "whatsapp", "status": "read",
                         "message_id": message_id})
    )
    return res.status_code


def send_message(to, msg_object):
    Conversation.objects.create(
        user_id=to,
        sent_by_system=True,
        message_content=msg_object
    )
    temp = {**{
        "messaging_product": "whatsapp",
        "to": to,
        "type": msg_object['type']
    }, **msg_object['child']}
    res = requests.post(
        url=settings.WA_ENDPOINT,
        headers=settings.WA_HEADER,
        data=json.dumps(
            temp
        ))
    return res.json()


def send_validation_error(to):
    msg_object = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": "I'm afraid I didn't understand, could you try again, please?"
        }
    }
    Conversation.objects.create(
        user_id=to,
        sent_by_system=True,
        message_content=msg_object
    )
    res = requests.post(
        url=settings.WA_ENDPOINT,
        headers=settings.WA_HEADER,
        data=json.dumps(msg_object)
    )
    return res.json()
