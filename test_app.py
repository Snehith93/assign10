import pytest
from app import app  # Import the Flask app from app.py

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    """Test the hello world route."""
    response = client.get('/')
    assert response.data == b'Hello Chinni'
    assert response.status_code == 200
