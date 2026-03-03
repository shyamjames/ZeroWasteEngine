from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import BusinessProfile

class ConversionMetrics(TimeStampedModel):
    """Singleton pattern model for standard co-efficients. Editable by Admin."""
    name = models.CharField(max_length=100, default='Standard Coefficients')
    biogas_per_kg = models.FloatField(default=0.04, help_text="m³ of biogas per kg of food waste")
    electricity_per_m3_biogas = models.FloatField(default=2.0, help_text="kWh of electricity per m³ of biogas")
    compost_per_kg = models.FloatField(default=0.3, help_text="kg of compost per kg of food waste")
    co2_offset_per_kg = models.FloatField(default=2.5, help_text="kg of CO2 offset per kg of food waste")
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Set all other instances to inactive
            ConversionMetrics.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - Active: {self.is_active}"

class WasteLog(TimeStampedModel):
    """Tracks waste weight given by businesses."""
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='waste_logs')
    weight_kg = models.FloatField()
    waste_type = models.CharField(max_length=100, default='Mixed organic')
    # Store standard conversion calculation in case the coefficients change later
    conversion_output = models.JSONField(
        blank=True, 
        null=True, 
        help_text="Snapshot of calculated metrics at the time of logging"
    )
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['business', 'logged_at']),
        ]

    def __str__(self):
        return f"{self.weight_kg} kg waste from {self.business.company_name} on {self.logged_at.date()}"
