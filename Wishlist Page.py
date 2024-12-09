# Wishlist Page
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to access your wishlist.")
        return redirect(url_for('login'))

    wishlist = Wishlist.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        product_id = request.form['product_id']
        new_item = WishlistItem(wishlist_id=wishlist.id, product_id=product_id)
        db.session.add(new_item)
        db.session.commit()
        flash("Item added to wishlist.")

    items = WishlistItem.query.filter_by(wishlist_id=wishlist.id).all()
    return render_template('wishlist.html', items=items)