from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.core.models import TimeStampedModel

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Admin')
    BUSINESS = 'BUSINESS', _('Hotel/Business')
    NGO = 'NGO', _('NGO')
    PLANT_OPERATOR = 'PLANT_OPERATOR', _('Waste Plant Operator')
    CORP_VIEWER = 'CORP_VIEWER', _('Corporation Viewer')

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ADMIN,
        help_text=_('Role dictates permissions and accessible dashboards.')
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"


class BusinessProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_profile')
    company_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    location_address = models.TextField()
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name


class NGOProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ngo_profile')
    ngo_name = models.CharField(max_length=255)
    license_id = models.CharField(max_length=100)
    service_areas = models.TextField(help_text="Comma separated service areas")
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.ngo_name
