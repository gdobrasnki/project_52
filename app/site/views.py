#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import random
from flask import Blueprint, render_template, url_for, flash, session, redirect
from flask_googlemaps import Map


from .data import FOOD, HYGIENE, SEX, WANTS, FNM, FNF, LN
from .utils import get_items, get_names

#, make_person

from app import db, app
from app.models import Items, User, UserVerify


#Cause i cont know better
from sqlalchemy import create_engine
from app.azure_db import azure_db
import urllib.parse 
import pyodbc
import pandas as pd

from app.twilio_verify import request_verification_token, check_verification_token

from app.forms import Confirm2faForm, TwoFactorForm, AskForAssistance

from twilio.rest import Client

import requests
 
from flask import request



a_db = azure_db()
#print(a_db.getConString())
params = urllib.parse.quote_plus(a_db.getConString())











www = Blueprint("site", __name__)

@www.route("/", methods=["GET", "POST"])
def mapview():

    if request.method == 'POST':
        userloc = request.get_json()
        print('userloc',userloc)
        for val in userloc:
            print(val)






    form = AskForAssistance()
    print(form.submit.data, form.validate())

    print('form val sub', form.validate_on_submit())
#    if form.validate_on_submit():

    
    
    if form.submit.data:
        print('submited')

        geodata = ConvertPostalLatLong(form.postal.data)
        print('postal dict ', geodata)
        age = random.randint(55, 95)
        sex = random.choice(SEX)
        needs = random.choice(FOOD)
        wants = random.choice(WANTS)
        print('needwants ', needs,wants)
        if sex == 'Male':
            firstname =random.choice(FNM)
        else:
            firstname =random.choice(FNF)
        lastname = random.choice(LN)


        fn = firstname
        ln=lastname 


        mobile=form.phone.data
        landline=''
        lat=geodata['lat']
        lng=geodata['lng']
        inneed=random.randint(0, 5)

        helper=0


        print('person ',personfromform(fn,ln,age,sex,needs,wants,mobile,landline,lat,lng,inneed,helper))

        redirect(url_for('site.mapview'))
        #return render_template("example.html",
        #                mymap=mymap,
        #                sndmap=sndmap,
        #                form = form,
        #                listoflist=listoflist)










    markers2 = []
    
    #Get list from Azure



    sql = 'select * from dbo.[user]'
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
	
    print(sql)
    data = pd.read_sql(sql, engine)
    #print(data)

    for index,row in data.iterrows():
        #print(row)
        #print(row['lat'])

        lat = float(row['lat'])
        lng = float(row['long'])
        pers = ''
        needs = random.choice(FOOD)
        wants = random.choice(WANTS)

        person = "<p>age:{}</p><p>sex:{}</p><p>needs:{}</p><p>wants:{}<p>"
        age = row['age']
        sex = row['sex']
        pid = row['id']

        person = person.format(age, sex, needs,wants)
        person += '<a href="/seeperson4/'+str(pid)+'">I can help in 4 hours or less</a>'
        person += '<div><a href="/seeperson8/'+str(pid)+'">I can help in 8 hours or less</a></div>'
        


        markers2.append(
            {
                "icon": "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
                "lat": lat,
                "lng": lng,
                "infobox": person,
            }
        )















    print('mapview')
    food = get_items(FOOD)
    hygiene = get_items(HYGIENE)
    listoflist = [*food, *hygiene]

    #mymap = Map(
    #    identifier="view-side",
    #    lat=53.5461,
    #    lng=-113.4938,
    #    markers=[(53.5461, -113.4938)]
    #)

    
    


    #Forms
    #Grab list of items needed



    sndmap = Map(
        identifier="sndmap",
        lat=53.5461,
        lng=-113.4938,
        zoom = 6,
        style="height:800px;width:100%;margin:0;",
        markers=markers2
    )

    #print('list o list ', listoflist)
    #for item in listoflist:
        #print(item)









    return render_template("example.html",
                            #mymap=mymap,
                            sndmap=sndmap,
                            form = form,
                            listoflist=listoflist,
                            
                            gapi="https://maps.googleapis.com/maps/api/js?key="+app.config['GAPI']+"&callback=initMap"
                            )











