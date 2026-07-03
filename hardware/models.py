from django.db import models
from employees.models import Employee

class HardwareAsset(models.Model):
    TYPE_CHOICES = (
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
        ('Monitor', 'Monitor'),
        ('Phone', 'Phone'),
    )
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
        ('In Repair', 'In Repair'),
        ('Retired', 'Retired'),
    )

    asset_id = models.CharField(max_length=50, unique=True)
    asset_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    model = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.asset_id} - {self.model}"