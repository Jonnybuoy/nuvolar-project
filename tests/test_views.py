from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from fleet_api.filters import FlightFilter
from fleet_api.models import Aircraft, Flight
from fleet_api.serializers import FlightSerializer

from .utils.conftest import api_client

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
    
    # Test case 1: valid filter parameters are provided
    response = api_client.get(url, data={
        'departure_airport': flight.departure_airport,
        'arrival_airport': flight.arrival_airport,
        'depature_datetime_start': timezone.now().isoformat(),
        'departure_datetime_end': (timezone.now() + timezone.timedelta(
            days=1)).isoformat()
        })
    serialized_flight = FlightSerializer([flight], many=True).data
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serialized_flight
    assert len(response.json()) > 0
    
    # Test case 2: no filter parameters provided
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0
    
    # Test case 3: with invalid filter parameters
    response = api_client.get(url, {
        'departure_airport': 'non-existent-airport',
        'arrival_airport': 'non-existent-airport',
        'depature_datetime_start': 'invalid-datetime',
        'departure_datetime_end': 'invalid-datetime'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_departure_airports_report(api_client, create_flight):
    flight = create_flight
    url = reverse('flight-departure-airports-report')
    
    # Test case 1: correct data returned when valid filter params are provided
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
    
    now = datetime.now()
    start_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
    end_datetime = now + timedelta(days=1)
    response = api_client.get(url, {
        'start_datetime': start_datetime,
        'end_datetime': end_datetime.strftime('%Y-%m-%d %H:%M:%S')
    })
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == response_data
    
    # Test case 2: no filter params provided
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'departure_airports' in response.json()
    assert 'in_flight_aircraft_count' in response.json()
    assert 'aircraft_in_flight' in response.json()
    
    # Test case 3: Test with invalid filter parameters
    response = api_client.get(url, {
        'start_datetime': 'invalid-datetime',
        'end_datetime': 'invalid-datetime'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
