# Generated by Django 3.2.25 on 2024-11-14 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
