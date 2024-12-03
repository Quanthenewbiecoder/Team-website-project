@app.route('/')
def homepage():
    collections = Collection.query.all()
    return render_template('homepage.html', collections=collections)
