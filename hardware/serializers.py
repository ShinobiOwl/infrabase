from rest_framework import serializers
from .models import HardwareAsset

class HardwareAssetSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.__str__', read_only=True, default=None)

    class Meta:
        model = HardwareAsset
        fields = '__all__'