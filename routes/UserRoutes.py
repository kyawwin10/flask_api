from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from services.UserService import get_user_by_email_service, create_user_service

auth_bp = Blueprint('auth', __name__)

blacklist = set()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')

    if not username or not password or not phone or not email:
        return jsonify({'error': 'Username, password, phone, and email are required'}), 400

    if get_user_by_email_service(email):
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    user = create_user_service(username, hashed_password, phone, email)
    return jsonify({'message': 'Register created successfully', 'user': user}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
        
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and Password required'}), 400

    user = get_user_by_email_service(email)
    if not user or not check_password_hash(user.password, password):
        print("Password", password)
        return jsonify({'error': 'Invalid Email or Password'}), 401

    access_token = create_access_token(identity=user.password)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/logout', methods=['GET'])
def logout():
    response = jsonify({'msg': 'Successfully logged out'})
    unset_jwt_cookies(response)
    return response, 200