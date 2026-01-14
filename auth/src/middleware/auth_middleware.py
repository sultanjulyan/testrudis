"""
Authentication middleware - JWT verification
"""
from functools import wraps
from flask import request, jsonify, g
from utils.jwt import verify_access_token
from services.auth_service import get_user_by_id
from middleware.errors import UnauthorizedError


def require_auth(f):
    """
    Decorator to require authentication for a route.
    
    Sets g.current_user if authenticated.
    Returns 401 if not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("access_token")
        
        if not token:
            return jsonify({"error": "Authentication required"}), 401
        
        payload = verify_access_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        user_id = payload.get("user_id")
        if not user_id:
            return jsonify({"error": "Invalid token payload"}), 401
        
        try:
            user = get_user_by_id(user_id)
            g.current_user = user
        except UnauthorizedError:
            return jsonify({"error": "User not found"}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
