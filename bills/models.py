from django.db import models
from django.db.models import Sum,F
from django.db.models.functions import Cast
from patients.models import Patient
import datetime
from django.utils import timezone
from django import forms
from django.db import IntegrityError

class Bill(models.Model):
    """Represents a bill to a patient."""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    current_date = models.DateField(default=timezone.now)
    last_printed = models.DateTimeField(null=True, default=None)
    last_updated = models.DateTimeField(default=timezone.now)
    bill_id = models.CharField(max_length=10)

    @property
    def total(self):
        """The total price of the bill."""
    
        total = Order.objects.filter(bill=self).aggregate(total=Cast(Sum(F("amount") * F("price")),
            output_field=models.DecimalField()))["total"]
        return 0 if total == None else total

    def calculate_id(self):
        """Return the bill id based on current year and incrementing index"""

        year = self.current_date.year
        bill_id = Bill.objects.filter(current_date__year=year).count()
        return f"{year}/{bill_id:03}"

    def save(self, *args, **kwargs):
        if self.bill_id and not self.bill_id.startswith(str(self.current_date.year)):
            raise IntegrityError(f"Ausstellungsdatum muss mit Rechnungsnummer {self.bill_id} übereinstimmen!")
        if self.from_date > self.to_date:
            raise IntegrityError("from_date has to be less than to_date")
        super(Bill, self).save(*args, **kwargs)


class Order(models.Model):
    """Represents an individual order that is contained inside a bill. A bill consists of multiple Order's."""
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=5)

    @property
    def total(self):
        return self.amount * self.price

class Ordertypes(models.Model):
    """Represents the kind of the order."""

    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.name} ({self.price}€)"

