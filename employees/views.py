from rest_framework import viewsets
from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department').all()
    serializer_class = EmployeeSerializer