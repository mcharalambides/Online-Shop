import os
import time
# import sys
# import logging
from flask import Flask,flash, render_template,send_file,request,redirect,url_for, session, Response
# from mysql.connector import pooling
# import MySQLdb
from db_connector import Database
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import timedelta,datetime
from dotenv import load_dotenv
import pdfkit
from email_customer import send_email
import stripe

# pdfConfig = pdfkit.configuration(wkhtmltopdf='/home/MariosCh19/mysite/wkhtmltopdf/bin/wkhtmltopdf.exe')
load_dotenv()
import pytz
IST = pytz.timezone('Asia/Nicosia')


app = Flask(__name__)
app.config['SECRET KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
app.config['SQLALCHEMY_POOL_PRE_PING'] = True
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')

app.config.from_object(__name__)
db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)

sess = Session(app)

with app.app_context():
    db.create_all()

mydb = Database()

import schedule,views
#AVAILABLE RIDES
rides = {'EE' : 'Easy Enduro 1H', 'FT': 'First Timers', '2T': '2T Enduro'}
motors = {'EE' : 6, 'FT': 4, '2T': 5}
price = {'Easy Enduro 1H' : 60, 'First Timers': 70, '2T Enduro': 120}

def time_slots(day, ride, date):

    final_time_slots = []
    try:
        myresult = mydb.execute_proc('specificDate',(date,ride))
        for row in myresult:
            final_time_slots.append(row[0])
    except Exception as e:
        print(str(e))
    """An exeis ta dedomena stin mnimi tote yparxei kindinos na ginei kapoio transaction
     kai na min exoun enimerwthei ta dedomena kai na proxwriseis me to transaction pou den prepei
     na ginei. Otan ginei ena succesful transaction tote enimerwse to DataStructure pou xrisimopoieies"""
    return final_time_slots

def get_available_motors(date, ride, time):
    global motors
    global rides

    sql = "SELECT SUM(`Number of People`) FROM Orders WHERE `Date to Ride`= '" + date + "' AND Time = '" + time +"' AND Ride = '" \
    + rides[ride] + "' GROUP BY `Date to Ride`,Time, Ride"
    myresult = mydb.execute(sql)

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
    global mydb

    myresult = mydb.execute_proc("completeDays",(str(datetime.now(IST).date()+ timedelta(days=1)),str(datetime.now(IST).date() + timedelta(days=21))))
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
        end_date = datetime.now(IST) + timedelta(days=21)
        if not datetime.now(IST).date() < new_Date <=end_date.date():
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

    #REMOVE SPECIAL CHARACTERS FROM USERNAME AND PASSWORD THAT CAUSE PROBLEMS IN MYSQL

    myresult = mydb.execute(f"SELECT * FROM Users WHERE username ='{username}' and password = '{password}'")
    print(myresult)

    if len(myresult) == 1:
        if myresult[0][1] == username and myresult[0][2] == password:
            for key in list(session.keys()):
                if key != '_permanent':
                    del session[key]
            session['user'] = username
            session['firstName'] = myresult[0][4]
            return redirect(url_for("hello_world"))

    # CHECK IF THE USER EXISTS IS AN ADMIN
    myresult = mydb.execute(f"SELECT * FROM Admin WHERE username ='{username}' and password = '{password}'")
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

