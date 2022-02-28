from datetime import datetime, timedelta
from email.policy import default

import jwt
from flask import request

from app import db, config

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            access_token = jwt.encode(
                payload,
                config.JWT_SECRET,
                algorithm='HS256'
            )
            return True, {"access_token": access_token}
        except Exception as e:
            return False, {"message": "Error in generating token."+str(e), "status_code": 500}
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, config.JWT_SECRET, algorithms='HS256')
            return True, {"user_id": payload['sub']}
        except jwt.ExpiredSignatureError:
            return False, {"message": "Signature expired. Please log in again.", "status_code": 401}
        except jwt.InvalidTokenError:
            return False, {"message": "Invalid token. Please log in again.", "status_code": 401}
    
    @staticmethod
    def get_loggedin_user():
        access_token = request.headers.get('accessToken')
        if not access_token:
            return False, {"message": "User is not logged in.", "status_code": 401}
        
        op_status, resp = User.decode_auth_token(access_token)
        if not op_status:
            return False, resp
        
        user_id = resp["user_id"]
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return False, {"message": "Invalid token, User does not exist.", "status_code": 401}
        
        return True, {"user": {"id": user.id, "username": user.username}}
        
class TaxPayer(db.Model):
    __tablename__ = "tax_payers"
    id = db.Column(db.String(255), primary_key=True)
    user_id= db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    username= db.Column(db.String(255), server_default="",nullable=False)
    tax_status= db.Column(db.Integer,server_default="0", nullable=False)
    cgst= db.Column(db.Float, server_default="0", nullable=False)
    sgst= db.Column(db.Float, server_default="0", nullable=False)
    total_due= db.Column(db.String(255), server_default="",nullable=False)
    due_date= db.Column(db.DateTime, server_default="",nullable=False)