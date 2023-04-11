import pytest
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from fleet_api.models import Aircraft, Flight


@pytest.mark.django_db
class TestAircraftModel:
    def test_aircraft_model_str_representation(self):
        aircraft = Aircraft(serial_no='Boe4321', manufacturer='Boeing')
        assert str(aircraft) == 'Boe4321 - Boeing'

@pytest.mark.django_db
class TestFlightModel:
    def test_flight_model_departure_datetime_in_past(self):
        aircraft = Aircraft(serial_no='Boe001', manufacturer='Boeing')
        with pytest.raises(ValidationError) as excinfo:
            flight = Flight(
                departure_airport='HK',
                arrival_airport='LA',
                departure_datetime=timezone.now() - timezone.timedelta(days=1),
                arrival_datetime=timezone.now() + timezone.timedelta(hours=5),
                aircraft=aircraft
            )
            flight.full_clean()
        assert 'Depature datetime cannot be in the past.' in str(excinfo.value)

    def test_flight_model_unique_aircraft(self):
        aircraft1 = Aircraft(serial_no='Boe002', manufacturer='Boeing')
        aircraft1.save()
        flight1 = Flight(
            departure_airport='HK',
            arrival_airport='LA',
            departure_datetime=timezone.now(),
            arrival_datetime=timezone.now() + timezone.timedelta(hours=5),
            aircraft=aircraft1
        )
        flight1.save()
        aircraft2 = Aircraft(serial_no='Air001', manufacturer='Airbus')
        aircraft2.save()
        flight2 = Flight(
            departure_airport='SF',
            arrival_airport='OR',
            departure_datetime=timezone.now(),
            arrival_datetime=timezone.now() + timezone.timedelta(hours=3),
            aircraft=aircraft2
        )
        flight2.save()
        flight2.aircraft = aircraft1
        with pytest.raises(ValidationError):
            flight2.full_clean()
