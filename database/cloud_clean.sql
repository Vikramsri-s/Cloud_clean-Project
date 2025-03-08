-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 18, 2024 at 08:36 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cloud_clean`
--

-- --------------------------------------------------------

--
-- Table structure for table `cu_admin`
--

CREATE TABLE `cu_admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `server_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_admin`
--

INSERT INTO `cu_admin` (`username`, `password`, `server_st`) VALUES
('cloud', '12345', 1);

-- --------------------------------------------------------

--
-- Table structure for table `cu_files`
--

CREATE TABLE `cu_files` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `detail` varchar(100) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `filesize1` double NOT NULL,
  `filesize2` double NOT NULL,
  `share_st` int(11) NOT NULL,
  `used` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `pay_st` int(11) NOT NULL,
  `ehour` int(11) NOT NULL,
  `emin` int(11) NOT NULL,
  `edate` varchar(20) NOT NULL,
  `tsize` double NOT NULL,
  `sms_st` int(11) NOT NULL,
  `rtime` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_files`
--

INSERT INTO `cu_files` (`id`, `uname`, `filename`, `detail`, `rdate`, `filesize1`, `filesize2`, `share_st`, `used`, `pid`, `pay_st`, `ehour`, `emin`, `edate`, `tsize`, `sms_st`, `rtime`) VALUES
(2, 'raja', 'F2docmm.docx', 'test', '17-04-2024', 14240, 0.014, 0, 0, 1, 0, 11, 20, '2024-04-19', 4.69, 0, '10-58-30'),
(3, 'raja', 'F3mydoc1.pdf', 'test', '17-04-2024', 399193, 0.38, 0, 0, 1, 0, 10, 10, '2024-04-20', 9.48, 0, '10-59-10'),
(4, 'raja', 'F4audd.wav', 'test audio', '18-04-2024', 1282518, 1.222, 0, 0, 1, 0, 11, 20, '2024-04-19', 6.57, 0, '11-02-44'),
(5, 'kumar', 'F5career.txt', 'test', '18-04-2024', 135, 0, 0, 0, 2, 0, 15, 20, '2024-04-20', 9.48, 0, '12-06-04'),
(6, 'kumar', 'F6docmm.docx', 'test', '18-04-2024', 14240, 0.014, 0, 0, 2, 0, 15, 20, '2024-04-18', 6.57, 0, '12-06-34'),
(7, 'raja', 'F7vdd.mp4', 'test', '18-04-2024', 90461, 0.086, 0, 0, 1, 0, 15, 20, '2024-04-18', 3.64, 0, '13-17-28'),
(8, 'raja', 'F8aaa.txt', 'my data', '18-04-2024', 163, 0, 0, 0, 1, 0, 16, 15, '2024-04-18', 5.3, 0, '13-25-44');

-- --------------------------------------------------------

--
-- Table structure for table `cu_log`
--

CREATE TABLE `cu_log` (
  `id` int(11) NOT NULL,
  `utype` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `fname` varchar(20) NOT NULL,
  `fid` int(11) NOT NULL,
  `status` varchar(50) NOT NULL,
  `tempsize` double NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `rtime` varchar(20) NOT NULL,
  `owner` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_log`
--

