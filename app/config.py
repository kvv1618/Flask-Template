import os

from dotenv import load_dotenv

load_dotenv()

class config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")