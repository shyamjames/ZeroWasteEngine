from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import WasteLog
from .serializers import WasteLogSerializer
from .services import ConversionEngine
from apps.accounts.models import UserRole
import json

# ----------------- API VIEWS (DRF) ----------------- #

class WasteLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint for businesses to log their non-edible food waste.
    """
    serializer_class = WasteLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'business_profile'):
            return WasteLog.objects.filter(business=user.business_profile).order_by('-logged_at')
        elif user.role == UserRole.PLANT_OPERATOR:
            return WasteLog.objects.all().order_by('-logged_at')
        return WasteLog.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'business_profile'):
            raise serializers.ValidationError("Only businesses can log waste.")
        
        weight_kg = serializer.validated_data['weight_kg']
        
        # Use the service layer to calculate output
        calc_result = ConversionEngine.calculate(weight_kg)

        serializer.save(
            business=user.business_profile,
            conversion_output=calc_result
        )


# ----------------- HTMX & UI VIEWS ----------------- #

@login_required
def waste_dashboard(request):
    """Analytics and logging board for Businesses"""
    if request.user.role != UserRole.BUSINESS:
        return render(request, 'base.html', {'error': 'Unauthorized'})
    
    logs = WasteLog.objects.filter(business=request.user.business_profile).order_by('-logged_at')[:20]
    
    # Calculate simple aggregate for the chart
    total_waste = sum(log.weight_kg for log in logs)
    total_energy = sum(log.conversion_output.get('electricity_kwh', 0) for log in logs if log.conversion_output)
    total_compost = sum(log.conversion_output.get('compost_kg', 0) for log in logs if log.conversion_output)

    context = {
        'logs': logs,
        'total_waste': total_waste,
        'total_energy': round(total_energy, 2),
        'total_compost': round(total_compost, 2),
    }
    
    return render(request, 'bio_converter/waste_dashboard.html', context)

@login_required
def log_waste_htmx(request):
    """HTMX endpoint to append a new waste entry without reload"""
    if request.method == 'POST' and request.user.role == UserRole.BUSINESS:
        try:
            weight_kg = float(request.POST.get('weight_kg'))
            waste_type = request.POST.get('waste_type', 'Mixed organic')
            
            # Service layer calculation
            output = ConversionEngine.calculate(weight_kg)
            
            WasteLog.objects.create(
                business=request.user.business_profile,
                weight_kg=weight_kg,
                waste_type=waste_type,
                conversion_output=output
            )
            
            # Re-render partial table
            logs = WasteLog.objects.filter(business=request.user.business_profile).order_by('-logged_at')[:20]
            
            # Returning a custom HX-Trigger header will tell Chart.js to update on the frontend later
            response = render(request, 'bio_converter/partials/waste_logs.html', {'logs': logs})
            response['HX-Trigger'] = 'wasteLogged'
            return response
        except ValueError:
            from django.http import HttpResponseBadRequest
            return HttpResponseBadRequest("Invalid weight")
    from django.http import HttpResponseBadRequest
    return HttpResponseBadRequest()
