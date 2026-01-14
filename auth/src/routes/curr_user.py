"""
Current user routes - /me endpoint
"""
from flask import Blueprint, jsonify, g
from middleware.auth_middleware import require_auth


curr_user_bp = Blueprint("curr_user", __name__)


@curr_user_bp.route("/me", methods=["GET"])
@require_auth
def get_me():
    """
    Get current authenticated user info.
    
    Returns:
        200: User data (id, email, createdAt)
        401: Not authenticated
    """
    user = g.current_user
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "createdAt": user.createdAt.isoformat()
    }), 200
