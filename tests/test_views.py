import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from .utils.conftest import api_client
from fleet_api.models import Aircraft, Flight
from fleet_api.serializers import FlightSerializer
from fleet_api.filters import FlightFilter

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_aircraft():
    aircraft = Aircraft.objects.create(serial_no='ABC123', manufacturer='Boeing')
    return aircraft

@pytest.fixture
def create_flight(create_aircraft):
    aircraft = create_aircraft
    flight = Flight.objects.create(
        aircraft=aircraft,
        departure_airport='LEBL',
        arrival_airport='HK',
        departure_datetime=timezone.now(),
        arrival_datetime=timezone.now() + timezone.timedelta(hours=5)
    )
    return flight

def test_search_flights(api_client, create_flight):
    flight = create_flight
    url = reverse('flight-search-flights')
    
    response = api_client.get(url, data={'departure_airport': flight.departure_airport})
    assert response.status_code == status.HTTP_200_OK
    
    serialized_flight = FlightSerializer([flight], many=True).data
    assert response.json() == serialized_flight


def test_departure_airports_report(api_client, create_flight):
    flight = create_flight
    url = reverse('flight-departure-airports-report')
    
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    
    flight_filter = FlightFilter(data={}, queryset=Flight.objects.all())
    filtered_queryset = flight_filter.qs
    departure_airports = filtered_queryset.values_list('departure_airport', flat=True).distinct()
    in_flight_aircraft_count = filtered_queryset.values('aircraft').distinct().count()
    aircraft_in_flight = []
    now = timezone.now()
    for flight in filtered_queryset:
        aircraft_in_flight.append({
            'aircraft': flight.aircraft.serial_no,
            'in_flight_time_minutes': int(((now - flight.departure_datetime).total_seconds()) / 60)
        })

    response_data = {
        'departure_airports': list(departure_airports),
        'in_flight_aircraft_count': in_flight_aircraft_count,
        'aircraft_in_flight': aircraft_in_flight
    }

    assert response.json() == response_data
    