from functools import wraps
from datetime import datetime 
import random
import string
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import mongo
from app.models import *
from app.forms import *


# Create blueprint
routes_bp = Blueprint('routes', __name__)

# Role-based access control decorator
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('routes.login'))
            if current_user.role not in roles:
                flash("Access denied.", "danger")
                return redirect(url_for('routes.home'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@routes_bp.context_processor
def utility_processor():
    return dict(now=datetime.now())

# General Pages
@routes_bp.route('/')
def home():
    return render_template('homepage.html', now=datetime.now())

# Authentication Routes
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.find_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('routes.home'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html', now=datetime.now())

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('routes.home'))

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        existing_username = mongo.db.users.find_one({"username": form.username.data})
        if existing_username:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('routes.register'))

        existing_email = mongo.db.users.find_one({"email": form.email.data})
        if existing_email:
            flash("Email already registered. Please use a different email or log in.", "error")
            return redirect(url_for('routes.register'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            role='Customer',
            password=form.password.data
        )

        mongo.db.users.insert_one(new_user.__dict__)
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html', form=form)

@routes_bp.route('/order-replacement', methods=['GET', 'POST'])
@login_required
def order_replacement():
    return render_template('order-replacement.html')

@routes_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')

@routes_bp.route('/password_change', methods=['GET', 'POST'])
@login_required
def password_change():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        if not current_user.check_password(current_password):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('routes.password_change'))

        current_user.set_password(new_password)
        db.session.commit()

        flash("Password successfully updated!", "success")
        return redirect(url_for('routes.home'))

    return render_template('password_change.html')

@routes_bp.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@routes_bp.route('/contact')
def contact():
    return render_template('contact.html')

@routes_bp.route('/crystalcollection')
def crystalcollection():
    try:
        return render_template('crystalcollection.html', now=datetime.now())
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return f"Error: {str(e)}", 500

# Route to display all products or a single product
@routes_bp.route('/products/', defaults={'product_id': None}, methods=['GET'])
@routes_bp.route('/products/<string:product_id>', methods=['GET'])
def products(product_id):
    if product_id is None:
        all_products = list(mongo.db.products.find())
        return render_template('all_products.html', products=all_products, now=datetime.now())

    product = mongo.db.products.find_one({"_id": product_id})
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('routes.products'))

    product_reviews = list(mongo.db.reviews.find({"product_id": product_id}))

    return render_template('products.html', product=product, reviews=product_reviews)

# API Route to fetch all products
@routes_bp.route('/api/products', methods=['GET'])
def api_products():
    products = list(mongo.db.products.find())

    product_list = [{
        "id": str(product["_id"]),
        "name": product["name"],
        "type": product["type"],
        "price": product["price"],
        "image_url": url_for('static', filename=f'Images/{product["image_url"].split("/")[-1]}'),
        "collection": product.get("collection", "None"),
        "description": product["description"],
        "in_stock": bool(product["in_stock"])
    } for product in products]

    return jsonify(product_list)

# Route to add or edit a review (User can only post one review per product)
@routes_bp.route('/products/<int:product_id>/review', methods=['POST'])
@login_required  #  Ensures only logged-in users can access
def add_review(product_id):
    product = mongo.db.products.find_one({"_id": product_id})
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('routes.products', product_id=product_id))

    review_text = request.form.get('review')
    rating = request.form.get('rating')

    if not review_text or not rating:
        flash('Review and rating are required.', 'error')
        return redirect(url_for('routes.products', product_id=product_id))

    rating = int(rating)
    if rating < 1 or rating > 5:
        flash("Rating must be between 1 and 5.", "error")
        return redirect(url_for('routes.products', product_id=product_id))

    existing_review = mongo.db.reviews.find_one({"product_id": product_id, "user_id": current_user.get_id()})
    if existing_review:
        mongo.db.reviews.update_one(
            {"_id": existing_review["_id"]},
            {"$set": {"review": review_text, "rating": rating, "created_at": datetime.utcnow()}}
        )
        flash('Review updated successfully!', 'success')
    else:
        mongo.db.reviews.insert_one({
            "product_id": product_id,
            "user_id": current_user.get_id(),
            "review": review_text,
            "rating": rating,
            "created_at": datetime.utcnow()
        })
        flash('Review added successfully!', 'success')

    return redirect(url_for('routes.products', product_id=product_id))

