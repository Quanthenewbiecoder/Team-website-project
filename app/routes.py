from functools import wraps
from datetime import datetime 
import random
import string
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import mongo, login_manager
from app.models import *
from app.forms import *
from app.database import products_collection
from bson import ObjectId
from pymongo import DESCENDING  # Import DESCENDING for sorting
import json
from app import *
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
from flask_mail import Message

# Create blueprint
routes_bp = Blueprint('routes', __name__)

# Role-based access control decorator
def role_required(*roles):
    """Ensure the current user has one of the specified roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"success": False, "error": "Unauthorized. Please log in."}), 401
            
            if current_user.role not in roles:
                return jsonify({"success": False, "error": "Forbidden. You do not have permission."}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@routes_bp.context_processor
def utility_processor():
    return dict(now=datetime.now())

# General Pages
@routes_bp.route('/')
def home():
    return render_template('homepage.html', now=datetime.now())


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
            
            session["session_version"] = str(user.session_version) if hasattr(user, 'session_version') else None
            
            next_page = request.args.get('next')
            
            flash("Login successful!", "success")

            if user.role == "admin":
                return redirect(next_page or url_for('routes.home'))
            else:
                return redirect(next_page or url_for('routes.home'))
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

        # Generate session_version as an ObjectId
        session_version = ObjectId()

        new_user = {
            "username": form.username.data,
            "email": form.email.data,
            "name": form.name.data,
            "surname": form.surname.data,
            "role": "Customer",
            "password_hash": generate_password_hash(form.password.data),  # FIXED password hashing
            "session_version": session_version  # Store session_version as ObjectId
        }

        # Insert user into MongoDB
        mongo.db.users.insert_one(new_user)

        # Fetch the user back and create a User object
        user = User.find_by_email(new_user["email"])  # Ensure `find_by_email` retrieves `session_version`

        if user:
            login_user(user)  # Log in the new user
            session["session_version"] = str(session_version)  # Store ObjectId as a string in session
            
            flash('Your account has been created! You are now logged in.', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash("Error creating account. Please try again.", "danger")
            return redirect(url_for('routes.register'))

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

@routes_bp.route('/help')
def help():
    return render_template('help.html')

@routes_bp.route('/contact')
def contact():
    return render_template('contact.html')

@routes_bp.route('/contact', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    msg = Message(subject=f"Contact Form: {subject}",
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=["noreplydivinee@gmail.com"])
    msg.body = f"""📩 New message from contact form:

    👤 Name: {name}
    📧 Email: {email}
    📝 Subject: {subject}

    💬 Message:
    {message}

    -- End of message --
    """
    
    try:
        mail.send(msg)
        flash("Message sent successfully!", "success")
    except Exception as e:
        print(f"Failed to send email: {e}")
        flash("Failed to send message. Please try again.", "danger")

    return redirect(url_for('routes.contact'))

@routes_bp.route('/terms')
def terms():
    return render_template('terms.html')

@routes_bp.route('/StarReturn')
def StarReturn():
    return render_template('StarReturn.html')

@routes_bp.route('/chatBox')
def chatBox():
    return render_template('chatBox.html')

@routes_bp.route('/crystalcollection')
def crystalcollection():
    try:
        return render_template('crystalcollection.html', now=datetime.now())
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return f"Error: {str(e)}", 500

# Route to display all products or a single product
@routes_bp.route('/products', methods=['GET'])
def all_products():
    """Render the shop page with all products."""
    all_products = list(mongo.db.products.find())
    return render_template('all_products.html', products=all_products)


@routes_bp.route('/products/<string:product_id>', methods=['GET'])
def products(product_id):
    """Render the product details page."""
    if not product_id or not ObjectId.is_valid(product_id):
        flash("Invalid Product ID.", "danger")
        return redirect(url_for('routes.all_products'))  # Redirect back to shop page
    
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('routes.all_products'))
    
    product['_id'] = str(product['_id'])

    product_reviews = list(mongo.db.reviews.find({"product_id": product_id}))
    return render_template('products.html', product=product, reviews=product_reviews)

# API Route to fetch all products
@routes_bp.route('/api/products', methods=['GET'])
def api_products():
    products = list(mongo.db.products.find())

    product_list = []
    for product in products:
        image_filename = product.get("image_url", "")

        # Ensure images are correctly prefixed with "/static/images/"
        if image_filename and not image_filename.startswith("/static/images/"):
            image_url = f"/static/images/{os.path.basename(image_filename)}"
        else:
            image_url = image_filename  # If already correct


        product_list.append({
            "id": str(product["_id"]),
            "name": product.get("name", "No Name"),
            "type": product.get("type", "Unknown"),
            "price": float(product.get("price", 0)),
            "image_url": image_url,  # FIXED path
            "collection": product.get("collection", "None"),
            "description": product.get("description", ""),
            "in_stock": bool(product.get("in_stock", False))
        })

    return jsonify({"success": True, "products": product_list}), 200

# Route to add or edit a review (User can only post one review per product)
@routes_bp.route('/products/<string:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    """Handles adding/updating a review for a product"""
    print(f"🚀 Review submitted for product: {product_id}")
    print(f"🔍 Request Method: {request.method}")
    print(f"📝 Form Data: {request.form}")

    if not ObjectId.is_valid(product_id):
        return jsonify({"error": "Invalid Product ID"}), 400

    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        return jsonify({"error": "Product not found"}), 404

    review_text = request.form.get('review')
    rating = request.form.get('rating')

    if not review_text or not rating:
        return jsonify({"error": "Review and rating are required."}), 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5."}), 400
    except ValueError:
        return jsonify({"error": "Invalid rating value."}), 400

    existing_review = mongo.db.reviews.find_one({"product_id": product_id, "user_id": current_user.get_id()})
    if existing_review:
        mongo.db.reviews.update_one(
            {"_id": existing_review["_id"]},
            {"$set": {"review": review_text, "rating": rating, "created_at": datetime.utcnow()}}
        )
        return jsonify({"message": "Review updated successfully!"}), 200
    else:
        mongo.db.reviews.insert_one({
            "product_id": product_id,
            "user_id": current_user.get_id(),
            "review": review_text,
            "rating": rating,
            "created_at": datetime.utcnow()
        })
        return jsonify({"message": "Review added successfully!"}), 201


# Route to delete a review (Allows user to review again after deleting)
@routes_bp.route('/products/<string:product_id>/review/delete', methods=['POST'])
@login_required
def delete_review(product_id):
    if not ObjectId.is_valid(product_id):
        flash("Invalid Product ID.", "danger")
        return redirect(url_for('routes.all_products'))

    mongo.db.reviews.delete_one({"product_id": product_id, "user_id": current_user.get_id()})
    flash("Your review has been deleted.", "success")
    return redirect(url_for('routes.products', product_id=product_id))

# API Route to fetch reviews for a product
@routes_bp.route('/api/products/<string:product_id>/reviews', methods=['GET'])
def api_reviews(product_id):
    if not ObjectId.is_valid(product_id):
        return jsonify({"error": "Invalid Product ID"}), 400

    product_reviews = list(mongo.db.reviews.find({"product_id": product_id}))

    reviews_list = [{
        "id": str(review["_id"]),
        "product_id": review["product_id"],
        "user_id": review["user_id"],  # Include user ID for frontend checks
        "review": review["review"],
        "rating": review["rating"],
        "created_at": review["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    } for review in product_reviews]

    return jsonify({"success": True, "reviews": reviews_list}), 200


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
    
    
@routes_bp.route('/product/<string:product_id>/care_instructions')
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
            product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
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
    """Handles payment process and redirects to success page."""
    cart_items = []
    total_amount = 0

    # Extract shopping basket data
    if shopping_basket:
        for product_id, item in shopping_basket.items():
            product_name = item.get('product_name', 'Unknown Product')
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 1))
            image_path = item.get('image', '')

            cart_item = {
                'product_id': product_id,
                'name': product_name,
                'quantity': quantity,
                'price': price,
                'total': price * quantity,
                'image': image_path
            }

            cart_items.append(cart_item)
            total_amount += price * quantity

    if request.method == 'POST':
        try:
            if current_user.is_authenticated:
                # Create an order for logged-in users
                new_order = {
                    "user_id": current_user.get_id(),
                    "total_price": float(total_amount),
                    "items": cart_items,
                    "status": "Pending",
                    "created_at": datetime.utcnow()
                }
                result = mongo.db.orders.insert_one(new_order)
                order_id = str(result.inserted_id)  # MongoDB generated order ID

            else:
                # Generate a tracking number for guest orders
                order_id = "GUEST-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                
                guest_order = {
                    "user_id": "guest",
                    "guest_email": request.form.get('guest_email', ''),  # Ensure guest email is captured
                    "total_price": float(total_amount),
                    "items": cart_items,
                    "status": "Pending",
                    "created_at": datetime.utcnow(),
                    "guest_order_id": order_id  # Store tracking number correctly
                }
                result = mongo.db.orders.insert_one(guest_order)

            # Store tracking number in session for retrieval after payment
            session['last_order_tracking'] = order_id

            # Clear shopping basket
            shopping_basket.clear()

            # Fix: Redirect to success page with tracking number
            return redirect(url_for('routes.payment_success', order_id=order_id))

        except Exception as e:
            flash(f"Error processing payment: {str(e)}", "danger")
            return redirect(url_for('routes.payment'))

    return render_template('payment.html', cart_items=cart_items, total_amount=total_amount)

@routes_bp.route('/payment/success/<order_id>')
def payment_success(order_id):
    """Display payment success page with tracking number."""
    try:
        print(f"DEBUG: Received order_id → {order_id}")  # Check received order_id

        # Check session for tracking number (used for guest users)
        tracking_number = session.pop('last_order_tracking', None)

        if not tracking_number:
            # Modify the query to include user_order_id
            query = {"$or": [
                {"_id": ObjectId(order_id)} if ObjectId.is_valid(order_id) else None,
                {"guest_order_id": order_id},  # For guest orders
                {"user_order_id": order_id}  # For registered user orders
            ]}

            # Remove None values from query (MongoDB does not allow None in `$or`)
            query["$or"] = [q for q in query["$or"] if q is not None]

            # Fetch order from database
            order = mongo.db.orders.find_one(query)

            if order:
                print(f"DEBUG: Order found in database → {order}")  # Log found order
                # Fetch tracking number correctly for both user and guest orders
                tracking_number = order.get("guest_order_id") or order.get("user_order_id") or str(order["_id"])
                print(f"DEBUG: Extracted tracking_number → {tracking_number}")  # Log extracted tracking number
            else:
                print("DEBUG: No order found with given order_id")  # Log if no order found
                tracking_number = None  # If no order is found

        return render_template('payment.html', 
                               payment_status='success',
                               tracking_number=tracking_number)

    except Exception as e:
        print(f"ERROR: {str(e)}")  # Log error
        flash(f"Error displaying payment success: {str(e)}", "danger")
        return redirect(url_for('routes.home'))

@routes_bp.route('/api/get-current-user', methods=['GET'])
@login_required  # Ensure only logged-in users can access
def get_current_user():
    """Fetch the logged-in user's details."""
    return jsonify({
        'success': True,
        'user': {
            'id': str(current_user.get_id()),  # Use get_id() for Flask-Login
            'email': current_user.email,
            'username': current_user.username,
            'role': current_user.role  # Important for authorization
        }
    }), 200

