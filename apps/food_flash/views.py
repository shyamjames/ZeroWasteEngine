from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import SurplusFoodListing, FoodClaim, ListingStatus, ClaimStatus
from .serializers import SurplusFoodListingSerializer, FoodClaimSerializer
from apps.accounts.models import UserRole

# ----------------- API VIEWS (DRF) ----------------- #

class SurplusFoodListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Surplus Food.
    NGOs see available feed. Businesses see their own history.
    """
    serializer_class = SurplusFoodListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.NGO:
            return SurplusFoodListing.objects.filter(
                status=ListingStatus.AVAILABLE, 
                pickup_deadline__gt=timezone.now()
            ).order_by('pickup_deadline')
        elif hasattr(user, 'business_profile'):
            return SurplusFoodListing.objects.filter(
                business=user.business_profile
            ).order_by('-created_at')
        return SurplusFoodListing.objects.all()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'business_profile'):
            serializer.save(business=self.request.user.business_profile)

    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        listing = self.get_object()
        user = request.user
        
        if user.role != UserRole.NGO or not hasattr(user, 'ngo_profile'):
            return Response({"error": "Only authorized NGOs can claim food."}, status=status.HTTP_403_FORBIDDEN)
            
        if listing.status != ListingStatus.AVAILABLE:
            return Response({"error": "Listing is no longer available."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create claim
        claim = FoodClaim.objects.create(listing=listing, ngo=user.ngo_profile)
        
        # Update listing status
        listing.status = ListingStatus.CLAIMED
        listing.save()
        
        serializer = FoodClaimSerializer(claim)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------- HTMX & UI VIEWS ----------------- #

@login_required
def dashboard_redirect(request):
    """Router redirecting users to their specific role dashboard"""
    if request.user.role == UserRole.NGO:
        return redirect('ngo_dashboard')
    elif request.user.role == UserRole.BUSINESS:
        return redirect('business_dashboard')
    elif request.user.role == UserRole.ADMIN:
        return redirect('/admin/')
    return render(request, 'base.html')


@login_required
def ngo_dashboard(request):
    if request.user.role != UserRole.NGO:
        return redirect('dashboard')
    return render(request, 'food_flash/ngo_dashboard.html')


@login_required
def business_dashboard(request):
    if request.user.role != UserRole.BUSINESS:
        return redirect('dashboard')
    
    # Context data for business
    listings = SurplusFoodListing.objects.filter(
        business=request.user.business_profile
    ).order_by('-created_at')[:10]
    
    return render(request, 'food_flash/business_dashboard.html', {'listings': listings})


@login_required
def live_feed_partial(request):
    """
    HTMX polling endpoint returning only HTML rows of available listings
    for the real-time live feed.
    """
    listings = SurplusFoodListing.objects.filter(
        status=ListingStatus.AVAILABLE,
        pickup_deadline__gt=timezone.now()
    ).select_related('business').order_by('pickup_deadline')
    
    return render(request, 'food_flash/partials/listing_feed.html', {'listings': listings})

@login_required
def create_listing_htmx(request):
    """Endpoint for creating a listing entirely via HTMX form submission"""
    if request.method == 'POST' and request.user.role == UserRole.BUSINESS:
        food_type = request.POST.get('food_type')
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')
        location = request.POST.get('location')
        pickup_deadline = request.POST.get('pickup_deadline')
        
        SurplusFoodListing.objects.create(
            business=request.user.business_profile,
            food_type=food_type,
            quantity=quantity,
            unit=unit,
            location=location,
            pickup_deadline=pickup_deadline,
            status=ListingStatus.AVAILABLE
        )
        # Re-render the business listings partial to auto-update UI
        listings = SurplusFoodListing.objects.filter(
            business=request.user.business_profile
        ).order_by('-created_at')[:10]
        return render(request, 'food_flash/partials/business_listings.html', {'listings': listings})
    
    return Response(status=400)

@login_required
def claim_listing_htmx(request, pk):
    """HTMX endpoint to claim an item, returning updated row"""
    if request.method == 'POST' and request.user.role == UserRole.NGO:
        listing = get_object_or_404(SurplusFoodListing, pk=pk)
        if listing.status == ListingStatus.AVAILABLE:
            FoodClaim.objects.create(listing=listing, ngo=request.user.ngo_profile)
            listing.status = ListingStatus.CLAIMED
            listing.save()
        
        # Re-render immediately updated listing feed
        return live_feed_partial(request)
