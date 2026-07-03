from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import HardwareAsset
from .serializers import HardwareAssetSerializer

class HardwareAssetViewSet(viewsets.ModelViewSet):
    queryset = HardwareAsset.objects.select_related('assigned_to').all()
    serializer_class = HardwareAssetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['asset_type', 'status', 'assigned_to']
    search_fields = ['asset_id', 'manufacturer', 'model', 'serial_number']
    ordering_fields = ['purchase_date', 'asset_id']