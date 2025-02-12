from django.urls import path
from .views import get_categories

urlpatterns = [
    path('',view=get_categories,name='categories')
]