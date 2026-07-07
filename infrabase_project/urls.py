import json
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
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


# Custom HTML pages
def employees_page(request):
    employees = Employee.objects.select_related('department').all()
    departments = Department.objects.all()
    
    # Search functionality
    search = request.GET.get('search', '')
    dept_filter = request.GET.get('department', '')
    
    if search:
        employees = employees.filter(
            first_name__icontains=search
        ) | employees.filter(
            last_name__icontains=search
        ) | employees.filter(
            email__icontains=search
        )
    
    if dept_filter:
        employees = employees.filter(department__name=dept_filter)
    
    context = {
        'employees': employees,
        'departments': departments,
        'search': search,
        'dept_filter': dept_filter,
    }
    return render(request, 'pages/employees.html', context)


def hardware_page(request):
    assets = HardwareAsset.objects.select_related('assigned_to').all()
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        assets = assets.filter(status=status_filter)
    
    context = {
        'assets': assets,
        'status_filter': status_filter,
    }
    return render(request, 'pages/hardware.html', context)


def health_page(request):
    services = ServiceHealth.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'pages/health.html', context)


# CRUD Operations
@require_http_methods(["POST"])
def add_employee(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    department_id = request.POST.get('department')
    role = request.POST.get('role')
    status = request.POST.get('status', 'active')
    
    if not all([first_name, last_name, email, department_id, role]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    
    try:
        department = Department.objects.get(id=department_id)
        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            role=role,
            status=status,
        )
        return JsonResponse({'success': True, 'id': employee.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def add_hardware(request):
    asset_id = request.POST.get('asset_id')
    asset_type = request.POST.get('asset_type')
    manufacturer = request.POST.get('manufacturer')
    model = request.POST.get('model')
    status = request.POST.get('status', 'available')
    
    if not all([asset_id, asset_type, manufacturer, model]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    
    try:
        asset = HardwareAsset.objects.create(
            asset_id=asset_id,
            asset_type=asset_type,
            manufacturer=manufacturer,
            model=model,
            status=status,
        )
        return JsonResponse({'success': True, 'id': asset.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def update_service_status(request):
    service_id = request.POST.get('service_id')
    new_status = request.POST.get('status')
    response_time = request.POST.get('response_time')
    
    if not all([service_id, new_status, response_time]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    
    try:
        service = ServiceHealth.objects.get(id=service_id)
        service.status = new_status
        service.response_time_ms = int(response_time)
        service.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
    
    # Pages
    path('employees/', employees_page, name='employees-page'),
    path('hardware/', hardware_page, name='hardware-page'),
    path('services/', health_page, name='health-page'),
    
    # CRUD APIs
    path('api/add-employee/', add_employee, name='add-employee'),
    path('api/add-hardware/', add_hardware, name='add-hardware'),
    path('api/update-service/', update_service_status, name='update-service'),
]