from flask_restx import Api

from .auth import api as auth_namespace
from .tax_payers import api as tax_payers_namespace
from .view_tax_payers import api as viewing_tax_payers_namespace

api = Api(
    title="RedCarpet API",
    version="1.0",
    description="API for RedCarpet Assignment",
    doc="/docs",
    prefix="/api/v1",
    authorizations={
        "Access Token": {
            "type": "apiKey",
            "in": "header",
            "name": "accessToken",
        },
    },
)

api.add_namespace(auth_namespace)
api.add_namespace(tax_payers_namespace)
api.add_namespace(viewing_tax_payers_namespace)