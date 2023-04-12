from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Aircraft(models.Model):
    """Model to hold the aircraft details."""
    serial_no = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.serial_no} - {self.manufacturer}'


class Flight(models.Model):
    """Model to hold flight details."""
    created_at = models.DateTimeField(auto_now_add=True)
    departure_airport = models.CharField(max_length=4)
    arrival_airport = models.CharField(max_length=4)
    departure_datetime = models.DateTimeField(
        validators=[
            MinValueValidator(
                timezone.now(),
                message="Depature datetime cannot be in the past.")
        ]
    )
    arrival_datetime = models.DateTimeField()
    aircraft = models.OneToOneField(Aircraft, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.departure_airport} - {self.arrival_airport}'
