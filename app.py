from multiprocessing import reduction
import os
# import sys
import logging
# from typing import final
from flask import Flask,flash, render_template,send_file,request,redirect,url_for, session, Response
# import mysql.connector
# from mysql.connector import pooling
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import timedelta,datetime
from dotenv import load_dotenv
import pdfkit
# from sqlalchemy import true
from countries import availability
from email_customer import send_email


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
    mydb = MySQLdb.connect(
    host= os.getenv("MYSQL_HOST"),
    user= os.getenv("MYSQL_USER"),
    password= os.getenv("MYSQL_PASS"),
    database = os.getenv("MYSQL_DB"),
    autocommit=True
    )
    MySQLdb.threadsafety = 3
except Exception as e:
    print(str(e))

import views, schedule
#AVAILABLE RIDES
rides = {'EE' : 'Easy Enduro 1H', 'FT': 'First Timers', '2T': '2T Enduro'}
motors = {'EE' : 6, 'FT': 4, '2T': 5}
price = {'Easy Enduro 1H' : 60, 'First Timers': 70, '2T Enduro': 120}

def time_slots(day, ride, date):
    # new_time_slots = ['9:00-11:00','11:00-12:00','14:00-15:00','15:00-17:00']

    # #Because javascript numbers week days from index=0
    # day = int(day)
    # if day == 1:
    #     new_time_slots.remove('9:00-11:00')
    #     if ride == '2T':
    #         new_time_slots.remove('11:00-12:00')
    #         new_time_slots.remove('14:00-15:00')
    # if day == 2:
    #     if ride == '2T':
    #         new_time_slots.remove('14:00-15:00')
    #         new_time_slots.remove('11:00-12:00')
    #     if ride == 'FT':
    #         new_time_slots.remove('15:00-17:00')
    # if day == 3:
    #     if ride == 'FT':
    #         new_time_slots.remove('15:00-17:00')
    #     if ride == '2T':
    #         new_time_slots.remove('11:00-12:00')
    #         new_time_slots.remove('15:00-17:00')
    # if day == 4:
    #     new_time_slots.remove('14:00-15:00')
    #     if ride == 'FT':
    #         new_time_slots.remove('15:00-17:00')
    #     if ride == '2T':
    #         new_time_slots.remove('11:00-12:00')
    # if day == 5:
    #     if ride == '2T':
    #         new_time_slots.remove('11:00-12:00')
    #         new_time_slots.remove('15:00-17:00')
    # if day == 6:
    #     new_time_slots.remove('15:00-17:00')
    #     if ride == '2T':
    #         new_time_slots.remove('11:00-12:00')
    # if day == 0:
    #     new_time_slots.remove('15:00-17:00')
    #     if ride == 'FT':
    #         new_time_slots.remove('9:00-11:00')
    #     if ride == '2T':
    #         new_time_slots.remove('11:00-12:00')

    # # Check for number of orders in this time slots
    # final_time_slots = []
    # for time in new_time_slots:
    #     sql = "select count(*) FROM orders WHERE `Date to Ride`= '" + date + "' AND Time = '" + time +"' GROUP BY `Date to Ride`,Time"
    #     mycursor.execute(sql)
    #     myresult = mycursor.fetchall()
    #     # print(myresult[0],availability(time,date))
    #     if availability(time,date) > 0:
    #         if len(myresult) != 0 and myresult[0][0] < availability(time,date):
    #             final_time_slots.append(time)
    #         elif len(myresult) == 0:
    #             final_time_slots.append(time)

    final_time_slots = []
    try:
        mycursor = mydb.cursor()
        sql = f"call specificDate('{date}','{ride}')"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for row in myresult:
            final_time_slots.append(row[0])
    except Exception as e:
        print(str(e))
    finally: 
        mycursor.close()
    """An exeis ta dedomena stin mnimi tote yparxei kindinos na ginei kapoio transaction
     kai na min exoun enimerwthei ta dedomena kai na proxwriseis me to transaction pou den prepei 
     na ginei. Otan ginei ena succesful transaction tote enimerwse to DataStructure pou xrisimopoieies"""
    return final_time_slots

