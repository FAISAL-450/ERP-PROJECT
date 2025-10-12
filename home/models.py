from django.db import models

class Project(models.Model):
    name_of_project = models.CharField(max_length=255)
    project_address = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    contact_person_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


