from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(10), nullable=False)
    password=db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return 'User %r' %  self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

    