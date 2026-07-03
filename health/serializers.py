from rest_framework import serializers
from .models import ServiceHealth

class ServiceHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceHealth
        fields = '__all__'