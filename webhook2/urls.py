from django.urls import path

from .views import wa_webhook2

urlpatterns = [
    path('webhook', wa_webhook2),
]
