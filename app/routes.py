from functools import wraps
from datetime import datetime 
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from app.extensions import db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import *

# Create blueprint
routes_bp = Blueprint('routes', __name__)

# Role-based access control decorator
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('routes.login'))
            if current_user.user_role not in roles:
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
    return render_template('login.html', now=datetime.now())

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@routes_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', now=datetime.now())

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

# ---------------- Review Functionality ----------------
# In-memory storage for reviews, using product_id as keys
reviews = {}

@routes_bp.route('/products/', defaults={'product_id': None}, methods=['GET', 'POST'])
@routes_bp.route('/products/<int:product_id>', methods=['GET', 'POST'])
def products(product_id):
    if product_id is None:
        # Handle case where no product_id is provided (list all products)
        all_products = ["Product 1", "Product 2", "Product 3"]  # Example product list
        return render_template('all_products.html', products=all_products, now=datetime.now())
    
    # Handle case for a specific product
    product_reviews = reviews.get(product_id, [])
    
    if request.method == 'POST':
        review = request.form.get('review')
        rating = request.form.get('rating')

        # Basic validation
        if not review or not rating:
            flash('Review and rating are required.', 'error')
            return redirect(url_for('routes.products', product_id=product_id))
        
        # Add new review
        if product_id not in reviews:
            reviews[product_id] = []
        reviews[product_id].append({'review': review, 'rating': rating})
        flash('Review added successfully!', 'success')

    return render_template('products.html', product_id=product_id, reviews=product_reviews)


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
    
@routes_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    return render_template('product_detail.html', product_id=product_id)

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
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 0))
            cart_items.append({
                'id': product_id,
                'name': item['product_name'],
                'quantity': quantity,
                'price': price,
                'total': price * quantity,
                'image': item.get('image', '')
            })
            total_amount += price * quantity

    return render_template('currentbasket.html', 
                         cart_items=cart_items,
                         total_amount=total_amount)


@routes_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    cart_items = []
    total_amount = 0
    
    if shopping_basket:
        for product_id, item in shopping_basket.items():
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 0))
            cart_items.append({
                'id': product_id,
                'name': item['product_name'],
                'quantity': quantity,
                'price': price,
                'total': price * quantity,
                'image': item.get('image', '')
            })
            total_amount += price * quantity

    if request.method == 'POST':
        shopping_basket.clear()
        return redirect(url_for('routes.payment_success'))

    return render_template('payment.html', 
                         cart_items=cart_items,
                         total_amount=total_amount)

@routes_bp.route('/payment/success')
def payment_success():
    return render_template('payment.html', 
                         payment_status='success',
                         cart_items=[],
                         total_amount=0,
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

# Checkout and Orders
@routes_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    return render_template('checkout.html')

@routes_bp.route('/order_summary')
@login_required
def order_summary():
    return render_template('order_summary.html')

@routes_bp.route('/order_confirmation')
@login_required
def order_confirmation():
    return render_template('order_confirmation.html')

@routes_bp.route('/track_order/<int:order_id>')
@login_required
def track_order(order_id):
    return render_template('track_order.html', order_id=order_id)

@routes_bp.route('/history')
@login_required
def history():
    return render_template('history.html')

# Reviews and Feedback
@routes_bp.route('/product/<int:product_id>/reviews')
def product_reviews(product_id):
    return render_template('product_reviews.html', product_id=product_id)

@routes_bp.route('/product/<int:product_id>/add_review', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    return render_template('add_review.html', product_id=product_id)

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
