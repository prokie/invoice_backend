from django.urls import path
from . import views

urlpatterns = [
    path("customers/", views.get_customers, name="get_customers"),
    path("customer/create/", views.create_customer, name="create_customer"),
    path("customer/<int:pk>/", views.get_customer, name="get_customer"),
    path("customer/<int:pk>/update/", views.update_customer, name="update_customer"),
    path("customer/<int:pk>/delete/", views.delete_customer, name="delete_customer"),
    path("invoices/", views.get_invoices, name="get_invoices"),
    path("invoice/create/", views.create_invoice, name="create_invoice"),
    path("invoice/<int:pk>/delete/", views.delete_invoice, name="delete_invoice"),
    path("invoice/<int:pk>/", views.get_invoice, name="get_invoice"),
    path("invoice/<int:pk>/update/", views.update_invoice, name="update_invoice"),
    path("invoice/<int:pk>/pdf/", views.get_invoice_pdf, name="get_invoice_pdf"),
]
