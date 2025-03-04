# app/database.py

from pymongo import MongoClient
from config import Config  # Ensure Config has MONGO_URI

# ✅ Connect to MongoDB Atlas
client = MongoClient(Config.MONGO_URI)
db = client["divine"]  # ✅ Your database name is "divine"

# ✅ Define collections
products_collection = db["products"]
users_collection = db["users"]
orders_collection = db["orders"]
reviews_collection = db["reviews"]
