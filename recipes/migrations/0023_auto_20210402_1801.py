# Generated by Django 3.1.6 on 2021-04-02 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0022_auto_20210402_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название продукта'),
        ),
    ]
