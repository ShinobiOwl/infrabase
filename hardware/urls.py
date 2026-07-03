from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HardwareAssetViewSet

router = DefaultRouter()
router.register(r'hardware', HardwareAssetViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]