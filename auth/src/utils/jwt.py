"""
JWT Token utilities
"""
import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

# Get secret from environment
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24


def create_access_token(user_id: int, expires_in_seconds: Optional[int] = None) -> str:
    """
    Create a JWT access token for a user.
    
    Args:
        user_id: The user's ID to encode in the token.
        expires_in_seconds: Optional custom expiry time. Defaults to 24 hours.
    
    Returns:
        The encoded JWT string.
    """
    now = datetime.now(timezone.utc)
    
    if expires_in_seconds is not None:
        expiry = now + timedelta(seconds=expires_in_seconds)
    else:
        expiry = now + timedelta(hours=JWT_EXPIRY_HOURS)
    
    payload = {
        "user_id": user_id,
        "iat": now,
        "exp": expiry,
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT access token.
    
    Args:
        token: The JWT string to verify.
    
    Returns:
        The decoded payload if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
