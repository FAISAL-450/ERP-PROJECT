from django.urls import path
from . import views

urlpatterns = [
    # 📊 Unified Customer Dashboard (List + Create)
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # ✏️ Edit Customer Inline
    path('edit/<int:pk>/', views.edit_customer, name='edit_customer'),

    # 🗑️ Delete Customer
    path('delete/<int:pk>/', views.customer_delete, name='customer_delete'),
]

