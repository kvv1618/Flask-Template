from flask_restx import reqparse

def get_signup_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username cannot be blank', location='json')
    parser.add_argument('password', type=str, required=True, help='Password cannot be blank', location='json')
    parser.add_argument('role', type=str, required=True, help='Role cannot be blank', location='json')
    return parser

def get_login_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username cannot be blank', location='json')
    parser.add_argument('password', type=str, required=True, help='Password cannot be blank', location='json')
    return parser