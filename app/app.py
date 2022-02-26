from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)
bcrypt = Bcrypt(app)


@app.route("/")
def home():
        return {"message": "server is up and running, go to /docs for api"}