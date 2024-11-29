from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    connection_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Status: Pending, Accepted, Declined

    def __repr__(self):
        return f"Connection('{self.user_id}', '{self.connection_id}')"