def get_available_motors(date, ride, time):
    global motors
    global rides

    mycursor = mydb.cursor()
    sql = "SELECT SUM(`Number of People`) FROM orders WHERE `Date to Ride`= '" + date + "' AND Time = '" + time +"' AND Ride = '" \
    + rides[ride] + "' GROUP BY `Date to Ride`,Time, Ride"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()

    #Set number of motors for 2T at 3 for Tuesday and Monday at 15:00-17:00
    if ride == '2T':
        if time == '15:00-17:00' and (datetime.strptime(date, '%Y-%m-%d').weekday() in [1,3]):
            num_of_motors = 3
        else:
            num_of_motors = 5
    else:
        num_of_motors = motors[ride]

    #Calculate the remaining motors for each time slot
    if len(myresult) != 0:
        number_of_motors = num_of_motors - int(myresult[0][0])
    elif len(myresult) == 0:
        number_of_motors = num_of_motors
    
    if number_of_motors <= 0:
        return 0
    else:
        return number_of_motors
    

@app.route('/')
def hello_world():

    #POP KEYS DAY DAYOFWEEK MONTH RIDE ETC FROM SESSION DIC IF THEY EXIST
    print(session.keys(), session.values())
    return render_template("index.html")

@app.route('/getInactiveDays', methods = ["POST"])
def getInactiveDays():
    mycursor = mydb.cursor()
    sql = f"call completeDays('{datetime.now().date()}','{datetime.now().date() + timedelta(days=21)}')"
    mycursor.execute(f"call completeDays('{datetime.now().date() + timedelta(days=1)}','{datetime.now().date() + timedelta(days=21)}')")
    myresult = mycursor.fetchall()
    dates = []
    for row in myresult:
        dates.append(str(row[0]))
    return list(dates)

@app.route('/getDays', methods = ["POST"])
def getDays():
    day = request.form.get("day")

    #Check that the day is numeric and 1-7
    if not day.isnumeric():
        app.logger.error("User gave non numeric value")
        print("User gave non numeric value")
        return Response(status=500)
    elif 1 < int(day) > 7:
        print("User gave day our of range")
        return Response(status=500)
    
    #Check that the ride is one of the options
    ride = request.form.get("ride")

    if ride not in rides:
        print("User gave ride value not in list")
        return Response(status=500)
    
    date = request.form.get("date")
    try:
        new_Date = datetime.strptime(date, '%Y-%m-%d').date()
        end_date = datetime.now() + timedelta(days=21)
        if not datetime.today().date() < new_Date <=end_date.date():
            print("User gave date not in range of 1-21")
            return Response(status=500)
    except Exception as e:
        print(str(e))

    return time_slots(day,ride,date)

@app.route('/getMotors', methods=['POST'])
def getMorors():
    date = request.form.get("date")
    ride = request.form.get("ride")
    time = request.form.get("time")
    if time != "":
        return str(get_available_motors(date,ride,time))
    else:
        return '0'
    
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
    username = request.form['usrname']
    password = request.form['pass']

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM Users WHERE username ='{username}' and password = '{password}'")
    myresult = mycursor.fetchall()
    if len(myresult) == 1:
        if myresult[0][1] == username and myresult[0][2] == password:
            for key in list(session.keys()):
                if key != '_permanent':
                    del session[key]
            session['user'] = username
            session['firstName'] = myresult[0][4]
            mycursor.close()
            return redirect(url_for("hello_world"))

    # CHECK IF THE USER EXISTS IS AN ADMIN
    mycursor.execute(f"SELECT * FROM Admin WHERE username ='{username}' and password = '{password}'")
    myresult = mycursor.fetchall()
    if len(myresult) == 1:
        if myresult[0][1] == username and myresult[0][2] == password:
            for key in list(session.keys()):
                if key != '_permanent':
                    del session[key]
            session['admin'] = True
            session['page'] = 0
            session['firstName'] = ''
            session['lastName'] = ''
            session['dateFrom'] = ''
            session['dateTo'] = ''
            session['sortField'] = ''
            session['sortDierection'] = True
            # session['expiry'] = datetime.datetime.strptime(datetime.today(), "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1)
            mycursor.close()
            return redirect(url_for("admin"))

    #CHECK IF THE USER IS ALREADY LOGGED IN FROM SESSIONS AND FROM FIELD IN DATABASE
    mycursor.close() 
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

