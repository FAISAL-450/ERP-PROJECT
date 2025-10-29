# 📦 Core Imports
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# 🧮 Models
from account.models import Account  # Chart of Accounts for Finance

# 🔁 Pagination Utility
def get_paginated_queryset(request, queryset, per_page=10):
    """
    Paginate any queryset based on request 'page' parameter.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")

    try:
        return paginator.page(page_number)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# 💼 Finance Account List View
def finance_ac_list(request):
    """
    Renders a paginated list of finance accounts with optional search filtering.
    """
    query = request.GET.get('q', '').strip()
    accounts_qs = Account.objects.all()

    # 🔍 Apply search filter
    if query:
        accounts_qs = accounts_qs.filter(name__icontains=query)

    # 📄 Paginate results
    paginated_accounts = get_paginated_queryset(request, accounts_qs, per_page=10)

    # 📦 Context for template
    context = {
        'accounts': paginated_accounts,
        'query': query,
    }

    return render(request, 'finance/finance_ac_list.html', context)





