import os
from flask import jsonify, request, Blueprint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, create_access_token
from models import db, User

bcrypt = Bcrypt()
user_route = Blueprint('user_route', __name__)

@user_route.route('/users', methods=['GET'])
@user_route.route('/user/<int:id>', methods=['GET'])
def getUsers(id=None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            return jsonify(user.serialize()), 200
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200   

@user_route.route('/users', methods=['POST'])
@user_route.route('/user/<int:id>', methods=['PUT', 'DELETE'])
#@jwt_required
def otherUsers(id=None):
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = User()
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 200

    if request.method == 'PUT':
        user = User.query.get(id)
        username = request.json.get('username')
        password = request.json.get('password')
        user.username = username
        user.password = password
        db.session.commit()
        return jsonify(user.serialize()), 200
    
    if request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.serialize()), 200


@user_route.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username:
        return jsonify({'error': 'Usuario es obligatorio'}), 422
    if not password:
        return jsonify({'error': 'Contraseña es obligatorio'}), 422
    user = User.query.filter_by(username = username).first()
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else: 
        return jsonify({ "error": "Usuario o Contraseña Incorrectos" }), 200

    
@user_route.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username:
        return jsonify({'error': 'Usuario es obligatorio'}), 422
    if not password:
        return jsonify({'error': 'Contraseña es obligatorio'}), 422
    user = User()
    user.username = username
    user.password = bcrypt.generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "success": "Usuario registrado exitósamente",
        "user": user.serialize()
    }), 200


 