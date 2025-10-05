import logging
import base64
import json
from django.conf import settings
from .models import Profile

# 🔧 Initialize logger
logger = logging.getLogger(__name__)

class EnsureProfileAndDepartmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("✅ EnsureProfileAndDepartmentMiddleware initialized")

    def __call__(self, request):
        if request.user.is_authenticated:
            logger.info("🔄 Middleware triggered for user: %s", request.user.username)

            # ✅ Ensure Profile exists for every authenticated user
            profile, _ = Profile.objects.get_or_create(user=request.user)

            # 🔍 Extract email from Azure AD claims
            raw_principal = request.META.get('X-MS-CLIENT-PRINCIPAL', None)
            email = None

            if raw_principal:
                try:
                    decoded = base64.b64decode(raw_principal).decode('utf-8')
                    principal_data = json.loads(decoded)
                    logger.info(f"🔍 Azure AD claims:\n{json.dumps(principal_data, indent=2)}")

                    email_claim = next(
                        (claim.get('userId') for claim in principal_data.get('claims', []) if claim.get('typ') == 'email'),
                        None
                    )
                    if email_claim:
                        email = email_claim.lower().strip()
                        logger.info(f"✅ Azure AD email extracted: {email}")
                    else:
                        logger.warning("⚠️ Email claim not found in Azure AD principal")
                except Exception as e:
                    logger.error(f"❌ Error decoding Azure AD principal: {e}")

            # 🔁 Fallback to Django user email if Azure AD email not found
            if not email:
                email = request.user.email.lower().strip()
                logger.info(f"🔁 Fallback to Django user email: {email}")

            # 🧭 Use centralized mapping from settings.py
            department_map = getattr(settings, 'DEPARTMENT_EMAIL_MAP', {})
            mapped_department = department_map.get(email)

            if mapped_department:
                if profile.department != mapped_department:
                    profile.department = mapped_department
                    profile.save(update_fields=['department'])
                    logger.info(f"✅ Profile updated → {email} assigned to '{mapped_department}'")
                else:
                    logger.info(f"✅ Profile already correct → {email} is '{mapped_department}'")
            else:
                logger.warning(f"⚠️ Unmapped email: {email} — no department assigned")

        return self.get_response(request)