@app.route('/userProfile')
def userProfile():
    if "user" in session.keys():
        # GET DATA FOR USER IF LOGGED IN
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM Users WHERE username ='{session['user']}'")
        myresult =  mycursor.fetchall()
        mycursor.close()
        myresult = list(myresult[0])
        firstName = myresult[4]
        lastName = myresult[5]
        email = myresult[3]
        telephone = myresult[6]
        password = myresult[2]
    else:
        return redirect(url_for("hello_world"))
        
    return render_template("userProfile.html", data = [firstName, lastName, email, password, telephone])

@app.route('/checkout', methods = ["POST"])
def checkoutPage():
    checkoutData = request.get_json()
    print(checkoutData)

    if checkoutData is not None: 
        if not ('day' in checkoutData.keys() and checkoutData['day'].isnumeric() ): 
            print("problem with day")
            #CHECK THAT DAY IS IN THE 21 VALID DAYS THAT ARE NOT DISABLED
            return Response(status=500)
        
        if not ('month' in checkoutData.keys() and checkoutData['month'].isnumeric() ):
            print("problem with month") 
            return Response(status=500)
        
        if not ('year' in checkoutData.keys() and checkoutData['year'].isnumeric() ):
            print("problem with year") 
            return Response(status=500)
        
        print(checkoutData['people'])
        if not ('people' in checkoutData.keys() and checkoutData['people'] is not None and checkoutData['people'].isnumeric() ):
            print("problem with people") 
            return Response(status=500)

        if not ('ride' in checkoutData.keys() and checkoutData['ride'] in rides.keys()):
            print("problem with ride") 
            return Response(status=500)
        
        date = checkoutData['year'] + "-" + checkoutData['month'] + "-" + checkoutData['day']
        if not ('time' in checkoutData.keys() and checkoutData['time'] in time_slots(checkoutData['weekDay'], checkoutData['ride'], date)):
            print("problem with time")
            flash('You need to select a time') 
            return Response(status=500)
    else:
        print("not logged in")
        return Response(status=500)
    
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
    global rides

    if not set(['day','month','year','ride','time','people']).issubset(set(session.keys())):
        '''YOU NEED TO CHECK AGAIN EVERY FIELD BECAUSE HE CAN SUBMIT 1 VALID ORDER AND THEN THE KEYS
        # IN SESSION ARE SET SO HE CAN SUBMIT FALSE ORDERS. CREATE A FUNCTION THAT CHECKS THE FIELDS 
        # SO YOU CAN CALL EVERY TIME'''
        return redirect(url_for("hello_world"))
    
    session['price'] = price[session['ride']] * int(session['people'])
    if "user" in session.keys():
        # GET DATA FOR USER IF LOGGED IN
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM Users WHERE username ='{session['user']}'")
        myresult =  mycursor.fetchall()
        mycursor.close()
        myresult = list(myresult[0])
        firstName = myresult[4]
        lastName = myresult[5]
        email = myresult[3]
        telephone = myresult[6]
        return render_template("checkout.html", data=[firstName, lastName, email, telephone])
    
    #check if every field in checkoudata is set and correct
    return render_template("checkout.html")
    
