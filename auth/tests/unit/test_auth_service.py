"""
Unit tests for Auth Service - Registration
"""
import pytest
import sys
import os
import uuid

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


def unique_email(prefix: str = "test") -> str:
    """Generate a unique email for test isolation."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}@example.com"


class TestAuthServiceRegister:
    """Test cases for user registration service."""

    def test_register_creates_user_with_valid_data(self):
        """Given valid email and password, should create a new user."""
        # This test will fail until auth_service.register is implemented
        from services.auth_service import register_user
        
        email = unique_email("create")
        result = register_user(email, "password123")
        
        assert result is not None
        assert result.email == email
        assert result.id is not None

    def test_register_hashes_password(self):
        """Password should be hashed before storing."""
        from services.auth_service import register_user
        
        email = unique_email("hash")
        result = register_user(email, "plainpassword")
        
        # Password should not be stored as plain text
        assert result.password != "plainpassword"
        assert len(result.password) > 20  # Hashed passwords are longer

    def test_register_rejects_duplicate_email(self):
        """Should raise error when email already exists."""
        from services.auth_service import register_user
        from middleware.errors import ConflictError
        
        email = unique_email("dup")
        
        # First registration should succeed
        register_user(email, "password123")
        
        # Second registration with same email should fail
        with pytest.raises(ConflictError):
            register_user(email, "password456")

    def test_register_validates_email_format(self):
        """Should reject invalid email format."""
        from services.auth_service import register_user
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            register_user("invalid-email", "password123")

    def test_register_validates_password_length(self):
        """Should reject password shorter than 8 characters."""
        from services.auth_service import register_user
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            register_user(unique_email("short"), "short")