@routes_bp.route('/basket/add', methods=['POST'])
def add_to_basket():
    data = request.json
    product_id = str(data.get('product_id', ''))
    product_name = data.get('product_name', data.get('name', 'Unknown Product'))
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

@routes_bp.route('/order_confirmation/<order_id>')
def order_confirmation(order_id):
    #  Handle guest orders
    if order_id.startswith("GUEST-"):
        order = mongo.db.orders.find_one({"guest_order_id": order_id})
        if not order:
            flash("Order not found!", "danger")
            return redirect(url_for('routes.home'))
        
        # Convert ObjectId to string for template
        if '_id' in order:
            order['id'] = str(order['_id'])
        else:
            order['id'] = order_id
            
        order_items = order.get("items", [])
    else:
        #  Try fetching order from MongoDB
        try:
            order = mongo.db.orders.find_one({"_id": ObjectId(order_id)})  #  Fetch order
            if not order:
                flash("Order not found!", "danger")
                return redirect(url_for('routes.home'))
            
            # Convert ObjectId to string for template
            order['id'] = str(order['_id'])
            order_items = order.get("items", [])  #  Get embedded order items
        except Exception:
            flash("Invalid order ID.", "danger")
            return redirect(url_for('routes.home'))

    return render_template('order_confirmation.html', order=order, order_items=order_items)


