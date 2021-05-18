from flask import render_template, request, url_for
from application import app
from application.models import InputForm, Extract
import pickle


@app.route ('/', methods = ['GET', 'POST'])
def home():
    form = InputForm()
    print (request.form)

    if request.method == "POST" and form.validate_on_submit():
        with open ('model_building/random_forest_model.sav', 'rb') as file:
            model = pickle.load(file)
        #
        vector = Extract(request.form)
        print (vector.vector)
        feature = vector.vector
        pred = model.predict (feature)
        message = f"Your flight fare can be {pred[0]:.3f} Rb"
        return render_template('home.html', message = message, form = form)

    return render_template('home.html', form = form)