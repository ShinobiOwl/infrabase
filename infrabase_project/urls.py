import json
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from employees.models import Employee, Department
from hardware.models import HardwareAsset
from health.models import ServiceHealth


def dashboard(request):
    context = _get_dashboard_context()
    return render(request, 'dashboard.html', context)


def _get_dashboard_context():
    services = ServiceHealth.objects.all()
    services_json = json.dumps([
        {
            'name': s.service_name,
            'status': s.status,
            'response_time_ms': s.response_time_ms,
            'uptime_percentage': float(s.uptime_percentage),
        }
        for s in services
    ])
    return {
        'employee_count': Employee.objects.filter(status='active').count(),
        'department_count': Department.objects.count(),
        'hardware_count': HardwareAsset.objects.count(),
        'assigned_hardware': HardwareAsset.objects.filter(status='assigned').count(),
        'services': services,
        'services_json': services_json,
        'healthy_count': ServiceHealth.objects.filter(status='Healthy').count(),
        'recent_employees': Employee.objects.order_by('-date_joined')[:5],
    }


def htmx_stats(request):
    ctx = _get_dashboard_context()
    return render(request, 'partials/stats.html', ctx)


def htmx_services(request):
    ctx = _get_dashboard_context()
    return render(request, 'partials/services.html', ctx)


def htmx_employees(request):
    ctx = _get_dashboard_context()
    return render(request, 'partials/employees.html', ctx)


def htmx_health_chart_data(request):
    services = ServiceHealth.objects.all()
    data = [
        {
            'name': s.service_name,
            'status': s.status,
            'response_time_ms': s.response_time_ms,
            'uptime_percentage': float(s.uptime_percentage),
        }
        for s in services
    ]
    return JsonResponse(data, safe=False)


def htmx_asset_chart_data(request):
    assigned = HardwareAsset.objects.filter(status='assigned').count()
    available = HardwareAsset.objects.filter(status='available').count()
    in_repair = HardwareAsset.objects.filter(status='in_repair').count()
    return JsonResponse({
        'assigned': assigned,
        'available': available,
        'in_repair': in_repair,
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('api/employees/', include('employees.urls')),
    path('api/hardware/', include('hardware.urls')),
    path('api/health/', include('health.urls')),
    
    # HTMX partials
    path('htmx/stats/', htmx_stats, name='htmx-stats'),
    path('htmx/services/', htmx_services, name='htmx-services'),
    path('htmx/employees/', htmx_employees, name='htmx-employees'),
    path('htmx/chart/health/', htmx_health_chart_data, name='htmx-health-chart'),
    path('htmx/chart/assets/', htmx_asset_chart_data, name='htmx-asset-chart'),
]