@routes_bp.route('/history')
@login_required
def history():
    orders = list(mongo.db.orders.find({"user_id": current_user.get_id()}).sort("created_at", -1))
    return render_template('history.html', orders=orders)

# Reviews and Feedback
@routes_bp.route('/product/<string:product_id>/reviews')
def product_reviews(product_id):
    return render_template('product_reviews.html', product_id=product_id)

@routes_bp.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    return render_template('feedback.html')

@routes_bp.route('/dashboard')
@login_required
def user_dashboard():
    """Fetch all orders linked to the logged-in user and display them on the dashboard."""
    try:
        user_id_str = current_user.get_id()  # Get user ID as string
        try:
            user_id = ObjectId(user_id_str)  # Convert to ObjectId
        except Exception:
            user_id = user_id_str  # Fallback if it's already a string

        # Fetch only orders that belong to the current user
        orders = list(mongo.db.orders.find(
            {"$or": [
                {"user_id": user_id},  # Find by ObjectId (recommended)
                {"user_id": user_id_str},  # Find by string ID (for edge cases)
            ]}
        ).sort("created_at", -1))  # Sort orders by newest first

        # Convert `_id` and `created_at` for front-end compatibility
        for order in orders:
            order["_id"] = str(order["_id"])  # Ensure ObjectId is string for Jinja
            if "created_at" in order and isinstance(order["created_at"], datetime):
                order["created_at"] = order["created_at"].strftime('%d/%m/%Y')

        return render_template('user-dashboard.html', orders=orders)

    except Exception as e:
        print(f"Error fetching orders: {e}")
        flash("Error loading your orders.", "danger")
        return render_template('user-dashboard.html', orders=[])


# Admin Dashboard Route
@routes_bp.route('/admin')
@login_required
@role_required('admin', 'staff')
def admin_dashboard():
    """Admin panel to manage users, orders, and products."""
    total_users = mongo.db.users.count_documents({})
    total_orders = mongo.db.orders.count_documents({})
    
    return render_template(
        'admin_dashboard.html', 
        total_users=total_users, 
        total_orders=total_orders
    )

