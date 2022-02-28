from flask_restx import fields

tax_payer_schema = {
    "id": fields.String(required=True, description="User id"),
    "username": fields.String(required=True, description="Username")
}

tax_payers_schema = {
    "tax_payers": fields.List(fields.Nested(tax_payer_schema)),
}
