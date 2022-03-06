from flask_restx import fields
from . import taxEnum
class StateOfTax(fields.Raw):
    def format(self, value):
        return taxEnum(value).name
 

date_modified_schema = {
    "id": fields.String(required=True, description="User id",attribute='id'),
    "username": fields.String(required=True, description="Username",attribute='username'),
    "date_modified": fields.DateTime(required=True, description="Date modified",attribute='date_modified'),
    "due": fields.String(required=True, description="Due",attribute='total_due')
}

date_modified_payers_schema = {
    "tax_payers": fields.List(fields.Nested(date_modified_schema)),
}

state_of_tax_schema = {
    "id": fields.String(required=True, description="User id",attribute='id'),
    "username": fields.String(required=True, description="Username",attribute='username'),
    "state_of_tax": StateOfTax(required=True, description="State of tax",attribute='tax_status'),
    "due": fields.String(required=True, description="Due",attribute='total_due')
}

state_of_tax_payers_schema = {
    "tax_payers": fields.List(fields.Nested(state_of_tax_schema)),
}

date_created_schema = {
    "id": fields.String(required=True, description="User id",attribute='id'),
    "username": fields.String(required=True, description="Username",attribute='username'),
    "date_created": fields.DateTime(required=True, description="Date created",attribute='user_date_created'),
    "due": fields.String(required=True, description="Due",attribute='total_due')
}

date_created_payers_schema = {
    "tax_payers": fields.List(fields.Nested(date_created_schema)),
}

self_tax_payer_schema = {
    "id": fields.String(required=True, description="User id",attribute='id'),
    "username": fields.String(required=True, description="Username",attribute='username'),
    "state_of_tax": StateOfTax(required=True, description="State of tax",attribute='tax_status'),
    "due": fields.String(required=True, description="Due",attribute='total_due')
}
self_tax_payers_schema= {
    "tax_payers": fields.List(fields.Nested(self_tax_payer_schema)),
}