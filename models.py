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
            'username': self.username
        }

class Nota(db.Model):
    __tablename__='nota'
    id=db.Column(db.Integer, primary_key=True)
    value=db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)

    def __repr__(self):
        return 'Nota %r' %  self.value

    def serialize(self):
        return {
            'id': self.id,
            'value': self.value,
            'user': self.user.serialize()
        }

    