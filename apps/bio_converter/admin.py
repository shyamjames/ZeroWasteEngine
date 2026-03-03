from django.contrib import admin
from .models import ConversionMetrics, WasteLog

@admin.register(ConversionMetrics)
class ConversionMetricsAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'biogas_per_kg', 'electricity_per_m3_biogas', 'compost_per_kg', 'co2_offset_per_kg']
    list_filter = ['is_active']

@admin.register(WasteLog)
class WasteLogAdmin(admin.ModelAdmin):
    list_display = ['business', 'weight_kg', 'waste_type', 'logged_at']
    list_filter = ['waste_type', 'logged_at']
    search_fields = ['business__company_name']
    readonly_fields = ['conversion_output']
