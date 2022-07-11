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
    params = request.GET.dict()
    if 'hub.mode' in params and 'hub.verify_token' in params:
        if compare_digest(params['hub.mode'], 'subscribe') and compare_digest(params['hub.verify_token'], settings.WA_TOKEN):
            print('WEBHOOK VERIFIED')
            return HttpResponse(params['hub.challenge'], status=200)
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
    return HttpResponse("Message received okay", status=200)
