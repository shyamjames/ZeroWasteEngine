from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import BusinessProfile

class ComplianceReport(TimeStampedModel):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='reports')
    period_start = models.DateField()
    period_end = models.DateField()
    total_waste = models.FloatField(help_text="Total waste logged in kg", default=0)
    total_redistributed = models.FloatField(help_text="Total food redistributed in kg", default=0)
    energy_generated = models.FloatField(help_text="Estimated electricity generated in kWh", default=0)
    carbon_offset = models.FloatField(help_text="Estimated CO2 offset in kg", default=0)

    class Meta:
        indexes = [
            models.Index(fields=['business', 'period_start', 'period_end']),
        ]
        unique_together = ('business', 'period_start', 'period_end')

    def __str__(self):
        return f"Report {self.business.company_name} ({self.period_start} to {self.period_end})"
