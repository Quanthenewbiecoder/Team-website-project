from app import app, db
from models import User, Product, Collection, Order, OrderDetails  # Import models

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
