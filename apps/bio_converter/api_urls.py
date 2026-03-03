from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WasteLogViewSet

router = DefaultRouter()
router.register(r'logs', WasteLogViewSet, basename='waste-logs')

urlpatterns = [
    path('', include(router.urls)),
]
