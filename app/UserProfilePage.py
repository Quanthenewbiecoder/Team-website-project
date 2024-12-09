# User Profile Page
@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to access your profile.")
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    orders = Order.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        user.email = request.form['email']
        user.password = request.form['password']  # Add proper hashing for passwords
        db.session.commit()
        flash("Profile updated successfully.")

    return render_template('profile.html', user=user, orders=orders)