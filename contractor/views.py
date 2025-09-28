# A - Import Required Modules #
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from .models import Contractor
from .forms import ContractorForm

# B - Filtering Function (contractor_name and project_name-Based) #
def filter_contractors(query=None):
    queryset = Contractor.objects.select_related('project_name').all()
    if query:
        queryset = queryset.filter(
            Q(contractor_name__icontains=query) |
            Q(project_name__name_of_project__icontains=query)
        )
    return queryset

# C - Reusable Pagination Function #
def get_paginated_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# D - Unified View (List View + Form Submission) #
def contractor_dashboard(request):
    query = request.GET.get("q", "").strip()
    contractors = filter_contractors(query)
    contractors_page = get_paginated_queryset(request, contractors, per_page=10)

    form = ContractorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contractor = form.save(commit=False)
        contractor.save()
        messages.success(request, "✅ Contractor created successfully.")
        return redirect(f"{reverse('contractor:contractor_dashboard')}?q={query}")

    return render(request, "contractor/contractor_dashboard.html", {
        "contractors": contractors_page,
        "query": query,
        "form": form,
        "mode": "list"
    })

# E - Edit View (Inline Form + List Table) #
def edit_contractor(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    query = request.GET.get("q", "").strip()

    form = ContractorForm(request.POST or None, instance=contractor)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Contractor updated successfully.")
        return redirect(f"{reverse('contractor:contractor_dashboard')}?q={query}")

    contractors = filter_contractors(query)
    contractors_page = get_paginated_queryset(request, contractors, per_page=10)

    return render(request, "contractor/contractor_dashboard.html", {
        "form": form,
        "mode": "edit",
        "contractor": contractor,
        "query": query,
        "contractors": contractors_page
    })

# F - Delete View (Confirmation + Redirect) #
def contractor_delete(request, pk):
    contractor = get_object_or_404(Contractor, pk=pk)
    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = contractor.contractor_name
        contractor.delete()
        messages.success(request, f"🗑️ Contractor '{name}' deleted successfully.")
        return redirect(f"{reverse('contractor:contractor_dashboard')}?q={query}")

