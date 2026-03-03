from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Root redirects to dashboard
    path('', lambda req: redirect('dashboard'), name='home'),

    # UI routes under generic namespace
    path('accounts/', include('apps.accounts.ui_urls')),
    path('core/', include('apps.core.ui_urls')),
    path('flash/', include('apps.food_flash.ui_urls')),
    path('bio/', include('apps.bio_converter.ui_urls')),
    path('compliance/', include('apps.compliance.ui_urls')),
    
    # Dedicated API v1 namespace
    path('api/v1/food-flash/', include('apps.food_flash.api_urls')),
    path('api/v1/bio-converter/', include('apps.bio_converter.api_urls')),
    path('api/v1/compliance/', include('apps.compliance.api_urls')),

    # JWT Authentication paths (future integration for mobile)
    path('api/v1/auth/', include('rest_framework.urls')),
]
