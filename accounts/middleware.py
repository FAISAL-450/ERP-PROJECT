from django.conf import settings
from accounts.models import Profile
import logging

logger = logging.getLogger(__name__)

class EnsureProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            Profile.objects.get_or_create(user=request.user)
        return self.get_response(request)


class AzureEmailToDepartmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Extract Azure AD email from header
            email = request.META.get('X-MS-CLIENT-PRINCIPAL-NAME', '').lower()

            # Load mapping from settings
            department_map = getattr(settings, 'AZURE_AD_EMAIL_TO_DEPARTMENT', {})
            mapped_department = department_map.get(email)

            # Log and apply mapping
            if mapped_department:
                profile, _ = Profile.objects.get_or_create(user=request.user)
                if profile.department != mapped_department:
                    profile.department = mapped_department
                    profile.save()
                    logger.info(f"Updated department for {email} → {mapped_department}")
            else:
                logger.warning(f"Unmapped Azure AD email: {email}")

        return self.get_response(request)







