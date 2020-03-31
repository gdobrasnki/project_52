#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import (Form, StringField, TextAreaField
                    , PasswordField, SubmitField, BooleanField)
from wtforms.validators import DataRequired
#from app.models import User, Domain



    #2fa
class TwoFactorForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Send')

class Confirm2faForm(FlaskForm):
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField(('Verify'))

