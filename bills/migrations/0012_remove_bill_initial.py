# Generated by Django 3.1.4 on 2020-12-27 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0011_auto_20201227_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='initial',
        ),
    ]
