# Generated by Django 4.2.2 on 2023-06-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0009_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='lot',
            name='image',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]