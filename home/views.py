from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Project

def home_view(request):
    total_projects = Project.objects.count()

    region_summary = (
        Project.objects
        .values('project_address')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    top_contacts = (
        Project.objects
        .values('contact_person_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    monthly_trend = (
        Project.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    context = {
        'total_projects': total_projects,
        'region_summary': region_summary,
        'top_contacts': top_contacts,
        'monthly_trend': monthly_trend,
    }

    return render(request, 'home/home.html', context)

















