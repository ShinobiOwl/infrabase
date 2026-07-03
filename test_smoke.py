#!/usr/bin/env python
"""Quick smoke tests for InfraBase"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrabase_project.settings_dev')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.urls import reverse

def test_models():
    from employees.models import Department, Employee
    from hardware.models import HardwareAsset
    from health.models import ServiceHealth
    
    print("✓ Models imported successfully")
    print(f"  - Departments: {Department.objects.count()}")
    print(f"  - Employees: {Employee.objects.count()}")
    print(f"  - Hardware: {HardwareAsset.objects.count()}")
    print(f"  - Services: {ServiceHealth.objects.count()}")

def test_urls():
    client = Client()
    
    # Test dashboard
    response = client.get('/')
    assert response.status_code == 200, f"Dashboard failed: {response.status_code}"
    print("✓ Dashboard loads (200)")
    
    # Test API endpoints
    apis = [
        '/api/employees/list/',
        '/api/employees/departments/',
        '/api/hardware/assets/',
        '/api/health/services/',
    ]
    for api in apis:
        response = client.get(api)
        assert response.status_code == 200, f"{api} failed: {response.status_code}"
        print(f"✓ {api} → 200")

if __name__ == '__main__':
    print("=== InfraBase Smoke Tests ===\n")
    try:
        test_models()
        print()
        test_urls()
        print("\n✅ All smoke tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)