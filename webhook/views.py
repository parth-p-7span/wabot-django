import datetime as dt
import json
from secrets import compare_digest

from django.conf import settings
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .models import WebhookMessage


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@non_atomic_requests
def wa_webhook(request):
    print("====> ", request.content_params)

    if 'hub.mode' in request.content_params and 'hub.verify_token' in request.content_params:
        mode = request.POST.get('hub.mode', '')
        token = request.POST.get('hub.verify_token', '')

        if compare_digest(mode, 'subscribe') and compare_digest(token, settings.WA_TOKEN):
            print('WEBHOOK VERIFIED')
            challenge = request.args.get('hub.challenge')
            return challenge, 200
        else:
            return HttpResponseForbidden(
                "Incorrect Token Passed",
                content_type='text/plain'
            )

    WebhookMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=7)
    ).delete()

    payload = json.loads(request.body)

    print("payload ==> ", payload)

    WebhookMessage.objects.create(
        received_at=timezone.now(),
        payload=payload
    )
    return HttpResponse("Message received okay")
