from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import ServiceHealth
from .serializers import ServiceHealthSerializer

class ServiceHealthViewSet(viewsets.ModelViewSet):
    queryset = ServiceHealth.objects.all()
    serializer_class = ServiceHealthSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['service_name']