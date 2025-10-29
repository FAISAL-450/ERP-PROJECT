from django.contrib.auth.models import User
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departments = models.ManyToManyField(Department, blank=True)

    def __str__(self):
        dept_list = ", ".join([dept.name for dept in self.departments.all()])
        return f"{self.user.username} → {dept_list}"


