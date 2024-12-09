# Discount Page
@app.route('/apply-discount', methods=['POST'])
def apply_discount():
    code = request.form['discount_code']
    discount = Discount.query.filter_by(code=code).first()

    if not discount:
        flash("Invalid discount code.")
        return redirect(url_for('cart'))

    # Logic to validate discount conditions and apply it to the order/cart
    flash("Discount applied successfully.")
    return redirect(url_for('cart'))