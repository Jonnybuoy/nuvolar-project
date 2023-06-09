from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AircraftViewSet, FlightViewSet

router = DefaultRouter()
router.register(r'aircraft', AircraftViewSet, basename="aircraft")
router.register(r'flight', FlightViewSet, basename="flight")

urlpatterns = [
    path('', include(router.urls)),
    path('flight/search_flights', FlightViewSet.as_view(
        {'get': 'search_flights'})),
    path('flight/departure_airports_report', FlightViewSet.as_view(
        {'get': 'departure_airports_report'}))
]
