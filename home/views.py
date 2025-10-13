from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project.models import Project
from contractor.models import Contractor
from customer.models import Customer

@login_required
def home_view(request):
    # Safely get user email or fallback to username
    user_email = getattr(request.user, "email", "") or request.user.username or ""
    user_email = user_email.lower()

    # 📦 Project Summary
    project_qs = Project.objects.values_list('name_of_project', flat=True)
    project_names = list(project_qs) if project_qs.exists() else []
    total_projects = len(project_names)

    # 👷 Contractor Summary
    contractor_qs = Contractor.objects.values_list('contractor_name', flat=True)
    contractor_names = list(contractor_qs) if contractor_qs.exists() else []
    total_contractors = len(contractor_names)

    # 🧑‍💼 Customer Summary
    customer_qs = Customer.objects.values_list('customer_name', flat=True)
    customer_names = list(customer_qs) if customer_qs.exists() else []
    total_customers = len(customer_names)

    context = {
        "user_email": user_email,
        "project_summary": {
            "count": total_projects,
            "names": project_names,
        },
        "contractor_summary": {
            "count": total_contractors,
            "names": contractor_names,
        },
        "customer_summary": {
            "count": total_customers,
            "names": customer_names,
        },
    }

    return render(request, "home/home.html", context)
































