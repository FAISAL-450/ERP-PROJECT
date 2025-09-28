from django.conf import settings
from accounts.models import Profile

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
            email = request.META.get('X-MS-CLIENT-PRINCIPAL-NAME', '').lower()
            department_map = getattr(settings, 'AZURE_AD_EMAIL_TO_DEPARTMENT', {})
            mapped_department = department_map.get(email)

            if mapped_department:
                profile, _ = Profile.objects.get_or_create(user=request.user)
                if profile.department != mapped_department:
                    profile.department = mapped_department
                    profile.save()

        return self.get_response(request)





