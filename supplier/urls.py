from django.urls import path
from .views import get_page_suppliers,delete_supplier

urlpatterns = [
    path('',view=get_page_suppliers,name='suppliers'),
    path('delete/<int:id>',view=delete_supplier,name="delete_supplier")
]