from django.shortcuts import render, redirect
from .forms import BillForm, OrderForm
from .models import Bill, Order
from django.contrib import messages
from django.utils import timezone
from printer.models import PrintQueue
from django.db import IntegrityError

def check_bill_printed(request, bill):
    """Show warning if the user is editing a bill that was already printed to PDF."""
    if bill.last_printed:
        messages.info(request, "Es wurde bereits eine PDF dieser Rechnung erstellt. Vorsicht beim Ändern!")


def bills_form(request, id=None):
    """Show form to supply general information of a bill. Either create a new one, or edit an existing one."""
    bill_id = None
    if request.method == "GET":
        if id == None: # load form for new bill
            if "patient" in request.GET:
                form = BillForm({
                    'patient': request.GET["patient"],
                    'current_date': timezone.now()
                    }
                )
            else:
                form = BillForm()
        else: # load a bill to edit
            bill = Bill.objects.get(pk=id)
            check_bill_printed(request, bill)
            form = BillForm(instance=bill)
            bill_id = bill.bill_id
    else:
        if id == None: # save new bill
            form = BillForm(request.POST)
        else: # save edited bill
            bill = Bill.objects.get(pk=id)
            form = BillForm(request.POST, instance=bill)
            bill_id = bill.bill_id

        if form.is_valid():
            try:
                bill = form.save()
            except IntegrityError as e:
                messages.error(request, e) # and render the form again
            else:
                # calculate bill id, if bill is new
                if id == None: 
                    bill.bill_id = bill.calculate_id()

                bill.last_updated = timezone.now()
                bill.save()
                return redirect("bills_bill", bill.id)

        else: # if form is not valid
            messages.error(request, "Fehlerhafte Eingabe!")

    return render(request, "bills/form.html", {"form": form, "bill_id": bill_id})

def bills_list(request):
    """Show an overview of all bills in the database."""

    bills = Bill.objects.all().order_by("bill_id")
    total = sum(bill.total for bill in bills)
    hasqueue = PrintQueue.objects.all().exists()
    return render(request, "bills/list.html", {
        'bill_list': bills,
        'total': total,
        'hasQueue': hasqueue
        }
    )

def bills_bill(request, id):
    """Show form to add orders to an existing (initially empty) bill."""

    bill = Bill.objects.get(pk=id)
    orders = Order.objects.filter(bill=bill.id)
    check_bill_printed(request, bill)

    if request.method == "GET":
        form = OrderForm()
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            bill.last_updated = timezone.now()
            bill.save()
            Order.objects.create(bill=bill, name=form.cleaned_data["order"].name,
                amount=form.cleaned_data["amount"], price=form.cleaned_data["order"].price)

    return render(request, "bills/bill.html", {
        "bill": bill,
        'orders': orders,
        "order_form": form
        }
    )

def bills_delete(request, id):
    """Query to delete a bill from the database.
    Will ask the user to confirm, and then redirect to `bills_delete_yes`.
    """

    bill = Bill.objects.get(pk=id)
    return render(request, "bills/delete.html", {"bill": bill})

def bills_delete_yes(request, id):
    """Delete a bill from the database"""

    bill = Bill.objects.get(pk=id)
    bill.delete()
    return redirect("bills_list")

def bills_order_delete(request, id):
    """Delete a single order from a bill."""

    order = Order.objects.get(pk=id)
    bill = order.bill
    bill.last_updated = timezone.now()
    bill.save()
    order.delete()
    return redirect("bills_bill", bill.id)

def bills_update(request):
    pass
