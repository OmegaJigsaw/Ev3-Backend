# Generated by Django 3.2.25 on 2024-11-15 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_venta_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]
