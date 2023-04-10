/* Return the dates where there are no available instructors because of leave*/
drop procedure if exists completeDays;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE completeDays(IN startDate DATE, IN endDate DATE)  
begin

drop table if exists currentDates; 
CREATE TEMPORARY TABLE IF NOT EXISTS currentDates AS( WITH RECURSIVE t as (
    select startDate as selected_date
  UNION
    SELECT DATE_ADD(t.selected_date, INTERVAL 1 DAY) FROM t WHERE DATE_ADD(t.selected_date, INTERVAL 1 DAY) <= endDate
)
select * FROM t);

drop table if exists temp; 
CREATE TEMPORARY TABLE IF NOT EXISTS temp as (
SELECT selected_date,Time,IF(date_of_leave IS NOT NULL, IF (Availability.instructors - count(*) < 0, 0, instructors - count(*)), Availability.instructors ) as `available instructors` 
FROM currentDates 
INNER JOIN Availability ON (dayofweek(selected_date)-1) = Availability.day 
LEFT JOIN InstructorLeave ON selected_date = DATE(date_of_Leave) 
GROUP BY selected_date,Time  ORDER BY selected_date,Time);
/*select selected_date FROM temp GROUP BY selected_date HAVING sum(`available instructors`) = 0;*/

SELECT DISTINCT selected_date FROM( SELECT selected_date,temp.Time AS TIME1,`available instructors`,`Date to Ride`,allOrders.Time AS TIME2,IF(`Number of Orders` IS NULL,0,`Number of Orders`) AS `Number of Orders` 
FROM temp LEFT JOIN 
(SELECT `Date to Ride`,Time,count(*) AS `Number of Orders` FROM Orders WHERE (`Date to Ride` BETWEEN startDate AND endDate)  
GROUP BY `Date to Ride`,Orders.Time) allOrders on selected_date = `Date to Ride` and temp.Time = allOrders.Time 
WHERE `available instructors` > 0 
HAVING `available instructors` > `Number of Orders`) finalOrders;

end$$
DELIMITER ;