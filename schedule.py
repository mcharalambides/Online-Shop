from time import time
from flask import redirect, render_template, url_for, request
import json
import pandas as pd
from datetime import date, datetime, timedelta
from app import session,mydb
# from db_connector import Database

# mydb = Database()

def getSchedule():

    result = []
    result2 = mydb.execute('SELECT Day,Time,RideType,instructors FROM Availability INNER JOIN RideTimes on day = weekday and time = rideTime ORDER BY Day,Time ')
    result.append(result2)
    # mycursor.execute("SELECT distinct `Time` FROM Availability ORDER BY CAST(SUBSTRING_INDEX(`Time`,':',1) AS UNSIGNED) ASC")
    result2 = mydb.execute("SELECT `Time_range` FROM Time_frames ORDER BY CAST(SUBSTRING_INDEX(`Time_range`,':',1) AS UNSIGNED) ASC")
    result.append(result2)
    # mycursor.close()
    return list(result)

def getRidesforDate():
    day = request.form.get("day")
    time = request.form.get("time")
    sql = f"SELECT RideType FROM RideTimes WHERE weekday = {day} and rideTime = '{time}'"
    result = mydb.execute(sql)
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
    sql = f"DELETE FROM RideTimes WHERE weekday = {day} and rideTime = '{time}'"
    mydb.execute_update(sql)
    sql = f"DELETE FROM Availability WHERE Day = {day} and Time = '{time}'"
    mydb.execute_update(sql)

    if rides[0] != '':
        for ride in rides:
            print(ride)
            mydb.execute_update(f"INSERT INTO RideTimes(RideType, `weekday`, `rideTime`) VALUES ('{ride}',{day},'{time}')")
        mydb.execute_update(f"INSERT INTO Availability(Day, Time, instructors) VALUES ({day},'{time}',{instructors})")
    # else:
    #     mycursor.execute(f"INSERT INTO Availability(Day, Time, instructors) VALUES ({day},'{time}',{0})")
    #     mydb.commit()

    return redirect(url_for("schedule"))

def deleteTimeRow():
    time = request.args.get("time")

    #Delete records that match this time
    sql = f"DELETE FROM Time_frames WHERE Time_range = '{time}'"
    mydb.execute_update(sql)
    sql = f"DELETE FROM RideTimes WHERE rideTime = '{time}'"
    mydb.execute_update(sql)
    sql = f"DELETE FROM Availability WHERE Time = '{time}'"
    mydb.execute_update(sql)

    return redirect(url_for("schedule"))

def updateTime():
    fromTime = request.form.get("fromTime")
    fromTime = fromTime[1:] if fromTime[0] == '0' else fromTime
    toTime = request.form.get("toTime")
    toTime = toTime[1:] if toTime[0] == '0' else toTime


    mydb.execute_update(f"INSERT INTO Time_frames(Time_range) VALUES ('{fromTime + '-' + toTime}')")
    return redirect(url_for("schedule"))









