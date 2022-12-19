from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # unique = True
    data = db.Column(db.PickleType, nullable=False)
    access = db.Column(db.PickleType)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'User {self.id} - {self.username}'


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answers = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
    )
    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz.id', ondelete='CASCADE'),
    )
