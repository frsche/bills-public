from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.print_bill, name="printer_bill"),
    path('add_queue/<int:id>', views.add_queue, name="printer_add_queue"),
    path('remove_queue/<int:id>', views.remove_queue, name="printer_remove_queue"),
    path('print_queue', views.print_queue, name="printer_print_queue"),
    path('print', views.print_form, name="printer_print")
]

