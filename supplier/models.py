from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Supplier(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name = models.TextField(max_length=150)
    cnpj = models.CharField(max_length=18)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "cnpj"], 
                name="unique_supplier_per_user"
            ),
            models.UniqueConstraint(
                fields=["user", "email"], 
                name="unique_email_supplier_per_user"
            )
        ]