import logging
import base64
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .models import Profile

logger = logging.getLogger(__name__)

class EnsureProfileAndDepartmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("✅ EnsureProfileAndDepartmentMiddleware initialized")

    def __call__(self, request):
        try:
            raw_principal = request.META.get("HTTP_X_MS_CLIENT_PRINCIPAL") or request.META.get("X-MS-CLIENT-PRINCIPAL")
            email = None

            if raw_principal:
                try:
                    decoded = base64.b64decode(raw_principal).decode("utf-8")
                    principal_data = json.loads(decoded)
                    logger.info(f"🔍 Azure AD claims:\n{json.dumps(principal_data, indent=2)}")

                    email_claim = next(
                        (claim.get("val") for claim in principal_data.get("claims", [])
                         if claim.get("typ") in ["email", "preferred_username"]),
                        None
                    )
                    if email_claim:
                        email = email_claim.lower().strip()
                        logger.info(f"✅ Azure AD email extracted: {email}")
                    else:
                        logger.warning("⚠️ Email claim not found in Azure AD principal")
                except Exception as e:
                    logger.error(f"❌ Error decoding Azure AD principal: {e}")

            if email:
                user, _ = User.objects.get_or_create(username=email, defaults={"email": email})
                if not request.user.is_authenticated:
                    request.user = user
                logger.info(f"✅ Django user mapped: {user.username}")

                profile, _ = Profile.objects.get_or_create(user=user)

                department_map = getattr(settings, "DEPARTMENT_EMAIL_MAP", {})
                mapped_department = department_map.get(email)

                valid_departments = dict(Profile._meta.get_field("department").choices).keys()
                if mapped_department:
                    if mapped_department in valid_departments:
                        if profile.department != mapped_department:
                            profile.department = mapped_department
                            profile.save(update_fields=["department"])
                            logger.info(f"✅ Profile updated → {email} assigned to '{mapped_department}'")
                        else:
                            logger.info(f"✅ Profile already correct → {email} is '{mapped_department}'")
                    else:
                        logger.warning(f"⚠️ Invalid department '{mapped_department}' for {email}")
                else:
                    logger.warning(f"⚠️ Unmapped email: {email} — no department assigned")
            else:
                logger.warning("⚠️ No Azure AD principal found — redirecting to login")
                return redirect(settings.LOGIN_URL)

        except Exception as e:
            logger.error(f"❌ Middleware crash: {e}")
            return HttpResponse("Internal Server Error", status=500)

        return self.get_response(request)














