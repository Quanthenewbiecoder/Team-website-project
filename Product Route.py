@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)
