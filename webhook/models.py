from django.db import models


class WebhookMessage(models.Model):
    message_id = models.CharField(max_length=100)
    received_at = models.DateTimeField(help_text="When we received the event.")
    payload = models.JSONField(default=None,    null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]