INSERT INTO `cu_log` (`id`, `utype`, `uname`, `fname`, `fid`, `status`, `tempsize`, `rdate`, `rtime`, `owner`) VALUES
(1, 'Owner', 'raja', 'F1F1aa.jpg', 1, 'Outsourced Data', 0, '17-04-2024', '10-57-00', 'raja'),
(2, 'Owner', 'raja', 't1.temp', 1, 'Temp File Created', 5.3, '17-04-2024', '10-57-00', 'raja'),
(3, 'Owner', 'raja', 'F2docmm.docx', 2, 'Outsourced Data', 0, '17-04-2024', '10-58-30', 'raja'),
(4, 'Owner', 'raja', 't2.temp', 2, 'Temp File Created', 4.69, '17-04-2024', '10-58-30', 'raja'),
(5, 'Owner', 'raja', 'F3mydoc1.pdf', 3, 'Outsourced Data', 0, '18-04-2024', '10-59-11', 'raja'),
(6, 'Owner', 'raja', 't3.temp', 3, 'Temp File Created', 9.48, '18-04-2024', '10-59-11', 'raja'),
(7, 'Owner', 'raja', 'F2docmm.docx', 2, 'Deduplication Detected', 0, '18-04-2024', '11-00-02', 'raja'),
(8, 'Owner', 'raja', 'F1F1aa.jpg', 1, 'Deduplication Detected', 0, '18-04-2024', '11-02-10', 'raja'),
(9, 'Owner', 'raja', 'F4audd.wav', 4, 'Outsourced Data', 0, '18-04-2024', '11-02-44', 'raja'),
(10, 'Owner', 'raja', 't4.temp', 4, 'Temp File Created', 6.57, '18-04-2024', '11-02-44', 'raja'),
(11, 'Owner', 'raja', 'F1F1aa.jpg', 1, 'File Viewed', 0, '18-04-2024', '11-03-37', 'raja'),
(12, 'Owner', 'raja', 'F1F1aa.jpg', 1, 'Shared to suresh', 0, '18-04-2024', '11-03-44', 'raja'),
(13, 'Owner', 'raja', 'F5aa.txt', 5, 'Outsourced Data', 0, '18-04-2024', '11-09-01', 'raja'),
(14, 'Owner', 'raja', 't5.temp', 5, 'Temp File Created', 9.48, '18-04-2024', '11-09-01', 'raja'),
(15, 'Owner', 'raja', 'F5aa.txt', 5, 'File Deleted', 0, '18-04-2024', '11-09-47', 'raja'),
(16, 'Owner', 'raja', 'F3mydoc1.pdf', 3, 'File Viewed', 0, '18-04-2024', '11-10-31', 'raja'),
(17, 'Owner', 'raja', 'F5F1aa.jpg', 5, 'Outsourced Data', 0, '18-04-2024', '11-12-41', 'raja'),
(18, 'Owner', 'raja', 't5.temp', 5, 'Temp File Created', 4.69, '18-04-2024', '11-12-41', 'raja'),
(19, 'Owner', 'raja', 'F5F1aa.jpg', 5, 'Outsourced Data', 0, '18-04-2024', '11-21-26', 'raja'),
(20, 'Owner', 'raja', 't5.temp', 5, 'Temp File Created', 9.48, '18-04-2024', '11-21-26', 'raja'),
(21, 'Owner', 'raja', 'F4audd.wav', 4, 'Shared to suresh', 0, '18-04-2024', '11-21-59', 'raja'),
(22, 'Owner', 'raja', 'F3mydoc1.pdf', 3, 'File Viewed', 0, '18-04-2024', '11-24-39', 'raja'),
(23, 'Owner', 'raja', 'F3mydoc1.pdf', 3, 'Shared to suresh', 0, '18-04-2024', '11-24-46', 'raja'),
(24, 'Owner', 'raja', 'F3mydoc1.pdf', 3, 'File Downloaded', 0, '18-04-2024', '11-26-35', 'raja'),
(25, 'Owner', 'raja', 'F5F1aa.jpg', 5, 'Auto Deleted', 0, '18-04-2024', '11-30-13', 'raja'),
(26, 'User', 'suresh', 'F3mydoc1.pdf', 3, 'File Viewed', 0, '18-04-2024', '11-30-52', 'raja'),
(27, 'User', 'suresh', 'F3mydoc1.pdf', 3, 'File Downloaded', 0, '18-04-2024', '11-30-55', 'raja'),
(28, 'User', 'suresh', 'F3mydoc1.pdf', 3, 'File Update and Uploaded', 0, '18-04-2024', '11-31-44', 'raja'),
(29, 'User', 'suresh', 'F3mydoc1.pdf', 3, 'File Downloaded', 0, '18-04-2024', '12-04-17', 'raja'),
(30, 'Owner', 'kumar', 'F5career.txt', 5, 'Outsourced Data', 0, '18-04-2024', '12-06-05', 'kumar'),
(31, 'Owner', 'kumar', 't5.temp', 5, 'Temp File Created', 9.48, '18-04-2024', '12-06-05', 'kumar'),
(32, 'Owner', 'kumar', 'F6docmm.docx', 6, 'Outsourced Data', 0, '18-04-2024', '12-06-34', 'kumar'),
(33, 'Owner', 'kumar', 't6.temp', 6, 'Temp File Created', 6.57, '18-04-2024', '12-06-34', 'kumar'),
(34, 'Owner', 'kumar', 'F6docmm.docx', 6, 'Deduplication Detected', 0, '18-04-2024', '12-07-40', 'kumar'),
(35, 'Owner', 'raja', 'F7vdd.mp4', 7, 'Outsourced Data', 0, '18-04-2024', '13-17-28', 'raja'),
(36, 'Owner', 'raja', 't7.temp', 7, 'Temp File Created', 3.64, '18-04-2024', '13-17-28', 'raja'),
(37, 'Owner', 'raja', 'F8aaa.txt', 8, 'Outsourced Data', 0, '18-04-2024', '13-25-44', 'raja'),
(38, 'Owner', 'raja', 't8.temp', 8, 'Temp File Created', 5.3, '18-04-2024', '13-25-44', 'raja'),
(39, 'Owner', 'raja', 'F3mydoc1.pdf', 3, 'File Viewed', 0, '18-04-2024', '13-27-49', 'raja'),
(40, 'Owner', 'raja', 'F2docmm.docx', 2, 'File Viewed', 0, '18-04-2024', '13-27-54', 'raja'),
(41, 'Owner', 'raja', 'F2docmm.docx', 2, 'Shared to suresh', 0, '18-04-2024', '13-29-19', 'raja'),
(42, 'User', 'suresh', 'F2docmm.docx', 2, 'File Viewed', 0, '18-04-2024', '13-31-09', ''),
(43, 'Owner', 'raja', 'F3mydoc1.pdf', 3, 'Deduplication Detected', 0, '18-04-2024', '13-59-01', '');

