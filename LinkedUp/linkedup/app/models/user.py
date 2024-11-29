from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(20), default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    connections = db.relationship('Connection', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}')"
