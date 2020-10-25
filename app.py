from flask import Flask, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db

#routes
from routes.user import user_route
from routes.nota import nota_route

app=Flask(__name__)

app.url_map.strict_slashes = False
app.config.from_pyfile('settings.py')

jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html', name='home') 

app.register_blueprint(user_route) 
app.register_blueprint(nota_route)

if __name__ == '__main__':
    manager.run()