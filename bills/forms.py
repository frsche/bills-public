from django import forms
from .models import Bill, Order, Ordertypes

class BillForm(forms.ModelForm):
    """Form to set general information for a bill."""

    class Meta:
        model = Bill
        fields = ["patient", "from_date", "to_date", "current_date"]
        labels = {
            "patient": "Patient",
            "from_date": "von",
            "to_date": "bis",
            "current_date": "Ausstellungsdatum"
        }

class OrderForm(forms.Form):
    """Form to add orders to a bill."""

    amount = forms.IntegerField(initial=10, label="Anzahl")
    order = forms.ModelChoiceField(queryset=Ordertypes.objects.all(), label="Behandlungsart")