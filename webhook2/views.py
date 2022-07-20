import datetime as dt
from secrets import compare_digest

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from webhook.models import WebhookMessage
from webhook.func import *
from webhook.firebase import Firebase
from webhook.input_validator import *

instance = Firebase()

with open('webhook2/actions3.json', 'r') as f:
    actions = json.load(f)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@non_atomic_requests
def wa_webhook2(request):
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
def process_request(payload):
    print("Payload ==> ", payload)
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

                # READING MESSAGE TEXT FROM REQUEST PAYLOAD
                message_text = ""
                if message_type == "text":
                    message_text = message_object['text']['body']
                elif message_type == "interactive":
                    message_text = message_object['interactive']['button_reply']['title']
                elif message_type == "document":
                    message_text = {
                        "id": message_object['document']['id'],
                        "name": message_object['document']['filename']
                    }

                mark_as_read(message_id)

                users_data = instance.get_state(user_id)
                action_location = ""
                action_object = {}
                last_action_object = {}
                is_starter = False
                if users_data is None:
                    instance.create_user(user_id, author_name)
                    action_location = 'actions["1"]'
                    action_object = actions["1"]
                    is_starter = True
                else:
                    if users_data['action_type'] == "text":
                        last_state = users_data['state']
                        last_action_object = eval(last_state)
                        for i in range(len(last_state) - 1, 0, -1):
                            if last_state[i] == "[":
                                action_location = last_state[:i]
                                break
                        if last_action_object["next"] == "end":
                            return
                        action_location += f'["{last_action_object["next"]}"]'
                        action_object = eval(action_location)
                    elif users_data['action_type'] == "interactive":
                        last_state = users_data['state']
                        last_action_object = eval(last_state)
                        for i in range(len(last_state) - 1, 0, -1):
                            if last_state[i] == "[":
                                action_location = last_state[:i]
                                break
                        response_id = message_object['interactive']['button_reply']['id']
                        if last_action_object["next"] == "end":
                            return
                        action_location += f'["{last_action_object["next"][response_id]}"]'
                        action_object = eval(action_location)

                if not is_starter:
                    if verify_data(last_action_object['expected'], message_text):
                        instance.update_user(user_id, field_name=last_action_object['name'], field_value=message_text)
                    else:
                        send_validation_error(user_id)
                        return
                send_message(user_id, action_object)
                while not action_object['user_input']:
                    print(action_object)
                    new_action_location = ""
                    for i in range(len(action_location) - 1, 0, -1):
                        if action_location[i] == "[":
                            new_action_location = action_location[:i]
                            break
                    if last_action_object["next"] == "end":
                        return
                    action_location = new_action_location + f'["{action_object["next"]}"]'
                    action_object = eval(action_location)
                    print(action_location, action_object)
                    send_message(user_id, action_object)

                instance.update_state(user_id, state=action_location, action_type=action_object['type'])


def verify_data(expected, data):
    print("===>", expected, "===", data)
    if expected == "text" or expected == "interactive":
        return True
    if expected == "email":
        return verify_email(data)
    if expected == "mobile":
        return verify_mobile(data)
    if expected == "age":
        return verify_age(data)
    if expected == "media":
        return verify_media(data)
    if expected == "date":
        return verify_date(data)
    if expected == "url":
        return verify_url(data)
    return False
