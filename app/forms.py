#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import (Form, StringField, TextAreaField, SelectField
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


class AskForAssistance(FlaskForm):
    phone = StringField('Phone')
    postal = StringField('Postal')
    time = SelectField(
    u'When Do you need it by?',
    choices = [('4 hours', '4 hours'), ('8 hours', '8 hours')]
    )


    submit = SubmitField('Send')