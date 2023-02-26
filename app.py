from calendar import month
from concurrent.futures import thread
from html.entities import html5
# from crypt import methods
import os
import sys
import logging
from flask import Flask,flash, render_template,send_file,request,redirect,url_for, session, Response
import pandas as pd
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import timedelta
from countries import available_countries
from datetime import datetime
from dotenv import load_dotenv
import pdfkit

pdfConfig = pdfkit.configuration(wkhtmltopdf='wkhtmltopdf/bin/wkhtmltopdf.exe')
load_dotenv()
logging.basicConfig(filename='record.log', level=logging.DEBUG)
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config['SECRET KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')

app.config.from_object(__name__)
db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)

sess = Session(app)

with app.app_context():
    db.create_all()

#DATABASE CONNECTION
try:
    mydb = mysql.connector.connect(
    host= os.getenv("MYSQL_HOST"),
    user= os.getenv("MYSQL_USER"),
    password= os.getenv("MYSQL_PASS"),
    database = os.getenv("MYSQL_DB")
    )
except Exception as e:
    print(str(e))

import views
#AVAILABLE RIDES
rides = {'EE' : 'Easy Enduro', 'FT': 'First Timers', '2T': '2T Enduro'}
price = {'Easy Enduro' : 60, 'First Timers': 70, '2T Enduro': 120}

def time_slots(day, ride):
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

    # Check for availabiity
    """An exeis ta dedomena stin mnimi tote yparxei kindinos na ginei kapoio transaction
     kai na min exoun enimerwthei ta dedomena kai na proxwriseis me to transaction pou den prepei 
     na ginei. Otan ginei ena succesful transaction tote enimerwse to DataStructure pou xrisimopoieies"""
    # mycursor = mydb.cursor()
    # myTable = pd.read_sql('select * from orders',mydb)
    # print(len(myTable.loc[ myTable['Time'] == '9:00-11:00']))
    # for time in new_time_slots:
    #     mycursor.execute(f"SELECT * FROM Orders WHERE Time ='{time}'")
    #     myresult =  mycursor.fetchall()
    # mycursor.close()
    # myresult = list(myresult[0])
    return new_time_slots


def check_time_clots():
    pass
def check_availability():
    pass

@app.route('/')
def hello_world():
    # if 'user' in session.keys():
    #     return render_template("index.html", data = session['user'])
    # else:
    #     return render_template("index.html")
    #POP KEYS DAY DAYOFWEEK MONTH RIDE ETC FROM SESSION DIC IF THEY EXIST
    
    # if 'user' in session:
    #     for key in list(session.keys()):
    #         if key != '_permanent':
    #             del session[key]
         
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

    if ride not in rides:
        return Response(status=500)
    
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
    if len(myresult) == 1:
        # session.clear()
        session['user'] = username
        mycursor.close()
        if 'admin' in session:
            del session['admin']
        return redirect(url_for("hello_world"))

    # CHECK IF THE USER EXISTS IS AN ADMIN
    mycursor.execute(f"SELECT * FROM Admin WHERE username ='{username}' and password = '{password}'")
    myresult = mycursor.fetchall()
    if len(myresult) == 1:
        # session.clear()
        session['admin'] = True
        session['page'] = 1
        # session['expiry'] = datetime.datetime.strptime(datetime.today(), "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
        mycursor.close()
        return redirect(url_for("admin"))

    #CHECK IF THE USER IS ALREADY LOGGED IN FROM SESSIONS AND FROM FIELD IN DATABASE 
    return redirect(url_for("loginPage"))

@app.route('/logoutUser')
def logoutRequest():
    session.clear()
    # Clear session and delete connection to db AND DELETE RECORD IN SESSIONS
    # SET FIELD IN DATABASE TO NOT LOGGED IN
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
        if not ('time' in checkoutData.keys() and checkoutData['time'] in time_slots(checkoutData['weekDay'], checkoutData['ride']) ):
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

    session['price'] = price[session['ride']] * int(session['people'])
    if "user" in session.keys():
        # GET DATA FOR USER IF LOGGED IN
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM Users WHERE username ='{session['user']}'")
        myresult =  mycursor.fetchall()
        mycursor.close()
        myresult = list(myresult[0])
        print(myresult)
        firstName = myresult[4]
        lastName = myresult[5]
        email = myresult[3]
        telephone = myresult[6]
        session['firstName'] = firstName
        session['lastName'] = lastName
        session['email'] = email
        session['telephone'] = telephone
    
    # data = request.get_json();
    # day = request.form.get("day")
    # month = request.form.get("month")
    # year = request.form.get("year")
    # ride = request.form.get("ride")
    
    #check if every field in checkoudata is set and correct

    return render_template("checkout.html")

@app.route('/submitOrder', methods=['POST'])
def submitOrder():

    #CHEC KFIELDS FOR VALIDITY
    username = session.get("user", "Guest")
    ride = session['ride']
    dateToRide = session["year"] + "-" + session["month"] + "-" + session["day"]
    time = session['time']
    people = session['people']
    firstName  = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    telephone = request.form['telephone']
    ethnicity = request.form['ethnicity']
    residence = request.form['residence']
    birthday = request.form['birthday']
    driving = "YES" if 'license' in  request.form.keys() else "NO"


    sql = "INSERT INTO orders(`UserOrdered`, `ride`, `Date to Ride`, `Time`, `Number of People`, `FirstName`, `LastName`, `email`, `telephone`, `Ethnicity`, `Residence`, `Date Of Birth`, `Driving License`) " \
    +"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (username, ride, dateToRide, time, people, firstName, lastName, email, telephone, ethnicity, residence, birthday, driving)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    return redirect(url_for("hello_world"))


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
    telephone = request.form['telephone']

    # UPDATE DATABASE
    sql = "INSERT INTO Users(username, password, email, FirstName, LastName, telephone) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (username, password, email, firstName, lastName, telephone)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    # except:
    #     print("an error occured redirecting you")
    #     print(traceback.format_exc())
    #     print(sys.exc_info()[2])
    #     return redirect(url_for("registerPage"))

    return redirect(url_for('loginPage'))

app.add_url_rule('/admin', view_func=views.admin)

@app.route('/downloadPDF')
def downloadPDF():
    myTable = pd.read_sql('select * from orders',mydb)
    html_string = myTable.to_html()
    pdfkit.from_string(html_string, "orderTable.pdf", configuration=pdfConfig)
    return send_file('orderTable.pdf', download_name='orderTable.pdf',mimetype='application/pdf')

@app.route('/downloadCSV')
def downloadCSV():
    myTable = pd.read_sql('select * from orders',mydb)
    myTable.to_csv('customers.csv', encoding='utf-8', index=False)
    return send_file('customers.csv', download_name='table.csv',mimetype='text/csv')

# @app.after_request
# def after_request(response):
#     print(response)
#     response.headers.add("Cache-Control", "no-cache")
#     return response

if __name__ == '__main__':
    app.run(debug=True, port=8000, threaded=True)
