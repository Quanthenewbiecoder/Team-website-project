from flask import render_template, redirect, url_for
from app import app

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/login')  # form to login
def login():
    return render_template('login.html')

@app.route('/register')  # form to register
def register():
    return render_template('register.html')

@app.route('/Password_change')  # form to change password if the user forgot it
def password_change():
    return render_template('Password_change.html')

@app.route('/Contact')  # contact sending form
def contact():
    return render_template('Contact.html')

@app.route('/about_us')  # about us page
def about_us():
    return render_template('about_us.html')

@app.route('/Product')  # product page
def product():
    return render_template('Product.html')

@app.route('/Basket')  # basket page
def basket():
    return render_template('Basket.html')

@app.route('/History')  # history page
def history():
    return render_template('History.html')

@app.route('/Payment')  # form for the payment dummy
def payment():
    return render_template('Payment.html')
