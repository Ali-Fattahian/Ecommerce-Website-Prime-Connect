# Generated by Django 4.0 on 2023-03-22 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_product_hasdiscount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='numReviews',
        ),
    ]