import os
import sys
import django

# Setup Django inside the container
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrabase_project.settings')
django.setup()

from employees.models import Department, Employee
from hardware.models import HardwareAsset
from health.models import ServiceHealth
from datetime import date
import random

print("🗑️  Clearing old data...")
Employee.objects.all().delete()
Department.objects.all().delete()
HardwareAsset.objects.all().delete()
ServiceHealth.objects.all().delete()

print("🏢 Creating Departments...")
departments_data = [
    ("Cloud Infrastructure", "Manages AWS, OCI, and on-prem server clusters"),
    ("Platform Engineering", "Builds and maintains the Internal Developer Platform (IDP)"),
    ("Site Reliability (SRE)", "Ensures 99.99% uptime and incident response"),
    ("DevOps Automation", "CI/CD pipelines, Jenkins, Terraform, Ansible"),
    ("Security (InfoSec)", "Network security, compliance, and vulnerability management"),
    ("Data Engineering", "Kafka, Spark, ETL pipelines, and data lakes"),
    ("Backend Engineering", "Core API development, microservices architecture"),
    ("Frontend Engineering", "React, UI/UX, and web performance"),
    ("QA Automation", "Selenium, Cypress, and integration testing"),
    ("Product & Design", "Product management, Jira, Figma, and user research"),
]

departments = []
for name, desc in departments_data:
    dept = Department.objects.create(name=name, description=desc)
    departments.append(dept)
print(f"✅ Created {len(departments)} departments")

print("\n👨‍💻 Creating Employees...")
employees_data = [
    # Cloud Infra
    ("Rajesh", "Krishnamurthy", "rajesh.k@infrabase.io", "Cloud Infrastructure", "senior_developer", "active", "rajesh-cloud"),
    ("Anita", "Subramanian", "anita.s@infrabase.io", "Cloud Infrastructure", "tech_lead", "active", "anita-aws"),
    # Platform Eng
    ("Selvan", "Codex", "selvan.codex@infrabase.io", "Platform Engineering", "devops_engineer", "active", "selvan-devops"),
    ("Priya", "Sharma", "priya.sharma@infrabase.io", "Platform Engineering", "engineering_manager", "active", "priya-platform"),
    # SRE
    ("Vikram", "Patel", "vikram.p@infrabase.io", "Site Reliability (SRE)", "senior_developer", "active", "vikram-sre"),
    ("Fatima", "Khan", "fatima.k@infrabase.io", "Site Reliability (SRE)", "developer", "remote", "fatima-oncall"),
    # DevOps
    ("Arjun", "Reddy", "arjun.r@infrabase.io", "DevOps Automation", "devops_engineer", "active", "arjun-jenkins"),
    ("Mei", "Chen", "mei.c@infrabase.io", "DevOps Automation", "senior_developer", "active", "mei-terraform"),
    # Security
    ("David", "Singh", "david.s@infrabase.io", "Security (InfoSec)", "senior_developer", "active", "david-sec"),
    # Data
    ("Kavitha", "Rajendran", "kavitha.r@infrabase.io", "Data Engineering", "tech_lead", "on_leave", "kavitha-data"),
    # Backend
    ("Senthil", "Nathan", "senthil.n@infrabase.io", "Backend Engineering", "tech_lead", "active", "senthil-api"),
    ("Deepa", "Venkat", "deepa.v@infrabase.io", "Backend Engineering", "developer", "active", "deepa-django"),
    # Frontend
    ("Rahul", "Menon", "rahul.m@infrabase.io", "Frontend Engineering", "senior_developer", "remote", "rahul-react"),
    # QA
    ("Nisha", "Babu", "nisha.b@infrabase.io", "QA Automation", "qa_engineer", "active", "nisha-cypress"),
    # Product
    ("Oviya", "Saravanan", "oviya.s@infrabase.io", "Product & Design", "product_manager", "active", "oviya-jira"),
]

employees = []
for fn, ln, email, dept_name, role, status, github in employees_data:
    dept = next((d for d in departments if d.name == dept_name), None)
    emp = Employee.objects.create(
        first_name=fn, last_name=ln, email=email,
        department=dept, role=role, status=status,
        github_username=github, slack_handle=github
    )
    employees.append(emp)
