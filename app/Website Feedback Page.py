# Website Feedback Page
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user_id = session.get('user_id')
        feedback_text = request.form['feedback']
        rating = request.form.get('rating')

        new_feedback = Feedback(user_id=user_id, text=feedback_text, rating=rating)
        db.session.add(new_feedback)
        db.session.commit()
        flash("Thank you for your feedback!")
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback.html', feedbacks=feedbacks)