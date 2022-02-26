from flask_restx import Api

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
