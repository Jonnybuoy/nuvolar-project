# Generated by Django 4.2 on 2023-04-10 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='arrival_time',
            new_name='arrival_datetime',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='departure_time',
            new_name='departure_datetime',
        ),
    ]