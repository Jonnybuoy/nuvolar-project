from datetime import datetime

from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import FlightFilter
from .models import Aircraft, Flight
from .serializers import AircraftSerializer, FlightSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter

    @action(detail=False, methods=['get'])
    def search_flights(self, request):
        # Get the filtered queryset using the filter class
        filtered_queryset = self.filter_queryset(self.get_queryset())

        # Access the filter parameters
        departure_airport = self.request.query_params.get(
            'departure_airport', None)
        arrival_airport = self.request.query_params.get(
            'arrival_airport', None)
        departure_datetime_start = self.request.query_params.get(
            'departure_datetime_start', None)
        departure_datetime_end = self.request.query_params.get(
            'departure_datetime_end', None)

        if departure_airport:
            filtered_queryset = filtered_queryset.filter(
                departure_airport=departure_airport)

        if arrival_airport:
            filtered_queryset = filtered_queryset.filter(
                arrival_airport=arrival_airport)

        if departure_datetime_start:
            filtered_queryset = filtered_queryset.filter(
                departure_datetime__gte=departure_datetime_start)

        if departure_datetime_end:
            filtered_queryset = filtered_queryset.filter(
                departure_datetime__lte=departure_datetime_end)

        # Serialize and return the filtered data
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def departure_airports_report(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())

        start_datetime = self.request.query_params.get('start_datetime', None)
        end_datetime = self.request.query_params.get('end_datetime', None)

        # Validate datetime values
        try:
            if start_datetime:
                start_datetime = datetime.strptime(
                    start_datetime, '%Y-%m-%d %H:%M:%S')
            if end_datetime:
                end_datetime = datetime.strptime(
                    end_datetime, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise serializers.ValidationError(
                'Invalid datetime format. Use YYYY-MM-DD HH:MM:SS format.')

        if start_datetime and end_datetime:
            filtered_queryset = filtered_queryset.filter(
                Q(departure_datetime__range=(start_datetime, end_datetime)) |
                Q(arrival_datetime__range=(start_datetime, end_datetime)) |
                Q(departure_datetime__lte=start_datetime,
                  arrival_datetime__gte=end_datetime)
            )

        departure_airports = filtered_queryset.values_list(
            'departure_airport', flat=True).distinct()
        in_flight_aircraft_count = filtered_queryset.values(
            'aircraft').distinct().count()

        aircraft_in_flight = []
        now = timezone.now()
        for flight in filtered_queryset:
            aircraft_in_flight.append({
                'aircraft': flight.aircraft.serial_no,
                'in_flight_time_minutes': int((
                    (now - flight.departure_datetime).total_seconds()) / 60)
            })

        response_data = {
            'departure_airports': departure_airports,
            'in_flight_aircraft_count': in_flight_aircraft_count,
            'aircraft_in_flight': aircraft_in_flight
        }

        return Response(response_data)
