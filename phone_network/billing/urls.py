from django.urls import path
from . import views

urlpatterns = [
    # Здесь будут маршруты вашего приложения
    path('', views.index, name='index'),  # временный маршрут
]