@app.route('/submitOrder', methods=['POST'])
def submitOrder():

    #CHECK FIELDS FOR VALIDITY
    '''YOU NEED TO CHECK THAT ALL FIELDS ARE SET HERE BECAUSE HE CAN MAKE AN ORDER THEN PRESS THE BACK BUTTON AND GO BACK TO THE CHECKOUT
    PAGE TO RESUMBIT AND ALREADY SUBMITED PAGE. OFCOURSE HE WILL BE AT THE STRIPE PAGE BUT STILL'''
    username = session.get("user", "Guest")
    ride = session['ride']
    dateToRide = session["year"] + "-" + session["month"] + "-" + session["day"]
    time = session['time']
    people = session['people']
    firstName  = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    telephone = request.form['telephone']
    ethnicity = request.form.get('ethnicity','')
    residence = request.form.get('residence','')
    birthday = request.form['birthday']
    driving = "YES" if 'license' in  request.form.keys() else "NO"

    if not set(['day','month','year','ride','time','people']).issubset(set(session.keys())):
        print("missing fields")
        print(session)
        return redirect(url_for("hello_world"))

    from payment import create_payemnt
    url = create_payemnt(session['price'])
    redirect(url)
    
    sql = "INSERT INTO orders(`UserOrdered`, `ride`, `Date to Ride`, `Time`, `Number of People`, `FirstName`, `LastName`, `email`, `telephone`, `Ethnicity`, `Residence`, `Date Of Birth`, `Driving License`) " \
    +"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (username, ride, dateToRide, time, people, firstName, lastName, email, telephone, ethnicity, residence, birthday, driving)
    mycursor = mydb.cursor()
    print(f'INSERT INTO orders(`UserOrdered`, `ride`, `Date to Ride`, `Time`, `Number of People`, `FirstName`, `LastName`, `email`, `telephone`, `Ethnicity`, `Residence`, `Date Of Birth`, `Driving License`) " \
    +"VALUES ({username}, {ride}, {dateToRide}, {time}, {people}, {firstName}, {lastName}, {email}, {telephone}, {ethnicity}, {residence}, {birthday}, {driving}')
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()


    # send_email(email, time, dateToRide)
    # from payment import create_payemnt
    # url = create_payemnt(session['price'])
    for key in list(session.keys()):
        if key not in ['_permanent', 'user', 'firstName']:
            del session[key]

    return redirect(url_for("hello_world"))


# @app.route('/2T_enduro_ride.jpg')
# def image1():
#     return send_file("rides/2T_enduro_ride.jpg", mimetype='image/gif')

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
app.add_url_rule('/schedule', view_func=views.schedule)
app.add_url_rule('/adminfilters', view_func=views.adminfilters, methods=['POST'])
app.add_url_rule('/sortfilters', view_func=views.sortFilerts, methods=['POST'])
app.add_url_rule('/userProfileUpdate', view_func=views.userProfileUpdate, methods=['POST'])
app.add_url_rule('/nextPage', view_func=views.nextPage, methods=['GET'])
app.add_url_rule('/instructorLeave', view_func=views.instructorLeave, methods=['POST'])
app.add_url_rule('/getSchedule', view_func=schedule.getSchedule, methods=['POST'])
app.add_url_rule('/getRidesforDate', view_func=schedule.getRidesforDate, methods=['POST'])
app.add_url_rule('/updateFromAdmin', view_func=schedule.updateRidesTable, methods=['GET'])
app.add_url_rule('/deleteTimeRow', view_func=schedule.deleteTimeRow, methods=['GET'])
app.add_url_rule('/updateTime', view_func=schedule.updateTime, methods=['POST'])




# app.add_url_rule('/getOrders', view_func=views.getOrders, methods=['GET'])

@app.route('/downloadPDF', methods=['GET'])
def downloadPDF():
    from views import filterData
    myTable = filterData()
    html_string = myTable.to_html()
    pdfkit.from_string(html_string, "orderTable.pdf", configuration=pdfConfig)
    return send_file('orderTable.pdf', download_name='orderTable.pdf',mimetype='application/pdf')

@app.route('/downloadCSV', methods=['GET'])
def downloadCSV():
    from views import filterData
    myTable = filterData()
    myTable.to_csv('customers.csv', encoding='utf-8', index=False)
    return send_file('customers.csv', download_name='table.csv',mimetype='text/csv')

@app.route('/adminScript.js')
def adminScript():
    return render_template("adminScript.js")

@app.route('/scheduleScript.js')
def scheduleScript():
    return render_template("scheduleScript.js")

# @app.after_request
# def after_request(response):
#     print(response)
#     response.headers.add("Cache-Control", "no-cache")
#     return response

if __name__ == '__main__':
    app.run(debug=True, port=8000, threaded=True)
