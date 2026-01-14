"""
Integration tests for /me endpoint (protected)
"""
import pytest
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from app import app


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def unique_email():
    """Generate unique email for test isolation."""
    return f"metest_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def authenticated_client(client, unique_email):
    """Create a registered user and return client with auth cookie."""
    # Register user
    reg_response = client.post('/api/users/register', json={
        'email': unique_email,
        'password': 'testpassword123'
    })
    
    # Login to get cookie
    login_response = client.post('/api/users/login', json={
        'email': unique_email,
        'password': 'testpassword123'
    })
    
    # Return client with the email for assertions
    client.test_email = unique_email
    return client


class TestMeEndpoint:
    """Integration tests for GET /api/users/me"""

    def test_me_returns_200_when_authenticated(self, authenticated_client):
        """GET /me with valid cookie returns 200 and user data."""
        response = authenticated_client.get('/api/users/me')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data
        assert data['email'] == authenticated_client.test_email
        assert 'password' not in data

    def test_me_returns_401_without_cookie(self, client):
        """GET /me without cookie returns 401."""
        response = client.get('/api/users/me')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_me_returns_401_with_invalid_token(self, client):
        """GET /me with invalid token returns 401."""
        client.set_cookie('access_token', 'invalid.token.here', domain='localhost')
        response = client.get('/api/users/me')
        
        assert response.status_code == 401
