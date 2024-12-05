import os
from urllib.parse import quote_plus

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://Team:Database8080@localhost/cs2team20_divine_jewelry'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'SecretKey'