from django.urls import path
from . import views  # Правильный путь для импорта views из текущей директории

urlpatterns = [
    path('', views.some_view, name='some-view-name'),
    # Другие URL-маршруты
]
