from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name']

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'role', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'github_username']
    ordering_fields = ['last_name', 'date_joined']