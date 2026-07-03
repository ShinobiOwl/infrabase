from django.contrib import admin
from .models import HardwareAsset

@admin.register(HardwareAsset)
class HardwareAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_id', 'asset_type', 'manufacturer', 'model', 'assigned_to', 'status']
    list_filter = ['asset_type', 'status']
    search_fields = ['asset_id', 'manufacturer', 'model', 'serial_number']