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
        received_at__lte=timezone.now() - dt.timedelta(days=3)
    ).delete()

    payload = json.loads(request.body)

    try:
        message_id = payload['entry'][0]['changes'][0]['value']['messages'][0]['id']

        print("payload ==> ", payload)

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
        print("EXCEPTION ===> ", e)
        return HttpResponseForbidden(
            "Something went wrong",
            content_type='text/plain'
        )


# @atomic
# def process_request(payload):
#     if 'object' in payload and payload['object'] == 'whatsapp_business_account':
#
#         message_value = payload['entry'][0]['changes'][0]['value']
#         message_product = message_value['messaging_product']
#         if message_product == 'whatsapp':
#             if 'messages' in message_value:
#                 author_name = message_value['contacts'][0]['profile']['name']
#                 message_object = message_value['messages'][0]
#                 message_type = message_object['type']
#                 message_id = message_object['id']
#                 user_id = message_object['from']
#
#                 mark_as_read(message_id)
#
#                 users_data = instance.get_user_data(user_id)
#
#                 last_msg = -2
#                 for i, value in enumerate(users_data):
#                     if value == 0:
#                         last_msg = i - 1
#                         break
#
#                 print("-------->", users_data)
#
#                 if message_type == "interactive":
#                     message_text = message_object['interactive']['button_reply']['title']
#                     instance.update_user(user_id, "platform", message_text)
#                     # clickup.set_custom_field_value(task_id, constants.mediator_field_id,
#                     #                                [constants.custom_field_ids[message_text]])
#                     string = "11. Please upload your resume then you are finish with the process."
#                     response = send_message(string, message_object['from'])
#                     print(response)
#
#                 elif message_type == "document" and last_msg == 10:
#                     doc_name = message_object['document']['filename']
#                     doc_id = message_object['document']['id']
#                     instance.update_user(user_id, "resume", {"id": doc_id, "name": doc_name})
#                     string = "Thank you for applying to 7Span, our HR will contact you shortly."
#                     response = send_message(string, message_object['from'])
#                     print(response)
#
#                 elif message_type == "text":
#                     message_text = message_object['text']['body']
#
#                     if message_text.lower() == "hi" or message_text.lower() == "hello" or message_text.lower() == "hii":
#                         instance.delete_data(user_id)
#                         instance.create_user(user_id, author_name)
#                         # response = clickup.create_new_task(author_name)
#                         # clickup.set_custom_field_value(response['id'], constants.whatsapp_field_id,
#                         #                                message_object['from'])
#
#                         string = f"Hi {author_name},\nThankyou for applying in 7Span. I am auto-reply Bot of 7Span. You just have to answer few questions to send your application.\n\n1.Please enter your full name."
#                         response = send_message(string, message_object['from'])
#                         print(response)
#                         last_msg = -2
#
#                     if last_msg == 0:
#                         instance.update_user(user_id, "name", message_text)
#                         # clickup.update_task_name(task_id, message_text)
#                         # clickup.set_custom_field_value(task_id, constants.name_field_id, message_text)
#                         string = "2. Please enter your official email address."
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 1:
#                         instance.update_user(user_id, "email", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.email_field_id, message_text)
#                         string = "3. Please enter your official mobile number."
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 2:
#                         instance.update_user(user_id, "mobile", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.mobile_field_id, f'+91{message_text}')
#                         string = "4. Please enter your skills separated by comma. e.g. React, Laravel, Angular, Python"
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 3:
#                         instance.update_user(user_id, "skills", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.skills_field_id, message_text)
#                         string = "5. Please enter your total years of experience."
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 4:
#                         instance.update_user(user_id, "experience", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.experience_field_id, message_text)
#                         string = "6. Please enter your current/last company name"
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 5:
#                         instance.update_user(user_id, "last_company", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.last_company_field_id, message_text)
#                         string = "7. Please enter your current CTC(Per Annum)"
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 6:
#                         instance.update_user(user_id, "ctc", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.ctc_field_id, message_text)
#                         string = "8. Please enter your current location"
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 7:
#                         instance.update_user(user_id, "location", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.location_field_id, message_text)
#                         string = "9. Please enter little summary about you."
#                         response = send_message(string, message_object['from'])
#                         print(response)
#
#                     if last_msg == 8:
#                         instance.update_user(user_id, "summary", message_text)
#                         # clickup.set_custom_field_value(task_id, constants.summary_field_id, message_text)
#                         response = send_selection_msg(message_object['from'])
#                         print(response)
#
#         return 'EVENT_RECEIVED', 200


@atomic
def process_request(payload, is_recursive=False):
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

                msg_to_send = 0
                for i, (key, value) in enumerate(users_data.items()):
                    if value == 0:
                        msg_to_send = i
                        break

                print("-------->", users_data, "-----", msg_to_send)
                msg_action = actions['steps'][msg_to_send]

                if not msg_action['user_input']:
                    send_message(user_id, msg_action)
                    instance.update_user(user_id, msg_action['name'], "sent")
                    process_request(payload, is_recursive=True)
                else:
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
                    send_message(user_id, msg_action)
                    if not is_recursive:
                        instance.update_user(user_id, msg_action['name'], message_text)

                    print(instance.get_user_data(user_id))
        return 'EVENT_RECEIVED', 200
