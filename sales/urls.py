from django.urls import path
from . import views
app_name = 'sales'
urlpatterns = [
    path('customer-details/', views.sales_cd_list, name='sales_cd_list'),
    
]
