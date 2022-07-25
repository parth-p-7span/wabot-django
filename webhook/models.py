from django.db import models
import uuid


class WebhookMessage(models.Model):
    message_id = models.CharField(max_length=100)
    received_at = models.DateTimeField(help_text="When we received the event.")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]


class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user_id = models.CharField(max_length=100)
    sent_by_system = models.BooleanField(default=False,
                                         help_text="returns True if message is sent by Bot, else returns False.")
    message_content = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
