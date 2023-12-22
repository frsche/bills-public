from django.db import models
from bills.models import Bill

class PrintQueue(models.Model):
    """A list of bills that is added to a queue to print."""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
