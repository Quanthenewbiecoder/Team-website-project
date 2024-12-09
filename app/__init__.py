from flask import Flask
from app.extensions import db, login_manager, migrate
from config import Config  # Adjusted import path

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Login view
    login_manager.login_view = 'routes.login'

    # Import and register blueprints
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    # Import models
    with app.app_context():
        from app.models import User
        db.create_all()

    return app
