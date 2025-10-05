import logging
import json
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Profile

logger = logging.getLogger(__name__)

def azure_login_callback(request):
    logger.info("🚦 azure_login_callback triggered")

    # 🧾 Extract claims from session
    claims = request.session.get("claims")
    if not claims:
        logger.error("❌ No claims found in session — cannot proceed")
        return redirect("login_error")

    # 🧠 Parse claims safely
    try:
        email = next((c["userId"] for c in claims if c.get("typ") == "email"), None)
        name = next((c["userId"] for c in claims if c.get("typ") == "name"), None)
    except Exception as e:
        logger.error(f"❌ Error parsing claims: {e}")
        return redirect("login_error")

    if not email:
        logger.error("❌ Email claim missing — cannot authenticate user")
        return redirect("login_error")

    username = email.split("@")[0]
    try:
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": username, "first_name": name or username}
        )
    except Exception as e:
        logger.error(f"❌ User creation failed: {e}")
        return redirect("login_error")

    logger.info(f"{'🆕 User created' if created else '🔄 Existing user logged in'}: {email}")

    # 👤 Ensure Profile exists
    profile, _ = Profile.objects.get_or_create(user=user)

    # 🧭 Assign department from settings
    department_map = getattr(settings, 'DEPARTMENT_EMAIL_MAP', {})
    mapped_department = department_map.get(email.lower().strip())

    if mapped_department:
        if profile.department != mapped_department:
            profile.department = mapped_department
            profile.save(update_fields=['department'])
            logger.info(f"✅ Profile updated → {email} assigned to '{mapped_department}'")
        else:
            logger.info(f"✅ Profile already correct → {email} is '{mapped_department}'")
    else:
        logger.warning(f"⚠️ Unmapped email: {email} — no department assigned")

    # 🔐 Log in and redirect
    login(request, user)
    logger.info(f"🚀 User logged in and redirected: {email}")
    return redirect("dashboard")



