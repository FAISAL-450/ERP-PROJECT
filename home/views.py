from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project.models import Project
from contractor.models import Contractor
from customer.models import Customer

@login_required
def home_view(request):
    user_email = (getattr(request.user, "email", "") or request.user.username or "").lower()

    # 📦 Project Summary
    project_names = list(Project.objects.values_list("name_of_project", flat=True))
    project_summary = {
        "count": len(project_names),
        "names": project_names,
    }

    # 👷 Contractor Summary
    contractor_names = list(Contractor.objects.values_list("contractor_name", flat=True))
    contractor_summary = {
        "count": len(contractor_names),
        "names": contractor_names,
    }

    # 🧑‍💼 Customer Summary
    customer_names = list(Customer.objects.values_list("customer_name", flat=True))
    customer_summary = {
        "count": len(customer_names),
        "names": customer_names,
    }

    context = {
        "user_email": user_email,
        "project_summary": project_summary,
        "contractor_summary": contractor_summary,
        "customer_summary": customer_summary,
    }

    return render(request, "home/home.html", context)



































