from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets, permissions
from .models import ComplianceReport
from .serializers import ComplianceReportSerializer
from .services import ComplianceService
from apps.accounts.models import UserRole

# ----------------- API VIEWS (DRF) ----------------- #

class ComplianceReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing compliance reports.
    Businesses can view their own. Admins/Corp Viewers can view all.
    """
    serializer_class = ComplianceReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'business_profile'):
            return ComplianceReport.objects.filter(business=user.business_profile).order_by('-period_start')
        elif user.role in [UserRole.ADMIN, UserRole.CORP_VIEWER]:
            return ComplianceReport.objects.all().order_by('-period_start')
        return ComplianceReport.objects.none()

# ----------------- UI VIEWS ----------------- #

@login_required
def compliance_dashboard(request):
    """Business dashboard to view compiled ecological impact points."""
    if request.user.role != UserRole.BUSINESS:
        return redirect('dashboard')
        
    business = request.user.business_profile
    now = timezone.now()
    
    # 1. Force a live generation for the *current* month so dashboard is always up to date
    current_report = ComplianceService.generate_monthly_report(business, now.year, now.month)
    
    # 2. Fetch all historical reports
    historical_reports = ComplianceReport.objects.filter(
        business=business
    ).exclude(id=current_report.id).order_by('-period_start')[:12]
    
    context = {
        'current': current_report,
        'history': historical_reports,
    }
    
    return render(request, 'compliance/dashboard.html', context)

@login_required
def export_reports_csv(request):
    """Endpoint for Businesses to download their own CSV"""
    if request.user.role != UserRole.BUSINESS:
        return redirect('dashboard')
        
    qs = ComplianceReport.objects.filter(business=request.user.business_profile).order_by('-period_start')
    return ComplianceService.export_reports_to_csv(qs)
