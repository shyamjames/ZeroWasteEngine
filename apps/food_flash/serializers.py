from rest_framework import serializers
from .models import SurplusFoodListing, FoodClaim

class SurplusFoodListingSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.company_name', read_only=True)

    class Meta:
        model = SurplusFoodListing
        fields = [
            'id', 'business', 'business_name', 'food_type', 
            'quantity', 'unit', 'pickup_deadline', 'location', 
            'status', 'created_at'
        ]
        read_only_fields = ['status', 'business']

class FoodClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodClaim
        fields = ['id', 'listing', 'ngo', 'claimed_at', 'picked_up_at', 'status']
        read_only_fields = ['status', 'ngo', 'picked_up_at']
