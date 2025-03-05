from app import db
from app.models import Product
from app import create_app

app = create_app()

with app.app_context():
    products = [
        Product(
            name="Crystal Bracelet",
            type="Bracelets",
            price=49.99,
            image_url="Images/crystal_bracelet.jpg",
            collection="Crystal",
            description="A beautiful crystal bracelet to enhance your style.",
            in_stock=True
        ),
        Product(
            name="Leaf Earrings",
            type="Earrings",
            price=29.99,
            image_url="Images/leaf_earring_1.jpg",
            collection="Leaf",
            description="Elegant leaf-shaped earrings with a modern design.",
            in_stock=True
        ),
        Product(
            name="Pearl Ring",
            type="Rings",
            price=99.99,
            image_url="Images/pearl ring 1.webp",
            collection="Pearl",
            description="A classic pearl ring with a timeless design.",
            in_stock=True
        ),
        Product(
            name="Luxury Watch",
            type="Watches",
            price=199.99,
            image_url="Images/Watch3.jpg",
            collection=None,
            description="A luxury watch for every occasion.",
            in_stock=False
        ),
        Product(
            name="Leaf Necklace",
            type="Necklaces",
            price=79.99,
            image_url="Images/leaf necklace 3.webp",
            collection="Leaf",
            description="A delicate necklace inspired by nature.",
            in_stock=True
        ),
    ]

    db.session.add_all(products)
    db.session.commit()
    print("Products added successfully!")
