from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_filename="config"):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    from .routes.auth import auth_bp
    from .routes.profile import profile_bp
    from .routes.content import content_bp
    from .routes.connection import connection_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(content_bp, url_prefix="/api/posts")
    app.register_blueprint(connection_bp, url_prefix="/api/connections")

    return app
