from django.db import models
from django.contrib.auth import get_user_model
from department.models import Department
from asset.models import Asset
# Create your models here.

class Movement(models.Model):
    TYPE_CHOICES = [
        ('entry', 'Entry'),
        ('exit', 'Exit'),
        ('transfer', 'Transfer')
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    origin = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements_origin')
    destination = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='movements_destination')
    movement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)