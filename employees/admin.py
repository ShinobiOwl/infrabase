from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'department', 'role', 'status']
    list_filter = ['department', 'role', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'github_username']