from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Root redirects to dashboard
    path('', lambda req: redirect('dashboard'), name='home'),

    # UI routes under generic namespace
    path('flash/', include('apps.food_flash.ui_urls')),
    
    # Dedicated API v1 namespace
    path('api/v1/food-flash/', include('apps.food_flash.api_urls')),

    # JWT Authentication paths (future integration for mobile)
    path('api/v1/auth/', include('rest_framework.urls')),
]
