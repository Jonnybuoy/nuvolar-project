from django_filters import rest_framework as filters

from .models import Flight


class FlightFilter(filters.FilterSet):
    departure_airport = filters.CharFilter(lookup_expr='exact')
    arrival_airport = filters.CharFilter(lookup_expr='exact')
    departure_datetime_start = filters.DateTimeFilter(
        field_name='departure_datetime', lookup_expr='gte')
    departure_datetime_end = filters.DateTimeFilter(
        field_name='departure_datetime', lookup_expr='lte')
    
    
    class Meta:
        model = Flight
        fields = ['departure_airport', 'arrival_airport',
                  'departure_datetime']
