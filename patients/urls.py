from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name="patients_list"),
    path('form/', views.patient_form, name="patients_insert"),
    path('form/<int:id>', views.patient_form, name="patients_update"),
    path('delete/<int:id>', views.patient_delete, name="patients_delete"),
    path('delete/yes/<int:id>', views.patient_delete_yes, name="patients_delete_yes")
]

