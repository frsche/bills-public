from django import template
from printer.models import PrintQueue
from bills.models import Order

register = template.Library()

@register.filter
def isInQueue(value):
    return PrintQueue.objects.filter(bill=value).exists()

@register.filter
def getOrders(value):
    return Order.objects.filter(bill=value)