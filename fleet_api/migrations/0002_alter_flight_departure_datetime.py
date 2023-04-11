# Generated by Django 4.2 on 2023-04-11 13:39

import datetime

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='departure_datetime',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2023, 4, 11, 13, 39, 22, 934287, tzinfo=datetime.timezone.utc), message='Depature datetime cannot be in the past.')]),
        ),
    ]
