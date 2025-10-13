from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project.models import Project
from contractor.models import Contractor
from customer.models import Customer

@login_required
def home_view(request):
    # Safely get user email or fallback to username
    user_email = getattr(request.user, "email", request.user.username).lower()

    # 📦 Project Summary
    total_projects = Project.objects.count()
    project_names = list(Project.objects.order_by("name_of_project").values_list("name_of_project", flat=True))

    # 👷 Contractor Summary
    total_contractors = Contractor.objects.count()
    contractor_names = list(Contractor.objects.order_by("contractor_name").values_list("contractor_name", flat=True))

    # 🧑‍💼 Customer Summary
    total_customers = Customer.objects.count()
    customer_names = list(Customer.objects.order_by("customer_name").values_list("customer_name", flat=True))

    context = {
        "user_email": user_email,
        "total_projects": total_projects,
        "project_names": project_names,
        "total_contractors": total_contractors,
        "contractor_names": contractor_names,
        "total_customers": total_customers,
        "customer_names": customer_names,
    }

    return render(request, "home/home.html", context)






































