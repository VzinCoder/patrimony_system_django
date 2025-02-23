from django.urls import path
from .views import get_page_departments,delete_department

urlpatterns = [
    path('',view=get_page_departments,name='departments'),
    path('delete/<int:id>',view=delete_department,name="delete_department")
]