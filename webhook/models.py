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
    message_content = models.JSONField(default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
        ]


class CustomerFeedback(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user_id = models.CharField(max_length=100)
    feedback = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class UserState(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user_id = models.CharField(max_length=100)
    state = models.JSONField(default=None, null=True)
    action_type = models.CharField(max_length=50, default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserData(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user_id = models.CharField(max_length=100)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
