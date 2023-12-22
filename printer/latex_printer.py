from bills.models import Bill, Order
from patients.models import Patient
from django.template.loader import render_to_string
from django.utils import timezone

from pdflatex import PDFLaTeX

def bills_to_pdf(bills, _):
    """Prints a set of bills to PDF using a latex template"""

    assert(bills)
    for bill in bills:
        bill.last_printed = timezone.now()
        bill.save()
    latex_bill = render_to_string("printer/bill.tex", {"bills": bills})
    pdfl = PDFLaTeX.from_binarystring(latex_bill.encode("utf-8"), "bill")
    pdf, _, _ = pdfl.create_pdf()
    return pdf

def bills_list_to_pdf(bills, title):
    """Prints an overview of a set of bills to PDF.
    Not the individual bills, but a table showing an overview.
    """

    total = sum(bill.total for bill in bills)
    latex_list = render_to_string("printer/list.tex", {"bills": bills, "total": total, "title": title})
    pdfl = PDFLaTeX.from_binarystring(latex_list.encode("utf-8"), "list")
    pdf, _, _ = pdfl.create_pdf()
    return pdf

def print_year(handler, year):
    """Print all bills from a single year."""

    bills = Bill.objects.filter(current_date__year=year)
    return handler(bills, f"Jahr {year}")

def print_bill_range(handler, bill_id_from, bill_id_to):
    """Print all bills with a bill id in the given range."""

    bills = Bill.objects.filter(bill_id__gte=bill_id_from, bill_id__lte=bill_id_to)
    return handler(bills, f"Rechnungsnummer von {bill_id_from} bis {bill_id_to}")

def print_time_range(handler, time_from, time_to):
    """Print all bills with a bill date in the given range."""

    bills = Bill.objects.filter(current_date__gte=time_from, current_date__lte=time_to)
    return handler(bills, f"Ausstellungsdatum von {time_from} bis {time_to}")

def print_patient(handler, patient):
    """Print all bills going to an individual patient."""

    patient = Patient.objects.get(pk=patient)
    bills = Bill.objects.filter(patient=patient)
    return handler(bills, f"{patient.first_name} {patient.last_name}")

def print_unprinted(handler):
    """Print all bills that were not printed already."""

    bills = Bill.objects.filter(last_printed__isnull=True)
    return handler(bills, "Noch nicht gedruckt")