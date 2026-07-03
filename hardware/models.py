from django.db import models
from employees.models import Employee

class HardwareAsset(models.Model):
    ASSET_TYPE_CHOICES = (
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('monitor', 'Monitor'),
        ('phone', 'Phone'),
        ('tablet', 'Tablet'),
        ('server', 'Server'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('in_repair', 'In Repair'),
        ('retired', 'Retired'),
    )

    asset_id = models.CharField(max_length=50, unique=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='hardware_assets')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purchase_date = models.DateField()
    warranty_expiry = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['asset_id']

    def __str__(self):
        return f"{self.asset_id} - {self.manufacturer} {self.model}"