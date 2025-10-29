from accounts.models import Profile
from django.conf import settings

def user_profile(request):
    if request.user.is_authenticated:
        email = request.user.email.lower().strip()

        # Define department access per Azure AD email
        department_access = {
            'elias@dzignscapeprofessionals.onmicrosoft.com': ['construction'],
            'jakir@dzignscapeprofessionals.onmicrosoft.com': ['sales'],
            'admin@dzignscapeprofessionals.onmicrosoft.com': ['construction', 'sales', 'finance'],
            'salim@dzignscapeprofessionals.onmicrosoft.com': ['construction'],
            'belal@dzignscapeprofessionals.onmicrosoft.com': ['salesmarketing'],
            'emon@dzignscapeprofessionals.onmicrosoft.com': ['salesmarketing'],
        }

        try:
            profile = Profile.objects.get(user=request.user)
            # Get departments from model
            model_departments = list(profile.departments.values_list('name', flat=True))
            # Override with hardcoded access if defined
            mapped_departments = department_access.get(email, model_departments)
            return {
                'user_profile': profile,
                'user_departments': mapped_departments,
            }
        except Profile.DoesNotExist:
            return {
                'user_departments': department_access.get(email, []),
            }

    return {}

