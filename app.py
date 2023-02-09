from concurrent.futures import thread
from os import times_result
from time import time
import traceback
import sys
import logging
from flask import Flask,flash, render_template,send_file,flash,request,redirect,url_for, session, Response
import numpy
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

logging.basicConfig(filename='record.log', level=logging.DEBUG)
app = Flask(__name__)
app.config['SECRET KEY'] = 'myscretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/OnlineShop'
app.config['SESSION_TYPE'] = 'sqlalchemy'

app.config.from_object(__name__)
db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

with app.app_context():
    db.create_all()

#DATABASE CONNECTION
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database ="OnlineShop"
)

#AVAILABLE RIDES
rides = {'EE' : 'Easy Enduro', 'FT': 'First Timers', '2T': '2T Enduro'}

def time_slots(day,ride):
    new_time_slots = ['9:00-11:00','11:00-12:00','14:00-15:00','15:00-17:00']

    #Because javascript numbers week days from index=0
    day = int(day) + 1

    if day == 2:
        new_time_slots.remove('9:00-11:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
            new_time_slots.remove('14:00-15:00')
    if day == 3:
        if ride == '2T':
            new_time_slots.remove('14:00-15:00')
            new_time_slots.remove('11:00-12:00')
        if ride == 'FT':
            new_time_slots.remove('15:00-17:00')
    if day == 4:
        if ride == 'FT':
            new_time_slots.remove('15:00-17:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
            new_time_slots.remove('15:00-17:00')
    if day == 5:
        new_time_slots.remove('14:00-15:00')
        if ride == 'FT':
            new_time_slots.remove('15:00-17:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
    if day == 6:
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
            new_time_slots.remove('15:00-17:00')
    if day == 7:
        new_time_slots.remove('15:00-17:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
    if day == 1:
        new_time_slots.remove('15:00-17:00')
        if ride == 'FT':
            new_time_slots.remove('9:00-11:00')
        if ride == '2T':
            new_time_slots.remove('11:00-12:00')
    return new_time_slots

@app.route('/')
def hello_world():
    if 'user' in session.keys():
        return render_template("index.html", data = session['user'])
    else:
        return render_template("index.html")


@app.route('/getDays', methods = ["POST"])
def getDays():
    day = request.form.get("day")

    #Check that the day is numeric and 1-7
    if not day.isnumeric():
        app.logger.error("User gave non numeric value")
        return Response(status=500)
    elif 1 < int(day) > 7:
        return Response(status=500)
    
    #Check that the ride is one of the options
    ride = request.form.get("ride")

    return time_slots(day,ride)

@app.route('/style.css')
def styling():
    return render_template("static/style.css")

@app.route('/checkoutStyle.css')
def checkoutStyling():
    return render_template("static/checkoutStyle.css")

@app.route('/loginForm.css')
def loginStyling():
    return render_template("static/loginForm.css")

@app.route('/loginUser', methods = ["POST"])
def loginRequest():
    # CHECK IF THE USER EXISTS IN DATABASE
    mycursor = mydb.cursor()
    username = request.form['usrname']
    password = request.form['pass']

    mycursor.execute(f"SELECT * FROM Users WHERE username ='{username}' and password = '{password}'")
    myresult = mycursor.fetchall()
    if len(myresult) != 1:
        return redirect(url_for("loginPage"))

    session['user'] = username 
    return redirect(url_for("hello_world"))

@app.route('/registerForm.css')
def registerStyling():
    return render_template("static/registerForm.css")

@app.route('/elements.js')
def elements():
    return render_template("elements.js")

@app.route('/script.js')
def mainScript():
    return render_template("script.js")

@app.route('/registerScript.js')
def registerScript():
    return render_template("registerScript.js")

@app.route('/checkoutScript.js')
def checkoutScript():
    return render_template("checkoutScript.js")

@app.route('/login.html')
def loginPage():
    return render_template("login.html")

@app.route('/register.html')
def registerPage():
    return render_template("register.html")

checkoutData = None
@app.route('/checkout', methods = ["POST"])
def checkoutPage():
    global checkoutData
    checkoutData = request.get_json()
    print(checkoutData)

    if checkoutData is not None: 
        if not ('day' in checkoutData.keys() and checkoutData['day'].isnumeric() ): 
            print("problem with day")
            return redirect(url_for("hello_world"))
        
        if not ('month' in checkoutData.keys() and checkoutData['month'].isnumeric() ):
            print("problem with month") 
            return redirect(url_for("hello_world"))
        
        if not ('year' in checkoutData.keys() and checkoutData['year'].isnumeric() ):
            print("problem with year") 
            return redirect(url_for("hello_world"))

        if not ('people' in checkoutData.keys() and checkoutData['people'].isnumeric() ):
            print("problem with people") 
            return redirect(url_for("hello_world"))

        if not ('ride' in checkoutData.keys() and checkoutData['ride'] in rides.keys()):
            print("problem with ride") 
            return redirect(url_for("hello_world"))
        if not ('time' in checkoutData.keys() and checkoutData['time'] in time_slots(checkoutData['day'], checkoutData['ride']) ):
            print("problem with time") 
            return redirect(url_for("hello_world"))
    else:
        print("not logged in")
        return redirect(url_for("hello_world"))
    
    print("All checks passed")
    session['day'] = checkoutData['day']
    session['month'] = checkoutData['month']
    session['year'] = checkoutData['year']
    session['time'] = checkoutData['time']
    session['people'] = checkoutData['people']
    session['ride'] = rides[checkoutData['ride']]

    # return render_template("checkout.html", data=[data['day'],data['month'],data['year']])
    return "Success"
    
@app.route('/checkoutComplete', methods = ["GET"])
def checkoutComplete():
    global checkoutData
    global rides

    if not set(['day','month','year','ride','time','people']).issubset(set(session.keys())):
        return redirect(url_for("hello_world"))
    
    # data = request.get_json();
    # day = request.form.get("day")
    # month = request.form.get("month")
    # year = request.form.get("year")
    # ride = request.form.get("ride")
    
    #check if every field in checkoudata is sey and correct

    return render_template("checkout.html")

@app.route('/2T_enduro_ride.jpg')
def image1():
    return send_file("rides/2T_enduro_ride.jpg", mimetype='image/gif')

@app.route('/rides/easy_enduro_ride.jpg')
def image2():
    return send_file("rides/easy_enduro_ride.jpg", mimetype='image/gif')

@app.route('/rides/First_timers_.jpg')
def image3():
    return send_file("First_timers_.jpg", mimetype='image/gif')

@app.route('/registerUser', methods = ["POST"])
def registerUser():
    # flash('You were successfully logged in')


    #CHECK EACH FIELD IS LIKE ITS SUPPOSED TO BE AND THAT IT WONT BREAK THE PROGRAM OR THE DB
    #WHAT HAPPENS IF YOU DONT RECIEVE ALL THE FIELDS ?
    username  = request.form['usrname']
    password = request.form['pass']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']

    # UPDATE DATABASE
    sql = "INSERT INTO Users(username, password, email, FirstName, LastName) VALUES (%s, %s, %s, %s, %s)"
    val = (username, password, email, firstName, lastName)
    mydb.cursor().execute(sql, val)
    mydb.commit()

    # except:
    #     print("an error occured redirecting you")
    #     print(traceback.format_exc())
    #     print(sys.exc_info()[2])
    #     return redirect(url_for("registerPage"))

    return redirect(url_for('loginPage'))


if __name__ == '__main__':
    app.run(debug=True, port=8000, threaded=True)
