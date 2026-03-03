from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('business/', views.business_dashboard, name='business_dashboard'),
    path('ngo/', views.ngo_dashboard, name='ngo_dashboard'),
    
    # HTMX Partial Endpoints
    path('htmx/live-feed/', views.live_feed_partial, name='live_feed'),
    path('htmx/create-listing/', views.create_listing_htmx, name='create_listing_htmx'),
    path('htmx/claim/<int:pk>/', views.claim_listing_htmx, name='claim_listing_htmx'),
]
