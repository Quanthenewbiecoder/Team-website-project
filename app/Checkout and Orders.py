@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user_id = 1  # Replace with logged-in user ID
        total_price = request.form['total_price']
        new_order = Order(user_id=user_id, total_price=total_price, status="Processing")
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('order_confirmation', order_id=new_order.id))
    return render_template('payment.html')
