from concurrent.futures import thread
import traceback
import sys
from flask import Flask,render_template,send_file,flash,request,redirect,url_for, session
import numpy
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

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

@app.route('/')
def hello_world():
    if 'user' in session.keys():
        data = session['user']
    else:
        data = 'Guest'
    return render_template("index.html", data = data)

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

@app.route('/checkout.html')
def checkoutPage():
    day = request.args.get("day")
    month = request.args.get("month")
    year = request.args.get("year")

    return render_template("checkout.html", data=[day,month,year])

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
    sql = "INSERT INTO Users(id, username, password, email, FirstName, LastName) VALUES (%s, %s, %s, %s, %s, %s)"
    val = ("randomId", username, password, email, firstName, lastName)
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
