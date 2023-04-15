-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 18, 2020 at 02:05 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.2

use OnlineShop;
show tables;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Table structure for table `Admin`
--

CREATE TABLE `Admin` (
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `Admin` (`email`, `username`, `password`) VALUES
('admin@gmail.com', 'admin', 'admin');


drop table InstructorLeave;
CREATE TABLE `InstructorLeave` (
  `id` INT COLLATE utf8mb4_bin auto_increment PRIMARY KEY,
  `date_of_Leave` DATE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `InstructorLeave` (`date_of_Leave`) VALUES
('2023-02-27'),
('2023-02-27'),
('2023-02-28');




CREATE TABLE `Users` (
  `id` INT COLLATE utf8mb4_bin auto_increment PRIMARY KEY,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `FirstName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `telephone` varchar(255) NOT NULL,
  UNIQUE(username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`id`, `username`, `password`, `email`, `FirstName`, `LastName`) VALUES
('Bkee4I8iTW5fTCkueipzUw==', 'marios', '1234', 'marios@gmail.com', '', '');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


SELECT TABLE_SCHEMA AS `Database`, TABLE_NAME AS `Table`, ROUND((DATA_LENGTH + INDEX_LENGTH)) AS `Size (MB)` FROM information_schema.tables WHERE TABLE_SCHEMA = 'OnlineShop';
select table_schema, sum((data_length+index_length)/1024/1024) AS MB from information_schema.tables group by 1;

drop table if exists Orders;
CREATE TABLE `Orders` (
  `id` INT auto_increment PRIMARY KEY,
  `UserOrdered` varchar(255) NOT NULL,
  `Ride` varchar(20) NOT NULL,
  `Date Of Order` DATETIME DEFAULT current_timestamp NOT NULL,
  `Date to Ride` DATE NOT NULL,
  `Time` varchar(255) NOT NULL,
  `Number of People` INT not null,
  `FirstName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telephone` varchar(255) NOT NULL,
  `Ethnicity` varchar(255) NOT NULL,
  `Residence` varchar(255) NOT NULL,
  `Date Of Birth` DATE NOT NULL,
  `Driving License` ENUM('YES','NO') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX ordersIndex
ON orders (`Date to Ride`);

drop table if exists Time_frames;
CREATE TABLE Time_frames (
  `Time_range` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Time_frames` (`Time_range`) VALUES
('9:00-11:00'),('11:00-12:00'),('14:00-15:00'),('15:00-17:00'),('8:00-9:00');

drop table if exists Availability;
CREATE TABLE Availability (
  `Day` INT NOT NULL,
  `Time` varchar(255) NOT NULL,
  `instructors` INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO `Availability` (`Day`, `Time`, `instructors`) VALUES
(1, '9:00-11:00', 0),
(1, '11:00-12:00', 2),
(1,  '14:00-15:00', 2),
(1,  '15:00-17:00', 2),
(2,  '9:00-11:00', 2),
(2,  '11:00-12:00', 2),
(2,  '14:00-15:00', 1),
(2,  '15:00-17:00', 1),
(3,  '9:00-11:00', 2),
(3,  '11:00-12:00', 2),
(3,  '14:00-15:00', 1),
(3,  '15:00-17:00', 1),
(4,  '9:00-11:00', 2),
(4,  '11:00-12:00', 2),
(4,  '14:00-15:00', 0),
(4,  '15:00-17:00', 1),
(5,  '9:00-11:00', 2),
(5,  '11:00-12:00', 2),
(5,  '14:00-15:00', 2),
(5,  '15:00-17:00', 2),
(6,  '9:00-11:00', 3),
(6,  '11:00-12:00', 3),
(6,  '14:00-15:00', 3),
(6,  '15:00-17:00', 0),
(0,  '9:00-11:00', 3),
(0,  '11:00-12:00', 3),
(0,  '14:00-15:00', 3),
(0,  '15:00-17:00', 0);

drop table if exists RideTimes;
CREATE TABLE RideTimes (
  RideType ENUM('FT','EE','2T'), 
  `weekday` INT NOT NULL,
  `rideTime` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `RideTimes` (RideType, `weekday`, `rideTime`) VALUES
('FT', 1, '11:00-12:00'),
('FT', 1, '14:00-15:00'),
('FT', 1, '15:00-17:00'),
('FT', 2, '9:00-11:00'),
('FT', 2, '11:00-12:00'),
('FT', 2, '14:00-15:00'),
('FT', 3, '9:00-11:00'),
('FT', 3, '11:00-12:00'),
('FT', 3, '14:00-15:00'),
('FT', 4, '9:00-11:00'),
('FT', 4, '11:00-12:00'),
('FT', 5, '9:00-11:00'),
('FT', 5, '11:00-12:00'),
('FT', 5, '14:00-15:00'),
('FT', 5, '15:00-17:00'),
('FT', 6, '9:00-11:00'),
('FT', 6, '11:00-12:00'),
('FT', 6, '14:00-15:00'),
('FT', 0, '9:00-11:00'),
('FT', 0, '11:00-12:00'),
('FT', 0, '14:00-15:00'),

('EE', 1, '11:00-12:00'),
('EE', 1, '14:00-15:00'),
('EE', 1, '15:00-17:00'),
('EE', 2, '9:00-11:00'),
('EE', 2, '11:00-12:00'),
('EE', 2, '14:00-15:00'),
('EE', 2, '15:00-17:00'),
('EE', 3, '9:00-11:00'),
('EE', 3, '11:00-12:00'),
('EE', 3, '14:00-15:00'),
('EE', 3, '15:00-17:00'),
('EE', 4, '9:00-11:00'),
('EE', 4, '11:00-12:00'),
('EE', 4, '15:00-17:00'),
('EE', 5, '9:00-11:00'),
('EE', 5, '11:00-12:00'),
('EE', 5, '14:00-15:00'),
('EE', 5, '15:00-17:00'),
('EE', 6, '9:00-11:00'),
('EE', 6, '11:00-12:00'),
('EE', 6, '14:00-15:00'),
('EE', 0, '9:00-11:00'),
('EE', 0, '11:00-12:00'),
('EE', 0, '14:00-15:00'),

('2T', 1, '15:00-17:00'),
('2T', 2, '9:00-11:00'),
('2T', 2, '15:00-17:00'),
('2T', 3, '9:00-11:00'),
('2T', 3, '14:00-15:00'),
('2T', 4, '9:00-11:00'),
('2T', 4, '15:00-17:00'),
('2T', 5, '9:00-11:00'),
('2T', 5, '14:00-15:00'),
('2T', 6, '9:00-11:00'),
('2T', 6, '14:00-15:00'),
('2T', 0, '9:00-11:00'),
('2T', 0, '14:00-15:00');

select * from orders LIMIT 15,10;
delete from orders where id = 12;
drop table admin;
SELECT * FROM ADMIN where username = 'ADMIN' and password='admin';
truncate table orders;
select count(*), sum(`Number of People`) FROM orders WHERE `Date to Ride`= '18-3-2023' AND Time = '14:00-15:00' GROUP BY `Date to Ride`,Time;
select `Date to Ride` as Day, Time, count(*), sum(`Number of People`) FROM orders WHERE `Date to Ride`>= CURDATE() AND `Date to Ride`<= DATE_ADD(`Date to Ride`, INTERVAL 21 DAY) GROUP BY `Date to Ride`,time HAVING count(*) <= 2; 
select *,count(*),IF(date_of_Leave IS NOT NULL, instructors - count(*),instructors) as available_instructors FROM availability as a left join instructorLeave as b on a.day = DAYOFWEEK(b.date_of_leave)-1  group by Day,Time,date_of_Leave;
select Day,Time,IF(date_of_Leave IS NOT NULL, instructors - count(*),instructors) as available_instructors FROM availability as a left join instructorLeave as b on a.day = DAYOFWEEK(b.date_of_leave)-1  group by Day,Time,date_of_Leave;


select *,count(*) from orders WHERE `Date to Ride` = startDate GROUP BY `Date to Ride`,orders.Time;

select * from currentDates2;
INSERT INTO `InstructorLeave` (`date_of_Leave`) VALUES ('2023-04-01');
select * from availability inner join RideTimes on RideTimes.weekday = availability.day and RideTimes.ridetime = availability.Time order by Day,Time;