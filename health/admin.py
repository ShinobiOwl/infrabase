from django.contrib import admin
from .models import ServiceHealth

@admin.register(ServiceHealth)
class ServiceHealthAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'url', 'status', 'response_time_ms', 'last_checked']
    list_filter = ['status']