from flask import render_template, request, url_for
from application import app
from application.models import InputForm


@app.route ('/', methods = ['GET', 'POST'])
def home():
    form = InputForm()
    if request.method == "POST" and form.validate_on_submit():
        message = "success"
        print (message)
        return render_template('home.html', message = message, form = form)

    return render_template('home.html', form = form)