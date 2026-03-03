import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.accounts.models import CustomUser, UserRole, BusinessProfile, NGOProfile
from apps.food_flash.models import SurplusFoodListing, ListingStatus, FoodClaim
from apps.bio_converter.models import WasteLog
from apps.bio_converter.services import ConversionEngine

def populate():
    # Create Business User
    business_user, created = CustomUser.objects.get_or_create(
        username='hotel_kochi',
        email='contact@hotelkochi.com',
        role=UserRole.BUSINESS
    )
    if created:
        business_user.set_password('hotelpassword123')
        business_user.save()
        
    business_profile, _ = BusinessProfile.objects.get_or_create(
        user=business_user,
        defaults={
            'company_name': 'Grand Hyatt Kochi Bolgatty',
            'registration_number': 'KOC-12345',
            'location_address': 'Bolgatty Island, Kochi, Kerala',
            'contact_phone': '+91-9876543210'
        }
    )

    # Create NGO User
    ngo_user, created = CustomUser.objects.get_or_create(
        username='ngo_kochi',
        email='hello@ngokochi.org',
        role=UserRole.NGO
    )
    if created:
        ngo_user.set_password('ngopassword123')
        ngo_user.save()

    ngo_profile, _ = NGOProfile.objects.get_or_create(
        user=ngo_user,
        defaults={
            'ngo_name': 'Robin Hood Army Kochi',
            'license_id': 'NGO-KER-999',
            'service_areas': 'Ernakulam, Fort Kochi, Edappally',
            'contact_phone': '+91-9998887776'
        }
    )

    # Add Surplus Food Listings
    now = timezone.now()
    SurplusFoodListing.objects.get_or_create(
        business=business_profile,
        food_type='Vegetable Biriyani and Curries',
        quantity=50,
        unit='Meals',
        pickup_deadline=now + timedelta(hours=3),
        location='Gate 2 - Kitchen Loading Bay',
        status=ListingStatus.AVAILABLE
    )

    SurplusFoodListing.objects.get_or_create(
        business=business_profile,
        food_type='Assorted Bread and Pastries',
        quantity=15,
        unit='Kg',
        pickup_deadline=now + timedelta(hours=5),
        location='Bakery Backdoor',
        status=ListingStatus.AVAILABLE
    )
    
    # Claimed listing
    claimed_listing, _ = SurplusFoodListing.objects.get_or_create(
        business=business_profile,
        food_type='Buffet Surplus - Mixed Non-Veg',
        quantity=30,
        unit='Meals',
        pickup_deadline=now + timedelta(hours=1),
        location='Main Kitchen',
        status=ListingStatus.CLAIMED
    )
    
    FoodClaim.objects.get_or_create(
        listing=claimed_listing,
        ngo=ngo_profile
    )

    # Add Waste Logs
    for i in range(5):
        weight = 25.5 + (i * 5)
        calc = ConversionEngine.calculate(weight)
        WasteLog.objects.get_or_create(
            business=business_profile,
            weight_kg=weight,
            waste_type='Mixed Organic',
            defaults={'conversion_output': calc}
        )

    print("Database successfully populated with mock data.")
    print("---------------------------------------------")
    print("BUSINESS ACCOUNT")
    print("Username: hotel_kochi")
    print("Password: hotelpassword123")
    print("Company: Grand Hyatt Kochi Bolgatty")
    print("---------------------------------------------")
    print("NGO ACCOUNT")
    print("Username: ngo_kochi")
    print("Password: ngopassword123")
    print("NGO: Robin Hood Army Kochi")
    print("---------------------------------------------")

if __name__ == '__main__':
    populate()
