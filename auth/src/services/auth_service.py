"""
Auth Service - Business logic for authentication
"""
import asyncio
from prisma.models import User
from utils.prisma import prisma
from utils.security import hash_password, verify_password
from models.user import UserRegisterInput, UserLoginInput
from middleware.errors import ConflictError, UnauthorizedError


def _get_or_create_loop():
    """Get existing event loop or create a new one."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def _run_async(coro):
    """Helper to run async code in sync context."""
    loop = _get_or_create_loop()
    return loop.run_until_complete(coro)


async def _ensure_connected():
    """Ensure Prisma is connected."""
    if not prisma.is_connected():
        await prisma.connect()


async def _register_user_async(email: str, password: str) -> User:
    """
    Register a new user (async implementation).
    
    Args:
        email: User's email address.
        password: User's plain text password.
    
    Returns:
        The created User object.
    
    Raises:
        ConflictError: If email already exists.
    """
    await _ensure_connected()
    
    # Check if email already exists
    existing_user = await prisma.user.find_unique(where={"email": email})
    if existing_user:
        raise ConflictError("Email already in use")
    
    # Hash password and create user
    hashed_password = hash_password(password)
    user = await prisma.user.create(
        data={
            "email": email,
            "password": hashed_password,
        }
    )
    
    return user


async def _login_user_async(email: str, password: str) -> User:
    """
    Authenticate a user (async implementation).
    
    Args:
        email: User's email address.
        password: User's plain text password.
    
    Returns:
        The authenticated User object.
    
    Raises:
        UnauthorizedError: If credentials are invalid.
    """
    await _ensure_connected()
    
    # Find user by email
    user = await prisma.user.find_unique(where={"email": email})
    if not user:
        raise UnauthorizedError("Invalid credentials")
    
    # Verify password
    if not verify_password(password, user.password):
        raise UnauthorizedError("Invalid credentials")
    
    return user


async def _get_user_by_id_async(user_id: int) -> User:
    """Get user by ID (async implementation)."""
    await _ensure_connected()
    
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise UnauthorizedError("User not found")
    
    return user


# Sync wrappers for Flask routes
def register_user(email: str, password: str) -> User:
    """Register a new user (sync wrapper)."""
    # Validate input
    validated = UserRegisterInput(email=email, password=password)
    return _run_async(_register_user_async(validated.email, validated.password))


def login_user(email: str, password: str) -> User:
    """Authenticate a user (sync wrapper)."""
    validated = UserLoginInput(email=email, password=password)
    return _run_async(_login_user_async(validated.email, validated.password))


def get_user_by_id(user_id: int) -> User:
    """Get user by ID (sync wrapper)."""
    return _run_async(_get_user_by_id_async(user_id))
