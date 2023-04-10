from django.db import models

# Create your models here.


class Aircraft(models.Model):
    serial_no = models.CharField(max_length=100, unique=True)
    manufacturer = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.serial_no} - {self.manufacturer}'


class Flight(models.Model):
    departure_airport = models.CharField(max_length=4)
    arrival_airport = models.CharField(max_length=4)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, unique=True)
    
    def __str__(self):
        return f'{self.departure_airport} - {self.arrival_airport}'