@www.route("/seeperson4/<page>", methods=["GET", "POST"])
def seeperson4(page):
    #Store the tenative commit
    session['tenativeCommitId'] = page




    #Get user ID again
    #Tell user he is going to commit to this and get a verification token.
    user = User.query.filter_by(id=page).first()
    print(user.id,user.firstname)

    needs = random.choice(FOOD)
    wants = random.choice(WANTS)

    message = "You have commited to helping " + user.firstname + ". A "+str(user.age) + " year old " + user.sex+ ". You are making a promise that you can get to them in the next 4 hours. They need " +needs+ " and want " + wants + ". Please enter your mobile number as we will use it to verify you and send you the contact info of the User."






    form = TwoFactorForm()
    
    if form.validate_on_submit():
        #flash('2fa requested for phone {}'.format(form.phone.data))
        
        #NA only 
        session['mobile'] = "+" + str(form.phone.data)
        session['UserInNeed'] = user.id  

        request_verification_token(session['mobile'])





        return redirect(url_for('site.confirm_2fa'))

    #    return redirect(url_for('index'))
    return render_template('2fa.html',  title='2fa', form=form, Message = message)






    return render_template('2fa.html',  title='2fa', form=form)



@www.route("/seeperson8/<page>", methods=["GET", "POST"])
def seeperson8(page):
    #Store the tenative commit
    session['tenativeCommitId'] = page




    #Get user ID again
    #Tell user he is going to commit to this and get a verification token.
    user = User.query.filter_by(id=page).first()
    print(user.id,user.firstname)

    needs = random.choice(FOOD)
    wants = random.choice(WANTS)

    message = "You have commited to helping " + user.firstname + ". A "+str(user.age) + " year old " + user.sex+ ". You are making a promise that you can get to them in the next 8 hours. They need " +needs+ " and want " + wants + ". Please enter your mobile number as we will use it to verify you and send you the contact info of the User."


    form = TwoFactorForm()

    

    if form.validate_on_submit():
        #flash('2fa requested for phone {}'.format(form.phone.data))
        

        session['mobile'] = "+1" + str(form.phone.data)
        session['UserInNeed'] = user.id  

        request_verification_token(session['mobile'])



        return redirect(url_for('site.confirm_2fa'))

    #    return redirect(url_for('index'))
    return render_template('2fa.html',  title='2fa', form=form, Message = message)






    return render_template('2fa.html',  title='2fa', form=form)









@www.route("/makeppl", methods=["GET", "POST"])
def makeppl():
    print('mapview')
    food = get_items(FOOD)
    hygiene = get_items(HYGIENE)
    listoflist = [*food, *hygiene]

    mymap = Map(
        identifier="view-side",
        lat=53.5461,
        lng=-113.4938,
        markers=[(53.5461, -113.4938)]
    )

    markers2 = []
    for _ in range(1, 19):
        lat = random.randrange(5346000, 5363000)/100000
        lng = random.randrange(11342000, 11361000)/100000
        lng = -lng

        markers2.append(
            {
                "icon": "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
                "lat": lat,
                "lng": lng,
                "infobox": make_person(),
            }
        )

    sndmap = Map(
        identifier="sndmap",
        lat=53.5461,
        lng=-113.4938,
        style="height:600px;width:100%;margin:0;",
        markers=markers2
    )

    return render_template("example.html",
                            mymap=mymap,
                            sndmap=sndmap,
                            listoflist=listoflist)




@www.route("/createitems", methods=["GET", "POST"])
def createsome():

#user1 = User(username='test4')
#db.session.add(user1)
#db.session.commit()

#FOOD = ['Canned Vegtables', 'Canned Meat', 'Fresh Vegtables', 'Fresh Meat', 'Dried Beans']

    i1 = Items(Needed_item='Canned Vegtables',country='Canada')
    i2 = Items(Needed_item='Canned Vegtables',country='Canada')
    i3 = Items(Needed_item='Fresh Vegtables',country='Canada')
    i4 = Items(Needed_item='Bread',country='Canada')
    i5 = Items(Needed_item='Eggs',country='Canada')
    i6 = Items(Needed_item='Milk',country='Canada')
    i7 = Items(Needed_item='Butter',country='Canada')
   
    db.session.add(i1)
    db.session.add(i2)
    db.session.add(i3)
    db.session.add(i4)
    db.session.add(i5)
    db.session.add(i6)
    db.session.add(i7)
    db.session.commit()

    return 'created :'


