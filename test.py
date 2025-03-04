from pymongo import MongoClient
from config import Config

try:
    client = MongoClient(Config.MONGO_URI)
    db = client.get_database()  # Connect to your default database
    print("✅ MongoDB Connection Successful! Available Collections:", db.list_collection_names())
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
