from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .filters import FlightFilter
from .models import Aircraft, Flight
from .serializers import AircraftSerializer, FlightSerializer


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class= AircraftSerializer


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
        departure_airport = self.request.query_params.get('departure_airport', None)
        arrival_airport = self.request.query_params.get('arrival_airport', None)
        departure_datetime_start = self.request.query_params.get('departure_datetime_start', None)
        departure_datetime_end = self.request.query_params.get('departure_datetime_end', None)

        
        if departure_airport:
            filtered_queryset = filtered_queryset.filter(departure_airport=departure_airport)

        if arrival_airport:
            filtered_queryset = filtered_queryset.filter(arrival_airport=arrival_airport)

        if departure_datetime_start:
            filtered_queryset = filtered_queryset.filter(departure_datetime__gte=departure_datetime_start)
            
        if departure_datetime_end:
            filtered_queryset = filtered_queryset.filter(departure_datetime__lte=departure_datetime_end)

        # Serialize and return the filtered data
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
        
