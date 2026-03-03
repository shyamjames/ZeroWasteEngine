from rest_framework import serializers
from .models import ComplianceReport

class ComplianceReportSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.company_name', read_only=True)

    class Meta:
        model = ComplianceReport
        fields = ['id', 'business', 'business_name', 'period_start', 'period_end', 
                  'total_waste', 'total_redistributed', 'energy_generated', 'carbon_offset']
        read_only_fields = fields
