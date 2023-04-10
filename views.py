from time import time
from flask import redirect, render_template, url_for, request
import json
import pandas as pd
from datetime import date, datetime, timedelta
from __main__ import mydb,session

#User requests
# def getOrders():
#     from __main__ import mydb

#     month = request.args['month']
#     year = request.args['year']
#     day = request.args['day']
#     mycursor = mydb.cursor()
#     sql = "SELECT `Date to Ride` as Day, Time, count(*), sum(`Number of People`) FROM orders WHERE `Date to Ride`>= CURDATE() AND `Date to Ride`<= DATE_ADD(`Date to Ride`, INTERVAL 21 DAY) GROUP BY `Date to Ride`,time;
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#     mycursor.close()
    
#     return myresult
def admin():
    if 'admin' not in session:
        return redirect(url_for("hello_world"))
    
    mycursor = mydb.cursor()
    sql = "SELECT id,firstName,lastName,Ride, DATE_FORMAT(`Date to Ride`,'%d-%m-%Y'), Time, `Number of People`, email, telephone,"\
     +"`Date of Birth`, ethnicity, residence, `Driving License`, DATE_FORMAT(`Date of Order`,'%d-%m-%Y %H:%i:%s') FROM Orders ORDER BY `Date to Ride` LIMIT 0,20"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()
    
    session['admin'] = True
    session['page'] = 0
    session['firstName'] = ''
    session['lastName'] = ''
    session['dateFrom'] = ''
    session['dateTo'] = ''
    session['sortField'] = ''
    session['sortDierection'] = True
    return render_template('admin.html', data=myresult)

def schedule():
    if 'admin' not in session:
        return redirect(url_for("hello_world"))

    return render_template('schedule.html')

def adminfilters():

    session['firstName'] = request.form.get('firstName')
    session['lastName'] = request.form.get('lastName')
    session['dateFrom'] = request.form.get('dateFrom')
    session['dateTo'] = request.form.get('dateTo')

    
    session['page'] = 0
    session['sortField'] = ''
    session['sortDierection'] = True
    return [filterData().values.tolist(), session['page']]

def userProfileUpdate():
    
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    password = request.form.get('password')
    telephone = request.form.get('telephone')
    sql = "UPDATE Users SET FirstName = %s,  LastName = %s, email = %s, password = %s, telephone = %s WHERE username = %s"
    val = (firstName, lastName, email, password, telephone, session['user'])
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

    session['firstName'] = firstName
    return redirect(url_for("hello_world"))

def nextPage():

    myTable = filterData()
    if request.args.get('procedure') == 'next':
        session['page'] = session['page'] + 1
    elif request.args.get('procedure') == 'prev':
        if session['page'] == 0:
            session['page'] = 0
        else:
            session['page'] = session['page'] - 1
    elif request.args.get('procedure') == 'maxprev':
        session['page'] = 0
    elif request.args.get('procedure') == 'maxnext':
        session['page'] = int(int(len(myTable.values.tolist())) / 20)


    return [myTable.iloc[session['page']*20:(session['page'] + 1)*20].values.tolist(), session['page']]


def sortFilerts():
    session['sortField'] = request.form.get('field')
    session['sortDierection'] = not session['sortDierection']

    return filterData().values.tolist()

def filterData():
    import inspect
    sql = "select * from orders order by `Date to Ride`"
    try:
        myTable = pd.read_sql(sql,mydb)
    except Exception as e:
        print(str(e))
    # finally:
    #     mydb.cursor().close()

    if session['firstName']:
        myTable = myTable.loc[myTable['FirstName'] == session['firstName']]

    if session['lastName']:
        myTable = myTable.loc[myTable['LastName'] == session['lastName']]

    if session['dateFrom']:
        myTable = myTable[myTable['Date to Ride'] >= datetime.strptime(session['dateFrom'], '%Y-%m-%d').date()]

    if session['dateTo']:
        myTable = myTable[myTable['Date to Ride'] <= datetime.strptime(session['dateTo'], '%Y-%m-%d').date()]

    if session['sortField']:
       myTable =  myTable.sort_values(by=session['sortField'], ascending = session['sortDierection'])

    if inspect.stack()[1].function in ['downloadPDF', 'downloadCSV', 'nextPage']:
        return myTable

    return myTable.iloc[session['page']*20:(session['page'] + 1)*20]


def instructorLeave():
    # UPDATE DATABASE
    dateFrom = request.form.get('dateFrom')
    dateTo = request.form.get('dateTo')

    stringToAdd = ""
    dateFrom = datetime.strptime(dateFrom, '%Y-%m-%d').date()
    dateTo = datetime.strptime(dateTo, '%Y-%m-%d').date()
    diff = dateTo - dateFrom
    diff = int(divmod(diff.total_seconds(), 86400)[0])
    for i in range(0,diff+1):
        stringToAdd = stringToAdd + "('" + str(dateFrom + timedelta(days=i)) + "'),"
    stringToAdd = stringToAdd[:-1]
    sql = "INSERT INTO `InstructorLeave` (`date_of_Leave`) VALUES "
    sql += stringToAdd
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    return 'Success'