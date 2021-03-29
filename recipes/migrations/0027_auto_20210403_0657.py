# Generated by Django 3.1.6 on 2021-04-03 06:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0026_auto_20210403_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.DecimalField(decimal_places=1, max_digits=6, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
