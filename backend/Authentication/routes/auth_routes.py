from flask import Blueprint, request, jsonify
from backend.Authentication.auth_service import authenticate_user, create_user, get_user

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.post("/login")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Calls the authentication function
    user = authenticate_user(username, password)
    valid = user is not None
    if valid:
        return jsonify({"authenticated": valid, 'user_id': user[0]})
    else:
        return jsonify({"authenticated": valid})

@auth_bp.post("/signup")
def signup():
    data = request.json
    success, message, user_id = create_user(data)
    if success:
        return jsonify({'success': True, 'message': message, 'user_id': user_id})
    else:
        return jsonify({'success': False, 'message': message}), 400

@auth_bp.get("/user/<int:user_id>")
def get_user_endpoint(user_id):
    user = get_user(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404