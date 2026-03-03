from rest_framework import serializers
from .models import WasteLog

class WasteLogSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.company_name', read_only=True)

    class Meta:
        model = WasteLog
        fields = ['id', 'business', 'business_name', 'weight_kg', 'waste_type', 'conversion_output', 'logged_at']
        read_only_fields = ['business', 'conversion_output']
