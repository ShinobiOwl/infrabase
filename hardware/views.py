from rest_framework import viewsets
from .models import HardwareAsset
from .serializers import HardwareAssetSerializer

class HardwareAssetViewSet(viewsets.ModelViewSet):
    queryset = HardwareAsset.objects.select_related('assigned_to').all()
    serializer_class = HardwareAssetSerializer