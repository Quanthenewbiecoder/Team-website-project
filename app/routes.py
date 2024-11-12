from functools import wraps
from flask import render_template, redirect, url_for, request, flash, session
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import (
    User, Address, Product, ProductSize, Tag, ProductTag, 
    Bundle, BundleItem, CustomizationOption, Basket, 
    BasketItem, Wishlist, WishlistItem, Order, OrderItem, 
    CareInstruction, Admin, Supplier, ProductInventory, 
    Payment, Discount, Invoice
)
def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.user_role not in roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# Authentication & User Management
# Routes for logging in, logging out, registration, password reset, and password change.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Renders the login page and processes login credentials
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # Logs out the current user and redirects to home page
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Renders the registration page and handles new user registration
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    # Page for users to initiate a password reset
    return render_template('forgot_password.html')

@app.route('/Password_change')
def password_change():
    # Page for users to change password after resetting it
    return render_template('Password_change.html')

# General Pages
# Basic site pages that provide information about the company and contact details.
@app.route('/')
def home():
    # Renders the homepage with introductory content
    return render_template('base.html')

@app.route('/about_us')
def about_us():
    # Renders the "About Us" page with company background information
    return render_template('about_us.html')

@app.route('/Contact')
def contact():
    # Renders the contact form for users to reach support
    return render_template('Contact.html')

# Product & Bundle Pages
# Routes for displaying products, individual product details, care instructions, and bundles.
@app.route('/Product')
def product():
    # Displays a list of all available products
    return render_template('Product.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # Shows details for a specific product
    return render_template('product_detail.html', product_id=product_id)

@app.route('/product/<int:product_id>/care_instructions')
def product_care_instructions(product_id):
    # Displays care instructions specific to the product
    return render_template('care_instructions.html', product_id=product_id)

@app.route('/bundles')
def bundles():
    # Lists available product bundles
    return render_template('bundles.html')

@app.route('/bundle/<int:bundle_id>')
def bundle_detail(bundle_id):
    # Shows details for a specific bundle
    return render_template('bundle_detail.html', bundle_id=bundle_id)

# Basket, Wishlist & Checkout
# Routes for viewing and managing the shopping basket, wishlist, and checkout process.
@app.route('/Basket')
def basket():
    # Displays the contents of the user's shopping basket
    return render_template('Basket.html')

@app.route('/add_to_basket/<int:product_id>', methods=['POST'])
@login_required
def add_to_basket(product_id):
    # Adds a selected product to the user's basket
    return redirect(url_for('basket'))

@app.route('/wishlist')
@login_required
def wishlist():
    # Displays the user's wishlist
    return render_template('wishlist.html')

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    # Adds a product to the user's wishlist
    return redirect(url_for('wishlist'))

@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    # Removes a product from the user's wishlist
    return redirect(url_for('wishlist'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    # Handles the checkout process
    return render_template('checkout.html')

@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    # Applies a discount to the user's order
    return redirect(url_for('basket'))

@app.route('/order_summary')
@login_required
def order_summary():
    # Shows a summary of the order before confirming
    return render_template('order_summary.html')

@app.route('/order_confirmation')
@login_required
def order_confirmation():
    # Displays the order confirmation page after successful purchase
    return render_template('order_confirmation.html')

# Order Management
# Routes for tracking, canceling, requesting refunds, and viewing order history.
@app.route('/track_order/<int:order_id>')
@login_required
def track_order(order_id):
    # Allows the user to track the status of their order
    return render_template('track_order.html', order_id=order_id)

@app.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    # Cancels the specified order
    return redirect(url_for('history'))

@app.route('/request_refund/<int:order_id>', methods=['POST'])
@login_required
def request_refund(order_id):
    # Initiates a refund request for the specified order
    return redirect(url_for('history'))

@app.route('/History')
def history():
    # Displays the user's past orders
    return render_template('History.html')

# Reviews and Feedback
# Routes for viewing and submitting product reviews, and for submitting general feedback.
@app.route('/product/<int:product_id>/reviews')
def product_reviews(product_id):
    # Displays all reviews for a given product
    return render_template('product_reviews.html', product_id=product_id)

@app.route('/product/<int:product_id>/add_review', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    # Allows a user to add a review for a product
    return render_template('add_review.html', product_id=product_id)

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    # Page for submitting feedback on the platform
    return render_template('feedback.html')

# User Profile & Address Management
# Routes for viewing and editing the user profile and managing addresses.
@app.route('/profile')
@login_required
def profile():
    # Displays the user's profile information
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Allows the user to edit their profile information
    return render_template('edit_profile.html')

# Admin & Supplier Management
# Routes for admin and supplier-specific views and management tasks.
@app.route('/admin')
@login_required
@role_required('admin', 'staff')
def admin_dashboard():
    # Displays the main dashboard for admin users
    return render_template('admin_dashboard.html')

@app.route('/suppliers')
@role_required('admin', 'staff', 'suppliers')
def suppliers():
    # Lists supplier details for authorized users
    return render_template('suppliers.html')

@app.route('/admin/users')
@login_required
@role_required('admin', 'staff')
def manage_users():
    # Allows admin users to manage platform users
    return render_template('manage_users.html')

@app.route('/admin/orders')
@login_required
@role_required('admin', 'staff')
def manage_orders():
    # Allows admin users to view and manage orders
    return render_template('manage_orders.html')

@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'staff')
def add_product():
    # Allows admins to add new products to the catalog
    return render_template('add_product.html')

@app.route('/manage_inventory/<int:product_id>', methods=['POST'])
@login_required
@role_required('admin', 'staff')
def manage_inventory(product_id):
    # Updates inventory levels for a product
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/inventory')
@login_required
@role_required('admin', 'staff')
def inventory_dashboard():
    # Displays inventory overview for admin users
    return render_template('inventory_dashboard.html')

@app.route('/admin/manage_discounts', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'staff')
def manage_discounts():
    # Allows admins to create and edit discount codes
    return render_template('manage_discounts.html')

@app.route('/admin/manage_tags')
@login_required
@role_required('admin', 'staff')
def manage_tags():
    # Manages product tags for better organization
    return render_template('manage_tags.html')

@app.route('/admin/manage_bundles')
@login_required
@role_required('admin', 'staff')
def manage_bundles():
    # Manages product bundles for the store
    return render_template('manage_bundles.html')

@app.route('/admin/reports')
@login_required
@role_required('admin', 'staff')
def reports():
    # Generates reports on sales, users, and inventory
    return render_template('reports.html')

# Payment Processing
# Routes related to payments and order confirmation emails.
@app.route('/Payment')
def payment():
    # Renders a dummy payment page for transaction processing
    return render_template('Payment.html')

@app.route('/send_order_confirmation/<int:order_id>')
@login_required
def send_order_confirmation(order_id):
    # Sends an email confirming the order
    return redirect(url_for('order'))

# Customizations
# Routes for custom product orders, such as custom colors or sizes.
@app.route('/product/<int:product_id>/customize', methods=['GET', 'POST'])
@login_required
def customize_product(product_id):
    # Renders form for product customizations
    return render_template('customize_product.html', product_id=product_id)
