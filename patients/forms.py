from django import forms
from .models import Patient
from django import forms

class PatientForm(forms.ModelForm):
    """Form to add or edit a patient in the list of patients"""

    class Meta:
        model = Patient
        fields = ["greeting", "first_name", "last_name", "street", "street_nr", "plz", "place"]
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'street': "Straße",
            'street_nr': "Nr.",
            'plz': "PLZ",
            'place': "Ort",
            'greeting': "Anrede"
        }
        widgets = {
            'street_nr': forms.TextInput(),
            'plz': forms.TextInput()
        }

class PatientSearchForm(forms.Form):
    """Form to search for a patient/filter the list of patients"""

    search = forms.CharField(label="")