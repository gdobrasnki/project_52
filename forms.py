from flask_wtf import FlaskForm
from wtforms import (Form, StringField, TextAreaField, SelectField
                    , PasswordField, SubmitField, BooleanField, FloatField, DateField)
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, EqualTo, Required, NumberRange, Optional
#from upspark.models import User, Domain
from datetime import date


class RegisterNeed(FlaskForm):
    age= StringField('Age ', validators=[])
    firstname = StringField('First', validators=[])
    lastname = StringField('Last',  validators=[])

    sex= StringField('Last',  validators=[])
    #sex = RadioField('Sex', choices=[('Female','Female'),('Male','Male'),('N\A','')])

    needs = StringField('Needs',  validators=[])
    wants= StringField('Wants',  validators=[])
    phonenumber = StringField('Phonenumber (7 digits)', validators=[])
    postal = StringField('Postal Code',  validators=[])
    
    submit = SubmitField('submit')

