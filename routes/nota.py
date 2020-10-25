from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from models import db, Nota

nota_route = Blueprint('nota_route', __name__)

@nota_route.route('/notas', methods=['GET'])
@nota_route.route('/nota/<int:id>', methods=['GET'])
def getNotas(id=None):
    if request.method == 'GET':
        if id is not None:
            nota = Nota.query.get(id)
            return jsonify(nota.serialize()), 200
        else:
            notas = Nota.query.all()
            notas = list(map(lambda nota: nota.serialize(), notas))
            return jsonify(notas), 200   

@nota_route.route('/notas', methods=['POST'])
@nota_route.route('/nota/<int:id>', methods=['PUT', 'DELETE'])
#@jwt_required
def otherNotas(id=None):
    if request.method == 'POST':
        value = request.json.get('value')
        user_id = request.json.get('user_id')
        nota = Nota()
        nota.value = value
        nota.user_id = user_id
        db.session.add(nota)
        db.session.commit()
        return jsonify(nota.serialize()), 200

    if request.method == 'PUT':
        nota = Nota.query.get(id)
        value = request.json.get('value')
        user_id = request.json.get('user_id')
        nota.value = value
        nota.user_id = user_id
        db.session.commit()
        return jsonify(nota.serialize()), 200
    
    if request.method == 'DELETE':
        nota = Nota.query.get(id)
        db.session.delete(nota)
        db.session.commit()
        return jsonify(nota.serialize()), 200
