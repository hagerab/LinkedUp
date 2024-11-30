from flask import Blueprint, request, jsonify, url_for
from app.models.user import User, db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.services.auth_service import handle_oauth_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = generate_password_hash(data.get('password'), method='sha256')
    name = data.get('name')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(email=email, password=password, name=name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401



@auth_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.auth_google', _external=True)
    return handle_oauth_login(redirect_uri)  # Redirect to Google OAuth

@auth_bp.route('/auth/callback')
def auth_google():

    token = request.args.get('token')  
    user = handle_oauth_login(token)
    
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "OAuth authentication failed."}), 401