from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.waste_dashboard, name='waste_dashboard'),
    path('htmx/log-waste/', views.log_waste_htmx, name='log_waste_htmx'),
]
