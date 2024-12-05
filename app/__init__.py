from flask import Flask
from app.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///divine.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize plugins
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    # Import User model after db is defined
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app