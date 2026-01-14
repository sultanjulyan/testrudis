"""
Integration tests for /login endpoint
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


@pytest.fixture
def registered_user(client):
    """Create a registered user for login tests."""
    email = unique_email("logintest")
    client.post('/api/users/register', json={
        'email': email,
        'password': 'testpassword123'
    })
    return {
        'email': email,
        'password': 'testpassword123'
    }


class TestLoginEndpoint:
    """Integration tests for POST /api/users/login"""

    def test_login_returns_200_for_valid_credentials(self, client, registered_user):
        """POST /login with valid credentials returns 200 and sets cookie."""
        response = client.post('/api/users/login', json={
            'email': registered_user['email'],
            'password': registered_user['password']
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data
        assert data['email'] == registered_user['email']
        
        # Should set HttpOnly cookie
        cookies = response.headers.getlist('Set-Cookie')
        assert any('access_token' in cookie for cookie in cookies)

    def test_login_returns_400_for_wrong_password(self, client, registered_user):
        """POST /login with wrong password returns 400."""
        response = client.post('/api/users/login', json={
            'email': registered_user['email'],
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert 'Invalid credentials' in data['error']

    def test_login_returns_400_for_nonexistent_email(self, client):
        """POST /login with non-existent email returns 400."""
        response = client.post('/api/users/login', json={
            'email': unique_email("nonexistent"),
            'password': 'somepassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        # Generic error for security (don't reveal if email exists)
        assert 'Invalid credentials' in data['error']

    def test_login_returns_400_for_missing_email(self, client):
        """POST /login without email returns 400."""
        response = client.post('/api/users/login', json={
            'password': 'somepassword'
        })
        
        assert response.status_code == 400

    def test_login_returns_400_for_missing_password(self, client):
        """POST /login without password returns 400."""
        response = client.post('/api/users/login', json={
            'email': unique_email()
        })
        
        assert response.status_code == 400
