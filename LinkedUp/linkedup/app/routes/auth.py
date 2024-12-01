from flask import Blueprint, request, jsonify, url_for
from app.models.user import User, db
from werkzeug.security import generate_password_hash, check_password_hash
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Both fields are required!"}), 400

    conn = sqlite3.connect('instance/app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "User not found!"}), 404

    stored_password = user[2]  # Assuming password is the 3rd column
    if not check_password_hash(stored_password, password):
        return jsonify({"error": "Invalid password!"}), 401

    # Generate JWT token
    token = jwt.encode(
        {'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        app.config['SECRET_KEY'], algorithm="HS256"
    )

    return jsonify({'message': 'Login successful', 'token': token}), 200

@auth_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('auth.auth_google', _external=True)
    return handle_oauth_login(redirect_uri)

@auth_bp.route('/auth/callback')
def auth_google():

    token = request.args.get('token')  
    user = handle_oauth_login(token)
    
    if user:
        access_token = create_access_token(identity=user.user_id)  # Fixed user_id reference
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "OAuth authentication failed."}), 401
