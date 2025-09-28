from django.urls import path
from . import views

app_name = 'contractor'

urlpatterns = [
    path('dashboard/', views.contractor_dashboard, name='contractor_dashboard'),
    path('edit/<int:pk>/', views.edit_contractor, name='edit_contractor'),
    path('delete/<int:pk>/', views.contractor_delete, name='contractor_delete'),
]





