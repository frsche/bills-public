from django.urls import path
from . import views

urlpatterns = [
    path('', views.bills_list, name="bills_list"),
    path('form/', views.bills_form, name="bills_new"),
    path('form/<int:id>', views.bills_form, name="bills_update"),
    path('delete/<int:id>', views.bills_delete, name="bills_delete"),
    path('delete/<int:id>/yes', views.bills_delete_yes, name="bills_delete_yes"),
    path('bill/<int:id>', views.bills_bill, name="bills_bill"),
    path('bill/delete_order/<int:id>', views.bills_order_delete, name="bills_order_delete")
]