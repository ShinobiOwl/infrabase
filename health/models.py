from django.db import models

class ServiceHealth(models.Model):
    STATUS_CHOICES = (
        ('Healthy', 'Healthy'),
        ('Degraded', 'Degraded'),
        ('Down', 'Down'),
    )

    service_name = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Healthy')
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name