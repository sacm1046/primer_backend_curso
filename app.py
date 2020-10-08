import os
from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

app.url_map.strict_slashes = False

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.route('/')
def home():
    return render_template('index.html', name='home')

@app.route('/users', methods=['GET', 'POST'])
@app.route('/user/<int:id>', methods=['GET'])
def getUsers(id=None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            return jsonify(user.serialize()), 200
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200    
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = User()
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()

        return jsonify(user.serialize()), 200 

if __name__ == '__main__':
    manager.run()