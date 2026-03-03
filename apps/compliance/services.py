import csv
from django.http import HttpResponse
from django.utils import timezone
from .models import ComplianceReport
from apps.food_flash.models import SurplusFoodListing, ListingStatus
from apps.bio_converter.models import WasteLog

class ComplianceService:
    @staticmethod
    def generate_monthly_report(business, year, month):
        """
        Aggregate data for a given month and generate/update the Compliance Report.
        """
        import calendar
        from datetime import date
        
        _, last_day = calendar.monthrange(year, month)
        period_start = date(year, month, 1)
        period_end = date(year, month, last_day)
        
        # 1. Calculate Redistributed Food (Successfully Picked Up or Claimed)
        redistributed_listings = SurplusFoodListing.objects.filter(
            business=business,
            created_at__date__gte=period_start,
            created_at__date__lte=period_end,
            status__in=[ListingStatus.CLAIMED, ListingStatus.PICKED_UP]
        )
        
        # Approximate 0.5kg per "Meal" if unit is Meals, otherwise take direct quantity if Kg.
        # This is a simplified proxy since units can differ.
        total_redistributed_kg = 0
        for listing in redistributed_listings:
            if listing.unit.lower() == 'kg':
                total_redistributed_kg += listing.quantity
            elif listing.unit.lower() == 'meals':
                total_redistributed_kg += listing.quantity * 0.5
            else:
                total_redistributed_kg += listing.quantity * 0.2 # fallback approximation for packets
                
        # 2. Calculate Bio Waste conversions
        waste_logs = WasteLog.objects.filter(
            business=business,
            logged_at__date__gte=period_start,
            logged_at__date__lte=period_end
        )
        
        total_waste = sum(log.weight_kg for log in waste_logs)
        total_energy = sum(log.conversion_output.get('electricity_kwh', 0) for log in waste_logs if log.conversion_output)
        total_offset = sum(log.conversion_output.get('co2_offset_kg', 0) for log in waste_logs if log.conversion_output)

        # 3. Create or update the report
        report, created = ComplianceReport.objects.update_or_create(
            business=business,
            period_start=period_start,
            period_end=period_end,
            defaults={
                'total_waste': round(total_waste, 2),
                'total_redistributed': round(total_redistributed_kg, 2),
                'energy_generated': round(total_energy, 2),
                'carbon_offset': round(total_offset, 2)
            }
        )
        return report

    @staticmethod
    def export_reports_to_csv(reports_queryset):
        """Generate a CSV response for the given reports."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="eco_compliance_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Business', 'Period Start', 'Period End', 'Waste Logged (kg)', 'Food Redistributed (kg)', 'Energy Gen (kWh)', 'CO2 Offset (kg)'])
        
        for report in reports_queryset:
            writer.writerow([
                report.business.company_name,
                report.period_start,
                report.period_end,
                report.total_waste,
                report.total_redistributed,
                report.energy_generated,
                report.carbon_offset
            ])
            
        return response
