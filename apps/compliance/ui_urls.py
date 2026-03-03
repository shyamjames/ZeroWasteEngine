from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.compliance_dashboard, name='compliance_dashboard'),
    path('export/csv/', views.export_reports_csv, name='export_csv'),
]
