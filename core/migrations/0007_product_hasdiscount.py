# Generated by Django 4.0 on 2023-03-21 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_product_hasdiscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hasDiscount',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]