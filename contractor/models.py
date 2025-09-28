from django.db import models
from project.models import Project

class Contractor(models.Model):
    project_name = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Project Name"
    )
    contractor_name = models.CharField("Contractor Name", max_length=255)
    contractor_phone = models.CharField("Contractor Phone", max_length=15, unique=True)
    contractor_address = models.TextField("Contractor Address", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp for last update

    def __str__(self):
        return self.contractor_name
