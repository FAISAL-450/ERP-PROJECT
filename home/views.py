from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        email = request.user.email
        if email == 'elias@dzignscapeprofessionals.onmicrosoft.com':
            return render(request, 'construction_cd_list.html')
        elif email == 'jakir@dzignscapeprofessionals.onmicrosoft.com':
            return render(request, 'sales_cd_list.html')
    return render(request, 'home.html')  # default for others



