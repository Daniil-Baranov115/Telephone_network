"""
URL configuration for phone_network project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('billing.urls')),  # Подключаем URLs приложения billing
]
