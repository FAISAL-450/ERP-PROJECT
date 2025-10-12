from django.shortcuts import render
from project.models import Project  # Importing from the project app

def home_view(request):
    total_projects = Project.objects.count()
    project_names = Project.objects.values_list('name_of_project', flat=True)

    context = {
        "total_projects": total_projects,
        "project_names": project_names,
    }

    return render(request, "home/home.html", context)



















