import os
from flask import Flask

from db import engine, Base
# Import both festival and session blueprints
from Festival_micro.resources.Festival_CRUD import bp as festival_bp
from Festival_micro.resources.Session_CRUD import bp as session_bp

# Initialize Flask app
def create_app():
    app = Flask(__name__)

    # Enable debug mode based on environment variable (optional, useful for development)
    app.config["DEBUG"] = os.getenv('FLASK_ENV', 'production') == 'development'

    # Register the festival and session blueprints
    app.register_blueprint(festival_bp)
    app.register_blueprint(session_bp)

    # Ensure database tables are created (still needed for Blueprint-based setup)
    Base.metadata.create_all(bind=engine)

    return app

if __name__ == '__main__':
    # Set port via environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    app = create_app()
    app.run(host='0.0.0.0', port=port)