@app.route('/userProfile')
def userProfile():
    if "user" in session.keys():
        # GET DATA FOR USER IF LOGGED IN
        myresult = mydb.execute(f"SELECT * FROM Users WHERE username ='{session['user']}'")
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

    if session['time'] == '9:00-11:00':
        session['price'] = price[session['ride']] * int(session['people']) *2
    else:
        session['price'] = price[session['ride']] * int(session['people'])

    if "user" in session.keys():
        # GET DATA FOR USER IF LOGGED IN
        myresult = mydb.execute(f"SELECT * FROM Users WHERE username ='{session['user']}'")
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
    #########EDW NA ELEKSW TA PEDIA##############
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
    url = create_payemnt(session['price'], email)
    '''An einai swsta tote prosthese sto tempOrders'''
    sql = "INSERT INTO tempOrders(`UserOrdered`, `ride`,`Date of Order`, `Date to Ride`, `Time`, `Number of People`, `FirstName`, `LastName`, `email`, `telephone`, `Ethnicity`, `Residence`, `Date Of Birth`, `Driving License`) " \
    +"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (session['stripe_session'], ride,datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"), dateToRide, time, people, firstName, lastName, email, telephone, ethnicity, residence, birthday, driving)
    mydb.execute_update(sql, val)


    # send_email(email, time, dateToRide)
    # from payment import create_payemnt
    # url = create_payemnt(session['price'])

    return redirect(url)
    # return redirect(url_for("hello_world"))


@app.route('/success', methods=['POST','GET'])
def successPage():

    if not 'stripe_session' in session.keys():
        return redirect(url_for("hello_world"))

    status = 0
    payment_status = 0
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    try:
        status = stripe.checkout.Session.retrieve(session['stripe_session'])['status']
        payment_status = stripe.checkout.Session.retrieve(session['stripe_session'])['payment_status']
    except Exception as e:
        print(str(e))
        print("i failed to receive the info for the stripe session")
        mydb.execute_update("DELETE FROM tempOrders WHERE UserOrdered='" + session['stripe_session'] + "'")
        for key in list(session.keys()):
            if key not in ['_permanent', 'user', 'firstName']:
                del session[key]
        return render_template('cancelPage.html'), {"Refresh": "5; url=http://mariosch19.pythonanywhere.com"}

    if status == 'complete' and payment_status == 'paid':
        print("transaction was complete")
        myresult = mydb.execute("SELECT * FROM tempOrders WHERE UserOrdered='" + session['stripe_session'] + "'")
        myresult = list(myresult[0])
        username = session.get("user", "Guest")
        ride = myresult[2]
        dateToRide = myresult[4]
        time = myresult[5]
        people = myresult[6]
        firstName  = myresult[7]
        lastName = myresult[8]
        email = myresult[9]
        telephone = myresult[10]
        ethnicity = myresult[11]
        residence = myresult[12]
        birthday = myresult[13]
        driving = myresult[14]
        mydb.execute_update("DELETE FROM tempOrders WHERE UserOrdered='" + session['stripe_session'] + "'")
        sql = "INSERT INTO Orders(`UserOrdered`, `ride`,`Date of Order`, `Date to Ride`, `Time`, `Number of People`, `FirstName`, `LastName`, `email`, `telephone`, `Ethnicity`, `Residence`, `Date Of Birth`, `Driving License`) " \
        +"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (username, ride,datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"), dateToRide, time, people, firstName, lastName, email, telephone, ethnicity, residence, birthday, driving)
        mydb.execute_update(sql, val)

        for key in list(session.keys()):
            if key not in ['_permanent', 'user', 'firstName']:
                del session[key]
        return render_template('successPage.html'), {"Refresh": "5; url=http://mariosch19.pythonanywhere.com"}
    else:
        print("the trasnaction was not succesful")
        mydb.execute_update("DELETE FROM tempOrders WHERE UserOrdered='" + session['stripe_session'] + "'")
        for key in list(session.keys()):
            if key not in ['_permanent', 'user', 'firstName']:
                del session[key]
        return render_template('cancelPage.html'), {"Refresh": "5; url=http://mariosch19.pythonanywhere.com"}

