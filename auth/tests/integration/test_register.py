"""
Integration tests for /register endpoint
"""
import pytest
import sys
import os
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from app import app


def unique_email(prefix: str = "test") -> str:
    """Generate a unique email for test isolation."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestRegisterEndpoint:
    """Integration tests for POST /api/users/register"""

    def test_register_returns_201_for_valid_request(self, client):
        """POST /register with valid data returns 201 and user data."""
        email = unique_email("newuser")
        response = client.post('/api/users/register', json={
            'email': email,
            'password': 'securepassword123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['email'] == email
        assert 'password' not in data  # Password should not be returned

    def test_register_returns_400_for_missing_email(self, client):
        """POST /register without email returns 400."""
        response = client.post('/api/users/register', json={
            'password': 'securepassword123'
        })
        
        assert response.status_code == 400

    def test_register_returns_400_for_missing_password(self, client):
        """POST /register without password returns 400."""
        response = client.post('/api/users/register', json={
            'email': unique_email()
        })
        
        assert response.status_code == 400

    def test_register_returns_409_for_duplicate_email(self, client):
        """POST /register with existing email returns 409."""
        email = unique_email("existing")
        
        # First registration
        client.post('/api/users/register', json={
            'email': email,
            'password': 'password123'
        })
        
        # Second registration with same email
        response = client.post('/api/users/register', json={
            'email': email,
            'password': 'differentpassword'
        })
        
        assert response.status_code == 409
        data = response.get_json()
        assert 'error' in data

    def test_register_returns_400_for_invalid_email(self, client):
        """POST /register with invalid email format returns 400."""
        response = client.post('/api/users/register', json={
            'email': 'not-an-email',
            'password': 'password123'
        })
        
        assert response.status_code == 400

    def test_register_returns_400_for_short_password(self, client):
        """POST /register with password < 8 chars returns 400."""
        response = client.post('/api/users/register', json={
            'email': unique_email(),
            'password': 'short'
        })
        
        assert response.status_code == 400
