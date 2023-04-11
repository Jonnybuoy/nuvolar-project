import pytest
from django.test.client import Client

@pytest.fixture
def api_client():
    """
    Fixture for creating an API client instance.
    """
    client = Client()
    return client