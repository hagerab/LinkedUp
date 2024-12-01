from app import create_app
from app.routes.auth import auth_bp  # Import the auth blueprint

app = create_app()  # Create the app instance
app.register_blueprint(auth_bp, url_prefix='/auth')  # Register the auth blueprint

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
