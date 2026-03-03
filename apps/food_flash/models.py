from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel
from apps.accounts.models import BusinessProfile, NGOProfile

class ListingStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', _('Available')
    CLAIMED = 'CLAIMED', _('Claimed')
    EXPIRED = 'EXPIRED', _('Expired')
    PICKED_UP = 'PICKED_UP', _('Picked Up')

class ClaimStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    COMPLETED = 'COMPLETED', _('Completed')
    NO_SHOW = 'NO_SHOW', _('No Show')

class SurplusFoodListing(TimeStampedModel):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='food_listings')
    food_type = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50) # e.g., 'Meals', 'Kg', 'Packets'
    pickup_deadline = models.DateTimeField()
    location = models.TextField()
    status = models.CharField(max_length=20, choices=ListingStatus.choices, default=ListingStatus.AVAILABLE)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'pickup_deadline']),
            models.Index(fields=['business']),
        ]

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.food_type} by {self.business.company_name}"

class FoodClaim(TimeStampedModel):
    listing = models.OneToOneField(SurplusFoodListing, on_delete=models.CASCADE, related_name='claim')
    ngo = models.ForeignKey(NGOProfile, on_delete=models.CASCADE, related_name='claims')
    claimed_at = models.DateTimeField(auto_now_add=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ClaimStatus.choices, default=ClaimStatus.PENDING)

    class Meta:
        indexes = [
            models.Index(fields=['listing', 'ngo']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Claim by {self.ngo.ngo_name} for {self.listing.food_type}"
