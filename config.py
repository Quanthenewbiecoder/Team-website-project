import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    
    # MySQL database credentials
    user = os.environ.get('DB_USER', 'Nas')
    password = os.environ.get('DB_PASSWORD', 'Database8080')
    host = os.environ.get('DB_HOST', '10.76.4.182')
    db_name = os.environ.get('DB_NAME', 'team')
    SQLALCHEMY_DATABASE_URI = f'mysql://{user}:{quote_plus(password)}@{host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False