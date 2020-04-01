#from django.db import models
#from django.utils import timezone



from app import db, app
from datetime import datetime



#GD - Create
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from app.azure_db import azure_db
#import urllib.parse 
#import pyodbc
#app = Flask(__name__)
#a_db = azure_db()
#print(a_db.getConString())
#params = urllib.parse.quote_plus(a_db.getConString())
#app.config['SQLALCHEMY_DATABASE_URI'] ="mssql+pyodbc:///?odbc_connect=%s" % params
#db = SQLAlchemy(app)




class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Needed_item = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    country = db.Column(db.String(200))

    def __str__(self):
        return self.item

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    mobile = db.Column(db.String(20))
    landlinenumber = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    long = db.Column(db.Float)
    lat = db.Column(db.Float)
    sex = db.Column(db.String(10))
    age =  db.Column(db.Integer)



    inneed = db.Column(db.Integer)
    helper = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return self.cellnumber

   
class UserVerify(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ID1 = db.Column(db.String(100))
    ID2 = db.Column(db.String(100))
    ID3 = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __str__(self):
        return self.cellnumber

#print('create',db.create_all())
#print('commit',db.session.commit())