#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_sqlalchemy import SQLAlchemy
from app.azure_db import azure_db

import urllib.parse 

#?
import os
from app.azure_db import azure_db


app = Flask(__name__)
app.config.from_object("config")

a_db = azure_db()
params = urllib.parse.quote_plus(a_db.getConString())

app.config['SQLALCHEMY_DATABASE_URI'] ="mssql+pyodbc:///?odbc_connect=%s" % params

#twil
app.config['TWILIO_ACCOUNT_SID'] = os.getenv('TWILIO_ACCOUNT_SID')
app.config['TWILIO_AUTH_TOKEN'] = os.getenv('TWILIO_AUTH_TOKEN')
app.config['TWILIO_VERIFY_SERVICE_ID'] = os.getenv('TWILIO_VERIFY_SERVICE_ID')

app.config['GAPI'] = os.getenv('GAPI')






a_db = azure_db()
params = urllib.parse.quote_plus(a_db.getConString())


Bootstrap(app)
GoogleMaps(app, key=app.config['GAPI'] )
db = SQLAlchemy(app)




from .site.views import www

app.register_blueprint(www)
