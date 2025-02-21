from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['id','name','description']
        error_messages = {
            'name': {
                'unique': "Já existe uma categoria com este nome. Escolha outro nome.",
            }
        }