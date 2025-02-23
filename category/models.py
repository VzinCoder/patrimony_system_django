from django.db import models
from django.contrib.auth import get_user_model 
# Create your models here.


class Category(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.fields.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    description = models.TextField(
        blank=True, 
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], 
                name="unique_category_per_user"
            )
        ]

    def __str__(self):
        return self.name