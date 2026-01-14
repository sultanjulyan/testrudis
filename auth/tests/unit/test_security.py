"""
Unit tests for Security utilities - Password and JWT
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from utils.security import hash_password, verify_password


class TestPasswordHashing:
    """Test cases for password hashing utilities."""

    def test_hash_password_returns_different_value(self):
        """Hash should be different from plain password."""
        plain = "mysecurepassword"
        hashed = hash_password(plain)
        
        assert hashed != plain
        assert len(hashed) > len(plain)

    def test_hash_password_produces_unique_hashes(self):
        """Same password should produce different hashes (due to salt)."""
        plain = "mysecurepassword"
        hash1 = hash_password(plain)
        hash2 = hash_password(plain)
        
        # Argon2 uses random salt, so hashes should differ
        assert hash1 != hash2

    def test_verify_password_returns_true_for_correct(self):
        """Verify should return True for correct password."""
        plain = "mysecurepassword"
        hashed = hash_password(plain)
        
        assert verify_password(plain, hashed) is True

    def test_verify_password_returns_false_for_incorrect(self):
        """Verify should return False for incorrect password."""
        plain = "mysecurepassword"
        hashed = hash_password(plain)
        
        assert verify_password("wrongpassword", hashed) is False


class TestJWTToken:
    """Test cases for JWT token utilities."""

    def test_create_token_returns_string(self):
        """Create token should return a JWT string."""
        from utils.jwt import create_access_token
        
        token = create_access_token(user_id=1)
        
        assert isinstance(token, str)
        assert len(token) > 0
        # JWT has 3 parts separated by dots
        assert token.count('.') == 2

    def test_verify_token_returns_payload(self):
        """Verify should return the token payload."""
        from utils.jwt import create_access_token, verify_access_token
        
        token = create_access_token(user_id=42)
        payload = verify_access_token(token)
        
        assert payload is not None
        assert payload.get("user_id") == 42

    def test_verify_token_fails_for_invalid(self):
        """Verify should return None for invalid token."""
        from utils.jwt import verify_access_token
        
        result = verify_access_token("invalid.token.here")
        
        assert result is None

    def test_verify_token_fails_for_expired(self):
        """Verify should return None for expired token."""
        from utils.jwt import create_access_token, verify_access_token
        import time
        
        # Create token with very short expiry (already expired)
        token = create_access_token(user_id=1, expires_in_seconds=-10)
        
        result = verify_access_token(token)
        
        assert result is None
