-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 08, 2022 at 10:24 AM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `karmacaters`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `bid` int(11) NOT NULL,
  `oid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `place` varchar(1000) NOT NULL,
  `quantity` varchar(20) NOT NULL,
  `date` varchar(12) NOT NULL,
  `time` varchar(10) NOT NULL,
  `currentdatetime` timestamp NOT NULL DEFAULT current_timestamp(),
  `checked` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`bid`, `oid`, `name`, `email`, `contact`, `place`, `quantity`, `date`, `time`, `currentdatetime`, `checked`) VALUES
(1, 3, 'durgaprasad', 'dp744916@gmail.com', '8078255178', 'Town Hall, varapuzha', '200', '2022-05-05', '10:00', '2022-05-04 06:59:04', 1),
(2, 2, 'goutham', 'official.goutham11@gmail.com', '9656637893', 'ernakulam', '100', '2022-05-15', '11:30', '2022-05-04 07:01:31', 1),
(3, 2, 'prajitha', 'prajithaap199@gmail.com', '9446911499', 'cherthala', '3', '2022-05-05', '13:00', '2022-05-04 10:18:36', 1),
(4, 4, 'gopika Suresh', 'gopikasuresh225@gmail.com', '8157023455', 'palarivattom', '2000', '2022-05-05', '09:00', '2022-05-04 10:23:30', 1),
(5, 3, 'Hemand K r', 'krhemand@gmail.com', '8089459358', 'varapuzha', '100', '2022-05-06', '10:00', '2022-05-04 14:20:31', 1),
(6, 5, 'durgaprasad', 'dp744916@gmail.com', '8078255178', 'varapuzha townhall', '100', '2022-06-02', '10:00', '2022-05-05 02:36:05', 1),
(7, 3, ' durgaprasad subramanian', 'dp744916@gmail.com', '8078255178', 'kadamakkudy, townhall', '200', '2022-05-09', '09:00', '2022-05-08 07:18:24', 1),
(8, 5, 'mauprasad', 'manuprasad11@gmail.com', '8136892307', 'pandaraparmbil,kadamakudy,pizhala po', '4', '2022-05-08', '02:00', '2022-05-08 07:23:39', 1);

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `review` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `username`, `email`, `review`) VALUES
(1, 'MANU PRASAD', 'manuprasad11@gmail.com', 'its very good');

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `item` varchar(100) NOT NULL,
  `img` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `item`, `img`) VALUES
(1, 'frid rise(veg/non-veg)', '1.jpg'),
(2, 'Traditional Sadhya', '2.jpg'),
(3, 'biriyani', '3.jpg'),
(4, 'dessert food', '4.jpg'),
(5, 'cocktails', '5.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `log_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`log_id`, `username`, `password`, `role`) VALUES
(1, 'admin@gmail.com', 'pass@123', 'Admin');

-- --------------------------------------------------------

--
-- Table structure for table `upload`
--

CREATE TABLE `upload` (
  `uid` int(11) NOT NULL,
  `discription` varchar(1000) NOT NULL,
  `img` varchar(10) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `upload`
--

INSERT INTO `upload` (`uid`, `discription`, `img`, `date`, `time`) VALUES
(1, 'Karma Caters', '1.jpg', '2022-05-07', '2022-05-07 10:17:48'),
(2, 'Karma Caters', '2.mp4', '2022-05-07', '2022-05-07 10:18:24'),
(3, 'karma', '3.mp4', '2022-05-07', '2022-05-07 16:08:12'),
(4, 'karma', '4.jpg', '2022-05-07', '2022-05-07 16:08:38');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`bid`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`log_id`);

--
-- Indexes for table `upload`
--
ALTER TABLE `upload`
  ADD PRIMARY KEY (`uid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
