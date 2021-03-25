# Generated by Django 3.1 on 2020-09-09 13:57
import csv
import os

from django.conf import settings
from django.db import migrations


def write_ingredients(apps, schema_editor):
    ingredients = os.path.join(settings.BASE_DIR, 'ingredients.csv')
    with open(ingredients, 'r') as ing:
        f = csv.reader(ing, delimiter=',')
        Product = apps.get_model('recipes.Product')
        products = []
        for row in f:
            products.append(Product(title=row[0], unit=row[1]))
        Product.objects.bulk_create(products)


def write_tags(apps, schema_editor):
    Tag = apps.get_model('recipes.Tag')
    tag_names = {
        'breakfast': 'завтрак',
        'lunch': 'обед',
        'dinner': 'ужин'
    }
    tags = []
    for key in tag_names:
        tags.append(Tag(slug=key, name=tag_names[key]))
    Tag.objects.bulk_create(tags)


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(write_ingredients),
        migrations.RunPython(write_tags),
    ]