def personfromform(fn,ln,age,sex,needs,wants,mobile,landline,lat,lng,inneed,helper):
    p1 = User(mobile = mobile, landlinenumber = landline, age = age, sex = sex, firstname = fn ,lastname = ln , inneed = inneed, helper = helper, long = lng, lat = lat)
    db.session.add(p1)
    db.session.commit()

    print('p1 id', p1.id)
    db.session.remove()

    return 'done'



def make_person():
    person = "<p>age:{}</p><p>sex:{}</p><p>needs:{}</p><p>wants:{}<p>"
    age = random.randint(55, 95)
    sex = random.choice(SEX)
    needs = random.choice(FOOD)
    wants = random.choice(WANTS)
    print('needwants ', needs,wants)
    if sex == 'Male':
        firstname =random.choice(FNM)
    else:
        firstname =random.choice(FNF)
    lastname = random.choice(LN)




    #Just for demo purpose


    lat = random.randrange(5346000, 5363000)/100000
    lng = random.randrange(11342000, 11361000)/100000


    p1 = User(mobile = '5555551234', landlinenumber = '', age = age, sex = sex, firstname = firstname ,lastname = lastname , inneed = random.randint(1, 6), helper = 0, long = lng, lat = lat)
    db.session.add(p1)
    db.session.commit()
    print('p1 id', p1.id)

    person = person.format(age, sex, needs,wants)
    person += '<a href="/seeperson4/'+str(p1.id)+'">I can help in 4 hours or less</a>'
    person += '<div><a href="/seeperson8/'+str(p1.id)+'">I can help in 8 hours or less</a></div>'

    return person



@www.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@www.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500



#Verification






@www.route('/2fa', methods=['GET', 'POST'])
def twofa():
    form = TwoFactorForm()

    if form.validate_on_submit():
        flash('2fa requested for phone {}'.format(form.phone.data))
        request_verification_token(form.phone.data)
        session['mobile'] = form.phone.data

        return redirect(url_for('site.confirm_2fa'))

    #    return redirect(url_for('index'))
    return render_template('2fa.html',  title='2fa', form=form)



@www.route('/confirm_2fa', methods=['GET', 'POST'])
def confirm_2fa():
    form = Confirm2faForm()
    print('test')

    if form.validate_on_submit():

        phone = session['mobile']
        #need a better way for this feb 24

        if len(phone) == 10:
            phone = '+1' + session['mobile']


        print("c2fa phone with +1 is ", phone, 'tok data',form.token.data)
        print('1')
        if check_verification_token(phone, form.token.data):
            #del session['mobile']
            print('verified')



            user = User.query.filter_by(id=session['UserInNeed']).first()

            HelpNextDoorPhoneNumber = "+15877410102"

            smsmsg = "Thank you. The individual you are assisting is " + user.firstname + ". Their Phone Number (Or Agency assisting) is " + user.mobile + " Please contact them directly to setup a Time and location for drop off. Thank you again for helping your Community."

            tennant_twilio_account_sid = app.config['TWILIO_ACCOUNT_SID']
            tennant_twilio_auth_token = app.config['TWILIO_AUTH_TOKEN']

            #For Debug Only Glen Only

            #Hardcoded for Solut?
            client = Client(tennant_twilio_account_sid, tennant_twilio_auth_token)
            message = client.messages.create(body=(smsmsg),from_=HelpNextDoorPhoneNumber, to=session['mobile'])
            returnstring = message











            return redirect(url_for('site.verifyandcommit'))

        else:
            form.token.errors.append(('Invalid token'))

    return render_template('verify_2fa.html', form=form)



@www.route('/verifyandcommit', methods=['GET', 'POST'])
def verifyandcommit():

    return "Thank you. You have commited and will Recieve the contact info of the Person in need shortly"




#more utils
def ConvertPostalLatLong(postal):


    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
    #    'address': '221B Baker Street, London, United Kingdom',
    #    'sensor': 'false',
    #    'region': 'uk',
        'key': app.config['GAPI'],
        'components':'postal_code:' + postal
    }

    #    'components':'country:GB|postal_code:CH21EU'


    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()

    # Use the first result
    result = res['results'][0]

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    print('(lat, lng) = ({lat}, {lng})'.format(**geodata))
    return geodata

