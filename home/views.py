from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project.models import Project
from contractor.models import Contractor
from customer.models import Customer  # ✅ Add this

@login_required
def home_view(request):
    # Safely get user email or fallback to username
    user_email = getattr(request.user, "email", request.user.username or "").lower()

    # 📦 Project Summary
    total_projects = Project.objects.count()
    project_names = Project.objects.values_list('name_of_project', flat=True)

    # 👷 Contractor Summary
    total_contractors = Contractor.objects.count()
    contractor_names = Contractor.objects.values_list('contractor_name', flat=True)

    # 🧑‍💼 Customer Summary — ✅ This was missing
    total_customers = Customer.objects.count()
    customer_names = Customer.objects.values_list('customer_name', flat=True)

    context = {
        "user_email": user_email,
        "total_projects": total_projects,
        "project_names": project_names,
        "total_contractors": total_contractors,
        "contractor_names": contractor_names,
        "total_customers": total_customers,       # ✅ Add to context
        "customer_names": customer_names,         # ✅ Add to context
    }

    return render(request, "home/home.html", context)






























