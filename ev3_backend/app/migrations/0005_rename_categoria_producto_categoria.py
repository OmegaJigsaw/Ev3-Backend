# Generated by Django 3.2.25 on 2024-11-15 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_categoria_disponible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='Categoria',
            new_name='categoria',
        ),
    ]