import logging
from django.conf import settings
from .models import Profile

logger = logging.getLogger(__name__)

class EnsureProfileAndDepartmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("EnsureProfileAndDepartmentMiddleware initialized")

    def __call__(self, request):
        if request.user.is_authenticated:
            # Ensure Profile exists
            profile, _ = Profile.objects.get_or_create(user=request.user)

            # Extract email and normalize
            email = request.user.email.lower().strip()

            # Hardcoded mapping (can move to settings later)
            department_map = {
                'elias@DzignscapeProfessionals.onmicrosoft.com': 'construction',
                'jakir@DzignscapeProfessionals.onmicrosoft.com': 'sales',
                # Add more mappings here
            }

            # Map department if matched
            mapped_department = department_map.get(email)
            if mapped_department:
                if profile.department != mapped_department:
                    profile.department = mapped_department
                    profile.save()
                    logger.info(f"Profile updated → {email} assigned to '{mapped_department}'")
                else:
                    logger.info(f"Profile already correct → {email} is '{mapped_department}'")
            else:
                logger.warning(f"Unmapped email: {email} — no department assigned")

        return self.get_response(request)









