# Generated by Django 3.1.4 on 2020-12-27 16:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0010_bill_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
