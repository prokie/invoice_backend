import os
from pathlib import Path
from shutil import copyfile
from typing import ItemsView

from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200, unique=True)
    phone = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    house = models.CharField(max_length=200, unique=True, blank=True, null=True)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    social_security = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.name)


class Item(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=200, blank=True, null=True, default="st")

    def __str__(self) -> str:
        return f"{self.name} - {self.price} - {self.quantity} - {self.total}"


class Invoice(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, blank=True, null=True, on_delete=models.RESTRICT
    )
    invoice_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    due_days = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    items = models.JSONField(blank=True, null=True, default=list)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    work_hour = models.IntegerField(blank=True, null=True)
    work_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    rot = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
