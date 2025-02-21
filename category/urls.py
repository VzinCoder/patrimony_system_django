from django.urls import path
from .views import get_page_categories,delete_category

urlpatterns = [
    path('',view=get_page_categories,name='categories'),
    path('delete/<int:id>',view=delete_category,name="delete_category")
]