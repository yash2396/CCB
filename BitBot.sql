-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 14, 2018 at 02:00 AM
-- Server version: 5.7.21-0ubuntu0.16.04.1
-- PHP Version: 7.0.28-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `BitBot`
--

-- --------------------------------------------------------

--
-- Table structure for table `Administration`
--

CREATE TABLE `Administration` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Administration`
--

INSERT INTO `Administration` (`tag`, `status`) VALUES
('ACPC_site', 'www.acpc.ac.in'),
('Break_timing', '2pm to 3pm'),
('bus_details', '24 Vadodara city routes and 1 Bharuch route. '),
('Campus_facility', 'Our capmus have WFI internet, CCTV facility.'),
('College_placement', '95%'),
('College_site', 'www.bitseducampus.org'),
('Fees', '1.2 lacs'),
('hostel_details', 'Facilities are AC, Non AC rooms, WIFI, Hot water, playground.'),
('rooms_boys_hostel', '50'),
('rooms_girls_hostel', '50'),
('Security_deposit', '10,000'),
('TFW_Students', '2'),
('Timing', '10 am to 5pm'),
('University', 'Gujarat Technological University');

-- --------------------------------------------------------

--
-- Table structure for table `Civil_Engineering`
--

CREATE TABLE `Civil_Engineering` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Civil_Engineering`
--

INSERT INTO `Civil_Engineering` (`tag`, `status`) VALUES
('Abroad', 'Canada and Spain'),
('APCP_Seats', '100'),
('BG_Ratio', '2:3'),
('Classes', '3'),
('Companies', '102'),
('Companies_name', 'ABC'),
('Cutoff', 'for shift-1 8,000 and for shift-2 9,000'),
('D2D_Seats', '10'),
('Instruments', '80'),
('Labs', '12'),
('Master', 'We do not have master program.'),
('MQ_Seats', '80'),
('Package', '2.5 lacs'),
('Placement', '98'),
('Schedule', '4 hours lectures and 2 hours labs'),
('Scope', 'Future is all about technology'),
('shifts', '2'),
('Staffs', '25'),
('Students_Class', '60'),
('Syllabus', 'gtu.ac.in'),
('Total_Seats', '180');

-- --------------------------------------------------------

--
-- Table structure for table `Computer_Engineering`
--

CREATE TABLE `Computer_Engineering` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Computer_Engineering`
--

INSERT INTO `Computer_Engineering` (`tag`, `status`) VALUES
('Abroad', 'Canada and Spain'),
('APCP_Seats', '100'),
('Classes', '3'),
('Companies', '102'),
('Companies_name', 'ABC'),
('Cutoff', 'for shift-1 8,000 and for shift-2 9,000'),
('D2D_Seats', '10'),
('Instruments', '80'),
('Labs', '12'),
('Master', 'We do not have master program'),
('MQ_Seats', '80'),
('Package', '2.5 lacs'),
('Placement', '98'),
('Schedule', '4 hours lectures and 2 hours labs'),
('Scope', 'Future is all about technology'),
('shifts', '2'),
('Staffs', '25'),
('Students_Class', '60'),
('Syllabus', 'gtu.ac.in'),
('Total_Seats', '180');

-- --------------------------------------------------------

--
-- Table structure for table `Electrical_Engineering`
--

CREATE TABLE `Electrical_Engineering` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Electrical_Engineering`
--

INSERT INTO `Electrical_Engineering` (`tag`, `status`) VALUES
('Abroad', 'Canada and Spain'),
('APCP_Seats', '100'),
('BG_Ratio', '2:3'),
('Classes', '3'),
('Companies', '102'),
('Companies_name', 'ABC'),
('Cutoff', 'for shift-1 8,000 and for shift-2 9,000'),
('D2D_Seats', '10'),
('Instruments', '80'),
('Labs', '12'),
('Master', 'We do not have master program'),
('MQ_Seats', '80'),
('Package', '2.5 lacs'),
('Placement', '98'),
('Schedule', '4 hours lectures and 2 hours labs'),
('Scope', 'Future is all about technology'),
('shifts', '2'),
('Staffs', '25'),
('Students_Class', '60'),
('Syllabus', 'gtu.ac.in'),
('Total_Seats', '180');

-- --------------------------------------------------------

--
-- Table structure for table `Electronic_Communication_Engineering`
--

CREATE TABLE `Electronic_Communication_Engineering` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Electronic_Communication_Engineering`
--

INSERT INTO `Electronic_Communication_Engineering` (`tag`, `status`) VALUES
('Abroad', 'Canada and Spain'),
('APCP_Seats', '100'),
('BG_Ratio', '2:3'),
('Classes', '3'),
('Companies', '102'),
('Companies_name', 'ABC'),
('Cutoff', 'for shift-1 8,000 and for shift-2 9,000'),
('D2D_Seats', '10'),
('Instruments', '80'),
('Labs', '12'),
('Master', 'we have master program for electronics'),
('MQ_Seats', '80'),
('Package', '2.5 lacs'),
('Placement', '98'),
('Schedule', '4 hours lectures and 2 hours labs'),
('Scope', 'Future is all about technology'),
('shifts', '2'),
('Staffs', '25'),
('Students_Class', '60'),
('Syllabus', 'gtu.ac.in'),
('Total_Seats', '180');

-- --------------------------------------------------------

--
-- Table structure for table `Manager`
--

CREATE TABLE `Manager` (
  `id` int(3) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(32) NOT NULL,
  `email` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL,
  `random_id` int(6) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Manager`
