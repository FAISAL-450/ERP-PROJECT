# A - Import Required Modules #
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm

# B - Filtering Function-(customer_name and project-name-Based) #
def filter_customers(query=None):
    queryset = Customer.objects.select_related('project_name').all()
    if query:
        queryset = queryset.filter(
            Q(customer_name__icontains=query) |
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
def customer_dashboard(request):
    query = request.GET.get("q", "").strip()
    customers = filter_customers(query)
    customers_page = get_paginated_queryset(request, customers, per_page=10)

    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        customer = form.save(commit=False)
        customer.save()
        messages.success(request, "✅ Customer created successfully.")
        return redirect(f"{reverse('customer_dashboard')}?q={query}")

    return render(request, "customer/customer_dashboard.html", {
        "customers": customers_page,
        "query": query,
        "form": form,
        "mode": "list"
    })

# E - Edit View (Inline Form + List Table) #
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    query = request.GET.get("q", "").strip()

    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Customer updated successfully.")
        return redirect(f"{reverse('customer_dashboard')}?q={query}")

    customers = filter_customers(query)
    customers_page = get_paginated_queryset(request, customers, per_page=10)

    return render(request, "customer/customer_dashboard.html", {
        "form": form,
        "mode": "edit",
        "customer": customer,
        "query": query,
        "customers": customers_page
    })

# F - Delete View (Confirmation + Redirect) #
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    query = request.GET.get("q", "").strip()

    if request.method == 'POST':
        name = customer.customer_name
        customer.delete()
        messages.success(request, f"🗑️ Customer '{name}' deleted successfully.")
        return redirect(f"{reverse('customer_dashboard')}?q={query}")

