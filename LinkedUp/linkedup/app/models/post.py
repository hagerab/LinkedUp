from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Post(db.Model):
    __tablename__ = 'post'  # Ensure it matches the name of your table

    post_id = db.Column(db.Integer, primary_key=True)  # Post ID
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # User FK

    user = db.relationship('User', backref='user_posts', lazy=True)  # Rename the backref here
    comments = db.relationship('Comment', backref='post', lazy=True)  # Added relationship

    def __repr__(self):
        return f"Post('{self.post_id}', '{self.content}')"

class Reaction(db.Model):
    __tablename__ = 'reaction'  # Ensure it matches the name of your table

    reaction_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    post = db.relationship('Post', backref='reactions', lazy=True)
    user = db.relationship('User', backref='user_reactions', lazy=True)  # Renamed backref

    def __repr__(self):
        return f"Reaction('{self.reaction_id}', '{self.user_id}', '{self.post_id}')"

class Comment(db.Model):
    __tablename__ = 'comment'  # Ensure it matches the name of your table

    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)  # Post FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # User FK

    user = db.relationship('User', backref='user_comments', lazy=True)  # Renamed backref here to match naming convention

    def __repr__(self):
        return f"Comment('{self.comment_id}', '{self.content}')"

