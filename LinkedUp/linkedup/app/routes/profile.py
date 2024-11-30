from flask import Blueprint, request, jsonify
from app.models.user import User, db
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('', methods=['GET', 'PUT'])
@login_required
def profile():
    
    if request.method == 'GET':
        # Return the profile data of the currently logged-in user
        return jsonify({
            "name": current_user.name,
            "email": current_user.email,
            "bio": current_user.bio  # Include bio in the response
        })

    if request.method == 'PUT':
        # Update the user's profile data
        data = request.get_json()
        current_user.name = data.get('name', current_user.name)
        current_user.bio = data.get('bio', current_user.bio)  # Update bio if provided
        db.session.commit()

        return jsonify({"message": "Profile updated successfully."}), 200

@profile_bp.route('/delete', methods=['DELETE'])
@login_required
def delete_profile():
    # Delete the currently logged-in user's profile
    db.session.delete(current_user)
    db.session.commit()

    return jsonify({"message": "Profile deleted successfully."}), 200