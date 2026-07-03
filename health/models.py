from django.db import models

class ServiceHealth(models.Model):
    STATUS_CHOICES = (
        ('Healthy', 'Healthy'),
        ('Degraded', 'Degraded'),
        ('Down', 'Down'),
        ('Maintenance', 'Maintenance'),
    )

    service_name = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Healthy')
    response_time_ms = models.PositiveIntegerField(default=0, help_text="Response time in ms")
    uptime_percentage = models.FloatField(default=100.0)
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['service_name']
        verbose_name_plural = 'Services Health'

    def __str__(self):
        return f"{self.service_name} - {self.status}"