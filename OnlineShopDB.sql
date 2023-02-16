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
  `username` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Admin`
--

INSERT INTO `Admin` (`email`, `username`, `password`) VALUES
('admin@gmail.com', 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `Arxeio`
--

CREATE TABLE `Arxeio` (
  `user_id` varchar(255) NOT NULL,
  `timestampMs` datetime NOT NULL,
  `heading` int(50) DEFAULT NULL,
  `velocity` int(50) DEFAULT NULL,
  `accuracy` int(50) NOT NULL,
  `altitude` int(50) DEFAULT NULL,
  `latitudeE7` bigint(20) NOT NULL,
  `longitudeE7` bigint(20) NOT NULL,
  `verticalAccuracy` int(50) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `id` INT COLLATE utf8mb4_bin auto_increment PRIMARY KEY,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `FirstName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL
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

CREATE TABLE `Orders` (
  `id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `UserOrdered` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `Ride` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `Date Of Order` DATETIME COLLATE utf8mb4_bin DEFAULT current_timestamp NOT NULL,
  `Date to Ride` DATE NOT NULL,
  `Time` ENUM('9:00-11:00','11:00-12:00','14:00-15:00','15:00-17:00') NOT NULL,
  `Number of People` INT not null,
   FOREIGN KEY (UserOrdered) REFERENCES Users(id)
   ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

show tables;
drop table Users;
UPDATE Users
SET id = 'randomid2'
WHERE username = 'MariosCh2';

select * from sessions;