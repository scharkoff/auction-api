# Generated by Django 3.2.19 on 2023-08-23 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0018_alter_bid_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]