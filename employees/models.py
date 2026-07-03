from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    ROLE_CHOICES = (
        ('developer', 'Developer'),
        ('senior_developer', 'Senior Developer'),
        ('tech_lead', 'Tech Lead'),
        ('devops_engineer', 'DevOps Engineer'),
        ('qa_engineer', 'QA Engineer'),
        ('product_manager', 'Product Manager'),
        ('engineering_manager', 'Engineering Manager'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('remote', 'Remote'),
        ('inactive', 'Inactive'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    slack_handle = models.CharField(max_length=100, blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"