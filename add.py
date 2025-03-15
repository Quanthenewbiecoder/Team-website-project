from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from config import Config  # Ensure this contains your MongoDB URI
from datetime import datetime

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client["divine"]  # Change to your actual database name
users_collection = db["users"]

# Admin user details
admin_user = {
    "username": "admin",
    "email": "admin@divine.com",
    "name": "Admin",
    "surname": "User",
    "role": "admin",  # Ensure this matches the role_required decorator in routes
    "password_hash": generate_password_hash("Admin123!"),  # Change password as needed
    "created_at": datetime.utcnow()
}

# Check if the admin already exists
existing_admin = users_collection.find_one({"email": admin_user["email"]})

if not existing_admin:
    result = users_collection.insert_one(admin_user)
    print(f"Admin account created! ID: {result.inserted_id}")
else:
    print("Admin account already exists.")
