@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password: 
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')
