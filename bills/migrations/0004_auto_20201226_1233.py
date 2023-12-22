# Generated by Django 3.1.4 on 2020-12-26 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0003_auto_20201225_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordertypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]