# Route to delete a review (Allows user to review again after deleting)
@routes_bp.route('/products/<int:product_id>/review/delete', methods=['POST'])
@login_required  #  Ensures only logged-in users can delete reviews
def delete_review(product_id):
    mongo.db.reviews.delete_one({"product_id": product_id, "user_id": current_user.get_id()})
    flash("Your review has been deleted.", "success")
    return redirect(url_for('routes.products', product_id=product_id))


# API Route to fetch reviews for a product
@routes_bp.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def api_reviews(product_id):
    product = Product.query.get_or_404(product_id)
    product_reviews = Review.query.filter_by(product_id=product.id).all()

    reviews_list = [{
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,  # Include user ID for frontend checks
        "review": review.review,
        "rating": review.rating,
        "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for review in product_reviews]

    return jsonify(reviews_list)


@routes_bp.route('/leafcollection')
def leafcollection():
    try:
        return render_template('leafcollection.html', now=datetime.now())
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return f"Error: {str(e)}", 500

@routes_bp.route('/pearlcollection')
def pearlcollection():
    try:
        return render_template('pearlcollection.html', now=datetime.now())
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return f"Error: {str(e)}", 500
    
    
@routes_bp.route('/product/<int:product_id>/care_instructions')
def product_care_instructions(product_id):
    return render_template('care_instructions.html', product_id=product_id)

# Basket Functionality
shopping_basket = {}

@routes_bp.route('/basket', methods=['GET'])
def basket():
    cart_items = []
    total_amount = 0

    if shopping_basket:
        for product_id, item in shopping_basket.items():
            product = mongo.db.products.find_one({"_id": product_id})
            if product:
                cart_items.append({
                    "id": product_id,
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": item["quantity"],
                    "total": product["price"] * item["quantity"]
                })
                total_amount += product["price"] * item["quantity"]

    return render_template('currentbasket.html', cart_items=cart_items, total_amount=total_amount)

@routes_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    cart_items = []
    total_amount = 0
    
    #  Extract shopping basket data
    if shopping_basket:
        for product_id, item in shopping_basket.items():
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 0))
            cart_items.append({
                'product_id': product_id,  #  Store product ID
                'name': item['product_name'],
                'quantity': quantity,
                'price': price,
                'total': price * quantity,
                'image': item.get('image', '')
            })
            total_amount += price * quantity

    if request.method == 'POST':
        if current_user.is_authenticated:
            #  Create a new order in MongoDB
            new_order = Order(
                user_id=current_user.get_id(),  #  MongoDB needs string ID
                total_price=total_amount,
                items=cart_items,  #  Embed items in order
                status='Pending'
            )
            result = mongo.db.orders.insert_one(new_order.__dict__)  #  Save to MongoDB
            order_id = str(result.inserted_id)  #  Convert ObjectId to string
        else:
            #  Guest order with random ID
            order_id = "GUEST-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            guest_order = {
                "user_id": "guest",
                "total_price": total_amount,
                "items": cart_items,
                "status": "Pending",
                "created_at": datetime.utcnow(),
                "guest_order_id": order_id
            }
            mongo.db.orders.insert_one(guest_order)  #  Save guest order to MongoDB

        #  Clear shopping basket
        shopping_basket.clear()
        
        #  Redirect to success page
        return redirect(url_for('routes.payment_success', order_id=order_id))

    return render_template('payment.html', cart_items=cart_items, total_amount=total_amount)


@routes_bp.route('/payment/success/<order_id>')
def payment_success(order_id):
    return render_template('payment.html', 
                           payment_status='success',
                           cart_items=[],
                           total_amount=0,
                           order_id=order_id,
                           now=datetime.now())


@routes_bp.route('/basket/add', methods=['POST'])
def add_to_basket():
    data = request.json
    product_id = str(data.get('product_id', ''))
    product_name = data.get('product_name')
    price = float(data.get('price', 0))
    quantity = int(data.get('quantity', 1))
    image = data.get('image', '')

    if product_id in shopping_basket:
        shopping_basket[product_id]['quantity'] += quantity
    else:
        shopping_basket[product_id] = {
            'product_name': product_name,
            'quantity': quantity,
            'price': price,
            'image': image
        }

    return jsonify({
        'message': 'Product added to basket',
        'basket': shopping_basket
    })

@routes_bp.route('/basket/update', methods=['POST'])
def update_basket():
    data = request.json
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if product_id in shopping_basket:
        shopping_basket[product_id]['quantity'] = quantity
        return jsonify({
            'message': 'Quantity updated',
            'basket': shopping_basket
        }), 200
    return jsonify({'error': 'Product not found'}), 404

