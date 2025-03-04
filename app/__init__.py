from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config

#  Initialize Flask extensions
mongo = PyMongo()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #  Initialize MongoDB
    mongo.init_app(app)

    #  Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    #  Load user from MongoDB for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.get(user_id)

    #  Register Blueprints (Routes)
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
