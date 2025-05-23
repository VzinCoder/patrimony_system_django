from django.db import models
from django.contrib.auth import get_user_model


class Department(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], 
                name="unique_department_per_user"
            )
        ]
        
    def __str__(self):
        return self.name