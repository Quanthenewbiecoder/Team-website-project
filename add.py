from flask import Flask, render_template

app = Flask(__name__)

# Route for homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Route for crystal collection
@app.route('/crystalcollection')
def crystal_collection():
    return render_template('crystalcollection.html')

# Other routes (add as needed)
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/products')
def products():
    return render_template('products.html')

# You can add more routes here as per your application's needs
