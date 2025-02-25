from django.db import models
from django.contrib.auth import get_user_model
from category.models import Category
from department.models import Department
from supplier.models import Supplier
# Create your models here.
class Asset(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Ativo"
        MAINTENANCE = "maintenance", "Em Manutenção"
        DECOMMISSIONED = "decommissioned", "Desativado"
        LOST = "lost", "Perdido"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rfid = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    acquisition_date = models.DateField()
    is_deleted = models.BooleanField(default=False)
    
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "rfid"], 
                name="unique_asset_per_user"
            )
        ]