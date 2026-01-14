"""
Global Error Handling Middleware
"""
from flask import Flask, jsonify
from pydantic import ValidationError


class AppError(Exception):
    """Base application error."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundError(AppError):
    """Resource not found error."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ConflictError(AppError):
    """Conflict error (e.g., duplicate resource)."""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, 409)


class UnauthorizedError(AppError):
    """Unauthorized access error."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


def register_error_handlers(app: Flask) -> None:
    """Register global error handlers for the Flask app."""
    
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({
            "error": "Validation failed",
            "details": error.errors()
        }), 400

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception):
        # Log the error in production
        app.logger.error(f"Unhandled error: {str(error)}")
        return jsonify({"error": "Internal server error"}), 500
