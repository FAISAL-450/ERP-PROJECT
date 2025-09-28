from django.db import models
from project.models import Project

class Customer(models.Model):
    project_name = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Project Name"
    )
    customer_name = models.CharField("Customer Name", max_length=255)
    customer_email = models.EmailField("Customer Email", unique=True)
    customer_phone = models.CharField("Customer Phone", max_length=15, unique=True)
    customer_address = models.TextField("Customer Address", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when customer was added
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp for last update

    def __str__(self):
        return self.customer_name