@app.route('/cancel', methods=['POST','GET'])
def cancelPage():
    print("i am in cancelPage")


    stripe.api_key = os.getenv('STRIPE_API_KEY')
    if 'stripe_session' in session.keys():
        try:
            stripe.checkout.Session.expire(session['stripe_session'])
        except Exception as e:
            print(str(e))
            print("i failed to receive the info for the stripe session")

        mydb.execute_update("DELETE FROM tempOrders WHERE UserOrdered='" + session['stripe_session'] + "'")
        for key in list(session.keys()):
            if key not in ['_permanent', 'user', 'firstName']:
                del session[key]
        return render_template('cancelPage.html'), {"Refresh": "5; url=http://mariosch19.pythonanywhere.com"}
    else:
        return redirect(url_for("hello_world"))


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
    if username == "Guest":
        return redirect(url_for('loginPage'))
    password = request.form['pass']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    telephone = request.form['telephone']

    # UPDATE DATABASE
    sql = "INSERT INTO Users(username, password, email, FirstName, LastName, telephone) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (username, password, email, firstName, lastName, telephone)
    mydb.execute_update(sql, val)

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
app.add_url_rule('/getOrders', view_func=views.getOrders, methods=['GET'])


def checkFields(username=None,firstName=None,lastName=None,email=None, \
                telephone=None,ethnicity=None,residence=None,birthday=None,driving=None):

    if not isinstance(username,str) or len(username) > 50 or len(username) == 0 or username.isspace:
        raise ValueError("Invalid Username")

    if not isinstance(firstName,str) or len(firstName) > 50 or len(firstName) == 0 or firstName.isspace:
        raise ValueError("Invalid FirstName")

    if not isinstance(lastName,str) or len(lastName) > 50 or len(lastName) == 0 or lastName.isspace:
        raise ValueError("Invalid LastName")

    if not isinstance(email,str) or len(email) > 50 or len(email) == 0 or email.isspace:
        raise ValueError("Invalid email")

    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not (re.fullmatch(regex, email)):
        raise ValueError("Invalid email type")

    from countries import available_countries

    if ethnicity != '' and ethnicity not in available_countries():
        raise ValueError("Invalid Ethnicity")

    if residence != '' and residence not in available_countries():
        raise ValueError("Invalid Residence")

    try:
        finalBirthday = datetime.datetime(birthday)
    except Exception as e:
        raise ValueError("Invalid Birthday")

    if driving != 'YES' and driving != 'NO':
        raise ValueError("Invalid Driving")

    return True


# @app.route('/downloadPDF', methods=['GET'])
# def downloadPDF():
    # if 'admin' not in session:
    #     return redirect(url_for("hello_world"))
#     from views import filterData
#     myTable = filterData()
#     html_string = myTable.to_html()
#     pdfkit.from_string(html_string, "orderTable.pdf", configuration=pdfConfig)
#     return send_file('orderTable.pdf', download_name='orderTable.pdf',mimetype='application/pdf')

@app.route('/downloadPDF', methods=['GET'])
def downloadPDF():
    if 'admin' not in session:
        return redirect(url_for("hello_world"))

    from views import filterData

    myTable = filterData()
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QTextDocument, QFont, QTextOption
    from PyQt5.QtPrintSupport import QPrinter

    # from PySide2.QtPrintSupport.Q import QTextDocument, QPrinter, QApplication

    import sys
    app = QApplication(sys.argv)

    option = QTextOption()
    option.setWrapMode(QTextOption.WrapAnywhere)
    doc = QTextDocument()
    font = QFont()
    font.setPointSize(6)
    doc.setHtml(myTable.to_html())
    doc.setDefaultFont(font)
    doc.setDefaultTextOption(option)
    printer = QPrinter()
    printer.setOutputFileName("orderTable2.pdf")
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPageSize(QPrinter.A4)
    printer.setPageMargins(0, 0, 0, 0, QPrinter.Millimeter)

    doc.print_(printer)
    return send_file('orderTable2.pdf', download_name='orderTable2.pdf',mimetype='application/pdf')

@app.route('/downloadCSV', methods=['GET'])
def downloadCSV():
    if 'admin' not in session:
        return redirect(url_for("hello_world"))

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


if __name__ == '__main__':
    app.run(debug=True, port=8080, threaded=True)
