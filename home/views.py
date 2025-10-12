from django.shortcuts import render
from project.models import Project
from contractor.models import Contractor

def home_view(request):
    # 📦 Project Summary
    total_projects = Project.objects.count()
    project_names = Project.objects.values_list('name_of_project', flat=True)

    # 👷 Contractor Summary
    total_contractors = Contractor.objects.count()
    contractor_names = Contractor.objects.values_list('contractor_name', flat=True)

    context = {
        "total_projects": total_projects,
        "project_names": project_names,
        "total_contractors": total_contractors,
        "contractor_names": contractor_names,
    }

    return render(request, "home/home.html", context)




















