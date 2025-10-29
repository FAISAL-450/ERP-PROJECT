
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import Profile, Department
from django.conf import settings

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        # Normalize email
        email = instance.email.lower().strip()

        # Azure AD department mapping
        department_map = getattr(settings, "DEPARTMENT_EMAIL_MAP", {})
        mapped_departments = department_map.get(email)

        if mapped_departments:
            # Convert comma-separated string to list if needed
            if isinstance(mapped_departments, str):
                mapped_departments = [d.strip() for d in mapped_departments.split(",")]

            # Ensure departments exist and assign them
            valid_departments = []
            for dept_name in mapped_departments:
                dept_obj, _ = Department.objects.get_or_create(name=dept_name)
                valid_departments.append(dept_obj)

            profile.departments.set(valid_departments)

