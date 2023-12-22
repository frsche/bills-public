from django.shortcuts import render, redirect
from django.http import HttpResponse
from .latex_printer import bills_to_pdf
from bills.models import Bill
from .models import PrintQueue
from django import template
from .forms import PrintForm
from django.contrib import messages
from . import latex_printer
from django.utils import timezone

def print_bill(request, id):
    """Print an bill with the given id to PDF"""

    bill = Bill.objects.get(pk=id)
    pdf = bills_to_pdf([bill], None)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response

def add_queue(request, id):
    """Add a bill to the queue, to print later"""

    bill = Bill.objects.get(pk=id)
    queue_elem = PrintQueue(bill=bill)
    queue_elem.save()
    return redirect("bills_list")

def remove_queue(request, id):
    """Remove a bill from the print queue"""

    bill = Bill.objects.get(pk=id)
    queue_elem = PrintQueue.objects.get(bill=bill)
    queue_elem.delete()
    return redirect("bills_list")

def print_queue(request):
    """Print all bills in the queue to PDF, and empty the queue."""

    bills = [queueElem.bill for queueElem in PrintQueue.objects.all()]
    if not bills:
        return redirect("bills_list")
    for bill in bills:
        bill.last_printed = timezone.now()
        bill.save()
    PrintQueue.objects.all().delete()
    pdf = bills_to_pdf(bills, None)
    return HttpResponse(pdf, content_type='application/pdf')

def print_form(request):
    """Display the form to select which bills to print."""

    if request.method == "GET":
        form = PrintForm()
    else:
        form = PrintForm(request.POST)
        if form.is_valid():
            if "btn-print" in request.POST:
                print_handler = latex_printer.bills_to_pdf
            elif "btn-list" in request.POST:
                print_handler = latex_printer.bills_list_to_pdf
            else:
                raise RuntimeError("Invalid post request")

            mode = int(form.cleaned_data["print_mode"])
            if mode == 0:
                pdf = latex_printer.print_year(print_handler, form.cleaned_data["year_select"])
            elif mode == 1:
                pdf = latex_printer.print_time_range(print_handler, form.cleaned_data["time_from"], form.cleaned_data["time_to"])
            elif mode == 2:
                pdf = latex_printer.print_bill_range(print_handler, form.cleaned_data["bill_id_from"], form.cleaned_data["bill_id_to"])
            elif mode == 3:
                pdf = latex_printer.print_patient(print_handler, form.cleaned_data["patient_select"])
            elif mode == 4:
                pdf = latex_printer.print_unprinted(print_handler)
            return HttpResponse(pdf, content_type="application/pdf")
        else:
            messages.error(request, "Form error")
    
    return render(request, "printer/print.html", {'form': form})