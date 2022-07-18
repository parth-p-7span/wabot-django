import datetime as dt
from secrets import compare_digest

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import WebhookMessage
from .func import *
from .firebase import Firebase
from .input_validator import *

instance = Firebase()

with open('webhook/actions.json', 'r') as f:
    actions = json.load(f)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@non_atomic_requests
def wa_webhook(request):
    params = request.GET.dict()
    if 'hub.mode' in params and 'hub.verify_token' in params:
        if compare_digest(params['hub.mode'], 'subscribe') and compare_digest(params['hub.verify_token'],
                                                                              settings.WA_VERIFY_TOKEN):
            print('WEBHOOK VERIFIED')
            return HttpResponse(params['hub.challenge'], status=200)
        else:
            return HttpResponseForbidden(
                "Incorrect Token Passed",
                content_type='text/plain'
            )

    WebhookMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=1)
    ).delete()

    payload = json.loads(request.body)

    try:

        # print("payload ==> ", payload)

        message_id = payload['entry'][0]['changes'][0]['value']['messages'][0]['id']
        # process_request(payload)
        # return HttpResponse("Message received okay", status=200)
        if not WebhookMessage.objects.filter(message_id=message_id):
            WebhookMessage.objects.create(
                message_id=message_id,
                received_at=timezone.now(),
                payload=payload
            )
            process_request(payload)
            return HttpResponse("Message received okay", status=200)
        else:
            return HttpResponseForbidden(
                "Message already received",
                content_type='text/plain'
            )
    except Exception as e:
        return HttpResponseForbidden(
            "Something went wrong",
            content_type='text/plain'
        )


@atomic
def process_request(payload, is_recursive=False, field_name="", input_type=""):
    if 'object' in payload and payload['object'] == 'whatsapp_business_account':

        message_value = payload['entry'][0]['changes'][0]['value']
        message_product = message_value['messaging_product']
        if message_product == 'whatsapp':
            if 'messages' in message_value:
                author_name = message_value['contacts'][0]['profile']['name']
                message_object = message_value['messages'][0]
                message_type = message_object['type']
                message_id = message_object['id']
                user_id = message_object['from']

                mark_as_read(message_id)

                users_data = instance.get_user_data(user_id)

                msg_to_send = -1
                for i, (key, value) in enumerate(users_data.items()):
                    if value == 0:
                        msg_to_send = i
                        break

                print("-------->", users_data, "-----", msg_to_send)
                msg_action = actions['steps'][msg_to_send]
                last_msg_action = actions['steps'][msg_to_send - 1] if msg_to_send != 0 else actions['steps'][
                    msg_to_send]

                message_text = ""
                if message_type == "text":
                    message_text = message_object['text']['body']
                elif message_type == "interactive":
                    message_text = message_object['interactive']['button_reply']['title']
                elif message_type == "media":
                    message_text = {
                        "id": message_object['document']['id'],
                        "name": message_object['document']['filename']
                    }

                if msg_to_send == -1:
                    instance.update_user(f'{user_id}', msg_action['name'], message_text)
                    return
                if not msg_action['user_input']:
                    if last_msg_action['user_input']:
                        print("===> ", last_msg_action['name'], "===", last_msg_action['expected'])
                        if verify_data(last_msg_action['expected'], message_text):
                            instance.update_user(f'{user_id}', last_msg_action['name'], message_text)
                        else:
                            send_validation_error(user_id)
                            return
                    send_message(user_id, msg_action)
                    instance.update_user(f'{user_id}/state', msg_action['name'], "sent")
                    temp_name = msg_action['name'] if msg_action['name'] != "starter" else ""
                    try:
                        temp_expected = msg_action['expected']
                    except:
                        temp_expected = ""
                    process_request(payload, is_recursive=True, field_name=temp_name, input_type=temp_expected)
                else:
                    if not is_recursive:
                        temp_name = last_msg_action['name'] if field_name == "" else field_name
                        temp_expected = last_msg_action['expected'] if input_type == "" else input_type

                        print("==> ", temp_name, "===", temp_expected)
                        if verify_data(temp_expected, message_text):
                            instance.update_user(f'{user_id}', temp_name, message_text)
                        else:
                            send_validation_error(user_id)
                            return

                    send_message(user_id, msg_action)
                    instance.update_user(f'{user_id}/state', msg_action['name'], "sent")
        return 'EVENT_RECEIVED', 200


def verify_data(expected, data):
    if expected == "text" or expected == "interactive":
        return True
    if expected == "email":
        return verify_email(data)
    if expected == "mobile":
        return verify_mobile(data)
    return False
