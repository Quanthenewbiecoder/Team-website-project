from pymongo import MongoClient
from config import Config  # Ensure this has MONGO_URI

# ✅ Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client["divine"]  # Your database name
products_collection = db["products"]

# ✅ Update all image URLs to replace spaces with underscores
update_result = products_collection.update_many(
    {"image_url": {"$regex": " "}},  # Find image URLs containing spaces
    [{"$set": {"image_url": {"$replaceAll": {"input": "$image_url", "find": " ", "replacement": "_"}}}}]
)

print(f"✅ Updated {update_result.modified_count} products in MongoDB")
