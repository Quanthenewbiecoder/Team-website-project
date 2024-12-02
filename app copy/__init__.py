from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create Flask application
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize database and migrations
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
