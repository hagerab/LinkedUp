from flask import Blueprint, request, jsonify
from app.models.post import Post, Comment, Reaction, db
from flask_login import login_required, current_user

content_bp = Blueprint('content', __name__)

@content_bp.route('', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    content = data.get('content')

    post = Post(content=content, user_id=current_user.user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created"}), 201

@content_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    
    post_data = []
    for post in posts:
        likes_count = Reaction.query.filter_by(post_id=post.post_id).count()  # Fixed to post_id
        comments_count = len(post.comments)  # This uses the relationship from Post to Comment

        post_data.append({
            "id": post.post_id,  # Use post_id here for consistency
            "content": post.content,
            "user_id": post.user_id,
            "timestamp": post.created_at,  # Using created_at
            "likes_count": likes_count, 
            "comments_count": comments_count
        })
    
    return jsonify(post_data), 200

@content_bp.route('/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if the user has already liked the post
    existing_like = Reaction.query.filter_by(post_id=post_id, user_id=current_user.user_id).first()  # Fix user_id field
    if existing_like:
        return jsonify({"message": "You have already liked this post."}), 400
    
    # Create a new like
    like = Reaction(post_id=post_id, user_id=current_user.user_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({"message": "Post liked successfully."}), 200

# Route to comment on a post
@content_bp.route('/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_on_post(post_id):
    data = request.get_json()
    content = data.get('content')

    post = Post.query.get_or_404(post_id)

    # Create a new comment
    comment = Comment(content=content, post_id=post_id, user_id=current_user.user_id)  # Fixed user_id
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully."}), 201
