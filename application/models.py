from wtforms import SelectField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from flask_wtf.form import Form, FlaskForm
from wtforms.validators import DataRequired, NumberRange


class InputForm (FlaskForm):
    total_stops = SelectField ("Total Stops",
                               choices=[('0', "Non times"), ('1', "1 time"), ('2', "2 times"), ('3', "3 times"), ('4', "4 times")],
                                        validators = [DataRequired()])

    airline = SelectField ("Airline",
                           choices=[('0', "Air India"),
                                    ('1', "GoAir"),
                                    ('2', "IndiGo"),
                                    ('3', "Jet Airways"),
                                    ('4', "Jet Airways Business"),
                                    ('5', "Multiple carriers"),
                                    ('6', "Multiple carriers Premium economy"),
                                    ('7', "SpiceJet"),
                                    ('8', "Trujet"),
                                    ('9', "Vistara"),
                                    ('10', "Vistara Premium economy")],
                           validators= [DataRequired()])

    source = SelectField ("Source",
                          choices=[('0', "Chennai"),
                                   ('1', "Delhi"),
                                   ('2', "Kolkata"),
                                   ('3', "Mumbai")],
                          validators= [DataRequired()])

    destination = SelectField ("Destination",
                               choices=[('0', "Cochin"),
                                        ('1', "Delhi"),
                                        ('2', "Hyderabad"),
                                        ('3', "Kolkata"),
                                        ('4', "New Delhi")],
                               validators=[DataRequired()])

    journey_date = DateField ("Journey time", format = "%Y-%m-%d", validators=[DataRequired()])
    dep_time = DateField("Dep time", format= "%Y-%m-%d", validators=[DataRequired()])
    arrival_time = DateField ("Arrival time", format= "%Y-%m-%d", validators=[DataRequired()])
    # duration = TimeField ("Duration", format= "%H:%M")
    hour_duration = IntegerField ("Hours", validators=[DataRequired(), NumberRange(min=0, max= 100)])
    min_duration = IntegerField("Minutes", validators=[DataRequired(), NumberRange(min=0, max=59)])
    submit = SubmitField ("Predict")