--

INSERT INTO `Manager` (`id`, `username`, `password`, `email`, `role`, `random_id`, `create_time`) VALUES
(1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'jabhi1210@gmail.com', 'admin', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `Mechanical_Engineering`
--

CREATE TABLE `Mechanical_Engineering` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Mechanical_Engineering`
--

INSERT INTO `Mechanical_Engineering` (`tag`, `status`) VALUES
('Abroad', 'Canada and Spain'),
('APCP_Seats', '100'),
('BG_Ratio', '2:3'),
('Classes', '3'),
('Companies', '102'),
('Companies_name', 'ABC'),
('Cutoff', 'for shift-1 8,000 and for shift-2 9,000'),
('D2D_Seats', '10'),
('Instruments', '80'),
('Labs', '12'),
('Master', 'We have master program.'),
('MQ_Seats', '80'),
('Package', '2.5 lacs'),
('Placement', '98'),
('Schedule', '4 hours lectures and 2 hours labs'),
('Scope', 'Future is all about technology'),
('shifts', '2'),
('Staffs', '25'),
('Students_Class', '60'),
('Syllabus', 'gtu.ac.in'),
('Total_Seats', '180');

-- --------------------------------------------------------

--
-- Table structure for table `Pharmacy`
--

CREATE TABLE `Pharmacy` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Pharmacy`
--

INSERT INTO `Pharmacy` (`tag`, `status`) VALUES
('Abroad', 'Canada and Spain'),
('APCP_Seats', '100'),
('Classes', '3'),
('Companies', '102'),
('Companies_name', 'ABC'),
('Cutoff', 'for shift-1 8,000 and for shift-2 9,000'),
('D2D_Seats', '10'),
('Duration', '4 years'),
('Eligibility', '12th science with min 45%'),
('Fees', '1.2 lacs'),
('Instruments', '80'),
('Labs', '12'),
('Master', 'We have master program.'),
('MQ_Seats', '80'),
('Package', '2.5 lacs'),
('Placement', '98'),
('Schedule', '4 hours lectures and 2 hours labs'),
('Scope', 'Future is all about technology'),
('shifts', '2'),
('Staffs', '25'),
('Students_Class', '60'),
('Syllabus', 'gtu.ac.in'),
('Timing', '10 am to 5pm'),
('Total_Seats', '180'),
('Training', '6 months'),
('University', 'GTU');

-- --------------------------------------------------------

--
-- Table structure for table `Physiotherapy`
--

CREATE TABLE `Physiotherapy` (
  `tag` varchar(50) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Physiotherapy`
--

INSERT INTO `Physiotherapy` (`tag`, `status`) VALUES
('Abroad', 'Canada and Spain'),
('APCP_Seats', '100'),
('Classes', '3'),
('Companies', '102'),
('Companies_name', 'ABC'),
('Cutoff', 'for shift-1 8,000 and for shift-2 9,000'),
('D2D_Seats', '10'),
('Duration', '4 years'),
('Eligibility', '12th science with min 45%'),
('Fees', '1.2 lacs'),
('Instruments', '80'),
('Labs', '12'),
('Master', 'We do not have master program.'),
('MQ_Seats', '80'),
('Package', '2.5 lacs'),
('Placement', '98'),
('Schedule', '4 hours lectures and 2 hours labs'),
('Scope', 'Future is all about technology'),
('shifts', '2'),
('Staffs', '25'),
('Students_Class', '60'),
('Syllabus', 'gtu.ac.in'),
('Timing', '10 am to 5pm'),
('Total_Seats', '180'),
('Training', '6 months'),
('University', 'Shri Govind Guru University Godhra and Government of Gujarat and UGC recognisated');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Administration`
--
ALTER TABLE `Administration`
  ADD PRIMARY KEY (`tag`);

--
-- Indexes for table `Civil_Engineering`
--
ALTER TABLE `Civil_Engineering`
  ADD PRIMARY KEY (`tag`);

--
-- Indexes for table `Computer_Engineering`
--
ALTER TABLE `Computer_Engineering`
  ADD PRIMARY KEY (`tag`);

--
-- Indexes for table `Electrical_Engineering`
--
ALTER TABLE `Electrical_Engineering`
  ADD PRIMARY KEY (`tag`);

--
-- Indexes for table `Electronic_Communication_Engineering`
--
ALTER TABLE `Electronic_Communication_Engineering`
  ADD PRIMARY KEY (`tag`);

--
-- Indexes for table `Manager`
--
ALTER TABLE `Manager`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Mechanical_Engineering`
--
ALTER TABLE `Mechanical_Engineering`
  ADD PRIMARY KEY (`tag`);

--
-- Indexes for table `Pharmacy`
--
ALTER TABLE `Pharmacy`
  ADD PRIMARY KEY (`tag`);

--
-- Indexes for table `Physiotherapy`
--
ALTER TABLE `Physiotherapy`
  ADD PRIMARY KEY (`tag`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Manager`
--
ALTER TABLE `Manager`
  MODIFY `id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
DELIMITER $$
--
-- Events
--
CREATE DEFINER=`root`@`localhost` EVENT `link_expire` ON SCHEDULE EVERY 1 MINUTE STARTS '2018-04-14 01:50:40' ON COMPLETION NOT PRESERVE ENABLE DO UPDATE Manager SET random_id = NULL, create_time = NULL WHERE  DATE_ADD(create_time, INTERVAL 15 MINUTE) <= NOW()$$

DELIMITER ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
