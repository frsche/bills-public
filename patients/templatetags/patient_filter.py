from django import template
from bills.models import Bill

register = template.Library()

@register.filter
def hasBills(patient):
    return Bill.objects.filter(patient=patient).exists()

@register.filter
def getOpening(patient):
    return patient.getOpening()