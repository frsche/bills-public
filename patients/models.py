from django.db import models
from django.forms.models import model_to_dict

class Greeting(models.Model):
    """Represents a greeting used in a bill."""

    greeting = models.CharField(max_length=20)
    opening_template = models.TextField()

    def __str__(self):
        return self.greeting

    def getOpening(self, patient):
        """For a given patient, returns the string that is used to greet that patient in the bill."""
        return self.opening_template.format(**model_to_dict(patient))


class Patient(models.Model):
    """Represents a patient (the receiver of a bill)."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    street_nr = models.CharField(max_length=5)
    plz = models.IntegerField()
    place = models.CharField(max_length=20)
    greeting = models.ForeignKey(Greeting, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def getOpening(self):
        """Returns the opening that is used to greet the patient in the bill."""
        return self.greeting.getOpening(self)