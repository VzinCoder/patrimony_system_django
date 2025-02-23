from django import forms
from .models import Department
from django.core.exceptions import ValidationError

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['id','name','description']
        error_messages = {
            'name': {
                'unique': "Já existe um departamento com este nome. Escolha outro nome.",
            }
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        """Garante que a categoria do usuário tenha nome único."""
        name = self.cleaned_data.get("name")
        user = self.user
        
        if Department.objects.filter(user=user, name=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Já existe um departamento com este nome para sua conta. Escolha outro nome.")
        
        return name
    
    def save(self, commit=True):
        department_instance = super().save(commit=False)
        if self.user:
            department_instance.user = self.user  
        if commit:
            department_instance.save()  
        return department_instance