from django import forms
from .models import Supplier
from django.core.exceptions import ValidationError

class SupplierForm(forms.ModelForm):
    
    class Meta:
        model = Supplier
        fields = ['name','cnpj','phone','email','address']
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def clean_cnpj(self):
        """Garante que o cnpj seja único."""
        cnpj = self.cleaned_data.get("cnpj")
        user = self.user
        
        if Supplier.objects.filter(user=user, cnpj=cnpj).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Já existe um Fornecedor com este cpnj para sua conta. Escolha outro cnpj.")
        
        return cnpj
    
    def clean_email(self):
        """Garante que o cnpj seja único."""
        email = self.cleaned_data.get("email")
        user = self.user
        
        if Supplier.objects.filter(user=user, email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Já existe um Fornecedor com este email para sua conta. Escolha outro email.")
        
        return email
    
    def save(self,commit=True):
        supplier = super().save(commit=False)
        if self.user:
            supplier.user = self.user
        if commit:
            supplier.save()
        return supplier
