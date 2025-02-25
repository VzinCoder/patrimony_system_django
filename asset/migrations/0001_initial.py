# Generated by Django 5.1.6 on 2025-02-24 23:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0005_alter_category_name'),
        ('department', '0001_initial'),
        ('supplier', '0003_alter_supplier_cnpj'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('acquisition_date', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Ativo'), ('maintenance', 'Em Manutenção'), ('decommissioned', 'Desativado'), ('lost', 'Perdido')], default='active', max_length=15)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.department')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supplier.supplier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('user', 'rfid'), name='unique_asset_per_user')],
            },
        ),
    ]