-- --------------------------------------------------------

--
-- Table structure for table `cu_owner`
--

CREATE TABLE `cu_owner` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `location` varchar(50) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `plan_id` int(11) NOT NULL,
  `bkey` varchar(20) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_owner`
--

INSERT INTO `cu_owner` (`id`, `name`, `gender`, `dob`, `mobile`, `email`, `location`, `uname`, `pass`, `rdate`, `status`, `plan_id`, `bkey`, `dtime`) VALUES
(1, 'Raja', 'Male', '1990-06-05', 9894442716, 'raja11@gmail.com', 'Salem', 'raja', '123456', '17-04-2024', 1, 1, '', '2024-04-18 13:24:04'),
(2, 'Kumar', 'Male', '1990-06-05', 9848451212, 'kumar@gmail.com', 'Chennai', 'kumar', '123456', '18-04-2024', 1, 2, '', '2024-04-18 12:05:22');

-- --------------------------------------------------------

--
-- Table structure for table `cu_payment`
--

CREATE TABLE `cu_payment` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `total_size` double NOT NULL,
  `amount` double NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `rtime` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_payment`
--


-- --------------------------------------------------------

--
-- Table structure for table `cu_plan`
--

CREATE TABLE `cu_plan` (
  `id` int(11) NOT NULL,
  `storage` double NOT NULL,
  `stype` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `duration` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_plan`
--

INSERT INTO `cu_plan` (`id`, `storage`, `stype`, `price`, `duration`) VALUES
(1, 100, 'MB', 1000, '3 months'),
(2, 50, 'MB', 500, '2 months'),
(3, 30, 'MB', 300, '1 month'),
(4, 10, 'MB', 100, '1 month'),
(5, 5, 'MB', 50, '1 month');

-- --------------------------------------------------------

--
-- Table structure for table `cu_share`
--

CREATE TABLE `cu_share` (
  `id` int(11) NOT NULL,
  `owner` varchar(20) NOT NULL,
  `user` varchar(20) NOT NULL,
  `fid` int(11) NOT NULL,
  `view_st` int(11) NOT NULL,
  `download_st` int(11) NOT NULL,
  `upload_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_share`
--

INSERT INTO `cu_share` (`id`, `owner`, `user`, `fid`, `view_st`, `download_st`, `upload_st`) VALUES
(4, 'raja', 'suresh', 3, 3, 0, 0),
(5, 'raja', 'suresh', 2, 3, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `cu_storage`
--

CREATE TABLE `cu_storage` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pid` int(11) NOT NULL,
  `storage` double NOT NULL,
  `stype` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `rdate` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `share` int(11) NOT NULL,
  `used` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_storage`
--

INSERT INTO `cu_storage` (`id`, `uname`, `pid`, `storage`, `stype`, `price`, `rdate`, `status`, `share`, `used`) VALUES
(1, 'raja', 1, 100, 'MB', 1000, '17-04-2024', 1, 0, 1.702),
(2, 'kumar', 2, 50, 'MB', 500, '18-04-2024', 1, 0, 0.014);

-- --------------------------------------------------------

--
-- Table structure for table `cu_user`
--

CREATE TABLE `cu_user` (
  `id` int(11) NOT NULL,
  `owner` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cu_user`
--

INSERT INTO `cu_user` (`id`, `owner`, `name`, `mobile`, `email`, `uname`, `pass`) VALUES
(1, 'raja', 'Suresh', 9854842545, 'bgeduscanner@gmail.com', 'suresh', '123456');
