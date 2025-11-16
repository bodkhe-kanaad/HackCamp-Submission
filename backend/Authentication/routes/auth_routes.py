from flask import Blueprint, request, jsonify
from backend.Authentication.auth_service import authenticate_user, create_user

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.post("/login")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Calls the authentication function
    valid = authenticate_user(username, password)

    return jsonify({"authenticated": valid})

@auth_bp.post("/signup")
def signup():
    data = request.json
    success, message, user_id = create_user(data)
    if success:
        return jsonify({'success': True, 'message': message, 'user_id': user_id})
    else:
        return jsonify({'success': False, 'message': message}), 400