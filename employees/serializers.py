from rest_framework import serializers
from .models import Department, Employee

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)

    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True, default=None)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['date_joined']