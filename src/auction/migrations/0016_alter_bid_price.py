# Generated by Django 4.2.2 on 2023-06-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0015_lot_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
