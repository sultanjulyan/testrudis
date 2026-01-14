"""
Auth Service - Flask Application Entry Point
"""
import asyncio
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from utils.prisma import prisma
from middleware.errors import register_error_handlers
from routes.auth_routes import auth_bp
from routes.curr_user import curr_user_bp

# Load environment variables
load_dotenv()


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Configure CORS for frontend
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/users")
    app.register_blueprint(curr_user_bp, url_prefix="/api/users")
    
    return app


app = create_app()


@app.before_request
def before_request():
    """Ensure Prisma is connected before each request."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if not prisma.is_connected():
        loop.run_until_complete(prisma.connect())


@app.teardown_appcontext
def teardown(exception=None):
    """Disconnect Prisma on app context teardown."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if prisma.is_connected():
        loop.run_until_complete(prisma.disconnect())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