@routes_bp.route('/api/admin/profile', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_admin_profile():
    """Returns the profile details of the currently logged-in admin."""
    admin = mongo.db.users.find_one({"email": current_user.email})

    if not admin:
        return jsonify({"success": False, "error": "Admin not found"}), 404

    return jsonify({
        "success": True,
        "admin": {
            "username": admin.get("username", ""),
            "email": admin.get("email", ""),
            "name": admin.get("name", ""),
            "surname": admin.get("surname", ""),
        }
    }), 200

@routes_bp.route('/api/admin/users/count', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_user_count():
    """Returns total number of users."""
    user_count = mongo.db.users.count_documents({})
    return jsonify({"count": user_count}), 200

@routes_bp.route('/api/admin/orders/count', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_order_count():
    """Returns total number of orders."""
    order_count = mongo.db.orders.count_documents({})
    return jsonify({"count": order_count}), 200

# User management
@routes_bp.route('/api/admin/users/<user_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_user(user_id):
    """Delete a user by ID"""
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid User ID"}), 400

    result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200

@routes_bp.route('/api/admin/users/<user_id>', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def view_user(user_id):
    """Fetch a user by ID."""
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid User ID"}), 400

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404

    orders = list(mongo.db.orders.find({"user_id": ObjectId(user_id)}))

    return jsonify({
        "_id": str(user["_id"]),
        "username": user.get("username", "N/A"),
        "name": user.get("name", "N/A"),
        "surname": user.get("surname", "N/A"),
        "email": user.get("email", "N/A"),
        "role": user.get("role", "Customer"),
        "created_at": user.get("created_at", datetime.utcnow()).strftime('%Y-%m-%d'),
        "orders": [
            {
                "_id": str(order["_id"]),
                "created_at": order.get("created_at", datetime.utcnow()).strftime('%Y-%m-%d'),
                "status": order.get("status", "Pending"),
                "total_price": order.get("total_price", 0)
            }
            for order in orders
        ]
    }), 200

@routes_bp.route('/api/admin/users/<user_id>', methods=['GET', 'PUT'])
@login_required
@role_required('admin', 'staff')
def edit_user(user_id):
    """Fetch or update user information."""
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid User ID"}), 400

    if request.method == 'GET':  # Fetch user details
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "_id": str(user["_id"]),
            "username": user.get("username", "N/A"),
            "name": user.get("name", "N/A"),
            "surname": user.get("surname", "N/A"),
            "email": user.get("email", "N/A"),
            "role": user.get("role", "Customer"),
            "created_at": user.get("created_at", datetime.utcnow()).strftime('%Y-%m-%d')
        }), 200

    elif request.method == 'PUT':  # Update user details
        data = request.json

        update_data = {}
        if "username" in data:
            update_data["username"] = data["username"]
        if "name" in data:
            update_data["name"] = data["name"]
        if "surname" in data:
            update_data["surname"] = data["surname"]
        if "email" in data:
            update_data["email"] = data["email"]
        if "role" in data:
            update_data["role"] = data["role"]

        result = mongo.db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200

@login_manager.user_loader
def load_user(user_id):
    """Load user and check session validity."""
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if user:
        # If session_version does not match, force logout
        if session.get("session_version") != str(user.get("session_version")):
            session.clear()  # Log the user out
            return None
        
        return User(**user)  # Convert MongoDB user data to `User` object

    return None

@routes_bp.route('/api/admin/users/<user_id>/reset-password', methods=['POST'])
@login_required
@role_required('admin')
def reset_user_password(user_id):  # Make sure user_id is received as a parameter
    if not ObjectId.is_valid(user_id):
        return jsonify({"error": "Invalid User ID"}), 400

    default_password = "Password123"
    hashed_password = generate_password_hash(default_password)

    result = mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password_hash": hashed_password, "session_version": ObjectId()}}  # Invalidate all sessions
    )

    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"success": True, "message": "Password reset successfully. User must log in again."}), 200

