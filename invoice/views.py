from pathlib import Path

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .invoice import (PDFCompany, PDFInvoice, PDFInvoiceCreator,
                      PDFInvoiceCustomer, PDFItem, PDFWork)
from .models import Customer, Invoice
from .serializers import CustomerSerializer, InvoiceSerializer


# Customer views
@api_view(["GET"])
def get_customers(request):
    """
    Get all customers from the database
    """
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_customer(request, pk):
    """
    Get a customer from the database
    """
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)


@api_view(["POST"])
def create_customer(request):
    """
    Create a new customer in the database
    """
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["PUT"])
def update_customer(request, pk):
    """
    Update a customer in the database
    """
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(instance=customer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["DELETE"])
def delete_customer(request, pk):
    """
    Delete a customer from the database
    """
    customer = Customer.objects.get(id=pk)
    customer.delete()
    return Response("Customer successfully deleted")


# End of Customer views

# Invoice views


@api_view(["GET"])
def get_invoices(request):
    """
    Get all invoices from the database
    """
    invoices = Invoice.objects.all()
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_invoice(request, pk):
    """
    Get a invoice from the database
    """
    invoice = Invoice.objects.get(id=pk)
    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data)


@api_view(["POST"])
def create_invoice(request):
    """
    Create a new invoice in the database
    """
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["DELETE"])
def delete_invoice(request, pk):
    """
    Delete a invoice from the database
    """
    invoice = Invoice.objects.get(id=pk)
    invoice.delete()
    return Response("Invoice successfully deleted")


@api_view(["PUT"])
def update_invoice(request, pk):
    """
    Update a invoice in the database
    """
    invoice = Invoice.objects.get(id=pk)
    data = request.data
    item_list = []

    for item in data["items"]:
        if item["price"] and item["name"]:
            item_list.append(
            PDFItem(
                item["name"],
                float(item["price"]),
                int(item["quantity"]),
                item["unit"],
            )
        )
    my_company = PDFCompany(
        "F:A Thomsson",
        "Tallundsgatan 8",
        "Visby",
        "Company state",
        "621 58",
        "0739736124",
        "Magnus Thomsson",
    )
    my_work = PDFWork("Arbetstid", float(data["work_hour"]), float(data["work_price"]))
    customer = Customer.objects.get(id=data["customer"])
    pdf_customer = PDFInvoiceCustomer(
        name=customer.name,
        address=customer.address,
        phone=customer.phone,
        email=customer.email,
        city=customer.city,
        zip_code=customer.zip_code,
        social_security=customer.social_security,
        house=customer.house,
    )

    my_invoice = PDFInvoice(
        customer=pdf_customer,
        items=item_list,
        company=my_company,
        work=my_work,
        number=data["id"],
        my_date=data["date"],
        due_days=int(data["due_days"]),
        start_date=data["start_date"],
        end_date=data["end_date"],
        rot=data["rot"],
        description=data["description"]
    )

    pdf_invoice = PDFInvoiceCreator(my_invoice, Path("C:/Invoice_Program/latex"))

    if my_invoice.rot:
        pdf_invoice.create_tex_rot()
    else:
        pdf_invoice.create_tex()

    pdf_invoice.run_latexmk(invoice.name)
    serializer = InvoiceSerializer(instance=invoice, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


# End of Invoice views


@api_view(["GET"])
def get_invoice_pdf(request, pk):
    """
    Get a invoice from the database
    """
    file_path = Path("D:/Projects/InvoiceV2/invoice.pdf")
    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/pdf")
        response["Content-Disposition"] = "inline; filename=invoice.pdf"
        return response