@routes_bp.route('/basket/remove/<product_id>', methods=['DELETE'])
def remove_from_basket(product_id):
    if product_id in shopping_basket:
        del shopping_basket[product_id]
        return jsonify({
            'message': 'Product removed',
            'basket': shopping_basket
        }), 200
    return jsonify({'error': 'Product not found'}), 404

@routes_bp.route('/basket/clear', methods=['POST'])
def clear_basket():
    shopping_basket.clear()
    return jsonify({
        'message': 'Basket cleared',
        'basket': shopping_basket
    }), 200

from bson import ObjectId

@routes_bp.route('/order_confirmation/<order_id>')
def order_confirmation(order_id):
    #  Handle guest orders
    if order_id.startswith("GUEST-"):
        order = {
            "id": order_id,
            "status": "Processing",
            "created_at": datetime.now()
        }
        order_items = []
    else:
        #  Try fetching order from MongoDB
        try:
            order = mongo.db.orders.find_one({"_id": ObjectId(order_id)})  #  Fetch order
            if not order:
                flash("Order not found!", "danger")
                return redirect(url_for('routes.home'))
            
            order_items = order.get("items", [])  #  Get embedded order items
        except Exception:
            flash("Invalid order ID.", "danger")
            return redirect(url_for('routes.home'))

    return render_template('order_confirmation.html', order=order, order_items=order_items)

@routes_bp.route('/track_order/<order_id>')
def track_order(order_id):
    # Removed login_required decorator and handle guest orders
    # Check if it's a guest order
    if isinstance(order_id, str) and order_id.startswith("GUEST-"):
        # Create mock order for guests
        order = {
            "id": order_id,
            "status": "Processing",
            "created_at": datetime.now()
        }
    else:
        # For authenticated users
        try:
            order_id = int(order_id)
            if current_user.is_authenticated:
                order = mongo.db.orders.find_one({"_id": ObjectId(order_id), "user_id": current_user.get_id()})
                if not order:
                    flash('Order not found or access denied.', 'danger')
                    return redirect(url_for('routes.history'))
            else:
                flash('Order not found or access denied.', 'danger')
                return redirect(url_for('routes.home'))
        except ValueError:
            flash('Invalid order ID', 'danger')
            return redirect(url_for('routes.home'))
    
    return render_template('track_order.html', order=order)

@routes_bp.route('/history')
@login_required
def history():
    orders = list(mongo.db.orders.find({"user_id": current_user.get_id()}).sort("created_at", -1))
    return render_template('history.html', orders=orders)

# Reviews and Feedback
@routes_bp.route('/product/<int:product_id>/reviews')
def product_reviews(product_id):
    return render_template('product_reviews.html', product_id=product_id)

@routes_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    return render_template('feedback.html')

# Admin and Staff Routes
@routes_bp.route('/admin')
@login_required
@role_required('admin', 'staff')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@routes_bp.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'staff')
def add_product():
    return render_template('add_product.html')

@routes_bp.route('/admin/reports')
@login_required
@role_required('admin', 'staff')
def reports():
    return render_template('reports.html')

# Product Customization
@routes_bp.route('/product/<int:product_id>/customize', methods=['GET', 'POST'])
@login_required
def customize_product(product_id):
    return render_template('customize_product.html', product_id=product_id)

# Test Route
@routes_bp.route('/test')
def test():
    return "Test route working!"

# Payment
@routes_bp.route('/privacy_policy')
def privacy_policy():
    now = datetime.utcnow()
    return render_template('privacy_policy.html', now = now)

# Subscriptions Functionality
subscriptions = []

@routes_bp.route('/subscriptions', methods=['GET'])
def view_subscriptions():
    """View all subscriptions."""
    return jsonify({'subscriptions': subscriptions}), 200

@routes_bp.route('/subscriptions/add', methods=['POST'])
def add_subscription():
    """Add a new subscription."""
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if email in subscriptions:
        return jsonify({'message': 'Email is already subscribed'}), 200

    subscriptions.append(email)
    return jsonify({'message': 'Subscription added', 'subscriptions': subscriptions}), 201

