from django.urls import path
from . import views
app_name = 'finance'  # ✅ Enables reverse('finance:finance_ac_list') style resolution
urlpatterns = [
    path('account-detailed/', views.finance_ac_list, name='finance_ac_list'),  # ✅ Maps to account list view
    path('transaction-detailed/', views.finance_tn_list, name='finance_tn_list'),  # ✅ Maps to transaction list view
]


