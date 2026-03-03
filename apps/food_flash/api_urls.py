from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurplusFoodListingViewSet

router = DefaultRouter()
router.register(r'listings', SurplusFoodListingViewSet, basename='surplus-listings')

urlpatterns = [
    path('', include(router.urls)),
]
