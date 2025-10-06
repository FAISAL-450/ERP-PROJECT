from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    email = request.user.email

    # Elias: redirect to construction dashboard
    if email == 'elias@dzignscapeprofessionals.onmicrosoft.com':
        return render(request, 'construction_cd_list.html')

    # Jakir: redirect to sales dashboard
    elif email == 'jakir@dzignscapeprofessionals.onmicrosoft.com':
        return render(request, 'sales_cd_list.html')

    # Default: show home page
    return render(request, 'home.html')




