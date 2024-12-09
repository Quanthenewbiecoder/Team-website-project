import os
from urllib.parse import quote_plus

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'divine.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
