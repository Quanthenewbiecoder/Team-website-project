from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default="Customer", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password, name, surname, role=None):
        self.username = username
        self.email = email
        if password:  # Only hash if password is provided
            self.set_password(password)
            
        self.name = name
        self.surname = surname
        self.role = role if role else "Customer"  # Ensuring default role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Price table tracking models
class PriceTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    update_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def update_table(self):
        self.update_count += 1
        self.last_updated = datetime.utcnow()

class TableUpdateLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    update_count = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Price history model
class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price_table_id = db.Column(db.Integer, db.ForeignKey('price_table.id'), nullable=False)
    old_data = db.Column(db.Text, nullable=False)  # Store old table data as JSON
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# News model
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<News {self.title}>'

# Role validation helpers
class RoleValidation:
    @staticmethod
    def can_edit_data(user_role):
        return user_role in ['Owner', 'Staff']

    @staticmethod
    def can_change_role(user_role):
        return user_role == 'Owner'

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(50), default='Pending')  # 'Pending', 'Completed', 'Canceled'

    # Relationship to User
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

# Order Item Model
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Relationship to Order
    order = db.relationship('Order', backref=db.backref('items', lazy=True))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., "Bracelets", "Earrings"
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    collection = db.Column(db.String(50), nullable=True)  # e.g., "Leaf", "Pearl"
    description = db.Column(db.Text, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Product {self.name}>"
