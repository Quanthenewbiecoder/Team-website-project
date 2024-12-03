@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get(order_id)
    return render_template('order_confirmation.html', order=order)
