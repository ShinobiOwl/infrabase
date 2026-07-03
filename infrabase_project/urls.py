from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from employees.models import Employee, Department
from hardware.models import HardwareAsset
from health.models import ServiceHealth

def dashboard(request):
    context = {
        'employee_count': Employee.objects.filter(status='active').count(),
        'department_count': Department.objects.count(),
        'hardware_count': HardwareAsset.objects.count(),
        'assigned_hardware': HardwareAsset.objects.filter(status='assigned').count(),
        'services': ServiceHealth.objects.all(),
        'healthy_count': ServiceHealth.objects.filter(status='Healthy').count(),
        'recent_employees': Employee.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'dashboard.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('api/employees/', include('employees.urls')),
    path('api/hardware/', include('hardware.urls')),
    path('api/health/', include('health.urls')),
]