drop procedure if exists specificDate;
DELIMITER $$
CREATE  PROCEDURE specificDate(IN startDate DATE, IN Ride ENUM('FT','EE','2T'))  
begin

/*drop table if exists currentDates2; 
CREATE TEMPORARY TABLE IF NOT EXISTS currentDates2 AS(
select startDate,day,Time,instructors from availability  where day = dayofweek(startDate)-1
);*/

/*We get the available time slots for the given Ride 
and the fixed number of instructors*/
drop table if exists sideTable;
CREATE TEMPORARY TABLE IF NOT EXISTS sideTable AS(
select *,startDate 
FROM Availability INNER JOIN RideTimes on Availability.day = RideTimes.weekday and Availability.Time = RideTimes.rideTime
WHERE Availability.day = dayofweek(startDate)-1 and RideTimes.RideType = Ride
);

/*We get the available time slots for the given Ride 
available Instructors that are not on leave for that time slot*/
drop table if exists currentDates3;
CREATE TEMPORARY TABLE IF NOT EXISTS currentDates3 AS( 
select *,IF(date_of_leave IS NOT NULL, IF (sideTable.instructors - count(*) < 0, 0, instructors - count(*)), sideTable.instructors ) as `available instructors` 
from sideTable LEFT JOIN InstructorLeave on sideTable.startDate = DATE(instructorLeave.date_of_leave) group by startDate,Time ORDER BY startDate,Time
);

/*Finally we get the number of orders for the given time slot and Ride. We then compare the number of orders
to the number of available instructors that are not on leave to get the final time slots that the user can select*/
select DISTINCT Time from ( select currentDates3.*,IF(`Number of Orders` IS NULL,0,`Number of Orders`) as `FINAL ORDERS`,`Date to Ride` 
from currentDates3 
LEFT JOIN (select `Date to Ride`,Time,count(*) as `Number of Orders` 
from orders 
WHERE `Date to Ride` = startdate 
GROUP BY `Date to Ride`,orders.Time) 
tempOrders on startDate = `Date to Ride` and currentDates3.Time = tempOrders.Time 
WHERE `available instructors` > 0 HAVING `available instructors` > `FINAL ORDERS`) final ORDER BY CAST(SUBSTRING_INDEX(`Time`,':',1) AS UNSIGNED) ASC;


end$$
DELIMITER ;