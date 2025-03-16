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
import random
from app import mongo  # Ensure your database connection is imported


#  Connect to MongoDB Atlas
client = MongoClient(Config.MONGO_URI)
db = client["divine"]  # Replace with your actual database name

#  User Model (users collection, compatible with Flask-Login)
class User(UserMixin):
    def __init__(self, username, email, name, surname, role="Customer", password=None, 
                 _id=None, created_at=None, password_hash=None, session_version=None):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.role = role
        self.created_at = created_at if created_at else datetime.utcnow()  # Ensure correct handling of MongoDB field
        self.password_hash = password_hash  # Ensure password_hash is set if loaded from MongoDB
        self.session_version = session_version or str(ObjectId())  # Ensure session_version exists
        self._id = str(ObjectId(_id)) if _id else str(ObjectId())  # Ensure _id is an ObjectId

        if password and not password_hash:
            self.set_password(password)  # Only hash password if it's newly set

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.session_version = str(ObjectId()) # Change session version to force logout of old sessions

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
    def find_by_id(order_id):
        """Find an order by MongoDB _id or guest_order_id"""
        try:
            # If order_id is a valid ObjectId, search by `_id`
            if ObjectId.is_valid(order_id):
                order_data = mongo.db.orders.find_one({"_id": ObjectId(order_id)})
            else:
                # If not an ObjectId, search by `guest_order_id`
                order_data = mongo.db.orders.find_one({"guest_order_id": order_id})
            
            return Order(**order_data) if order_data else None
        except Exception as e:
            print(f"Error finding order: {e}")
            return None
        
    @staticmethod
    def find_by_email(email):
        """Find a user by email and return a `User` object instead of a dictionary."""
        user_data = mongo.db.users.find_one({"email": email})
        
        if user_data:
            return User(
                username=user_data.get("username"),
                email=user_data.get("email"),
                name=user_data.get("name"),
                surname=user_data.get("surname"),
                role=user_data.get("role", "Customer"),
                password_hash=user_data.get("password_hash"),  # Ensure we set the hash properly
                _id=user_data.get("_id"),
                created_at=user_data.get("created_at")
            )
        return None  # Return None if no user found


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

class Order:
    def __init__(self, total_price, items, user_id=None, guest_email=None, guest_order_id=None, user_order_id=None, status="Pending", created_at=None, _id=None):
        if not user_id and not guest_email:
            raise ValueError("Either user_id or guest_email must be provided")

        self.user_id = ObjectId(user_id) if user_id and ObjectId.is_valid(user_id) else None  # Ensure user_id is valid
        self.guest_email = guest_email  # Guest user email
        self.total_price = total_price
        self.status = status  # 'Pending', 'Completed', 'Canceled'
        self.created_at = created_at if created_at else datetime.utcnow()
        self.items = items  # List of purchased items
        self._id = ObjectId(_id) if _id and ObjectId.is_valid(_id) else ObjectId()

        # Fix: Store Tracking Number for Both Guest & User Orders
        self.guest_order_id = guest_order_id if guest_order_id else (
            f"GUEST-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))}" if guest_email else None
        )
        self.user_order_id = user_order_id if user_order_id else (
            f"USER-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))}" if user_id else None
        )

    def save(self):
        """Save the order to MongoDB"""
        mongo.db.orders.update_one({"_id": self._id}, {"$set": self.to_dict()}, upsert=True)

    def to_dict(self):
        """Convert order object to dictionary for JSON response"""
        return {
            "_id": str(self._id),
            "user_id": str(self.user_id) if self.user_id else None,
            "guest_email": self.guest_email,
            "guest_order_id": self.guest_order_id,  # Guest tracking number
            "user_order_id": self.user_order_id,    # User tracking number
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at,
            "items": self.items
        }

    @staticmethod
    def find_by_id(order_id):
        """Find an order by MongoDB _id, guest_order_id, or user_order_id"""
        try:
            order_data = mongo.db.orders.find_one(
                {"$or": [{"_id": ObjectId(order_id)}, {"guest_order_id": order_id}, {"user_order_id": order_id}]}
            )
            return Order(**order_data) if order_data else None
        except Exception as e:
            print(f"Error finding order: {e}")
            return None

    @staticmethod
    def find_by_user(user_id):
        """Find all orders of a registered user"""
        if not ObjectId.is_valid(user_id):
            return []  # Prevent invalid ObjectId errors
        orders = mongo.db.orders.find({"user_id": ObjectId(user_id)})
        return [Order(**order) for order in orders]

    @staticmethod
    def find_by_guest_email(email):
        """Find orders made by a guest (email-based lookup)"""
        orders = mongo.db.orders.find({"guest_email": email})
        return [Order(**order) for order in orders]

    def update_status(self, new_status):
        """Update order status"""
        self.status = new_status
        mongo.db.orders.update_one({"_id": self._id}, {"$set": {"status": new_status}})

    @staticmethod
    def delete_by_id(order_id):
        """Delete an order by ID, guest_order_id, or user_order_id"""
        try:
            result = mongo.db.orders.delete_one(
                {"$or": [{"_id": ObjectId(order_id)}, {"guest_order_id": order_id}, {"user_order_id": order_id}]}
            )
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting order: {e}")
            return False
