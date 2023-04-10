from time import time
from flask import redirect, render_template, url_for, request
import json
import pandas as pd
from datetime import date, datetime, timedelta
from __main__ import mydb,session

def getSchedule():

    result = []
    mycursor = mydb.cursor()
    mycursor.execute('SELECT Day,Time,RideType,instructors FROM availability INNER JOIN RideTimes on day = weekday and time = rideTime ORDER BY Day,Time ')
    result.append(mycursor.fetchall())
    # mycursor.execute("SELECT distinct `Time` FROM availability ORDER BY CAST(SUBSTRING_INDEX(`Time`,':',1) AS UNSIGNED) ASC")
    mycursor.execute("SELECT `Time_range` FROM Time_frames ORDER BY CAST(SUBSTRING_INDEX(`Time_range`,':',1) AS UNSIGNED) ASC")
    result.append(mycursor.fetchall())
    mycursor.close()
    return list(result)

def getRidesforDate():
    day = request.form.get("day")
    time = request.form.get("time")
    mycursor = mydb.cursor()
    sql = f"SELECT RideType FROM RideTimes WHERE weekday = {day} and rideTime = '{time}'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    mycursor.close()
    return list(result)

def updateRidesTable():
    rides = request.args.get("cellRides")
    rides = rides.split(' ')
    instructors = request.args.get("instructors")
    if instructors is None:
        instructors = 0
    time = request.args.get("time")
    day = request.args.get("day")

    #Delete records that match the day and time
    mycursor = mydb.cursor()
    sql = f"DELETE FROM RideTimes WHERE weekday = {day} and rideTime = '{time}'"
    mycursor.execute(sql)
    sql = f"DELETE FROM availability WHERE Day = {day} and Time = '{time}'"
    mycursor.execute(sql)

    if rides[0] != '':
        for ride in rides:
            print(ride)
            mycursor.execute(f"INSERT INTO RideTimes(RideType, `weekday`, `rideTime`) VALUES ('{ride}',{day},'{time}')")
            mydb.commit()
        mycursor.execute(f"INSERT INTO availability(Day, Time, instructors) VALUES ({day},'{time}',{instructors})")
        mydb.commit()
    # else:
    #     mycursor.execute(f"INSERT INTO availability(Day, Time, instructors) VALUES ({day},'{time}',{0})")
    #     mydb.commit()

    mycursor.close()

    return redirect(url_for("schedule"))

def deleteTimeRow():
    time = request.args.get("time")

    #Delete records that match this time
    mycursor = mydb.cursor()
    sql = f"DELETE FROM Time_frames WHERE Time_range = '{time}'"
    mycursor.execute(sql)
    mydb.commit()
    sql = f"DELETE FROM RideTimes WHERE rideTime = '{time}'"
    mycursor.execute(sql)
    mydb.commit()
    sql = f"DELETE FROM availability WHERE Time = '{time}'"
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    return redirect(url_for("schedule"))

def updateTime():
    fromTime = request.form.get("fromTime")
    fromTime = fromTime[1:] if fromTime[0] == '0' else fromTime
    toTime = request.form.get("toTime")
    toTime = toTime[1:] if toTime[0] == '0' else toTime


    mycursor = mydb.cursor()
    mycursor.execute(f"INSERT INTO Time_frames(Time_range) VALUES ('{fromTime + '-' + toTime}')")
    mydb.commit()
    return redirect(url_for("schedule"))









