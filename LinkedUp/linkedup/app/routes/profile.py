from flask import Blueprint, request, jsonify
from app.models.user import User, db
from flask_login import login_required, current_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('', methods=['GET', 'PUT'])
@login_required
def profile():
    
    if request.method == 'GET':
        return jsonify({
            "name": current_user.name,
            "email": current_user.email,
            "profile_picture": current_user.profile_picture
        })

    if request.method == 'PUT':
        data = request.get_json()
        current_user.name = data.get('name', current_user.name)
        db.session.commit()
        return jsonify({"message": "Profile updated"}), 200
