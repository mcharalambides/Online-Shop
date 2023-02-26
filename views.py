from flask import redirect, render_template, url_for, send_file
from __main__ import session, mydb
import json


def admin():
    mycursor = mydb.cursor()
    sql = "SELECT id,firstName,lastName,Ride, `Date to Ride`, Time, `Number of People`, email, telephone,"\
     +"`Date of Birth`, ethnicity, residence, `Driving License`, `Date of Order` FROM Orders ORDER BY `Date of Order` "
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if 'admin' in session:
        return render_template('admin.html', data=myresult)

    return redirect(url_for("hello_world"))