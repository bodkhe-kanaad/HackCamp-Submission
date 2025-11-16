from flask import Blueprint, request, jsonify
from Authentication.auth_service import authenticate_user

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.post("/login")
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Calls the authentication function
    valid = authenticate_user(username, password)

    return jsonify({"authenticated": valid})
