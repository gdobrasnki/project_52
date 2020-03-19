from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import random
import decimal

from forms import RegisterNeed

app = Flask(__name__, template_folder=".",static_folder="static")

GoogleMaps(app, key="")
#GoogleMaps(app, key="AIza...")




@app.route("/", methods = ['GET','POST'])
def mapview():

    form = RegisterNeed(request.form)
#    if request.method == 'POST':
#        flash('Working','success') 
          
    if form.validate_on_submit():
        print('test')


    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=53.5461,
        lng=-113.4938,
        markers=[(53.5461, -113.4938)]
    )


    markers2 = []
    #list of markers
    for x in range(1,20):
        lat1 = random.randrange(5346000, 5363000)/100000
        lon1 = random.randrange(11342000, 11361000)/100000
        lon1 = 0- lon1
        print(lat1,lon1)
        markers2.append(
                      {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
#             'icon': 'http://www.entypo.com/images/hand.svg',
#             'icon': 'bed.png',
             'lat': lat1,
             'lng': lon1,
             'infobox': MakePerson()
          }
            )


    sndmap = Map(
        identifier="sndmap",
        lat=53.5461,
        lng=-113.4938,
        style ='height:600px;width:100%;margin:0;',
        markers = markers2
    )

    return render_template('example.html', mymap=mymap, sndmap=sndmap,form=form)



def MakePerson():
    sex = ['male','female']
    needs = ['Vegtables', 'Canned goods', 'Hand soap', 'Toothpaste', 'Toilet Paper']
    #days_left = range (0,10)
    wants = ['Phone Call', 'Video Call', 'Book','DVDs']
    

    #needs 
    rando=random.randrange(55, 95)
    Person = ""
    Person += "age:"+str(rando)+"<p>"
    rando=random.randrange(0, 2)
    Person += "sex:"+sex[rando]+"<p>"
    rando=random.randrange(0, 5)
    Person += "Needs:"+needs[rando]
    del needs[rando]
    
    rando=random.randrange(0, 4)
    Person += ", "+needs[rando]+"<p>"

    rando=random.randrange(0, 4)
    Person += "Wants:"+wants[rando]
    del wants[rando]
    rando=random.randrange(0, 3)
    Person += ", "+wants[rando]+"<p>"
    Person += '<a href="http://google.com">I can help in 4 hours or less</a>'
    Person += '<div class="uber-google-maps-info-window-field"><a href="http://google.com">I can help in 12 hours or less</a></div>'
    
    return Person


app.config['SECRET_KEY'] = "generated key"

if __name__ == "__main__":
    app.run(debug=True)