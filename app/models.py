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
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp when created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # Timestamp for updates
    user_role = db.Column(db.String(50), nullable=False, default='user')  # Possible values: 'admin', 'staff', 'user'

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
    product_type = db.Column(db.String(50), nullable=False)  # e.g., Necklace, Ring
    SKU = db.Column(db.String(100), unique=True, nullable=False)  # Unique identifier for each product
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp when created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # Timestamp for updates

    customizations = db.relationship('CustomizationOption', backref='product', lazy=True)
    care_instructions = db.relationship('CareInstruction', backref='product', lazy=True)
    sizes = db.relationship('ProductSize', backref='product', lazy=True)  # Link to sizes


class ProductSize(db.Model):
    __tablename__ = 'product_sizes'

    size_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    size_name = db.Column(db.String(50), nullable=False)  # Size description (e.g., "Small", "16 inches")
    size_value = db.Column(db.String(50), nullable=True)  # Numeric value if needed (e.g., "18")
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)  # Optional: Track quantity by size
    additional_price = db.Column(db.Numeric(10, 2), nullable=True)  # Optional: Price difference for size variations


class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class ProductTag(db.Model):
    __tablename__ = 'product_tags'
    product_tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)


class Bundle(db.Model):
    __tablename__ = 'bundles'
    bundle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    discount_percentage = db.Column(db.Numeric(5, 2))  # Optional: discount for the bundle

class BundleItem(db.Model):
    __tablename__ = 'bundle_items'
    bundle_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bundle_id = db.Column(db.Integer, db.ForeignKey('bundles.bundle_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Timestamp when created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # Timestamp for updates

    items = db.relationship('BasketItem', backref='basket', lazy=True)


class BasketItem(db.Model):
    __tablename__ = 'basket_items'

    basket_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.basket_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)


class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    wishlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    items = db.relationship('WishlistItem', backref='wishlist', lazy=True)

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'
    wishlist_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.wishlist_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # Foreign key to Discount table for order-level discounts
    discount_id = db.Column(db.Integer, db.ForeignKey('discounts.discount_id'), nullable=True)
    
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


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255))
    address = db.Column(db.String(255))

class ProductInventory(db.Model):
    __tablename__ = 'product_inventory'
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    restock_date = db.Column(db.DateTime)
    

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
    
    # Type of discount, e.g., 'Percentage' or 'Flat'
    discount_type = db.Column(db.String(50), nullable=False, default="Percentage")
    
    # Discount amounts
    percentage = db.Column(db.Numeric(5, 2), nullable=True)   # For percentage-based discounts (e.g., 10.00 for 10%)
    flat_amount = db.Column(db.Numeric(10, 2), nullable=True)  # For flat discounts (e.g., $10.00)

    # Validity and restrictions
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    minimum_purchase = db.Column(db.Numeric(10, 2), nullable=True)  # Minimum amount required to apply discount
    usage_limit = db.Column(db.Integer, default=None)  # Max number of times discount can be used overall
    usage_per_user = db.Column(db.Integer, default=None)  # Max number of times per user

    # Scope of applicability
    applicable_to_order = db.Column(db.Boolean, default=True)  # True if discount applies to the whole order
    applicable_to_product = db.Column(db.Boolean, default=False)  # True if discount applies to specific products
    applicable_category = db.Column(db.String(50), nullable=True)  # Optional: category this discount applies to

    # Relationships
    orders = db.relationship('Order', backref='discount', lazy=True)  # Order-level relationship
    products = db.relationship('Product', backref='discount', lazy=True)  # Product-level relationship


class Invoice(db.Model):
    __tablename__ = 'invoices'

    invoice_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid = db.Column(db.Boolean, default=False)

    order = db.relationship('Order', backref='invoice')