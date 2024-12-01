from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Ensure it matches the name of your table
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(20), default='default.jpg')
    user_posts = db.relationship('Post', backref='author', lazy=True)
    user_reactions = db.relationship('Reaction', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.user_id}', '{self.name}')"
