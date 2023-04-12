# Nuvolar Fleet Management

Nuvolar Fleet Management is a web api application built on Django Rest Framework that allows users to track flights, view flight details, and apply filters to search for flights based on various criteria.

## Features

- Create and manage aircraft and flight objects in the system.
- View flight details including departure airport, arrival airport, departure  datetime, and aircraft information.
- Apply filters to search for flights based on departure airport, arrival airport, and departure datetime.
- Display flight results in a paginated and sorted manner.
- API endpoints for CRUD (Create, Read, Update, Delete) operations on flights.

## Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher
- Django Rest Framework 3.12 or higher
- django-filters 3.0 or higher

## Installation
The project can be installed using docker by following these steps:

1. Clone the repository to your local machine:
```bash
$ git clone https://github.com/Jonnybuoy/nuvolar-project
```

2. Navigate to the project directory:
```bash
$ cd nuvolar-project
```

3. Ensure you have installed docker on your machine. You can install using the steps outlined [here](https://www.docker.com/get-started)

4. Since you've already cloned the repository, you have access to the Dockerfile and dockor_compose.yml file so simply run the following commands:
```bash
$ docker compose up -d --build
$ docker compose up
```
This files assume that they are only to be used for development purposes.

5. Access the Nuvolar Fleet Management application in your web browser at http://localhost:8000 or http://127.0.0.1:8000

## API Endpoints
- GET /api/aircraft/: Get a list of all aircrafts.
- POST /api/aircraft/: Create a new aircraft.
- PUT /api/aircraft/<aircraft_id>/: Update details of a specific aircraft.

- GET /api/flight/: Get a list of all flights.
- POST /api/flight/: Create a new flight.
- GET /api/flight/<flight_id>/: Get details of a specific flight.
- PUT /api/flight/<flight_id>/: Update details of a specific flight.
- DELETE /api/flight/<flight_id>/: Delete a specific flight.

- GET /flight/search_flights/: Search flights.
- GET /flight/departure_airports_report/: Retrieve the list of departure airports.


## Filters
Nuvolar Fleet Management supports the following filters for flight search:

- `departure_airport`: Filter flights by departure airport (exact match).
- `arrival_airport`: Filter flights by arrival airport (exact match).
- `departure_datetime_start`: Filter flights by departure datetime (greater than or equal to).
- `departure_datetime_end`: Filter flights by departure datetime (less than or equal to).

You can apply these filters in the query parameters of the API endpoints.

For example:

1. To retrieve the list of departure airports for a giving period of date and time, simply query:
- GET /flight/departure_airports_report/?start_datetime=2023-04-11 17:10:00&end_datetime=2023-04-12 02:00:00

This will retrieve the list of departure airports and all aircrafts in flight for the period between 2023-04-11 at 17:10 and 2023-04-12 at 02:00

2. To search for flights by departure and arrival airport and also by a departure date and time range, simply query:
- GET /flight/search_flights/?departure_airport=<airport_ICAO_CODE> OR
- GET /flight/search_flights/?arrival_airport=<airport_ICAO_CODE> OR
- GET /flight/search_flights/?departure_datetime_start=<datetime_start_range>&departure_datetime_end=<datetime_end_range>


## Testing
Nuvolar Fleet Management includes unit tests for the models, views, and filters. To run the tests, use the following command:

```bash
py.test tests/<test_file>
```
