from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.connection import Connection, db
from app.models.user import User

connection_bp = Blueprint('connection', __name__)

@connection_bp.route('/send', methods=['POST'])
@login_required
def send_connection_request():
    data = request.get_json()

    # Get the user_id of the user to whom the connection request is being sent
    target_user_id = data.get('user_id')
    
    # Check if the user is trying to connect with themselves
    if target_user_id == current_user.id:
        return jsonify({"message": "You cannot send a connection request to yourself."}), 400

    # Check if a connection already exists or if a request is already pending
    existing_connection = Connection.query.filter(
        ((Connection.user_id == current_user.id) & (Connection.connection_id == target_user_id)) |
        ((Connection.user_id == target_user_id) & (Connection.connection_id == current_user.id))
    ).first()

    if existing_connection:
        return jsonify({"message": "Connection request already exists or you are already connected."}), 400

    # Create new connection request
    new_request = Connection(user_id=current_user.id, connection_id=target_user_id, status="Pending")
    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": f"Connection request sent to {target_user_id}."}), 200

@connection_bp.route('/accept', methods=['POST'])
@login_required
def accept_connection_request():
    data = request.get_json()
    connection_request_id = data.get('connection_request_id')

    # Find the pending connection request in the database
    connection_request = Connection.query.filter_by(id=connection_request_id, connection_id=current_user.id, status="Pending").first()

    if not connection_request:
        return jsonify({"message": "Connection request not found or already processed."}), 404

    # Update status to 'Accepted'
    connection_request.status = "Accepted"
    db.session.commit()

    return jsonify({"message": "Connection request accepted."}), 200

@connection_bp.route('/reject', methods=['POST'])
@login_required
def reject_connection_request():
    data = request.get_json()
    connection_request_id = data.get('connection_request_id')

    # Find the pending connection request
    connection_request = Connection.query.filter_by(id=connection_request_id, connection_id=current_user.id, status="Pending").first()

    if not connection_request:
        return jsonify({"message": "Connection request not found or already processed."}), 404

    # Update status to 'Rejected'
    connection_request.status = "Rejected"
    db.session.commit()

    return jsonify({"message": "Connection request rejected."}), 200

@connection_bp.route('/list', methods=['GET'])
@login_required
def list_connections():
    # Find all the connections where the current user is either the sender or the receiver
    connections = Connection.query.filter(
        (Connection.user_id == current_user.id) | (Connection.connection_id == current_user.id)
    ).all()

    connection_data = []

    for connection in connections:
        # Determine the other user
        if connection.user_id == current_user.id:
            other_user_id = connection.connection_id
        else:
            other_user_id = connection.user_id

        # Get the other user’s details
        other_user = User.query.get(other_user_id)

        # Build response based on status
        connection_data.append({
            'connection_id': other_user.id,
            'name': other_user.name,
            'status': connection.status
        })

    return jsonify({"connections": connection_data}), 200
