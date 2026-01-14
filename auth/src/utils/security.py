"""
Security utilities - Password hashing and verification
"""
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize Argon2 password hasher with secure defaults
_hasher = PasswordHasher()


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using Argon2.
    
    Args:
        plain_password: The plain text password to hash.
    
    Returns:
        The hashed password string.
    """
    return _hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to compare against.
    
    Returns:
        True if the password matches, False otherwise.
    """
    try:
        _hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False
