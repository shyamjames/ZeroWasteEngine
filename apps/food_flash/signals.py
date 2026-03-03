from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FoodClaim, SurplusFoodListing
from apps.core.models import Notification

@receiver(post_save, sender=FoodClaim)
def claim_created_notification(sender, instance, created, **kwargs):
    if created:
        listing = instance.listing
        business_user = listing.business.user
        ngo_name = instance.ngo.ngo_name
        
        # Notify the Business
        Notification.objects.create(
            user=business_user,
            message=f"🔔 {ngo_name} just claimed your surplus '{listing.food_type}'! Ensure pickup readiness."
        )

@receiver(post_save, sender=SurplusFoodListing)
def listing_expired_notification(sender, instance, **kwargs):
    """
    In a real app, celery beats would trigger this state change to EXPIRED.
    For MVP, we just watch if the status changed.
    """
    if instance.status == 'EXPIRED':
        Notification.objects.create(
            user=instance.business.user,
            message=f"⚠️ Your listing for {instance.food_type} has expired without being claimed."
        )
