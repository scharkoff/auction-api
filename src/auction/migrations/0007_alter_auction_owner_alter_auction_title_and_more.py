# Generated by Django 4.2.2 on 2023-06-19 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction', '0006_rename_endtime_lot_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auction',
            name='title',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='lot',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
