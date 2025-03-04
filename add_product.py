from pymongo import MongoClient
from config import Config  # Ensure Config has MONGO_URI
from bson.objectid import ObjectId

# ✅ Connect to MongoDB Atlas
client = MongoClient(Config.MONGO_URI)
db = client["divine"]  # Use your actual database name
products_collection = db["products"]  # Collection name

# ✅ Product data converted from SQL
products = [
    {"_id": ObjectId(), "name": "Crystal Bracelet", "type": "Bracelets", "price": 49.99, "image_url": "images/crystal_bracelet.jpg", "collection": "Crystal", "description": "A beautiful crystal bracelet to enhance your style.", "in_stock": True},
    {"_id": ObjectId(), "name": "Leaf Earrings", "type": "Earrings", "price": 29.99, "image_url": "images/leaf_earring_1.jpg", "collection": "Leaf", "description": "Elegant leaf-shaped earrings with a modern design.", "in_stock": True},
    {"_id": ObjectId(), "name": "Pearl Ring", "type": "Rings", "price": 99.99, "image_url": "images/pearl_ring_1.webp", "collection": "Pearl", "description": "A classic pearl ring with a timeless design.", "in_stock": True},
    {"_id": ObjectId(), "name": "Luxury Watch", "type": "Watches", "price": 199.99, "image_url": "images/Watch3.jpg", "collection": None, "description": "A luxury watch for every occasion.", "in_stock": False},
    {"_id": ObjectId(), "name": "Leaf Necklace", "type": "Necklaces", "price": 79.99, "image_url": "images/leaf_necklace_3.webp", "collection": "Leaf", "description": "A delicate necklace inspired by nature.", "in_stock": True},
    {"_id": ObjectId(), "name": "Crystal Ring", "type": "Rings", "price": 119.99, "image_url": "images/crystal_ring_1.jpg", "collection": "Crystal", "description": "Exquisite crystal ring designed to catch the light with every angle.", "in_stock": True},
    {"_id": ObjectId(), "name": "Crystal Necklace", "type": "Necklaces", "price": 249.99, "image_url": "images/crystal_necklace_1.jpg", "collection": "Crystal", "description": "Elegant crystal necklace that adds sparkle to any outfit.", "in_stock": True},
    {"_id": ObjectId(), "name": "Leaf Ring", "type": "Rings", "price": 149.99, "image_url": "images/leaf_ring_1.webp", "collection": "Leaf", "description": "Elegant leaf design to enhance your style. Crafted with precision and care.", "in_stock": False},
    {"_id": ObjectId(), "name": "Leaf Bracelet", "type": "Bracelets", "price": 135.00, "image_url": "images/leaf_bracelet_1.webp", "collection": "Leaf", "description": "Beautiful bracelet designed with a delicate leaf motif to add elegance to your wrist.", "in_stock": True},
    {"_id": ObjectId(), "name": "Pearl Necklace", "type": "Necklaces", "price": 249.99, "image_url": "images/pearl_necklace_2.webp", "collection": "Pearl", "description": "A stunning necklace featuring lustrous pearls for an elegant look.", "in_stock": True},
    {"_id": ObjectId(), "name": "Pearl Earring", "type": "Earrings", "price": 180.00, "image_url": "images/pearl_earring_1.avif", "collection": "Pearl", "description": "Elegant pearl earrings that add a touch of sophistication to your look.", "in_stock": True},
    {"_id": ObjectId(), "name": "Pearl Bracelet", "type": "Bracelets", "price": 175.00, "image_url": "images/pearl_bracelet_1.jpg", "collection": "Pearl", "description": "A beautiful pearl bracelet, perfect for adding elegance to your wrist.", "in_stock": True},
    {"_id": ObjectId(), "name": "Titanium Horizon", "type": "Watches", "price": 449.99, "image_url": "images/Watch6.jpg", "description": "Premium titanium watch with precision mechanics and elegant design.", "in_stock": True},
    {"_id": ObjectId(), "name": "Timeless Triumph", "type": "Watches", "price": 549.99, "image_url": "images/Watch5.jpg", "description": "Beautiful blend of silver and brass watch with precision design.", "in_stock": True},
    {"_id": ObjectId(), "name": "Royal Reverie", "type": "Watches", "price": 749.99, "image_url": "images/Watch4.jpg", "description": "Beautiful blend of silver and brass made with exquisite care.", "in_stock": True},
    {"_id": ObjectId(), "name": "Phantom Contrast", "type": "Watches", "price": 249.99, "image_url": "images/Watch1.jpg", "description": "Simplistic yet elegant design with a dual-tone aesthetic.", "in_stock": False},
    {"_id": ObjectId(), "name": "Slow and Serene", "type": "Necklaces", "price": 149.99, "image_url": "images/Necklace1.webp", "description": "A natural themed necklace that looks both stylish and simple.", "in_stock": True},
    {"_id": ObjectId(), "name": "Summit Memories", "type": "Necklaces", "price": 250.00, "image_url": "images/Necklace2.webp", "description": "The style of the alps wrapped around your neck.", "in_stock": True},
    {"_id": ObjectId(), "name": "Ocean Whispers", "type": "Necklaces", "price": 299.99, "image_url": "images/Necklace3.webp", "description": "Experience the ocean breeze within the comfort of your own home.", "in_stock": True},
    {"_id": ObjectId(), "name": "Crystal Canopy", "type": "Necklaces", "price": 499.99, "image_url": "images/Necklace4.jpg", "description": "Enrich your life with the gleam of this crystalline pendant.", "in_stock": False},
    {"_id": ObjectId(), "name": "Radiant Circlet", "type": "Bracelets", "price": 599.99, "image_url": "images/Bracelet1.jpg", "description": "Bracelets plated with shimmering gold.", "in_stock": True},
    {"_id": ObjectId(), "name": "Luminous Whisper", "type": "Bracelets", "price": 499.99, "image_url": "images/Bracelet2.jpg", "description": "A symphony of elegance and understated brilliance.", "in_stock": True},
    {"_id": ObjectId(), "name": "Roman Bracers", "type": "Bracelets", "price": 399.99, "image_url": "images/Bracelet3.webp", "description": "A perfect blend of classic sophistication and modern design.", "in_stock": True},
    {"_id": ObjectId(), "name": "Alchemist's Gem", "type": "Earrings", "price": 249.99, "image_url": "images/Earrings1.jpg", "description": "A striking blend of bold elegance and timeless allure.", "in_stock": True},
    {"_id": ObjectId(), "name": "Teardrop Elegance", "type": "Earrings", "price": 179.99, "image_url": "images/Earrings2.jpg", "description": "A perfect blend of sophistication and modern design.", "in_stock": False},
    {"_id": ObjectId(), "name": "Celestial Harmony", "type": "Earrings", "price": 129.99, "image_url": "images/Earrings3.jpg", "description": "Delicately crafted crescent moons, made from premium silver that captures the ethereal glow of moonlight.", "in_stock": True},
    {"_id": ObjectId(), "name": "Eternal Night", "type": "Rings", "price": 119.99, "image_url": "images/Ring1.webp", "description": "A seamless blend of rich black and radiant gold.", "in_stock": True},
    {"_id": ObjectId(), "name": "Molten Mirage", "type": "Rings", "price": 169.99, "image_url": "images/Ring2.jpg", "description": "A mesmerizing blend of fiery intensity and sleek sophistication.", "in_stock": True},
    {"_id": ObjectId(), "name": "Steel Symphony", "type": "Rings", "price": 89.99, "image_url": "images/Ring3.jpg", "description": "A shining steel testament to strength and artistry.", "in_stock": False},
]

# ✅ Insert into MongoDB
products_collection.insert_many(products)
print(f"✅ Successfully imported {len(products)} products into MongoDB!")
