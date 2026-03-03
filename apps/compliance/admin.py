from django.contrib import admin
from .models import ComplianceReport
from .services import ComplianceService

@admin.action(description="Export selected Reports to CSV")
def export_selected_to_csv(modeladmin, request, queryset):
    return ComplianceService.export_reports_to_csv(queryset)

@admin.register(ComplianceReport)
class ComplianceReportAdmin(admin.ModelAdmin):
    list_display = ['business', 'period_start', 'total_waste', 'total_redistributed', 'carbon_offset']
    list_filter = ['period_start', 'business']
    actions = [export_selected_to_csv]
