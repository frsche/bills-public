# Generated by Django 3.1.4 on 2020-12-26 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_bill_was_printed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='was_printed',
        ),
        migrations.AddField(
            model_name='bill',
            name='last_printed',
            field=models.DateTimeField(null=True),
        ),
    ]
