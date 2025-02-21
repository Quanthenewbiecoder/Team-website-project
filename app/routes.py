from functools import wraps
from datetime import datetime 
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from app.extensions import db
from flask_login import login_user, logout_user, login_required, current_user
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
        redirect_url = request.args.get('redirect')
        if redirect_url:
            return redirect(url_for(f'routes.{redirect_url}'))
        return redirect(url_for('routes.home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            
            redirect_url = request.args.get('redirect')
            if redirect_url:
                return redirect(url_for(f'routes.{redirect_url}'))
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
        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=form.username.data).first()
        
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('routes.register'))
        
        # Create the user object without the password_hash
        user = User(
            username=form.username.data,
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data,
            role='Customer'
        )
        
        # Set the password after creating the user object (use the set_password method to hash the password)
        user.set_password(form.password.data)
        
        # Commit the new user to the database
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created!', 'success')
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

# Store reviews in memory (this should be a database in production)
reviews = {}

#  Route to display all products
@routes_bp.route('/products/', defaults={'product_id': None}, methods=['GET'])
@routes_bp.route('/products/<int:product_id>', methods=['GET'])
def products(product_id):
    if product_id is None:
        # Fetch all products from the database
        all_products = Product.query.all()
        return render_template('all_products.html', products=all_products, now=datetime.now())
    
    # Fetch a single product
    product = Product.query.get_or_404(product_id)
    product_reviews = reviews.get(product_id, [])
    
    return render_template('products.html', product=product, reviews=product_reviews)

#  Route to add a review
@routes_bp.route('/products/<int:product_id>/review', methods=['POST'])
def add_review(product_id):
    review = request.form.get('review')
    rating = request.form.get('rating')

    # Basic validation
    if not review or not rating:
        flash('Review and rating are required.', 'error')
        return redirect(url_for('products', product_id=product_id))
    
    # Add new review
    if product_id not in reviews:
        reviews[product_id] = []
    reviews[product_id].append({'review': review, 'rating': rating})
    flash('Review added successfully!', 'success')
    
    return redirect(url_for('products', product_id=product_id))

#  API Route to fetch all products
@routes_bp.route('/api/products', methods=['GET'])
def api_products():
    products = Product.query.all()
    product_list = [{
        "id": product.id,
        "name": product.name,
        "type": product.type,
        "price": product.price,
        "image_url": url_for('static', filename=product.image_url),  #  Fix image path issue
        "collection": product.collection,
        "description": product.description,
        "in_stock": product.in_stock
    } for product in products]

    return jsonify(product_list)



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
@login_required
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
@login_required
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
        # Create a new order in the database
        new_order = Order(
            user_id=current_user.id,
            total_price=total_amount,
            created_at=datetime.now(),
            status='Pending'
        )
        db.session.add(new_order)
        db.session.commit()

        # Save order items
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)

        db.session.commit()

        # Clear shopping basket
        shopping_basket.clear()

        # Redirect to order confirmation page
        return redirect(url_for('routes_bp.order_confirmation', order_id=new_order.id))

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

# Order Confirmation Page
@routes_bp.route('/order_confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    order_items = OrderItem.query.filter_by(order_id=order.id).all()

    return render_template('order_confirmation.html', order=order, order_items=order_items)

@routes_bp.route('/track_order/<int:order_id>')
@login_required
def track_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    
    if not order:
        flash('Order not found or access denied.', 'danger')
        return redirect(url_for('routes.history'))
    
    return render_template('track_order.html', order=order)

@routes_bp.route('/history')
@login_required
def history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
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
