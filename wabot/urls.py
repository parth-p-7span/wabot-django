from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('webhook.urls')),
    path('', include('webhook2.urls'))
]
