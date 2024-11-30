from app.models.user import User,db
from werkzeug.security import check_password_hash
from authlib.integrations.flask_client import OAuth
from flask import current_app

# OAuth initialization
oauth = OAuth(current_app)

def authenticate_user(email, password):
    """Handles email/password authentication."""
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        return user  # User found and password matches
    return None  # Authentication failed

def handle_oauth_login(redirect_uri=None):
    """Handles OAuth login (e.g., Google login)."""
    google = oauth.create_client('google')  # OAuth client setup for Google
    if redirect_uri:
        # Redirect the user to the Google OAuth login page
        return google.authorize_redirect(redirect_uri)
    else:
        # Exchange authorization code for tokens and authenticate user
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token)
        
        email = user_info.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            # If the user doesn't exist, create a new user
            user = User(email=email, name=user_info.get('name'))
            db.session.add(user)
            db.session.commit()

        return user
