from functools import wraps
from datetime import datetime  # Added datetime import
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.extensions import db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import (
    User, Address, Product, ProductSize, Tag, ProductTag,
    Bundle, Basket, Wishlist, Order, Admin, Supplier, Payment
)

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
    return render_template('register.html')

@routes_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template('forgot_password.html')

@routes_bp.route('/password_change', methods=['GET', 'POST'])
@login_required
def password_change():
    return render_template('password_change.html')


@routes_bp.route('/about_us')
def about_us():
    return render_template('about_us.html')

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

@routes_bp.route('/product')
def product():
    return render_template('products.html')

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

@routes_bp.route('/bundles')
def bundles():
    return render_template('bundles.html')

@routes_bp.route('/bundle/<int:bundle_id>')
def bundle_detail(bundle_id):
    return render_template('bundle_detail.html', bundle_id=bundle_id)

# Shopping Cart and Wishlist
@routes_bp.route('/basket')
@login_required
def basket():
    return render_template('basket.html')

@routes_bp.route('/add_to_basket/<int:product_id>', methods=['POST'])
@login_required
def add_to_basket(product_id):
    return redirect(url_for('routes.basket'))

@routes_bp.route('/wishlist')
@login_required
def wishlist():
    return render_template('wishlist.html')

@routes_bp.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    return redirect(url_for('routes.wishlist'))

@routes_bp.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    return redirect(url_for('routes.wishlist'))

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

# Payment
@routes_bp.route('/payment')
def payment():
    return render_template('payment.html')

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
    return render_template('privacy_policy.html')
