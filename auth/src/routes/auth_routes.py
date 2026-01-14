"""Auth routes for registration and login"""
from flask import Blueprint, request, jsonify, make_response
from pydantic import ValidationError

from services.auth_service import register_user, login_user
from models.user import UserResponse
from middleware.errors import AppError
from utils.jwt import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}, 200


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    
    POST /api/users/register
    Body: { "email": string, "password": string }
    Returns: 201 with user data or 400/409 on error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body required"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400
    
    try:
        user = register_user(email, password)
        response_data = UserResponse.model_validate(user)
        return jsonify(response_data.model_dump(mode="json")), 201
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login a user.
    
    POST /api/users/login
    Body: { "email": string, "password": string }
    Returns: 200 with user data and sets HttpOnly cookie, or 400/401 on error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body required"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400
    
    try:
        user = login_user(email, password)
        
        # Create JWT token
        token = create_access_token(user_id=user.id)
        
        # Create response with user data
        response_data = UserResponse.model_validate(user)
        response = make_response(jsonify(response_data.model_dump(mode="json")))
        
        # Set HttpOnly cookie for security
        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="Lax",
            max_age=86400  # 24 hours
        )
        
        return response, 200
    except ValidationError as e:
        return jsonify({"error": "Validation failed", "details": e.errors()}), 400
    except AppError as e:
        return jsonify({"error": e.message}), e.status_code


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Logout a user by clearing the access token cookie.
    
    POST /api/users/logout
    Returns: 200 on success
    """
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.delete_cookie("access_token")
    return response, 200