@routes_bp.route('/api/admin/users', methods=['POST'])
@login_required
@role_required('admin', 'staff')
def create_user():
    """Create a new user."""
    try:
        data = request.json  # Ensure we're receiving JSON data

        # Validate required fields
        required_fields = ["username", "name", "surname", "email", "role", "password"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        existing_user = mongo.db.users.find_one({"email": data["email"]})
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 409

        # Create new user object
        new_user = {
            "username": data["username"],
            "name": data["name"],
            "surname": data["surname"],
            "email": data["email"],
            "role": data["role"],
            "password": data["password"],  # You should hash the password before storing it!
            "created_at": datetime.utcnow()
        }

        # Insert into database
        result = mongo.db.users.insert_one(new_user)

        return jsonify({"success": True, "message": "User created", "_id": str(result.inserted_id)}), 201

    except Exception as e:
        print(f"Error creating user: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@routes_bp.route('/api/admin/change-password', methods=['POST'])
@login_required
@role_required('admin', 'staff')
def change_admin_password():
    """Allow admin to change their password and log out all other active sessions except the current one."""
    data = request.get_json()

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not current_user.check_password(current_password):
        return jsonify({"success": False, "error": "Incorrect current password"}), 400

    # Hash the new password
    hashed_password = generate_password_hash(new_password)

    # Generate a new session version (force logout for other devices)
    new_session_version = str(ObjectId())  # Unique session ID

    # Update the password & session version in the database
    mongo.db.users.update_one(
        {"_id": ObjectId(current_user.get_id())},
        {
            "$set": {
                "password_hash": hashed_password,
                "session_version": new_session_version
            }
        }
    )

    # Keep the current session logged in by updating session data
    session["session_version"] = new_session_version  # Store new session ID

    return jsonify({"success": True, "message": "Password changed successfully. Other sessions have been logged out."}), 200

# ORDER MANAGEMENT
@routes_bp.route('/api/admin/orders', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def manage_orders():
    """List all orders with pagination."""

    # Get page number (default = 1) and limit per page (default = 10)
    page = int(request.args.get("page", 1))
    per_page = 10

    # Get total order count
    total_orders = mongo.db.orders.count_documents({})

    # Fetch paginated orders
    orders_cursor = mongo.db.orders.find().sort("created_at", -1).skip((page - 1) * per_page).limit(per_page)
    orders = list(orders_cursor)

    return jsonify({
        "orders": [{
            "_id": str(order["_id"]),
            "created_at": order.get("created_at", datetime.utcnow()).strftime('%Y-%m-%d'),
            "user_id": str(order.get("user_id", "Guest")),
            "guest_email": order.get("guest_email", ""),
            "total_price": order.get("total_price", 0),
            "status": order.get("status", "Pending"),
            "items": order.get("items", [])  # Ensure items list is always present
        } for order in orders],
        "totalPages": (total_orders // per_page) + (1 if total_orders % per_page > 0 else 0),
        "currentPage": page
    }), 200

@routes_bp.route('/api/admin/orders/stats', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_order_stats():
    """Returns stats for orders over the last 6 months."""
    from datetime import datetime, timedelta

    six_months_ago = datetime.utcnow() - timedelta(days=180)
    orders = list(mongo.db.orders.find({"created_at": {"$gte": six_months_ago}}))

    monthly_counts = {}
    for order in orders:
        month = order["created_at"].strftime('%b')  # 'Jan', 'Feb', etc.
        monthly_counts[month] = monthly_counts.get(month, 0) + 1

    return jsonify({"chartData": {"labels": list(monthly_counts.keys()), "values": list(monthly_counts.values())}}), 200

@routes_bp.route('/api/admin/orders/<order_id>', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_order_details(order_id):
    """Fetch order details by ID"""
    try:
        order = mongo.db.orders.find_one({"_id": ObjectId(order_id)})
        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({
            "_id": str(order["_id"]),
            "created_at": order.get("created_at", "").strftime('%Y-%m-%d'),
            "user_id": str(order.get("user_id", "Guest")),
            "guest_email": order.get("guest_email"),
            "total_price": order.get("total_price"),
            "status": order.get("status"),
            "items": order.get("items", [])
        })

    except Exception as e:
        print(f"Error fetching order: {e}")
        return jsonify({"error": "Invalid Order ID"}), 400

@routes_bp.route('/admin/orders/update/<order_id>', methods=['POST'])
@login_required
@role_required('admin', 'staff')
def update_order(order_id):
    """Update order status."""
    status = request.form.get("status")
    if status not in ["Pending", "Processing", "Shipped", "Delivered", "Canceled"]:
        return jsonify({"error": "Invalid status"}), 400

    mongo.db.orders.update_one(
        {"_id": ObjectId(order_id)}, 
        {"$set": {"status": status}}
    )
    flash("Order status updated!", "success")
    return jsonify({"message": "Order updated"}), 200

@routes_bp.route('/api/admin/orders/<order_id>', methods=['DELETE'])
@login_required
@role_required('admin', 'staff')
def delete_order(order_id):
    """Delete an order by ID"""
    try:
        result = mongo.db.orders.delete_one({"_id": ObjectId(order_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Order not found"}), 404
        
        return jsonify({"success": True, "message": "Order deleted"}), 200

    except Exception as e:
        print(f"Error deleting order: {e}")
        return jsonify({"error": "Invalid Order ID"}), 400

@routes_bp.route('/api/admin/activity', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_recent_activity():
    """Returns recent admin activity."""
    activity = list(mongo.db.activity.find().sort("time", -1).limit(10))

    return jsonify([
        {"message": a.get("message", "Unknown activity"), "type": a.get("type", "info"), "time": a.get("time")}
        for a in activity
    ]), 200

@routes_bp.route('/api/admin/users', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_all_users():
    """Fetch paginated users."""
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '').strip()

    query = {}
    if search:
        query = {"$or": [
            {"username": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"name": {"$regex": search, "$options": "i"}},
            {"surname": {"$regex": search, "$options": "i"}}
        ]}

    users_cursor = mongo.db.users.find(query).skip((page - 1) * 10).limit(10)
    users = list(users_cursor)
    total_users = mongo.db.users.count_documents(query)

    return jsonify({
        "users": [
            {
                "_id": str(user["_id"]),
                "username": user.get("username", "N/A"),
                "name": user.get("name", "N/A"),
                "surname": user.get("surname", "N/A"),
                "email": user.get("email", "N/A"),
                "role": user.get("role", "Customer"),
                "created_at": user.get("created_at", datetime.utcnow()).strftime('%Y-%m-%d')
            } for user in users
        ],
        "totalPages": (total_users // 10) + 1
    }), 200

# PRODUCT MANAGEMENT API
@routes_bp.route('/api/products', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_all_products():
    """Fetch all products for admin management."""
    products = list(mongo.db.products.find())
    return jsonify([{
        "_id": str(product["_id"]),
        "name": product["name"],
        "type": product.get("type", ""),
        "price": float(product.get("price", 0)),
        "description": product.get("description", ""),
        "image_url": product.get("image_url", ""),
        "in_stock": product.get("in_stock", True)
    } for product in products]), 200


@routes_bp.route('/api/products/<product_id>', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_product(product_id):
    """Fetch a single product by ID."""
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        return jsonify({"error": "Product not found"}), 404

    product["_id"] = str(product["_id"])
    return jsonify({"success": True, "product": product}), 200

# Define the absolute path where images will be saved
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    """Check if the uploaded file has a valid extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@routes_bp.route("/api/products", methods=["POST"])
@login_required
@role_required("admin", "staff")
def add_product():
    try:
        name = request.form.get("name")
        price = float(request.form.get("price", 0))
        product_type = request.form.get("type", "")
        collection = request.form.get("collection", None)
        description = request.form.get("description", "")
        in_stock = request.form.get("in_stock") == "true"

        image_url = None

        # Handle Image Upload
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)  # FIXED HERE
                file.save(save_path)  # Save image to dynamically set UPLOAD_FOLDER
                image_url = f"images/{filename}"  # Store relative path in MongoDB

        # Create product document
        new_product = {
            "name": name,
            "type": product_type,
            "price": price,
            "collection": collection,
            "description": description,
            "image_url": image_url,
            "in_stock": in_stock
        }

        result = mongo.db.products.insert_one(new_product)
        return jsonify({"success": True, "message": "Product added", "product_id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routes_bp.route('/api/products/<product_id>', methods=['PUT'])
@login_required
@role_required('admin', 'staff')
def update_product(product_id):
    """Update an existing product."""
    try:
        data = request.json
        update_data = {
            "name": data.get("name"),
            "type": data.get("type", ""),
            "price": float(data.get("price", 0)),
            "description": data.get("description", ""),
            "image_url": data.get("image_url", ""),
            "in_stock": data.get("in_stock", True)
        }
        result = mongo.db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
        if result.matched_count == 0:
            return jsonify({"success": False, "error": "Product not found"}), 404
        return jsonify({"success": True, "message": "Product updated"}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routes_bp.route('/api/products/<product_id>', methods=['DELETE'])
@login_required
@role_required('admin', 'staff')
def delete_product(product_id):
    """Delete a product and optionally remove its image."""
    if current_user.role not in ["admin", "staff"]:
        return jsonify({"success": False, "error": "Forbidden"}), 403
    
    try:
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})

        if not product:
            return jsonify({"success": False, "error": "Product not found"}), 404

        # Check if the product has an associated image
        image_path = product.get("image_url")
        image_deleted = False

        # Ask the frontend whether to delete the image or keep it
        delete_image = request.args.get("delete_image", "false").lower() == "true"

        # Delete the product from the database
        result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})

        if result.deleted_count > 0:
            if delete_image and image_path:
                abs_image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], os.path.basename(image_path))  # FIXED HERE

                if os.path.exists(abs_image_path):
                    os.remove(abs_image_path)  # Delete the image file dynamically
                    image_deleted = True

            return jsonify({
                "success": True,
                "message": "Product deleted",
                "image_deleted": image_deleted
            }), 200

        return jsonify({"success": False, "error": "Product deletion failed"}), 500

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routes_bp.route('/admin/reports')
@login_required
@role_required('admin', 'staff')
def reports():
    return render_template('reports.html')

# Product Customization
@routes_bp.route('/product/<string:product_id>/customize', methods=['GET', 'POST'])
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

    mongo_query = {}

    if query:
        mongo_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"collection": {"$regex": query, "$options": "i"}},
                {"type": {"$regex": query, "$options": "i"}}
            ]
        }

    filtered_products_cursor = mongo.db.products.find(mongo_query)

    filtered_products = []
    for product in filtered_products_cursor:
        filtered_products.append({
            "id": str(product["_id"]),
            "name": product.get("name", "No Name"),
            "price": float(product.get("price", 0)),
            "description": product.get("description", ""),
            "image_url": url_for("static", filename=f"images/{product.get('image_url', '').split('/')[-1]}"),
            "product_type": product.get("type", ""),
            "collection": product.get("collection", "None"),
            "in_stock": product.get("in_stock", False)
        })

    return render_template('all_products.html', products=filtered_products, search_query=query)


@routes_bp.route('/previous-orders', methods=['GET', 'POST'])
def previous_orders():
    tracking_number = None
    order = None
    user_orders = []
    
    if request.method == 'GET' and 'tracking' in request.args:
        tracking_number = request.args.get('tracking', '').strip()
        
    if request.method == 'POST':
        tracking_number = request.form.get('tracking_number', '').strip()
    
    if tracking_number:
        try:
            if tracking_number.startswith('GUEST-'):
                order_data = mongo.db.orders.find_one({"guest_order_id": tracking_number})
            else:
                try:
                    order_id = ObjectId(tracking_number)
                    order_data = mongo.db.orders.find_one({"_id": order_id})
                except:
                    flash('Invalid order ID format.', 'danger')
                    order_data = None
            
            if order_data:
                if '_id' in order_data:
                    order_data['id'] = str(order_data['_id'])
                    
                if 'created_at' in order_data and not isinstance(order_data['created_at'], datetime):
                    try:
                        created_at_str = str(order_data['created_at'])
                        order_data['created_at'] = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    except:
                        order_data['created_at'] = datetime.utcnow()
                
                # Process items data if it exists to ensure it's usable in the template
                if 'items' in order_data and order_data['items']:
                    # Make sure item data has the necessary fields
                    for item in order_data['items']:
                        # Ensure item has all needed fields
                        if 'image' in item and item['image'] and not item['image'].startswith('http'):
                            # Fix image paths if needed
                            if item['image'].startswith('static/'):
                                item['image'] = item['image']
                            else:
                                item['image'] = f"images/{item['image'].split('/')[-1]}" if '/' in item['image'] else f"images/{item['image']}"
                        
                        # Add default image if missing
                        if 'image' not in item or not item['image']:
                            item['image'] = "images/default-product.jpg"
                
                order = order_data
            else:
                flash('No order found with that tracking number.', 'danger')
        except Exception as e:
            flash(f'Error retrieving order: {str(e)}', 'danger')
    
    if current_user.is_authenticated:
        try:
            user_orders_cursor = mongo.db.orders.find({"user_id": current_user.get_id()})
            user_orders = list(user_orders_cursor.sort("created_at", -1).limit(5))
            
            for user_order in user_orders:
                if '_id' in user_order:
                    user_order['id'] = str(user_order['_id'])
        except Exception as e:
            flash(f'Error retrieving order history: {str(e)}', 'danger')
            user_orders = []
    
    return render_template('previous_orders.html', 
                          tracking_number=tracking_number, 
                          order=order,
                          user_orders=user_orders)


@routes_bp.route('/clear_order_history', methods=['POST'])
@login_required 
def clear_order_history():
    try:
        user_id = current_user.get_id()
        
        result = mongo.db.orders.delete_many({"user_id": user_id})
        
        flash(f"Successfully cleared {result.deleted_count} orders from your history.", "success")
        
    except Exception as e:
        flash(f"Error clearing order history: {str(e)}", "danger")
    
    return redirect(url_for('routes.previous_orders'))

@routes_bp.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order for guests or registered users."""
    try:
        data = request.json

        print(f"DEBUG: Incoming order data → {json.dumps(data, indent=2)}")

        if not data or 'total_price' not in data or 'items' not in data:
            return jsonify({'success': False, 'error': 'Invalid order data'}), 400

        user_id = data.get('user_id')
        guest_email = data.get('guest_email')

        if not user_id and not guest_email:
            print("ERROR: Both user_id and guest_email are missing!")
            return jsonify({'success': False, 'error': 'User ID or guest email is required'}), 400

        print(f"Order Accepted: user_id={user_id}, guest_email={guest_email}")

        total_price = float(data['total_price'])

        if not isinstance(data['items'], list) or not all(isinstance(item, dict) for item in data['items']):
            return jsonify({'success': False, 'error': 'Items must be a list of objects'}), 400

        # FIX: Convert `user_id` from email to ObjectId if it's a registered user
        user_object_id = None
        if user_id and user_id != "guest":
            user_data = mongo.db.users.find_one({"email": user_id})  # Find user by email
            if user_data:
                user_object_id = user_data["_id"]  # Get user's ObjectId

        # Generate tracking number
        guest_order_id = None
        user_order_id = None
        if guest_email:
            guest_order_id = f"GUEST-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))}"
        if user_object_id:
            user_order_id = f"USER-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))}"

        order = {
            "user_id": user_object_id if user_object_id else "guest",
            "guest_email": guest_email if guest_email else None,
            "total_price": total_price,
            "items": data['items'],
            "status": "Pending",
            "created_at": datetime.utcnow(),
            "guest_order_id": guest_order_id,
            "user_order_id": user_order_id
        }

        result = mongo.db.orders.insert_one(order)
        order_id = str(result.inserted_id)

        return jsonify({'success': True, 'order_id': order_id, 'tracking_number': user_order_id or guest_order_id or order_id}), 201

    except Exception as e:
        print(f"ERROR CREATING ORDER: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500

    except Exception as e:
        print(f"ERROR CREATING ORDER: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500

### order-details-headerGET ORDER BY ID (User or Guest) ###
@routes_bp.route('/api/orders/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    """Retrieve an order by _id (for registered users) or guest_order_id (for guest users)."""
    try:
        order_data = None

        # If order_id is a valid ObjectId, search by `_id`
        if ObjectId.is_valid(order_id):
            order_data = mongo.db.orders.find_one({"_id": ObjectId(order_id)})
        else:
            # If not an ObjectId, assume it's a guest tracking number and search by `guest_order_id`
            order_data = mongo.db.orders.find_one({"guest_order_id": order_id})

        if not order_data:
            return jsonify({'success': False, 'error': 'Order not found'}), 404

        # Convert `_id` to string
        order_data['_id'] = str(order_data['_id'])

        return jsonify({'success': True, 'order': order_data}), 200

    except Exception as e:
        print(f"Error retrieving order: {e}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500

### order-details-headerGET ORDERS BY USER ID ###
@routes_bp.route('/api/orders/user/<user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """Retrieve all orders for a registered user."""
    try:
        orders = list(mongo.db.orders.find({"user_id": user_id}))
        for order in orders:
            order['_id'] = str(order['_id'])  # Convert ObjectId to string
        return jsonify({'success': True, 'orders': orders}), 200
    except Exception as e:
        print(f"order-details-headerError retrieving user orders: {e}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500

### order-details-headerGET ORDERS BY GUEST EMAIL
@routes_bp.route('/api/orders/guest', methods=['GET'])
def get_orders_by_guest():
    """Retrieve all orders for a guest user by email."""
    email = request.args.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    try:
        orders = list(mongo.db.orders.find({"guest_email": email}))
        for order in orders:
            order['_id'] = str(order['_id'])  # Convert ObjectId to string
        return jsonify({'success': True, 'orders': orders}), 200
    except Exception as e:
        print(f"order-details-headerError retrieving guest orders: {e}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500

### order-details-headerTRACK ORDER BY TRACKING NUMBER OR GUEST EMAIL
@routes_bp.route('/api/orders/track', methods=['GET'])
def track_order():
    """API endpoint to fetch order details by tracking number or guest email."""
    tracking_number = request.args.get('tracking')
    guest_email = request.args.get('guest_email')

    if not tracking_number and not guest_email:
        return jsonify({'success': False, 'error': 'Tracking number or email required'}), 400

    try:
        order = None

        # Search for the order using `user_order_id`, `guest_order_id`, or `_id`
        if tracking_number:
            order = mongo.db.orders.find_one({
                "$or": [
                    {"user_order_id": tracking_number},
                    {"guest_order_id": tracking_number},
                    {"_id": ObjectId(tracking_number) if ObjectId.is_valid(tracking_number) else None}
                ]
            })

        # If not found using tracking number, search by guest email
        if not order and guest_email:
            order = mongo.db.orders.find_one({"guest_email": guest_email}, sort=[("created_at", -1)])

        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404

        # Convert `_id` from ObjectId to string
        order['_id'] = str(order['_id'])

        return jsonify({'success': True, 'order': order}), 200

    except Exception as e:
        print(f"Error tracking order: {e}")
        return jsonify({'success': False, 'error': 'Internal Server Error'}), 500

### order-details-headerORDER TRACKING PAGE
@routes_bp.route('/order-tracking', methods=['GET'])
def order_tracking():
    """Render the order tracking page with order details."""
    order_id = request.args.get('order_id')

    if not order_id:
        flash("No tracking number provided.", "danger")
        return redirect(url_for('routes.previous_orders'))

    try:
        # Search using `_id`, `guest_order_id`, or `user_order_id`
        order = mongo.db.orders.find_one({
            "$or": [
                {"_id": ObjectId(order_id) if ObjectId.is_valid(order_id) else None},
                {"guest_order_id": order_id},
                {"user_order_id": order_id}
            ]
        })

        if not order:
            flash("Order not found!", "danger")
            return redirect(url_for('routes.previous_orders'))

        # Convert `_id` to string for template
        order['_id'] = str(order['_id'])

        return render_template('track_order.html', order=order, tracking_number=order_id)

    except Exception as e:
        flash(f"Error retrieving order: {str(e)}", "danger")
        return redirect(url_for('routes.previous_orders'))

@routes_bp.route('/save-inquiry', methods=['POST'])
def save_inquiry():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    inquiry = data.get('inquiry')

    if not name or not email or not inquiry:
        return jsonify({"error": "Name, email, and inquiry are required"}), 400

    # Save inquiry to MongoDB
    inquiry_data = {
        "name": name,
        "email": email,
        "inquiry": inquiry,
        "created_at": datetime.utcnow(),
        "status": "Pending"
    }

    # Insert into MongoDB (assuming you have a collection named 'inquiries')
    mongo.db.inquiries.insert_one(inquiry_data)

    return jsonify({"message": "Inquiry saved successfully!"}), 200

@routes_bp.route('/wishlist')
@login_required
def wishlist():
    return render_template('wishlist.html')