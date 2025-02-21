from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.fields.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False
    )

    description = models.TextField(
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.name