from flask import Blueprint, request, jsonify
from app.models.post import Post, db
from flask_login import login_required, current_user

content_bp = Blueprint('content', __name__)

@content_bp.route('', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    content = data.get('content')

    post = Post(content=content, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created"}), 201
@content_bp.route('', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{"content": post.content, "user": post.user_id} for post in posts]), 200
