from datetime import datetime
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

def get_tax_payer_details_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Tax Payer ID cannot be blank', location='json')
    parser.add_argument('pan_number', type=str, required=True, help='PAN number cannot be blank', location='json')
    parser.add_argument('base_value_forGST', type=int, required=True, help='Base value cannot be blank', location='json')
    parser.add_argument('profit_forIncomeTax', type=int, required=True, help='Profit cannot be blank', location='json')
    parser.add_argument('state', type=str, required=True, help='State cannot be blank', location='json')
    parser.add_argument('status', type=str, required=True, help='Status cannot be blank', location='json')
    parser.add_argument('due_date', type=str, required=True, help='Due date cannot be blank', location='json')
    return parser