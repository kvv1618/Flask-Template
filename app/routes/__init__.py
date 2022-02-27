from flask_restx import Api

from .auth import api as auth_namespace

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