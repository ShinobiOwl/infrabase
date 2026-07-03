from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceHealthViewSet

router = DefaultRouter()
router.register(r'services', ServiceHealthViewSet)

urlpatterns = [
    path('', include(router.urls)),
]