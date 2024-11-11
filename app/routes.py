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

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Add login logic here
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Add registration logic here
    return render_template('register.html')

# Password change route (for forgotten passwords)
@app.route('/Password_change')
def password_change():
    return render_template('Password_change.html')

# Contact form route
@app.route('/Contact')
def contact():
    return render_template('Contact.html')

# About Us page route
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

# Product page route
@app.route('/Product')
def product():
    return render_template('Product.html')

# Basket page route
@app.route('/Basket')
def basket():
    return render_template('Basket.html')

# Order history page route
@app.route('/History')
def history():
    return render_template('History.html')

# Payment form route (dummy payment page)
@app.route('/Payment')
def payment():
    return render_template('Payment.html')

# Admin Panel
@app.route('/admin')
@login_required
def admin_dashboard():
    # Logic for admin dashboard
    return render_template('admin_dashboard.html')

# Product Detail
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    # Fetch and display product details
    return render_template('product_detail.html', product_id=product_id)

# Add item to bastket and Wishlist:
@app.route('/add_to_basket/<int:product_id>', methods=['POST'])
@login_required
def add_to_basket(product_id):
    # Logic to add product to basket
    return redirect(url_for('basket'))

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    # Logic to add product to wishlist
    return redirect(url_for('wishlist'))

# Order Confirmation and Summary:
@app.route('/order_summary')
@login_required
def order_summary():
    # Display order summary
    return render_template('order_summary.html')

@app.route('/order_confirmation')
@login_required
def order_confirmation():
    # Display order confirmation details
    return render_template('order_confirmation.html')

# User Profile:
@app.route('/profile')
@login_required
def profile():
    # Display user profile
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Logic for editing user profile
    return render_template('edit_profile.html')

# Order discount
@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    # Logic to apply discount code
    return redirect(url_for('basket'))

# Order Tracking
@app.route('/track_order/<int:order_id>')
@login_required
def track_order(order_id):
    # Logic to track the order status
    return render_template('track_order.html', order_id=order_id)
