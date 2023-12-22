from django import forms
from bills.models import Bill
from patients.models import Patient
from django.db.models import Count
from django.db import connection
import re

'''
Form to select which bills to print to PDF.
'''
class PrintForm(forms.Form):
    '''
    Returns all years for which at least one bill exists.
    '''
    def get_year_choices():
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT strftime('%Y', bills_bill.current_date) AS year, COUNT(*)
                FROM bills_bill
                GROUP BY year
            ''')
            return [(year, f"{year} ({count})") for year, count in cursor.fetchall()]

    '''
    Returns the list of patients for which at least one bill exists.
    '''
    def get_patient_choices():
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT patient.id, patient.first_name, patient.last_name, COUNT(*)
                FROM bills_bill as bill, patients_patient AS patient
                WHERE bill.patient_id == patient.id
                GROUP BY patient.id
            ''')
            return [(id, f"{first_name} {last_name} ({count})") for id, first_name, last_name, count in cursor.fetchall()]

    '''
    Returns the possible modes to print a batch of bills at once.
    '''
    def get_print_mode_choices():
        unprinted_count = len(Bill.objects.filter(last_printed__isnull=True))
        return [
            (0, "ganzes Jahr"),
            (1, "Zeitraum"),
            (2, "Rechnungsnr."),
            (3, "Patient"),
            (4, f"noch nicht gedruckt ({unprinted_count})")
        ]


    year_select = forms.ChoiceField(choices=get_year_choices, required=False, label="")
    year_select.widget.attrs = {'class': 'year-control'}

    patient_select = forms.ChoiceField(choices=get_patient_choices, label="", required=False)
    patient_select.widget.attrs = {'class': 'patient-control'}

    time_from = forms.DateField(label="", required=False)
    time_from.widget.attrs = {'class': 'time-control'}
    time_to = forms.DateField(label="", required=False)
    time_to.widget.attrs = {'class': 'time-control'}

    bill_id_from = forms.CharField(max_length=10, label="", required=False)
    bill_id_from.widget.attrs = {'class': 'bill-control'}
    bill_id_to = forms.CharField(max_length=10, label="", required=False)
    bill_id_to.widget.attrs = {'class': 'bill-control'}

    sql_statement = forms.CharField(max_length=200, label="", required=False)
    sql_statement.widget.attrs = {'class': 'sql-control'}

    print_mode = forms.ChoiceField(widget=forms.RadioSelect, choices=get_print_mode_choices)

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        
        mode = int(self.cleaned_data["print_mode"])
        
        if not ((mode == 0 and self.cleaned_data["year_select"]) or \
        (mode == 1 and self.cleaned_data["time_from"] and self.cleaned_data["time_to"]) or \
        (mode == 2 and self.cleaned_data["bill_id_from"] and self.cleaned_data["bill_id_to"]) or \
        (mode == 3 and self.cleaned_data["patient_select"]) or \
         mode == 4):
            return False
        
        if not re.fullmatch(r"\d{4}/\d{3}", self.cleaned_data["bill_id_from"]) and \
            re.fullmatch(r"\d{4}/\d{3}", self.cleaned_data["bill_id_to"]):
            return False

        return True



