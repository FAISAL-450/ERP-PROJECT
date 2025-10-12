from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from project.models import Project  # ✅ Explicit import if Project is in another app

def home_view(request):
    # 🧮 Total number of projects
    total_projects = Project.objects.count()

    # 📍 Projects grouped by address (region summary)
    region_summary = (
        Project.objects
        .values('project_address')
        .annotate(project_count=Count('id'))
        .order_by('-project_count')
    )

    # 👤 Top 5 contact persons by project count
    top_contacts = (
        Project.objects
        .values('contact_person_name')
        .annotate(project_count=Count('id'))
        .order_by('-project_count')[:5]
    )

    # 📅 Monthly trend of project creation
    monthly_trend = (
        Project.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(project_count=Count('id'))
        .order_by('month')
    )

    # 📦 Context passed to the template
    context = {
        'total_projects': total_projects,
        'region_summary': region_summary,
        'top_contacts': top_contacts,
        'monthly_trend': monthly_trend,
    }

    return render(request, 'home/home.html', context)


















