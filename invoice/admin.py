from django.contrib import admin
from .models import Customer, Invoice, Item

# Register your models here.
admin.site.register(Customer)
admin.site.register(Invoice)
