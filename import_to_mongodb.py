from pymongo import MongoClient
import json
import os
from config import Config

# ✅ Connect to MongoDB Atlas
client = MongoClient(Config.MONGO_URI)
db = client["divine"]  # Ensure database name matches MongoDB Atlas

# ✅ List of tables to create in MongoDB
tables = [
    "user", "product", "order", "order_item",
    "news", "price_history", "price_table",
    "review", "table_update_log"
]

# ✅ Ensure each collection exists
for table in tables:
    if table not in db.list_collection_names():
        db.create_collection(table)
        print(f"✅ Created empty collection: {table}")

# ✅ Import JSON files into MongoDB collections
for table in tables:
    file_path = f"{table}.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list) and len(data) > 0:  # Ensure data is a list and not empty
            db[table].insert_many(data)
            print(f"✅ Imported {len(data)} records into {table} collection")
        else:
            print(f"⚠️ Skipping {table} - JSON file is empty but collection exists")
    else:
        print(f"⚠️ Skipping {table} - No JSON file found, but collection exists")
