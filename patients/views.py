from django.shortcuts import render, redirect
from .forms import PatientForm, PatientSearchForm
from .models import Patient
from django.contrib import messages
from django.db.models.functions import Concat
from django.db.models import Value

def patient_form(request, id=None):
    """Displays the form to create a new patient or edit the information of an existing one."""

    if request.method == "GET":
        if id == None:
            form = PatientForm()
        else:
            patient = Patient.objects.get(pk=id)
            form = PatientForm(instance=patient)

    else:
        if id == None:
            form = PatientForm(request.POST)
        else:
            patient = Patient.objects.get(pk=id)
            form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patients_list")
        else:
            messages.error("Form not valid")

    return render(request, "patients/form.html", {'form': form, 'title': "Patienten"})

def patient_list(request):
    """Lists all patients currently in the database. (possibly filtered by the filter form)"""

    if request.method == "GET":
        patients = Patient.objects.all().order_by("last_name", "first_name")
        searchForm = PatientSearchForm()
        searchTerm = None
    else:
        searchForm = PatientSearchForm(request.POST)
        patients = Patient.objects.all().order_by("last_name", "first_name")
        if searchForm.is_valid():
            searchTerm = searchForm.cleaned_data["search"]
            patients = patients.annotate(s=Concat("first_name", Value(" "), "last_name"))\
                .filter(s__icontains=searchTerm)

    return render(request, "patients/list.html", {
        'patient_list': patients,
        "search_form": searchForm,
        "search_term": searchTerm,
        'title': "Patienten"
        }
    )

def patient_delete(request, id):
    """Query to delete a patient from the database.
    Will ask the user to confirm, and then redirect to `patient_delete_yes`.
    """

    patient = Patient.objects.get(pk=id)
    return render(request, "patients/delete.html", {
        'patient': patient,
        'title': "Patienten"
        }
    )

def patient_delete_yes(request, id):
    """Deletes a patient from the database"""

    patient = Patient.objects.get(pk=id)
    patient.delete()
    return redirect("patients_list")