from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profile_picture = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    baskets = db.relationship('Basket', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)


class Address(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    address_type = db.Column(db.String(50), nullable=False)  # e.g., 'Shipping', 'Billing'
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    material = db.Column(db.String(50))
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    customizations = db.relationship('CustomizationOption', backref='product', lazy=True)
    care_instructions = db.relationship('CareInstruction', backref='product', lazy=True)


class CustomizationOption(db.Model):
    __tablename__ = 'customization_options'

    customization_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    option_type = db.Column(db.String(50), nullable=False)
    option_value = db.Column(db.String(50), nullable=False)
    additional_price = db.Column(db.Numeric(10, 2))

class Basket(db.Model):
    __tablename__ = 'baskets'

    basket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    items = db.relationship('BasketItem', backref='basket', lazy=True)


class BasketItem(db.Model):
    __tablename__ = 'basket_items'

    basket_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.basket_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')

    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)


class CareInstruction(db.Model):
    __tablename__ = 'care_instructions'

    instruction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    care_instruction = db.Column(db.Text, nullable=False)


class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., 'Credit Card', 'Direct Debit'
    billing_address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    payment_status = db.Column(db.String(50), default='Pending')
    transaction_id = db.Column(db.String(255), unique=True, nullable=False)
    payment_reference = db.Column(db.String(255), unique=True)  # reference from payment gateway

    billing_address = db.relationship('Address', foreign_keys=[billing_address_id])


class Discount(db.Model):
    __tablename__ = 'discounts'

    discount_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    percentage = db.Column(db.Numeric(5, 2), nullable=False)  # e.g., 10.00 for 10%
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    minimum_purchase = db.Column(db.Numeric(10, 2))
