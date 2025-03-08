-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 10, 2023 at 05:59 AM
-- Server version: 5.7.23-23
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iotcl6k4_projectdb2`
--

-- --------------------------------------------------------

--
-- Table structure for table `disk_chain`
--

CREATE TABLE `disk_chain` (
  `id` int(11) NOT NULL,
  `block_count` int(11) NOT NULL,
  `pre_value` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `bcode` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `rdate` varchar(20) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


--
-- Table structure for table `disk_chain_hash`
--

CREATE TABLE `disk_chain_hash` (
  `id` int(11) NOT NULL,
  `bcode` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `hdata` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `vdata` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
ALTER TABLE `disk_chain`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `disk_chain_hash`
--
ALTER TABLE `disk_chain_hash`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
