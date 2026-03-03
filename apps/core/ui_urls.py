from django.urls import path
from . import views

urlpatterns = [
    path('htmx/notifications/', views.notification_dropdown, name='notification_dropdown'),
]
