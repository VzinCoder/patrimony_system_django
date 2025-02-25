from django import forms
from .models import Asset
from django.core.exceptions import ValidationError
from movement.models import Movement

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['rfid','name','category','department','supplier','acquisition_date','status']
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_rfid(self):
        rfid = self.cleaned_data.get("rfid")
        user = self.user
        
        if Asset.objects.filter(user=user, rfid=rfid).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Já existe um patrimonio com este rfid para sua conta. Escolha outro rfid.")
        
        return rfid
    
    def save(self, commit=True):
        asset_instance = super().save(commit=False)

        if asset_instance.pk:
            old_asset = Asset.objects.get(pk=asset_instance.pk)
            old_department = old_asset.department
        else:
            old_department = None

        asset_instance.user = self.user  
        if commit:
            asset_instance.save()

            if not old_department:
                Movement.objects.create(
                    user=self.user,
                    type="entry",
                    asset=asset_instance,
                    destination=asset_instance.department,
                    notes="Movimentação inicial feita pelo sistema"
                )
            elif old_department != asset_instance.department:
                Movement.objects.create(
                    user=self.user,
                    type="transfer",
                    asset=asset_instance,
                    origin=old_department,
                    destination=asset_instance.department,
                    notes="Transferência de departamento feita pelo sistema"
                )

        return asset_instance