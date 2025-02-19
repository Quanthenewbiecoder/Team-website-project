import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    
    # SQLite database path
    db_path = os.environ.get('DB_PATH', os.path.join(os.getcwd(), 'divine.db'))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False