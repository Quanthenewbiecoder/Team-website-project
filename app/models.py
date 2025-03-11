from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson import ObjectId
from config import Config
from app.database import db, products_collection  # Import MongoDB connection
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bson import ObjectId
from app.database import subscriptions_collection

#  Connect to MongoDB Atlas
client = MongoClient(Config.MONGO_URI)
db = client["divine"]  # Replace with your actual database name

#  User Model (users collection, compatible with Flask-Login)
class User(UserMixin):
    def __init__(self, username, email, name, surname, role="Customer", password=None, _id=None, created_at=None, password_hash=None):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.role = role
        self.created_at = created_at if created_at else datetime.utcnow()  #  Ensure correct handling of MongoDB field
        self.password_hash = password_hash  #  Ensure password_hash is set if loaded from MongoDB
        self._id = ObjectId(_id) if _id else ObjectId()  #  Ensure _id is an ObjectId

        if password and not password_hash:
            self.set_password(password)  #  Only hash password if it's newly set

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self._id)  # Flask-Login requires a string ID

    def save(self):
        """Save user to MongoDB"""
        db.users.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

    @staticmethod
    def get(user_id):
        """Fetch a user by _id"""
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        return User(**user_data) if user_data else None

    @staticmethod
    def find_by_email(email):
        """Find user by email for authentication"""
        user_data = db.users.find_one({"email": email})
        return User(**user_data) if user_data else None

    def delete(self):
        """Delete user from MongoDB"""
        db.users.delete_one({"_id": self._id})

#  PriceTable Model (price_table collection)
class PriceTable:
    def __init__(self):
        self.update_count = 0
        self.last_updated = datetime.utcnow()

    def update_table(self):
        self.update_count += 1
        self.last_updated = datetime.utcnow()

    def save(self):
        """Save to MongoDB"""
        db.price_table.update_one({}, {"$set": self.__dict__}, upsert=True)

#  TableUpdateLog Model (table_update_log collection)
class TableUpdateLog:
    def __init__(self, update_count):
        self.update_count = update_count
        self.updated_at = datetime.utcnow()

    def save(self):
        """Save to MongoDB"""
        db.table_update_log.insert_one(self.__dict__)

#  PriceHistory Model (price_history collection)
class PriceHistory:
    def __init__(self, price_table_id, old_data):
        self.price_table_id = price_table_id
        self.old_data = old_data  # Store as a JSON string or dictionary
        self.updated_at = datetime.utcnow()

    def save(self):
        """Save to MongoDB"""
        db.price_history.insert_one(self.__dict__)

#  News Model (news collection)
class News:
    def __init__(self, title, content, _id=None):
        self.title = title
        self.content = content
        self.created_at = datetime.utcnow()
        self._id = ObjectId(_id) if _id else ObjectId()

    def save(self):
        """Save news to MongoDB"""
        db.news.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

    def delete(self):
        """Delete news from MongoDB"""
        db.news.delete_one({"_id": self._id})

    def __repr__(self):
        return f'<News {self.title}>'

#  Order Model (orders collection, with embedded order items)
class Order:
    def __init__(self, user_id, total_price, items=None, status="Pending", _id=None):
        self.user_id = user_id  # Reference to users
        self.total_price = total_price
        self.status = status  # 'Pending', 'Completed', 'Canceled'
        self.created_at = datetime.utcnow()
        self.items = items if items else []  #  Embedded list of order items
        self._id = ObjectId(_id) if _id else ObjectId()

    def add_item(self, product_name, quantity, price):
        self.items.append({"product_name": product_name, "quantity": quantity, "price": price})

    def save(self):
        """Save order to MongoDB"""
        db.orders.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

    @staticmethod
    def find_by_id(order_id):
        """Fetch order by _id"""
        order_data = db.orders.find_one({"_id": ObjectId(order_id)})
        return Order(**order_data) if order_data else None

    def delete(self):
        """Delete order from MongoDB"""
        db.orders.delete_one({"_id": self._id})


#  Product Model (products collection)
class Product:
    def __init__(self, name, product_type, price, image_url, collection=None, description="", in_stock=True, _id=None):
        self.name = name
        self.type = product_type
        self.price = price
        self.image_url = image_url.replace(" ", "_")  # Fix spaces in filenames
        self.collection = collection
        self.description = description
        self.in_stock = in_stock
        self._id = ObjectId(_id) if _id else ObjectId()

    def save(self):
        """Save product to MongoDB"""
        products_collection.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

    @staticmethod
    def find_by_id(product_id):
        """Fetch product by _id"""
        product_data = products_collection.find_one({"_id": ObjectId(product_id)})
        return Product(**product_data) if product_data else None

    def delete(self):
        """Delete product from MongoDB"""
        products_collection.delete_one({"_id": self._id})

    def __repr__(self):
        return f"<Product {self.name}>"

#  Review Model (reviews collection)
class Review:
    def __init__(self, product_id, user_id, review, rating, _id=None):
        self.product_id = product_id
        self.user_id = user_id
        self.review = review
        self.rating = rating
        self.created_at = datetime.utcnow()
        self._id = ObjectId(_id) if _id else ObjectId()

    def save(self):
        """Save review to MongoDB"""
        db.reviews.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

    @staticmethod
    def find_by_id(review_id):
        """Fetch review by _id"""
        review_data = db.reviews.find_one({"_id": ObjectId(review_id)})
        return Review(**review_data) if review_data else None

    def delete(self):
        """Delete review from MongoDB"""
        db.reviews.delete_one({"_id": self._id})



#Subscription part 
class Subscription:
    def __init__(self, email, _id=None):
        self.email = email
        self.subscribed_at = datetime.utcnow()
        self._id = ObjectId(_id) if _id else ObjectId()

    def save(self):
        """Save subscription to MongoDB"""
        subscriptions_collection.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

    @staticmethod
    def find_by_email(email):
        """Check if an email is already subscribed"""
        subscription = subscriptions_collection.find_one({"email": email})
        return Subscription(**subscription) if subscription else None

    @staticmethod
    def delete(email):
        """Remove subscription from MongoDB"""
        result = subscriptions_collection.delete_one({"email": email})
        return result.deleted_count > 0  # Returns True if deleted, False if not found