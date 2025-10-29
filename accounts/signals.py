from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import Profile, Department
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        profile = Profile.objects.create(user=instance)
        email = instance.email.lower().strip() if instance.email else None

        if not email:
            logger.warning(f"⚠️ User created without email: {instance.username}")
            return

        department_map = getattr(settings, "DEPARTMENT_EMAIL_MAP", {})
        mapped_departments = department_map.get(email)

        if mapped_departments:
            # Convert comma-separated string to list if needed
            if isinstance(mapped_departments, str):
                mapped_departments = [d.strip() for d in mapped_departments.split(",")]

            valid_departments = []
            for dept_name in mapped_departments:
                if dept_name:
                    dept_obj, _ = Department.objects.get_or_create(name=dept_name)
                    valid_departments.append(dept_obj)

            profile.departments.set(valid_departments)
            logger.info(f"✅ Profile created for {email} with departments: {', '.join([d.name for d in valid_departments])}")
        else:
            logger.warning(f"⚠️ No department mapping found for {email}")

    except Exception as e:
        logger.error(f"❌ Error creating profile for {instance.username}: {e}")




