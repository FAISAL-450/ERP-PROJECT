from django.shortcuts import render
from customer.models import Customer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# 🔁 Reusable Pagination Function
def get_paginated_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# 💼 Sales Customer Detailed View
def sales_cd_list(request):
    query = request.GET.get('q', '').strip()
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(customer_name__icontains=query)

    customers_page = get_paginated_queryset(request, customers, per_page=10)

    return render(request, 'sales/sales_cd_list.html', {
        'customers': customers_page,
        'query': query
    })


