from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import pymysql
from app.models.user import User  # Assuming the User model is in app.models.user
from flask import Flask, render_template

login_manager = LoginManager()

# Add this line to load the user from the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_filename="config"):
    load_dotenv()
    pymysql.install_as_MySQLdb()
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Linkedup-012@127.0.0.1/linkedup_dp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints (routes)
    from .routes.auth import auth_bp
    from .routes.profile import profile_bp
    from .routes.content import content_bp


    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(content_bp, url_prefix="/api/posts")

    # Serve the front-end (index.html)
    @app.route('/')
    def index():
        return render_template('index.html')  # Render the HTML page


    return app
