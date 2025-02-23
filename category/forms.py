from django import forms
from .models import Category
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['id','name','description']
        error_messages = {
            'name': {
                'unique': "Já existe uma categoria com este nome. Escolha outro nome.",
            }
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        """Garante que a categoria do usuário tenha nome único."""
        name = self.cleaned_data.get("name")
        user = self.user
        
        if Category.objects.filter(user=user, name=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Já existe uma categoria com este nome para sua conta. Escolha outro nome.")
        
        return name
    
    def save(self, commit=True):
        category_instance = super().save(commit=False)
        if self.user:
            category_instance.user = self.user  
        if commit:
            category_instance.save()  
        return category_instance