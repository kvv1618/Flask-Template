from flask_migrate import Migrate
from flask_restx import Resource

from app import app, config, db
from app.models import *
from app.routes import api

api.init_app(app)
migrate = Migrate(app, db, compare_type=True, compare_server_default=True)

@api.route("/info")
class Info(Resource):
    def get(self):
        return {"message": "RedCarpet API"}

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)