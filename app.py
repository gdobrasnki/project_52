# using python 3
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from data import  FOOD,HYGIENE

#gmap
from flask_googlemaps import GoogleMaps, Map
import random
import decimal

app = Flask(__name__)


#gmap
GoogleMaps(app, key="")



# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'some?bamboozle#string-foobar'
# Flask-Bootstrap requires this line
Bootstrap(app)
# this turns file-serving to static, using Bootstrap files installed in env
# instead of using a CDN
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    name = StringField('Which actor is your favorite?', validators=[Required()])
    submit = SubmitField('Submit')




    #Gmap


    
@app.route("/hfn", methods = ['GET','POST'])
def mapview():

    food = get_items(FOOD)
    hygiene = get_items(HYGIENE)
    print(food)
    listoflists = []
    listoflists.append(food)
    listoflists.append(hygiene)

    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    
    #form = NameForm()
    message = ""
    


    #form = RegisterNeed(request.form)
#    if request.method == 'POST':
#        flash('Working','success') 
          
    #if form.validate_on_submit():
    #    print('test')


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

    return render_template('example.html', mymap=mymap, sndmap=sndmap, listoflists=listoflists)



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









# retrieve all the names from the dataset and put them into a list
def get_names(source):
    names = []
    for row in source:
        name = row["name"]
        names.append(name)
    return sorted(names)



# define functions to be used by the routes

# retrieve all the names from the dataset and put them into a list
def get_items(source):
    print(type(source))
    items = []
    for x in source:
        items.append(x)
    return sorted(items)





# find the row that matches the id in the URL, retrieve name and photo
def get_actor(source, id):
    for row in source:
        if id == str( row["id"] ):
            name = row["name"]
            photo = row["photo"]
            # change number to string
            id = str(id)
            # return these if id is valid
            return id, name, photo
    # return these if id is not valid - not a great solution, but simple
    return "Unknown", "Unknown", ""

# find the row that matches the name in the form and retrieve matching id
def get_id(source, name):
    for row in source:
        if name == row["name"]:
            id = row["id"]
            # change number to string
            id = str(id)
            # return id if name is valid
            return id
    # return these if id is not valid - not a great solution, but simple
    return "Unknown"

# all Flask routes below

# two decorators using the same function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    names = get_names(ACTORS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name in names:
            # empty the form field
            form.name.data = ""
            id = get_id(ACTORS, name)
            # redirect the browser to another route and template
            return redirect( url_for('actor', id=id) )
        else:
            message = "That actor is not in our database."
    return render_template('index.html', names=names, form=form, message=message)


@app.route('/actor/<id>')
def actor(id):
    # run function to get actor data based on the id in the path
    id, name, photo = get_actor(ACTORS, id)
    if name == "Unknown":
        # redirect the browser to the error template 
        return render_template('404.html'), 404
    else:
        # pass all the data for the selected actor to the template
        return render_template('actor.html', id=id, name=name, photo=photo)


# routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
