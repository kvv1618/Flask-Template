from datetime import datetime
from uuid import uuid4
from flask_restx import Resource, Namespace

from app import bcrypt, db
from app.models import User
from app.schemas import RoleEnum
from app.utils import get_login_parser, get_signup_parser, access_token_required

api = Namespace('auth', path="/auth", description='Authentication related operations')
signup_parser = get_signup_parser()
login_parser = get_login_parser()

@api.route("/signup")
class Signup(Resource):
    @api.expect(signup_parser)
    def post(self):        
        payload = signup_parser.parse_args()
        username, password, role = payload['username'], payload['password'], payload['role']
        if role not in RoleEnum.__members__:
            return {"message": "Invalid role"}, 400

        role = RoleEnum[role].value
        existing_user = db.session.query(User).filter_by(username=username).first()
        if existing_user:
            return {"message": "User already exists"}, 400
        user = {
            "id": str(uuid4()),
            "username": username,
            "password": bcrypt.generate_password_hash(password).decode('utf-8'),
            "role": role,
            "created_at": datetime.utcnow(),
        }
        db.session.add(User(**user))
        db.session.commit()
        return {"message": "Signup Successful"}, 201
        
@api.route("/login")
class Login(Resource):
    @api.expect(login_parser)
    def post(self):
        payload = login_parser.parse_args()
        username, password = payload['username'], payload['password']
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            return {"message": "User not found with given username"}, 404
        
        if not bcrypt.check_password_hash(user.password, password):
            return {"message": "Invalid Credentials"}, 401
        
        op_status, resp = User.encode_auth_token(user.id)
        if not op_status:
            return {"message": resp["message"]}, resp["status_code"]
        
        return {"accessToken": resp["access_token"]}, 200

@api.route("/jwt")
class UserJwt(Resource):
    @api.doc(security='Access Token')
    @access_token_required
    def get(self):
        op_status, resp = User.get_loggedin_user()
        return {"message": "success", "user": resp["user"]}, 200