@routes_bp.route('/subscriptions/remove', methods=['POST'])
def remove_subscription():
    """Remove a subscription."""
    data = request.json
    email = data.get('email')

    if email in subscriptions:
        subscriptions.remove(email)
        return jsonify({'message': 'Subscription removed', 'subscriptions': subscriptions}), 200
    return jsonify({'error': 'Email not found in subscriptions'}), 404

@routes_bp.route('/search')
def search_products():
    query = request.args.get('query', '')
    
    all_products = [
        {
            'id': 1,
            'name': 'Crystal Ring',
            'price': 180.00,
            'description': 'Exquisite crystal ring designed to catch the light with every angle.',
            'image_url': 'images/crystal_ring_1.jpg',
            'product_type': 'Rings',
            'collection': 'Crystal',
            'in_stock': True
        },
        {
            'id': 2,
            'name': 'Crystal Necklace',
            'price': 250.00,
            'description': 'Elegant crystal necklace that adds sparkle to any outfit.',
            'image_url': 'images/crystal_necklace_1.jpg',
            'product_type': 'Necklaces',
            'collection': 'Crystal',
            'in_stock': True
        },
        {
            'id': 3,
            'name': 'Crystal Bracelet',
            'price': 150.00,
            'description': 'Stunning crystal bracelet that wraps your wrist in elegance.',
            'image_url': 'images/crystal_bracelet_1.jpg',
            'product_type': 'Bracelets',
            'collection': 'Crystal',
            'in_stock': True
        },
        {
            'id': 4,
            'name': 'Leaf Ring',
            'price': 150.00,
            'description': 'Elegant leaf design to enhance your style. Crafted with precision and care.',
            'image_url': 'images/leaf ring 1`.webp',
            'product_type': 'Rings',
            'collection': 'Leaf',
            'in_stock': True
        },
        {
            'id': 5,
            'name': 'Leaf Necklace',
            'price': 120.00,
            'description': 'Delicate leaf pendant necklace, a symbol of nature\'s grace.',
            'image_url': 'images/leaf necklace 1.jpg',
            'product_type': 'Necklaces',
            'collection': 'Leaf',
            'in_stock': True
        },
        {
            'id': 6, 
            'name': 'Leaf Earrings',
            'price': 85.00,
            'description': 'Chic earrings featuring the elegant shape of leaves, perfect for any occasion.',
            'image_url': 'images/leaf earring 1.jpg',
            'product_type': 'Earrings',
            'collection': 'Leaf',
            'in_stock': True
        },
        {
            'id': 7,
            'name': 'Leaf Bracelet',
            'price': 135.00,
            'description': 'Beautiful bracelet designed with a delicate leaf motif to add elegance to your wrist.',
            'image_url': 'images/leaf bracelet 1.webp',
            'product_type': 'Bracelets',
            'collection': 'Leaf',
            'in_stock': True
        },
        {
            'id': 8,
            'name': 'Pearl Ring',
            'price': 220.00,
            'description': 'A beautiful and timeless pearl ring, perfect for any occasion.',
            'image_url': 'images/pearl ring 1.webp',
            'product_type': 'Rings',
            'collection': 'Pearl',
            'in_stock': True
        },
        {
            'id': 9,
            'name': 'Pearl Necklace',
            'price': 250.00,
            'description': 'A stunning necklace featuring lustrous pearls for an elegant look.',
            'image_url': 'images/pearl necklace 3.webp',
            'product_type': 'Necklaces',
            'collection': 'Pearl',
            'in_stock': True
        },
        {
            'id': 10,
            'name': 'Pearl Earrings',
            'price': 180.00,
            'description': 'Elegant pearl earrings that add a touch of sophistication to your look.',
            'image_url': 'images/pearl earring 1.avif',
            'product_type': 'Earrings',
            'collection': 'Pearl',
            'in_stock': True
        },
        {
            'id': 11,
            'name': 'Pearl Bracelet',
            'price': 180.00,
            'description': 'A beautiful pearl bracelet, perfect for adding elegance to your wrist.',
            'image_url': 'images/pearl_bracelet_1.jpg',
            'product_type': 'Bracelets',
            'collection': 'Pearl',
            'in_stock': True
        }
    ]
    
    if query:
        filtered_products = [
            product for product in all_products 
            if query.lower() in product['name'].lower() or 
               query.lower() in product['description'].lower() or
               query.lower() in product['collection'].lower() or
               query.lower() in product['product_type'].lower()
        ]
    else:
        filtered_products = all_products
    
    return render_template('all_products.html', products=filtered_products, search_query=query)