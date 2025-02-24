# Generated by Django 5.1.6 on 2025-02-24 20:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='supplier',
            constraint=models.UniqueConstraint(fields=('user', 'email'), name='unique_email_supplier_per_user'),
        ),
    ]
