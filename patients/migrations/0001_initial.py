# Generated by Django 3.1.4 on 2020-12-24 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Greeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('greeting', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=100)),
                ('street_nr', models.IntegerField()),
                ('plz', models.IntegerField()),
                ('place', models.CharField(max_length=20)),
                ('greeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.greeting')),
            ],
        ),
    ]