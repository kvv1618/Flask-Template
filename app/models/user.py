from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)