import os
from flask import Flask

from db import engine, Base
# Import user and profile blueprints
from resources.User_CRUD import bp as user_bp
from resources.Profile_CRUD import bp as profile_bp

# Initialize Flask app
def create_app():
    app = Flask(__name__)

    # Enable debug mode based on environment variable (optional, useful for development)
    app.config["DEBUG"] = os.getenv('FLASK_ENV', 'production') == 'development'

    # Register the user and profile blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(profile_bp)

    # Ensure database tables are created (still needed for Blueprint-based setup)
    Base.metadata.create_all(bind=engine)

    return app

if __name__ == '__main__':
    # Set port via environment or default to 5001
    port = int(os.getenv('PORT', 5001))
    app = create_app()
    app.run(host='0.0.0.0', port=port)