print(f"✅ Created {len(employees)} employees")

print("\n💻 Creating Hardware Assets...")
hardware_data = [
    ("HW-LPT-001", "laptop", "Apple", "MacBook Pro 14 M3", "assigned", employees[3], "2023-06-15", "2026-06-15", "C2XK9AML"),
    ("HW-LPT-002", "laptop", "Apple", "MacBook Pro 16 M2 Max", "assigned", employees[2], "2023-01-10", "2026-01-10", "FVJ83MB2"),
    ("HW-LPT-003", "laptop", "Dell", "XPS 15 9530", "assigned", employees[0], "2023-08-22", "2026-08-22", "DL9382KS"),
    ("HW-LPT-004", "laptop", "Lenovo", "ThinkPad X1 Carbon Gen 11", "assigned", employees[1], "2023-09-01", "2026-09-01", "LN883JKL"),
    ("HW-MNT-001", "monitor", "Dell", "U2723QE 4K USB-C", "assigned", employees[0], "2023-08-22", "2027-08-22", "DL42MNT1"),
    ("HW-MNT-002", "monitor", "LG", "34WN80C-B Ultrawide", "assigned", employees[2], "2023-01-10", "2027-01-10", "LG34UW99"),
    ("HW-PHN-001", "phone", "Apple", "iPhone 15 Pro", "assigned", employees[3], "2023-10-05", "2025-10-05", "APL15PRO1"),
    ("HW-TBL-001", "tablet", "Apple", "iPad Pro 12.9 M2", "available", None, "2022-11-20", "2024-11-20", "APLIPD01"),
    ("HW-SRV-001", "server", "Dell", "PowerEdge R750xs", "assigned", employees[4], "2022-03-15", "2027-03-15", "DLR750XS1"),
    ("HW-LPT-005", "laptop", "HP", "EliteBook 840 G10", "in_repair", None, "2022-05-10", "2025-05-10", "HPEL84010"),
]

for asset_id, atype, manu, model, status, emp, purch, warranty, serial in hardware_data:
    HardwareAsset.objects.create(
        asset_id=asset_id, asset_type=atype, manufacturer=manu, model=model,
        status=status, assigned_to=emp, 
        purchase_date=purch, warranty_expiry=warranty, serial_number=serial
    )
print(f"✅ Created {len(hardware_data)} hardware assets")

print("\n📊 Creating Service Health Checks...")
services_data = [
    ("API Gateway (Kong)", "https://api.internal.infrabase.io/health", "Healthy", 45, 99.99),
    ("Auth Service (Keycloak)", "https://auth.internal.infrabase.io/health", "Healthy", 120, 99.98),
    ("CI/CD Platform (Jenkins)", "https://jenkins.internal.infrabase.io/api/json", "Healthy", 300, 99.95),
    ("Container Registry (OCIR)", "https://ocir.internal.infrabase.io/v2/", "Healthy", 85, 99.99),
    ("Kubernetes Cluster (Prod)", "https://k8s-prod.internal.infrabase.io/healthz", "Healthy", 15, 99.99),
    ("Monitoring Stack (Prometheus)", "https://prometheus.internal.infrabase.io/-/healthy", "Healthy", 22, 99.99),
    ("Log Aggregator (Loki)", "https://loki.internal.infrabase.io/ready", "Healthy", 180, 99.90),
    ("Database Cluster (MySQL)", "https://db-prod.internal.infrabase.io:3306/", "Healthy", 8, 99.99),
    ("Object Storage (OCI)", "https://objectstorage.infrabase.io/health", "Degraded", 450, 98.50),
    ("CDN Edge (Cloudflare)", "https://cdn.infrabase.io/health", "Healthy", 12, 100.00),
]

for name, url, status, ms, uptime in services_data:
    ServiceHealth.objects.create(
        service_name=name, url=url, status=status,
        response_time_ms=ms, uptime_percentage=uptime
    )
print(f"✅ Created {len(services_data)} service health records")

print("\n" + "="*50)
print("🚀 InfraBase Database Seeding Complete!")
print("="*50)