from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Car, CarType
from flask import session as login_session
import random
import string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)



# google client_secrets  client_id and application_name
CLIENT_ID = json.loads(
    open('client_secret_732755921963-bmuid1sv1cci0el3rljinhuctrhtde69.apps.googleusercontent.com.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Top Cars"



# Connect to Database and create database session
engine = create_engine('sqlite:///cars.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in  xrange(32))
    login_session['state'] = state
    # render a login template
    return render_template('login.html',STATE=state)




@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret_732755921963-bmuid1sv1cci0el3rljinhuctrhtde69.apps.googleusercontent.com.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print(result)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    #check if user is already logged in 
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    #here Database Rule to store user
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

#DISCONECT
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

    

# JSON APIs to view Restaurant Information
@app.route('/car/<int:car_id>/menu/JSON')
def showMenuJSON(car_id):
    restaurant = session.query(Car).filter_by(id=car_id).one()
    items = session.query(CarType).filter_by(
        car_id=car_id).all()
    return jsonify(CarModel=[i.serialize for i in items])


@app.route('/car/<int:car_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(car_id, menu_id):
    Menu_Item = session.query(CarType).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/car/JSON')
def restaurantsJSON():
    cars = session.query(Car).all()
    return jsonify(cars=[r.serialize for r in cars])







# this for handling search page in new page and  I added search
#alghrothem to showCars() without new page
@app.route('/search/', methods=['GET', 'POST'])
def makeSearch():
  
    if request.method == 'POST':        
                              
        myid = request.form['search']
        car = session.query(CarType).filter_by(name = myid).one()
        return render_template('menu.html', car = car)
       
    else:
        
        return render_template('search.html')
    

# Show all restaurants
@app.route('/')
@app.route('/car/', methods=['GET', 'POST'])
def showCars():    
    cars = session.query(Car).order_by(asc(Car.name))
    #check this next 10 lines Important 
    #it takes 3 hours to get it
    #I couldn't make join syntax in flask so I created my own join function
   
    get_lastAdded = session.query(CarType).order_by(CarType.id.desc()).limit(5).all()
    
    lastAdded = []
    index = 0
    
    for i in get_lastAdded:
        carName = session.query(Car).filter_by(id = i.car_id).one()        
                    
        class myObject:            
            model = i.name            
            name = carName.name
            myid = carName.id
        
        lastAdded.append(myObject)
# search function
    if request.method == 'POST':
        search_text = request.form['search']
        car = session.query(CarType).filter_by(name = search_text).one()
        tests = session.query(CarType).filter_by(name = search_text).all()
        return render_template('menu.html', car = car, car_id = car.car_id, menu_id = car.id, tests = tests)        
        
    
    return render_template('cars.html', cars = cars, last = lastAdded)

# Create a new restaurant


@app.route('/car/new/', methods=['GET', 'POST'])
def newCar():
    #check if login_session didn't store username
    #tha'ts mean not loged in redirct to login with flash message
    if 'username' not in login_session:
        flash('Please Login In To Add new Car')
        return redirect('/login')
    if request.method == 'POST':
        newCar = Car(image=request.form['image'], name=request.form['name'])        
        session.add(newCar)
        image = newCar.image
        flash('New Car %s Successfully Created' % newCar.name)        
        session.commit()
        return redirect(url_for('showCars'))
    else:
        return render_template('newCar.html')

# Edit a restaurant
#to make user made item can edit it
# add another clumon id DB in Car for creator
# compare it with session_login['username']

@app.route('/car/<int:car_id>/edit/', methods=['GET', 'POST'])
def editCar(car_id):
    #check if login_session didn't store username
    if 'username' not in login_session:
        flash('Please Login In To edit Car and you must be the createor ')
        return redirect('/login')
    
    editedCar = session.query(
        Car).filter_by(id=car_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCar.name = request.form['name']
            flash('Car Successfully Edited %s' % editedCar.name)
            return redirect(url_for('showCars'))
    else:
        return render_template('editCar.html', car=editedCar)


# Delete a restaurant
@app.route('/car/<int:car_id>/delete/', methods=['GET', 'POST'])
def deleteCar(car_id):
    if 'username' not in login_session:
        flash('Please Login In To Delete Car and you must be the createor ')
        return redirect('/login')
        
    carToDelete = session.query(
        Car).filter_by(id=car_id).one()
    if request.method == 'POST':
        session.delete(carToDelete)
        flash('%s Successfully Deleted' % carToDelete.name)
        session.commit()
        return redirect(url_for('showCars', car_id=car_id))
    else:
        return render_template('deleteCar.html', car=carToDelete)

# Show a restaurant menu


@app.route('/car/<int:car_id>/')
@app.route('/car/<int:car_id>/menu/')
def showMenu(car_id):
    car = session.query(Car).filter_by(id=car_id).one()
    items = session.query(CarType).filter_by(
        car_id=car_id).all()
    
    return render_template('menu.html', items=items, car=car)


# Create a new menu item
@app.route('/car/<int:car_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(car_id):
    if 'username' not in login_session:
        flash('Please Login In To Create new Car Model')
        return redirect('/login')
        
    car = session.query(Car).filter_by(id=car_id).one()
    if request.method == 'POST':
        newItem = CarType(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], car_id=car_id)
        session.add(newItem)
        session.commit()
        flash('New Car Model %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', car_id=car_id))
    else:
        return render_template('newmenuitem.html', car_id=car_id)

# Edit a menu item


@app.route('/car/<int:car_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(car_id, menu_id):
    if 'username' not in login_session:        
        flash('Please Login In To Edit Car Model and you must be the createor ')
        return redirect('/login')
        
    editedItem = session.query(CarType).filter_by(id=menu_id).one()
    car = session.query(Car).filter_by(id=car_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']        
        session.add(editedItem)
        session.commit()
        flash('Car Model Successfully Edited')
        return redirect(url_for('showMenu', car_id=car_id))
    else:
        return render_template('editmenuitem.html', car_id=car_id, menu_id=menu_id, item=editedItem)


# Delete a menu item
@app.route('/car/<int:car_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(car_id, menu_id):
    if 'username' not in login_session:
        flash('Please Login In To Delete Car Model and you must be the createor ')
        return redirect('/login')
        
    car = session.query(Car).filter_by(id=car_id).one()
    itemToDelete = session.query(CarType).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Car Model Successfully Deleted')
        return redirect(url_for('showMenu', car_id=car_id))
    else:
        return render_template('deleteMenuItem.html', car=car, item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
