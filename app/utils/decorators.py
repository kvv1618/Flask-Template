from functools import wraps

from app.models import User
from app.schemas import RoleEnum

def admin_access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        op_status, resp = User.get_loggedin_user()
        if not op_status:
            return {"message": resp["message"]}, resp["status_code"]
        
        user = resp["user"]
        user = User.query.filter_by(id=user['id']).first()
        if user.role != RoleEnum.ADMIN.value:
            return {"message": "You are not authorized to perform this action"}, 401
        return f(*args, **kwargs)
    return decorated

def tax_payer_access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        op_status, resp = User.get_loggedin_user()
        if not op_status:
            return {"message": resp["message"]}, resp["status_code"]
        
        user = resp["user"]
        user = User.query.filter_by(id=user['id']).first()
        if user.role != RoleEnum.TAX_PAYER.value:
            return {"message": "You are not authorized to perform this action"}, 401
        return f(*args, **kwargs)
    return decorated

def tax_accountant_access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        op_status, resp = User.get_loggedin_user()
        if not op_status:
            return {"message": resp["message"]}, resp["status_code"]
        
        user = resp["user"]
        user = User.query.filter_by(id=user['id']).first()
        if user.role != RoleEnum.TAX_ACCOUNTANT.value:
            return {"message": "You are not authorized to perform this action"}, 401
        return f(*args, **kwargs)
    return decorated

def access_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        op_status, resp = User.get_loggedin_user()
        if not op_status:
            return {"message": resp["message"]}, resp["status_code"]
        return f(*args, **kwargs)
    return decorated

def admin_or_accountant_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        op_status, resp = User.get_loggedin_user()
        if not op_status:
            return {"message": resp["message"]}, resp["status_code"]
        
        user = resp["user"]
        user = User.query.filter_by(id=user['id']).first()
        if user.role not in [RoleEnum.ADMIN.value, RoleEnum.TAX_ACCOUNTANT.value]:
            return {"message": "You are not authorized to perform this action"}, 401
        return f(*args, **kwargs)
    return decorated