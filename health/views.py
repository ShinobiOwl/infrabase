from rest_framework import viewsets
from .models import ServiceHealth
from .serializers import ServiceHealthSerializer

class ServiceHealthViewSet(viewsets.ModelViewSet):
    queryset = ServiceHealth.objects.all()
    serializer_class = ServiceHealthSerializer