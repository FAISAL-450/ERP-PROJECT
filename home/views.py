from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    email = request.user.email

    # Elias: show construction dashboard
    if email == 'elias@dzignscapeprofessionals.onmicrosoft.com':
        return render(request, 'construction/construction_pd_list.html')  # Adjusted path

    # Jakir: show sales dashboard
    elif email == 'jakir@dzignscapeprofessionals.onmicrosoft.com':
        return render(request, 'sales/sales_cd_list.html')  # Adjusted path

    # Default: show home page
    return render(request, 'home/home.html')  # Adjusted path






