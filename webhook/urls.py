from django.urls import path

from .views import wa_webhook

urlpatterns = [
    path('webhook', wa_webhook),
]
