from app import db

# Define your models here
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class PriceTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(db.DateTime, nullable=False)
    update_count = db.Column(db.Integer, default=0)
