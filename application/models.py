from wtforms import SelectField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from flask_wtf.form import FlaskForm
from wtforms.validators import DataRequired, NumberRange
import numpy as np
import pandas as pd


def one_hot_label (num_classes, index):
    one_hot = np.zeros ((1, num_classes))
    if index != -1:
        one_hot [0][index] = 1
    return one_hot


class Extract:
    columns = ['Total_Stops', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
       'Airline_Jet Airways', 'Airline_Jet Airways Business',
       'Airline_Multiple carriers',
       'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
       'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
       'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
       'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
       'Destination_Kolkata', 'Destination_New Delhi', 'Date_of_Journey_day',
       'Date_of_Journey_month', 'Dep_Time_hour', 'Dep_Time_min',
       'Arrival_Time_hour', 'Arrival_Time_min', 'Duration_hour',
       'Duration_min']

    # x = pd.DataFrame(x, columns=['Total_Stops', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
    #                              'Airline_Jet Airways', 'Airline_Jet Airways Business',
    #                              'Airline_Multiple carriers',
    #                              'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
    #                              'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
    #                              'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
    #                              'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
    #                              'Destination_Kolkata', 'Destination_New Delhi', 'Date_of_Journey_day',
    #                              'Date_of_Journey_month', 'Dep_Time_hour', 'Dep_Time_min',
    #                              'Arrival_Time_hour', 'Arrival_Time_min', 'Duration_hour',
    #                              'Duration_min'])

    def __init__ (self, form):
        self.form = form


    def __getitem__(self, column):
        return int (self.form[column])

    def one_hot_column (self, column, num_choices):
        if int(self.form[column]) < num_choices:
            airline_encode = one_hot_label(num_choices, int(self.form[column]))
        else:
            airline_encode = one_hot_label(num_choices, -1)
        self.feature_vector = np.concatenate ((self.feature_vector, airline_encode), axis = 1)

    def extract_date (self, column):
        date = self.form[column].split ('-')
        for i in range (3):
            date[i] = int (date[i])
        self.feature_vector = np.concatenate ((self.feature_vector, np.array([[date[2], date[1]]])), axis = 1)

    def extract_time (self, column):
        time = self.form [column].split (':')
        for i in range (2):
            time [i] = int (time[i])
        self.feature_vector = np.concatenate ((self.feature_vector, np.array ([time])), axis = 1)


    @property
    def vector (self):
        total_stops = self['total_stops']
        self.feature_vector = np.array([[total_stops]])
        self.one_hot_column('airline', 11)
        self.one_hot_column('source', 4)
        self.one_hot_column('destination', 5)
        self.extract_date('journey_date')
        self.extract_time('dep_time')
        self.extract_time('arrival_time')
        self.feature_vector = np.concatenate ((self.feature_vector, np.array([[self['hour_duration']]])), axis = 1)
        self.feature_vector = np.concatenate((self.feature_vector, np.array([[self['min_duration']]])), axis = 1)

        # return pd.DataFrame (self.feature_vector, columns=self.columns)
        return self.feature_vector


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
                                    ('10', "Vistara Premium economy"),
                                    ('11', "Jet Airways")],
                           validators= [DataRequired()])

    source = SelectField ("Source",
                          choices=[('0', "Chennai"),
                                   ('1', "Delhi"),
                                   ('2', "Kolkata"),
                                   ('3', "Mumbai"),
                                   ('4', "Banglore")],
                          validators= [DataRequired()])

    destination = SelectField ("Destination",
                               choices=[('0', "Cochin"),
                                        ('1', "Delhi"),
                                        ('2', "Hyderabad"),
                                        ('3', "Kolkata"),
                                        ('4', "New Delhi"),
                                        ('5', "Banglore")],
                               validators=[DataRequired()])

    journey_date = DateField ("Journey time", format = "%Y-%m-%d", validators=[DataRequired()])
    dep_time = TimeField("Dep time", validators=[DataRequired()])
    arrival_time = TimeField ("Arrival time", validators=[DataRequired()])
    # duration = TimeField ("Duration", format= "%H:%M")
    hour_duration = IntegerField ("Hours", validators=[DataRequired(), NumberRange(min=0, max= 100)])
    min_duration = IntegerField("Minutes", validators=[NumberRange(min=0, max=59)])
    submit = SubmitField ("Predict")



