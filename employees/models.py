from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    ROLE_CHOICES = (
        ('Developer', 'Developer'),
        ('DevOps', 'DevOps'),
        ('Manager', 'Manager'),
        ('QA', 'QA'),
    )
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('On Leave', 'On Leave'),
        ('Remote', 'Remote'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    github_username = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"