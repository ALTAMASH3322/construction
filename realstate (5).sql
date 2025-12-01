-- phpMyAdmin SQL Dump
-- version 5.2.1deb3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 01, 2025 at 08:38 AM
-- Server version: 8.0.44-0ubuntu0.24.04.1
-- PHP Version: 8.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `realstate`
--

DELIMITER $$
--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `generate_random_alphanum` (`length` INT) RETURNS VARCHAR(255) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci DETERMINISTIC BEGIN
    -- Define the set of characters to choose from.
    -- Ambiguous characters like 0, O, 1, I, l have been removed for clarity.
    DECLARE chars_str VARCHAR(255) DEFAULT 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'$$

CREATE DEFINER=`root`@`localhost` FUNCTION `generate_unique_agent_id` () RETURNS CHAR(8) CHARSET utf8mb4 DETERMINISTIC BEGIN
    DECLARE new_id CHAR(8)$$

CREATE DEFINER=`root`@`localhost` FUNCTION `generate_unique_invoice_number` () RETURNS CHAR(10) CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci DETERMINISTIC BEGIN
    -- Define the character set (uppercase letters and numbers)
    DECLARE chars_str VARCHAR(36) DEFAULT 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'$$

CREATE DEFINER=`root`@`localhost` FUNCTION `generate_unique_property_id` () RETURNS VARCHAR(10) CHARSET utf8mb4 DETERMINISTIC BEGIN
    DECLARE new_id VARCHAR(10)$$

CREATE DEFINER=`root`@`localhost` FUNCTION `generate_unique_user_id` () RETURNS VARCHAR(6) CHARSET utf8mb4 DETERMINISTIC BEGIN
    DECLARE new_id VARCHAR(6)$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `log_id` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `activity_type` varchar(100) DEFAULT NULL,
  `description` text,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `agents`
--

CREATE TABLE `agents` (
  `agent_id_1` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `agent_type` enum('independent','affiliated') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'independent',
  `company_id` int DEFAULT NULL,
  `company_position` varchar(100) DEFAULT NULL,
  `company_license_number` varchar(100) DEFAULT NULL,
  `personal_license_number` varchar(100) DEFAULT NULL,
  `license_issuing_authority` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `address_city` varchar(100) DEFAULT NULL,
  `address_postal_code` varchar(20) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `experience_years` int DEFAULT NULL,
  `specialization` text,
  `bio` text,
  `linkedin` varchar(255) DEFAULT NULL,
  `instagram` varchar(255) DEFAULT NULL,
  `facebook` varchar(255) DEFAULT NULL,
  `personal_website` varchar(255) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `agent_status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `x_account` varchar(255) DEFAULT NULL,
  `daily_booking_limit` int DEFAULT '5',
  `agent_id` char(8) NOT NULL,
  `average_rating` decimal(3,2) NOT NULL DEFAULT '0.00',
  `review_count` int NOT NULL DEFAULT '0',
  `free_posts_remaining` int NOT NULL DEFAULT '0',
  `paid_credits` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `agents`
--

INSERT INTO `agents` (`agent_id_1`, `user_id`, `agent_type`, `company_id`, `company_position`, `company_license_number`, `personal_license_number`, `license_issuing_authority`, `country`, `state`, `city`, `address_city`, `address_postal_code`, `contact_number`, `email`, `experience_years`, `specialization`, `bio`, `linkedin`, `instagram`, `facebook`, `personal_website`, `profile_picture`, `agent_status`, `created_at`, `updated_at`, `x_account`, `daily_booking_limit`, `agent_id`, `average_rating`, `review_count`, `free_posts_remaining`, `paid_credits`) VALUES
(39, 'UNG2OZ', 'independent', NULL, NULL, NULL, '77141714', 'government ', 'india', 'uttar pradesh', NULL, 'aligarh', '202001', '1234567890', 'farman@gmail.com', 2, 'Hr', 'hello', 'xyz', 'xyz', 'xyz', 'https://demo1.skyjaya.com/', '/uploads/18_1707132584657.jpg', 'approved', '2025-10-28 07:21:55', '2025-11-26 12:04:23', 'comeon', 10, 'AGNBYIE8', 0.00, 0, 0, 606),
(40, 'IE6C0P', 'affiliated', 39, 'manager', '00496496', '', '', ' Malaysia', ' Sabah', ' Kota Kinabalu', 'shah alam,40160', '059565', '8194067267', 'altamash3321@gmail.com', 5, NULL, 'hey i am software developer', 'xyz', 'xyz', 'xyz', 'https://demo1.skyjaya.com/', '/uploads/18_1707132584657.jpg', 'approved', '2025-10-28 07:28:24', '2025-12-01 07:13:52', 'xyz', 5, 'AGNQNTVL', 5.00, 1, 0, 304),
(41, '4UNG3R', 'independent', NULL, NULL, NULL, NULL, NULL, 'Malaysia', 'uttar pradesh', NULL, 'aligarh', NULL, '9058101306', 'ankit@gmail.com', 5, 'backend developer', 'ban gaya kya', 'xyz', 'xyz', 'xyz', 'https://demo1.skyjaya.com/', '/uploads/44_1707132584657.jpg', 'approved', '2025-11-18 07:15:31', '2025-11-26 10:59:25', NULL, 5, 'AGNKAG67', 0.00, 0, 2, 0),
(42, '579F1P', 'affiliated', 40, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Himanshu@gmail.com', 2, 'Hr', 'hey ye bhi ho gaya', 'https://demo1.skyjaya.com/', 'https://demo1.skyjaya.com/', 'https://demo1.skyjaya.com/', 'https://demo1.skyjaya.com/', '/uploads/45_1707132584657.jpg', 'pending', '2025-11-18 07:53:50', '2025-11-26 08:28:32', '', 5, 'AGNMCKJQ', 0.00, 0, 2, 0),
(43, 'RI1DGY', 'independent', NULL, NULL, NULL, NULL, NULL, 'Malaysia', 'indian', NULL, 'shah alam,40160', NULL, '9058101306', 'rekha@gmail.com', 2, ' frontend', 'dssdfdsdsd', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', '/uploads/48_1707132584657.jpg', 'pending', '2025-11-19 12:24:36', '2025-11-26 08:28:32', NULL, 5, 'AGNXDUTB', 0.00, 0, 2, 0),
(44, 'ZRMKN9', 'affiliated', 41, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'tabish@gmail.com', 2, ' frontend', 'gfgfg', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', '/uploads/49_1707132584657.jpg', 'pending', '2025-11-19 12:30:09', '2025-11-26 08:28:32', 'https://skyjaya.com/', 5, 'AGNCFR9S', 0.00, 0, 2, 0),
(48, '96S4X2', 'independent', NULL, NULL, NULL, NULL, NULL, 'Malaysia', 'Selangor', NULL, 'Shah Alam', NULL, '9915857690', 'basheer.mca@gmail.com', 5, 'Residentials', 'fadsf asfasfa asfddsdfas asfasdfa asdfasdfas asfddasf', '', '', '', 'http://www.abc.com', NULL, 'approved', '2025-11-20 16:08:03', '2025-11-26 16:29:17', NULL, 5, 'AGNZV75V', 0.00, 0, 0, 25),
(49, '1US551', 'affiliated', 45, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'basheer.atxlearning@gmail.com', 5, 'Residentials & Commercials', 'adsf asdfa sdfas asdfasfas adfssfsaf asfd', '', '', '', '', '/uploads/61_Chatbot_img.png', 'approved', '2025-11-20 16:24:36', '2025-11-26 08:28:32', '', 5, 'AGNTXYM2', 0.00, 0, 1, 0),
(50, 'S8L0YG', 'affiliated', 46, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'naim@gmail.com', 2, ' frontend', 'hey ', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', '/uploads/62_1707132584657.jpg', 'pending', '2025-11-21 09:25:42', '2025-11-26 08:28:32', 'https://skyjaya.com/', 5, 'AGNEGTEC', 0.00, 0, 2, 0),
(51, 'B1YFZC', 'independent', NULL, NULL, NULL, 'rdshesh', 'tyheh', 'India', 'Jharkhand', NULL, 'jamshedpur', '831004', '07257830471', 'md.altamash@gmail.com', 5, 'serheshs', 'WREGHARHARSH', 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', NULL, 'approved', '2025-11-21 11:28:49', '2025-11-26 10:59:16', 'https://www.perplexity.ai/', 5, 'AGN9IIPO', 0.00, 0, 1, 25),
(52, 'OZN0SL', 'affiliated', 42, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'saggy@gmail.com', 5, 'serheshs', 'wrhgarseharshaerbh', 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', NULL, 'approved', '2025-11-21 11:38:27', '2025-11-26 08:28:32', 'https://www.perplexity.ai/', 5, 'AGNTOREG', 0.00, 0, 2, 100),
(53, '1GWT5Y', 'independent', NULL, NULL, NULL, NULL, NULL, 'Malaysia', 'kualalumpur', NULL, 'kuala lumpur', NULL, '7257830471', 'farmaaaan@gmail.com', 5, 'commercial', 'fajfiyaeca iugauiba viba', '', '', '', '', NULL, 'approved', '2025-11-21 12:12:55', '2025-11-26 08:28:32', NULL, 5, 'AGNHIVLZ', 0.00, 0, 1, 100),
(54, '1ZJGEE', 'independent', NULL, NULL, NULL, NULL, NULL, 'Malaysia', 'Kedah', NULL, 'Kulim', NULL, '9058101306', 'sagar@gmail.com', 5, ' frontend', 'gfyfyu', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', NULL, 'pending', '2025-11-25 04:27:34', '2025-11-26 08:28:32', NULL, 5, 'AGNN1ZJH', 0.00, 0, 2, 0),
(55, 'KKVCX8', 'affiliated', 39, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'ramu@gmail.com', 2, ' frontend', 'hhhh', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', '/uploads/72_1707132584657.jpg', 'rejected', '2025-11-25 04:31:17', '2025-11-26 08:28:32', 'https://skyjaya.com/', 5, 'AGNMETMF', 0.00, 0, 2, 0),
(56, '6K020N', 'independent', NULL, NULL, NULL, NULL, NULL, 'Malaysia', 'Kelantan', NULL, 'Pasir Mas', NULL, '9058101306', 'farman.skyjaya@gmail.com', 5, 'backend developer', 'hhh', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', '/uploads/19_1707132584657.jpg', 'rejected', '2025-11-25 04:49:29', '2025-11-30 16:31:27', NULL, 5, 'AGNXPDKG', 0.00, 0, 2, 0),
(59, 'LT2NPD', 'independent', NULL, NULL, NULL, '1112254599', 'government of India', 'Malaysia', 'Labuan', NULL, 'Victoria', '87000', '9058101306', 'farman@testgmail.com', 5, 'Hr', 'aaaa', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', NULL, 'pending', '2025-11-26 10:57:36', '2025-11-26 10:58:30', 'https://skyjaya.com/', 5, 'DXADP48I', 0.00, 0, 3, 0),
(60, 'BTVM7V', 'independent', NULL, NULL, NULL, '1112254599', 'government of India', 'Malaysia', 'Kuala Lumpur', NULL, 'Cheras', '56100', '9058101306', 'home@gmail.com', 5, 'Hr', 'sssss', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', '/uploads/BTVM7V_Pixel-9-render-leak--1024x866.jpg', 'pending', '2025-11-26 12:15:13', '2025-11-26 12:15:13', 'https://skyjaya.com/', 5, 'AN230I8E', 0.00, 0, 3, 0),
(61, 'V4ORGS', 'affiliated', 41, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'dream@gmail.com', 2, ' frontend', 'aaa', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://skyjaya.com/', 'https://demo1.skyjaya.com/', NULL, 'pending', '2025-11-26 12:17:07', '2025-11-26 12:17:07', NULL, 5, 'RLEZG1I8', 0.00, 0, 3, 0);

--
-- Triggers `agents`
--
DELIMITER $$
CREATE TRIGGER `before_agent_insert` BEFORE INSERT ON `agents` FOR EACH ROW BEGIN
    SET NEW.agent_id = generate_unique_agent_id()$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL,
  `property_id` varchar(10) DEFAULT NULL,
  `agent_id` varchar(8) NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time DEFAULT NULL,
  `status` enum('pending','confirmed','cancelled','completed') NOT NULL DEFAULT 'pending',
  `user_notes` text,
  `agent_notes` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointment_id`, `property_id`, `agent_id`, `user_id`, `appointment_date`, `appointment_time`, `status`, `user_notes`, `agent_notes`, `created_at`, `updated_at`) VALUES
(11, '1GVRUQTMDQ', 'AGNQNTVL', '6K020N', '2025-11-29', '08:32:00', 'confirmed', 'aaban', 'ho bhai', '2025-10-31 10:35:38', '2025-11-26 09:17:37'),
(38, 'R7JS3SC345', 'AGNQNTVL', '6K020N', '2025-11-28', '16:12:00', 'confirmed', 'vvv', 'cdkytduyf', '2025-11-04 04:05:33', '2025-11-26 09:17:37'),
(39, '1GVRUQTMDQ', 'AGNQNTVL', 'IE6C0P', '2025-11-15', '14:08:00', 'confirmed', NULL, 'hh', '2025-11-10 11:20:28', '2025-11-26 09:17:37'),
(40, 'WBO6KYV76Z', 'AGNQNTVL', '6K020N', '2025-11-21', NULL, 'cancelled', 'jj', 'hdiy6rdugv;.', '2025-11-19 10:54:32', '2025-11-26 09:17:37'),
(43, 'K4NMWCQCB8', 'AGNQNTVL', '6T9LU7', '2025-11-22', '16:10:00', 'confirmed', 'srsbm', 'xtrjsuts', '2025-11-20 06:31:06', '2025-11-26 09:17:37'),
(44, 'K4NMWCQCB8', 'AGNQNTVL', '6K020N', '2025-11-29', '21:34:00', 'confirmed', 'hii', 'dffdff', '2025-11-20 11:18:55', '2025-11-26 09:17:37'),
(45, 'PVXPJAJJRY', 'AGNZV75V', '2TK4LE', '2025-11-24', '14:30:00', 'confirmed', 'fasdfas fsdsfasfads', 'dfsgs gsdgfsdg sgfdsdgfs sdfgsdgfs sdgffsd', '2025-11-20 17:13:53', '2025-11-26 09:17:37'),
(46, '9V9IHL9985', 'AGNQNTVL', '6K020N', '2025-11-29', NULL, 'pending', 'ss', NULL, '2025-11-21 10:00:29', '2025-11-26 09:17:37'),
(48, 'NKJT5Z6NG1', 'AGNBYIE8', 'A0TTD6', '2025-11-30', '20:00:00', 'confirmed', 'hi I want to see your apartment', 'please visit on this date and time', '2025-11-21 12:00:53', '2025-11-26 09:17:37'),
(49, 'PVXPJAJJRY', 'AGNQNTVL', 'IE6C0P', '2025-11-26', NULL, 'pending', 'fadsf afasf asfd', NULL, '2025-11-24 16:43:19', '2025-11-26 09:17:37'),
(50, 'YPDI4TFFLE', 'AGNZV75V', '2TK4LE', '2025-12-01', '15:00:00', 'confirmed', 'fdsf ads asfa sdfasf afsdadsdf afsasf asfas asf fasdfadsf', 'fadsf asdfasf as asdfasf asdfasdf asdfadsdf a', '2025-11-26 16:17:06', '2025-11-26 17:05:30'),
(51, 'W3HTC0SK99', 'AGNTXYM2', '2TK4LE', '2025-11-29', NULL, 'pending', 'dasfa dfasdf afs asdfsadf sdfdsfadsf asdfas', NULL, '2025-11-26 16:22:40', '2025-11-26 16:22:40');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `property_id` varchar(10) DEFAULT NULL,
  `scheduled_date` datetime NOT NULL,
  `status` enum('pending','confirmed','cancelled','completed') DEFAULT 'pending',
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `chat_messages`
--

CREATE TABLE `chat_messages` (
  `message_id` bigint NOT NULL,
  `conversation_id` int NOT NULL,
  `sender_user_id` varchar(6) NOT NULL,
  `message_content` text NOT NULL,
  `sent_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `read_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `chat_messages`
--

INSERT INTO `chat_messages` (`message_id`, `conversation_id`, `sender_user_id`, `message_content`, `sent_at`, `read_at`) VALUES
(3, 3, '6K020N', 'Hello, I want to start a chat.', '2025-11-06 04:36:29', NULL),
(4, 3, 'UNG2OZ', 'Hello! How can I help you today?', '2025-11-06 04:36:59', NULL),
(5, 3, '6K020N', 'hii', '2025-11-06 06:05:43', NULL),
(6, 3, '6K020N', 'hi', '2025-11-06 06:06:27', NULL),
(7, 3, '6K020N', 'hi', '2025-11-06 06:54:56', NULL),
(8, 3, '6K020N', 'hello how can i help you', '2025-11-06 09:02:57', NULL),
(9, 3, '6K020N', 'hi', '2025-11-06 09:06:51', NULL),
(10, 3, '6K020N', 'hi', '2025-11-06 10:41:51', NULL),
(11, 3, '6K020N', 'farru bhai', '2025-11-06 10:42:26', NULL),
(12, 3, '6K020N', 'hii', '2025-11-06 10:50:23', NULL),
(13, 3, '6K020N', '???', '2025-11-06 10:54:47', NULL),
(14, 3, '6K020N', '...', '2025-11-06 10:59:28', NULL),
(15, 3, 'UNG2OZ', '..', '2025-11-06 11:04:27', NULL),
(16, 3, '6K020N', 'ho gaya thk', '2025-11-06 11:08:59', NULL),
(17, 3, 'UNG2OZ', 'haan bhai ho gaya', '2025-11-06 11:09:27', NULL),
(18, 3, 'UNG2OZ', 'badiya', '2025-11-06 11:12:39', NULL),
(19, 3, '6K020N', 'mubarak ho', '2025-11-06 11:13:25', NULL),
(20, 3, '6K020N', 'gm', '2025-11-07 04:40:08', NULL),
(21, 3, '6K020N', 'hii', '2025-11-20 05:54:31', NULL),
(22, 3, 'UNG2OZ', 'hii', '2025-11-20 09:43:47', NULL),
(23, 3, '6K020N', 'farru', '2025-11-20 09:53:47', NULL),
(24, 3, 'UNG2OZ', 'hii', '2025-11-20 09:59:02', NULL),
(25, 3, '6K020N', 'Hi, I\'m interested in your property: \"wsfG\". Can you share more details?', '2025-11-20 10:16:52', NULL),
(26, 4, '6K020N', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-20 10:17:07', NULL),
(27, 4, '6K020N', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-20 10:17:07', NULL),
(28, 4, '6K020N', 'farru', '2025-11-20 10:17:20', NULL),
(29, 4, '6K020N', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-20 10:32:41', NULL),
(30, 4, '6K020N', 'farru', '2025-11-20 10:32:51', NULL),
(31, 4, '6K020N', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-20 10:34:29', NULL),
(32, 4, '6K020N', 'hii', '2025-11-20 10:34:38', NULL),
(33, 4, 'IE6C0P', 'yes', '2025-11-20 10:36:13', NULL),
(34, 4, '6K020N', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-20 10:46:29', NULL),
(35, 4, '6K020N', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-20 11:53:34', NULL),
(36, 4, '6K020N', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-20 11:55:57', NULL),
(37, 4, '6K020N', '..', '2025-11-20 11:56:04', NULL),
(38, 5, '2TK4LE', 'Hi, I\'m interested in your property: \"faheem \". Can you share more details?', '2025-11-20 15:29:06', NULL),
(39, 5, '2TK4LE', 'Hi, I\'m interested in your property: \"faheem \". Can you share more details?', '2025-11-20 15:29:06', NULL),
(40, 5, '2TK4LE', 'Hi', '2025-11-20 15:31:08', NULL),
(41, 5, '2TK4LE', 'Hi, I\'m interested in your property: \"Puteri Bayu, Bandar Puteri Puchong – Apartment For Rent\". Can you share more details?', '2025-11-20 15:33:31', NULL),
(42, 5, '2TK4LE', 'Hi, I\'m interested in your property: \"Puteri Bayu, Bandar Puteri Puchong – Apartment For Rent\". Can you share more details?', '2025-11-20 15:35:28', NULL),
(43, 6, '2TK4LE', 'Hi, I\'m interested in your property: \"3BHK Flat RM1500 for Rent\". Can you share more details?', '2025-11-20 17:16:19', NULL),
(44, 6, '2TK4LE', 'Hi, I\'m interested in your property: \"3BHK Flat RM1500 for Rent\". Can you share more details?', '2025-11-20 17:16:19', NULL),
(45, 7, '6T9LU7', 'Hi, I\'m interested in your property: \"faheem \". Can you share more details?', '2025-11-21 10:29:48', NULL),
(46, 7, '6T9LU7', 'Hi, I\'m interested in your property: \"faheem \". Can you share more details?', '2025-11-21 10:29:49', NULL),
(47, 8, 'B1YFZC', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-21 11:27:03', NULL),
(48, 8, 'B1YFZC', 'Hi, I\'m interested in your property: \"al fida \". Can you share more details?', '2025-11-21 11:27:03', NULL),
(49, 9, 'A0TTD6', 'Hi, I\'m interested in your property: \"Ghost House\". Can you share more details?', '2025-11-21 11:56:04', NULL),
(50, 9, 'A0TTD6', 'Hi, I\'m interested in your property: \"Ghost House\". Can you share more details?', '2025-11-21 11:56:04', NULL),
(51, 10, '6K020N', 'Hi, I\'m interested in your property: \"Ghost House\". Can you share more details?', '2025-11-24 04:11:24', NULL),
(52, 10, '6K020N', 'Hi, I\'m interested in your property: \"Ghost House\". Can you share more details?', '2025-11-24 04:11:24', NULL),
(53, 10, '6K020N', 'Hi, I\'m interested in your property: \"Ghost House\". Can you share more details?', '2025-11-24 04:18:52', NULL),
(54, 4, '6K020N', 'Hi, I\'m interested in your property: \"faheem \". Can you share more details?', '2025-11-24 04:19:22', NULL),
(55, 4, '6K020N', 'Hi, I\'m interested in your property: \"faheem \". Can you share more details?', '2025-11-24 04:19:55', NULL),
(56, 4, '6K020N', 'Hi, I\'m interested in your property: \"faheem \". Can you share more details?', '2025-11-24 04:32:34', NULL),
(57, 3, '6K020N', 'Hi, I\'m interested in your property: \"wsfG\". Can you share more details?', '2025-11-24 04:33:02', NULL),
(58, 3, '6K020N', 'Hi, I\'m interested in your property: \"wsfG\". Can you share more details?', '2025-11-24 04:36:31', NULL),
(59, 10, '6K020N', 'Hi, I\'m interested in your property: \"Ghost House\". Can you share more details?', '2025-11-24 05:07:38', NULL),
(60, 10, '6K020N', 'Hi, I\'m interested in your property: \"Ghost House\". Can you share more details?', '2025-11-24 09:57:56', NULL),
(61, 7, '6T9LU7', 'j', '2025-11-26 09:28:56', NULL),
(62, 3, 'UNG2OZ', 'hh', '2025-11-26 11:25:50', NULL),
(63, 6, '2TK4LE', 'Hi, I\'m interested in your property: \"4BHK Flat RM1800 for Rent\". Can you share more details?', '2025-11-26 16:06:31', NULL),
(64, 11, 'UNG2OZ', 'Hi, I\'m interested in your property: \"ytcavdad\". Can you share more details?', '2025-11-30 16:36:42', NULL),
(65, 10, '6K020N', 'H', '2025-12-01 07:51:41', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

CREATE TABLE `comment` (
  `id` int NOT NULL,
  `text` text NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `author_id` varchar(6) NOT NULL,
  `author_type` varchar(50) NOT NULL,
  `sentiment` varchar(50) DEFAULT NULL,
  `ticket_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`id`, `text`, `timestamp`, `author_id`, `author_type`, `sentiment`, `ticket_id`) VALUES
(4, 'erhaeryhadrsh', '2025-11-17 17:45:22', '0DH1FT', 'agent', NULL, 1),
(6, 'Okay we have fixed that now', '2025-11-17 17:52:13', '0DH1FT', 'agent', NULL, 3);

-- --------------------------------------------------------

--
-- Table structure for table `companies`
--

CREATE TABLE `companies` (
  `company_id` int NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `company_type` enum('Real Estate Agency','Real Estate Brokerage','Property Management Company','Developer / Builder','Other') DEFAULT NULL,
  `license_number` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `company_address` varchar(100) DEFAULT NULL,
  `postal_code` varchar(20) DEFAULT NULL,
  `contact_person_name` varchar(100) DEFAULT NULL,
  `contact_person_role` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `description` text,
  `years_in_business` int DEFAULT NULL,
  `facebook` varchar(255) DEFAULT NULL,
  `instagram` varchar(255) DEFAULT NULL,
  `linkedin` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `x_account` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `companies`
--

INSERT INTO `companies` (`company_id`, `company_name`, `company_type`, `license_number`, `country`, `state`, `city`, `company_address`, `postal_code`, `contact_person_name`, `contact_person_role`, `phone_number`, `email`, `website`, `description`, `years_in_business`, `facebook`, `instagram`, `linkedin`, `created_at`, `x_account`) VALUES
(39, 'wani.ai', 'Real Estate Brokerage', '00496496', 'Malaysia', 'Selangor', 'Petaling Jaya', '725 NE 166th St, Miami, FL 33162, USA', '46000', 'ramu', NULL, '+60135567890', 'ramu@gmail.com', 'www.wani.ai', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ', 3, 'https://skyjaya.com/', 'https://skyjaya.com/', NULL, '2025-10-28 07:27:17', 'https://skyjaya.com/'),
(40, 'Waniya Enterprises', 'Developer / Builder', '00465854', 'Malaysia', 'Selangor', 'Shah Alam', 'shah alam', '40000', '', NULL, '+60123456789', 'Himanshu@gmail.com', 'www.skyjaya.com', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ', 5, 'xyz', 'xyz', NULL, '2025-11-18 07:53:03', 'xyz'),
(41, 'skyjaya', 'Real Estate Brokerage', '00496496', 'Malaysia', 'Negeri Sembilan', 'Port Dickson', '725 NE 166th St, Miami, FL 33162, USA', '71000', 'tabish', NULL, '+60123456789', 'dream@gmail.com', 'www.skyjaya.com', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ', 5, 'https://skyjaya.com/', 'https://skyjaya.com/', NULL, '2025-11-19 12:29:46', 'https://skyjaya.com/'),
(42, 'kjsrtj', 'Real Estate Agency', 'jstjsrt', 'Malaysia', 'Perak', 'Ipoh', 'telco kharangajhar', '30000', 'rtghaeh', NULL, '+60123456595', 'saggy@gmail.com', 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', 5, 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', NULL, '2025-11-20 09:07:33', 'https://www.perplexity.ai/'),
(44, 'ATX', 'Property Management Company', 'hrhASZH', 'Malaysia', 'Perlis', 'Kangar', 'reherhd', '01000', 'edrhaerh', NULL, '+60123456789', 'alta@gmail.com', 'https://www.perplexity.ai/', 'raehaerh', 5, 'https://www.perplexity.ai/', 'https://www.perplexity.ai/', NULL, '2025-11-20 09:51:19', 'https://www.perplexity.ai/'),
(45, 'XYZ Pvt. Ltd.', 'Real Estate Agency', 'XYZ054782', 'Malaysia', 'Labuan', 'Victoria', 'Golden Street', '87000', 'Robin', NULL, '+60123440789', 'basheer.atxlearning@gmail.com', '', '', 3, '', '', NULL, '2025-11-20 16:23:04', ''),
(46, 'as web provider', 'Other', '77141714', 'Malaysia', 'Kuala Lumpur', 'Wangsa Maju', 'badi masjid jamalpur', '53300', 'naim', NULL, '+60135567890', 'naim@gmail.com', 'www.skyjaya.com', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ', 3, 'https://skyjaya.com/', 'https://skyjaya.com/', NULL, '2025-11-21 09:25:07', 'https://skyjaya.com/');

-- --------------------------------------------------------

--
-- Table structure for table `conversations`
--

CREATE TABLE `conversations` (
  `conversation_id` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `agent_id` char(8) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `conversations`
--

INSERT INTO `conversations` (`conversation_id`, `user_id`, `agent_id`, `created_at`, `updated_at`) VALUES
(3, '6K020N', 'AGNBYIE8', '2025-11-06 04:36:29', '2025-11-26 08:42:51'),
(4, '6K020N', 'AGNQNTVL', '2025-11-20 10:17:07', '2025-11-26 08:42:51'),
(5, '2TK4LE', 'AGNQNTVL', '2025-11-20 15:29:06', '2025-11-26 08:42:51'),
(6, '2TK4LE', 'AGNZV75V', '2025-11-20 17:16:19', '2025-11-26 08:42:51'),
(7, '6T9LU7', 'AGNQNTVL', '2025-11-21 10:29:48', '2025-11-26 08:42:51'),
(8, 'B1YFZC', 'AGNQNTVL', '2025-11-21 11:27:03', '2025-11-26 08:42:51'),
(9, 'A0TTD6', 'AGN9IIPO', '2025-11-21 11:56:04', '2025-11-26 08:42:51'),
(10, '6K020N', 'AGN9IIPO', '2025-11-24 04:11:24', '2025-11-26 08:42:51'),
(11, 'UNG2OZ', 'AGNHIVLZ', '2025-11-30 16:36:42', '2025-11-30 16:36:42');

-- --------------------------------------------------------

--
-- Table structure for table `credit_plans`
--

CREATE TABLE `credit_plans` (
  `plan_id` int NOT NULL,
  `plan_name` varchar(255) NOT NULL,
  `credits_amount` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `credit_plans`
--

INSERT INTO `credit_plans` (`plan_id`, `plan_name`, `credits_amount`, `price`, `description`, `is_active`, `created_at`) VALUES
(1, 'Starter Pack', 10, 10.00, 'Perfect for getting started.', 1, '2025-11-13 05:43:51'),
(2, 'Basic Bundle', 25, 22.50, 'A small discount for a few more posts.', 1, '2025-11-13 05:44:04'),
(3, 'Pro Pack', 50, 40.00, 'Best value for active agents.', 1, '2025-11-13 05:44:45'),
(4, 'Power User Bundle', 100, 75.00, 'For top-performing agents.', 1, '2025-11-13 05:45:12'),
(5, 'Old Promo Plan', 5, 5.00, NULL, 0, '2025-11-13 05:45:38'),
(6, 'altamash', 5, 45.00, 'saste ka maal raste me', 1, '2025-11-25 10:00:54'),
(7, 'power farru bundle', 9, 50.01, 'hii', 0, '2025-11-25 10:09:06');

-- --------------------------------------------------------

--
-- Table structure for table `favorites`
--

CREATE TABLE `favorites` (
  `favorite_id` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `property_id` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `favorites`
--

INSERT INTO `favorites` (`favorite_id`, `user_id`, `property_id`, `created_at`) VALUES
(224, 'IE6C0P', '1GVRUQTMDQ', '2025-11-14 07:35:03'),
(225, 'IE6C0P', 'I789DP8RRA', '2025-11-17 12:36:17'),
(231, '2TK4LE', 'WBO6KYV76Z', '2025-11-20 15:39:21'),
(232, '6T9LU7', 'K4NMWCQCB8', '2025-11-21 10:31:00'),
(233, 'B1YFZC', 'PVXPJAJJRY', '2025-11-21 11:26:39'),
(234, 'B1YFZC', 'K4NMWCQCB8', '2025-11-21 11:26:41'),
(235, 'A0TTD6', '5PTLBKIM97', '2025-11-21 11:56:38'),
(236, 'A0TTD6', 'PVXPJAJJRY', '2025-11-21 11:56:40');

-- --------------------------------------------------------

--
-- Table structure for table `invoices`
--

CREATE TABLE `invoices` (
  `invoice_id` int NOT NULL,
  `agent_id` char(8) DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'pending',
  `credits_purchased` int NOT NULL,
  `amount_paid` decimal(10,2) NOT NULL,
  `payment_gateway_ref` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `stripe_session_id` varchar(255) DEFAULT NULL,
  `invoice_number` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `invoices`
--

INSERT INTO `invoices` (`invoice_id`, `agent_id`, `status`, `credits_purchased`, `amount_paid`, `payment_gateway_ref`, `created_at`, `updated_at`, `stripe_session_id`, `invoice_number`) VALUES
(1, 'AGNBYIE8', 'paid', 10, 50.00, 'stripe_txn_12345abcde', '2025-11-13 05:26:52', '2025-11-26 08:42:51', NULL, 'O6KZ1VYWBO'),
(2, 'AGNBYIE8', 'paid', 50, 40.00, 'stripe_txn_xyz_98765', '2025-11-13 05:49:12', '2025-11-26 08:42:51', NULL, '7M96UGDB4F'),
(3, 'AGNQNTVL', 'paid', 10, 10.00, 'pi_3SSykOPPL66xhR3q1GIwk0Gu', '2025-11-13 11:27:47', '2025-11-26 08:42:51', 'cs_test_a1P2XipzNrCcmHIyqNaQUXztGKoJkTnWtlrTjjVIP4RY9AyJLmwdG0U2qr', 'FOSMH8F58G'),
(4, 'AGNQNTVL', 'pending', 25, 22.50, NULL, '2025-11-13 11:43:05', '2025-11-26 08:42:51', 'cs_test_a1lt87FXkOMkqNK5APjIGXvybsi6nPlHmOdkSCyf7RbQCPXmEK9rwWfvPG', '2TOKJS0H0E'),
(5, 'AGNQNTVL', 'paid', 25, 22.50, 'pi_3STG1OPPL66xhR3q01qEYHHl', '2025-11-14 05:55:32', '2025-11-26 08:42:51', 'cs_test_a1KU0J6zAkSeAIerCfBq9SUnv4uH23sYOBe1UqyipKprxCO1F8NXAswCKo', '0SMJGHQW03'),
(10, 'AGNQNTVL', 'pending', 10, 10.00, NULL, '2025-11-14 09:01:06', '2025-11-26 08:42:51', 'cs_test_a1iMtBekeG6c2dImezTooIqIZ8891oxMP9XE83ZczsFFPk5UzjQaOxhxDj', '0I65XXKSZ8'),
(11, 'AGNQNTVL', 'pending', 10, 10.00, NULL, '2025-11-14 09:12:30', '2025-11-26 08:42:51', 'cs_test_a1gA8iSm3Y3Dzyv6UHVLTXKCPutOJcmxYQFCeGRo7zb6jl0hpq0FXxA7oM', '6XWE1P7KZX'),
(12, 'AGNQNTVL', 'pending', 50, 40.00, NULL, '2025-11-14 09:13:00', '2025-11-26 08:42:51', 'cs_test_a15SanZjuX9GbsItL8DvnXdq4coxFQD3qiBsEXrnWqrGZ8SgIyQI5P87wc', 'XEYBGZ95MD'),
(13, 'AGNQNTVL', 'pending', 10, 10.00, NULL, '2025-11-14 09:20:45', '2025-11-26 08:42:51', 'cs_test_a1YOrLmaXgMZdTmNwqVg8dbzNl8tLaRVpWJp8eQkhISpmr11SgOfrYnAur', 'V19YN4EDEJ'),
(14, 'AGNQNTVL', 'pending', 10, 10.00, NULL, '2025-11-14 09:26:13', '2025-11-26 08:42:51', 'cs_test_a1iUpuJmXcJJqksj1d9g3WKfmkj0WEdQFBtzuAIdawjgltNirAhyjF5cWy', 'WQP2W3GR3Y'),
(15, 'AGNQNTVL', 'paid', 10, 10.00, 'pi_3STJJEPPL66xhR3q19lrz3PD', '2025-11-14 09:28:17', '2025-11-26 08:42:51', 'cs_test_a1wXjepM6vO5IRBEiPLFDTbF8PfemSHhP3yNw7Ph2Em2q49hdjDtqJWeZM', '8N93HTBWAF'),
(16, 'AGNQNTVL', 'paid', 10, 10.00, 'pi_3STJP3PPL66xhR3q0mPC940b', '2025-11-14 09:34:22', '2025-11-26 08:42:51', 'cs_test_a15W7EGqBAJqemWXmgHDZGnVbGND5RkAyFVFKi6DE4ZJAPlPnZHFgfrtms', 'IZ22VXPFUK'),
(17, 'AGNQNTVL', 'paid', 10, 10.00, 'pi_3STJacPPL66xhR3q02kSi6ux', '2025-11-14 09:46:21', '2025-11-26 08:42:51', 'cs_test_a1Z8fzK3v1cdxG38hiVkZAMDjjEZQT6UXTs2jNkmECWYB5TML0b3S3IMzD', 'I4R42P1SK5'),
(18, 'AGNQNTVL', 'paid', 25, 22.50, 'pi_3STJbsPPL66xhR3q0DGAzox3', '2025-11-14 09:47:35', '2025-11-26 08:42:51', 'cs_test_a14rGnwsSjQSghnpxTONTNS8YxEzaNSunJoRRJSMLwFKZR11RDLf1CVLW0', '7Z244Z8XPE'),
(19, 'AGNQNTVL', 'pending', 25, 22.50, NULL, '2025-11-14 09:48:42', '2025-11-26 08:42:51', 'cs_test_a1jhB9aPXjWIJEP3drC1XM22XhgPQZBgjxycJb5I9PMiU5WpTTHXMeTxgl', '7S2PZMU1GT'),
(20, 'AGNQNTVL', 'paid', 25, 22.50, 'pi_3STJdjPPL66xhR3q1dqa0wnX', '2025-11-14 09:49:30', '2025-11-26 08:42:51', 'cs_test_a13YD8feYRK6y4S4J9BJaCE2eO1uhx06TLwyeJ1LBA5vzwjQOqOz7hDHxQ', 'EP2Y95ONZN'),
(21, 'AGNQNTVL', 'pending', 25, 22.50, NULL, '2025-11-14 09:50:51', '2025-11-26 08:42:51', 'cs_test_a1IkkonIIGID7lwkevfXrDrayIL3LRcL49pd3bHlj2kDO5uQjaakz18li5', 'B4D7OI66Z6'),
(22, 'AGNBYIE8', 'pending', 10, 10.00, NULL, '2025-11-14 11:05:16', '2025-11-26 08:42:51', 'cs_test_a1JD4N1KVvXqgW08vpkASqRhKAWcBaFmf0BFcAqpS6FBE3bfSoOHEgsGJj', '7M5ONXG550'),
(23, 'AGNQNTVL', 'pending', 10, 10.00, NULL, '2025-11-20 10:06:45', '2025-11-26 08:42:51', 'cs_test_a1rhJcdMKoLayMRRdnQ78wsg781O4s0W7x8dbo2uRb7OmpQYviETcI8udS', 'VPOXBLPI5W'),
(24, 'AGNQNTVL', 'pending', 10, 10.00, NULL, '2025-11-20 10:07:37', '2025-11-26 08:42:51', 'cs_test_a1uI7YSDcevEDHsdVwvuRkvDZ4xSFjyPrZ9n39g4N31e5MUp7xq3WGYuGc', 'NPDFTIR2RB'),
(25, 'AGNQNTVL', 'paid', 10, 10.00, 'pi_3SVUnnPPL66xhR3q11YHuNPR', '2025-11-20 10:08:09', '2025-11-26 08:42:51', 'cs_test_a1GnHCM4RPC9F8vrjN9QLR4kCNTHD0vaAerBszskfHw8QC9tQFzLpZcpKM', 'PI3Q568DTQ'),
(26, 'AGNQNTVL', 'paid', 50, 40.00, 'pi_3SVUodPPL66xhR3q1oLFal4w', '2025-11-20 10:10:04', '2025-11-26 08:42:51', 'cs_test_a1XCTZMVt0A3NB2X2zGHXEdVVvndg1EYfR127Vvr0cxr4mrZlCqXv54S5s', '6GGPW2DFR7'),
(27, 'AGNQNTVL', 'paid', 100, 75.00, 'pi_3SVVlOPPL66xhR3q1wlhRRB2', '2025-11-20 11:10:45', '2025-11-26 08:42:51', 'cs_test_a112CbBrBhgetjCHHCCYWiWUQTCzB87QdJzVw2RfhjiDnsTOD4eF2uEudE', '1NV3NO5GJ2'),
(28, 'AGNQNTVL', 'paid', 25, 22.50, 'pi_3SVWvhPPL66xhR3q1tsjLoUQ', '2025-11-20 12:25:14', '2025-11-26 08:42:51', 'cs_test_a1oOxBBzDA5RLBTHtpmtWLo2h4ezNrgmEbDgow2y6lssMGKKm22luBRm7x', 'JT50ELLXHF'),
(29, 'AGNQNTVL', 'pending', 10, 10.00, NULL, '2025-11-20 12:29:07', '2025-11-26 08:42:51', 'cs_test_a1KlMyJ0cnFs51SHJ5R0MuRcUYyK6DFndPE5BxquweqVjy6LWrwCHKKczf', '2W18RVU8DU'),
(30, 'AGNZV75V', 'pending', 10, 10.00, NULL, '2025-11-20 17:01:42', '2025-11-26 08:42:51', 'cs_test_a1FrlpSBVX9oFhXsVyMhmNogF3D9loH2mBtvLHXlQJDFflySPDKv39nGwM', 'XAEUS3SFGS'),
(31, 'AGN9IIPO', 'paid', 25, 22.50, 'pi_3SVsXwPPL66xhR3q0c6SyHSo', '2025-11-21 11:30:04', '2025-11-26 08:42:51', 'cs_test_a1ikyiYAdXMuYxq2YKY7bcr1eCeONs9v74JpBalBdCZqQsVitSp9J9oA5c', 'U78AG4ZBA6'),
(32, 'AGNTOREG', 'paid', 100, 75.00, 'pi_3SVshgPPL66xhR3q1fdAFDZ7', '2025-11-21 11:40:30', '2025-11-26 08:42:51', 'cs_test_a1W6GA7sPSIrXeIh3c9nBakctqW7d11KCmP0UZnKZ1p9RI0L9jc3PgV1WP', '65XXLYO8VC'),
(33, 'AGNHIVLZ', 'paid', 100, 75.00, 'pi_3SVtHBPPL66xhR3q09QMmw2b', '2025-11-21 12:16:05', '2025-11-26 08:42:51', 'cs_test_a11nN4BNQ3xyIngKXKXZOuCDnJQUpu4rDtjkSBvXyPCKs7McDue5pt7Voa', 'HS9N5ITAOB'),
(34, 'AGNBYIE8', 'pending', 10, 10.00, NULL, '2025-11-25 04:51:24', '2025-11-26 08:42:51', 'cs_test_a1Nq1pSgRKBH7dsKa3A4KI18tD7OF0OZ8qYUuiP60GLjbZICxgWLeiPz9k', 'Z10O36DYDR'),
(35, 'AGNBYIE8', 'pending', 10, 10.00, NULL, '2025-11-25 04:52:47', '2025-11-26 08:42:51', 'cs_test_a1zFcmkSmfIfTO9yOIDtEZldU0QuDVouJSyjeKqm5FVzZtUQrKOvnsprTE', 'H0DI8BMXF2'),
(36, 'AGNBYIE8', 'pending', 10, 10.00, NULL, '2025-11-25 04:53:07', '2025-11-26 08:42:51', 'cs_test_a1lr0JzWptn58W8qwtkJPzoS884KKKijRhnPX3jBkBzS6kCjibumxY95DR', 'LQLKSZA5L8'),
(37, 'AGNBYIE8', 'paid', 10, 10.00, 'pi_3SXEITPPL66xhR3q1uruarJ3', '2025-11-25 04:54:40', '2025-11-26 08:42:51', 'cs_test_a1QkaEbg8vCjro7y8YlFa4ReGtzPBC2SDCKe3sblinaeCs4DOvLS3Jtu4Q', 'B242RC5EB5'),
(38, 'AGNBYIE8', 'paid', 10, 10.00, 'pi_3SXEYsPPL66xhR3q07ARpWNV', '2025-11-25 05:12:37', '2025-11-26 08:42:51', 'cs_test_a1MvaDsM5AWGzxE2T1hCx8J9DaFGHANQJV5j9tqW5Purm34sNNVaGdSvAT', 'F9RRBXF3X3'),
(39, 'AGNBYIE8', 'paid', 100, 75.00, 'pi_3SXEawPPL66xhR3q0ZV3pRJm', '2025-11-25 05:14:57', '2025-11-26 08:42:51', 'cs_test_a1jZCnBPzpgBNwTKqK5rR5elTgZMgW3acVuz08tCv7s3hQPDEhFMhAL0lU', 'E1P47GEC7O'),
(40, 'AGNBYIE8', 'paid', 50, 40.00, 'pi_3SXEfYPPL66xhR3q0MwQ4APb', '2025-11-25 05:19:42', '2025-11-26 08:42:51', 'cs_test_a1JGBs83aPnG9Gmj3I0OthWW5blXS7Zgv70PXgivYjwORzUSnLpXJ9Fsow', '7F9OEP2VWM'),
(41, 'AGNBYIE8', 'paid', 25, 22.50, 'pi_3SXElAPPL66xhR3q023GEH98', '2025-11-25 05:25:31', '2025-11-26 08:42:51', 'cs_test_a1GUZwcq4sp84jD7MxZ9rBt0MCnKgpU44vEvhVUK5oenfdrsrDEqYDDjJV', '17NBDMRMJM'),
(42, 'AGNBYIE8', 'paid', 25, 22.50, 'pi_3SXEmEPPL66xhR3q0LfOswuB', '2025-11-25 05:26:37', '2025-11-26 08:42:51', 'cs_test_a1VGaAqV9PWsGjYlNgwmZMQuxgU5LpDtmeZTF5dX7xCxV8lpt28BB2uoL2', '1CEP0P6K02'),
(43, 'AGNBYIE8', 'paid', 10, 10.00, 'pi_3SXF2OPPL66xhR3q1Yyo5jyq', '2025-11-25 05:43:15', '2025-11-26 08:42:51', 'cs_test_a1QSNLKPG7mY5HsfxnGblKsv7s4SHDVDk3nGXFOD7a4RCWimIKZPZHXqc2', '5WPLJL5QVW'),
(44, 'AGNBYIE8', 'paid', 10, 10.00, 'pi_3SXFdDPPL66xhR3q1jBX7OWa', '2025-11-25 06:21:21', '2025-11-26 08:42:51', 'cs_test_a1Y8QyEOvjcyXZFVpWdJOslKIHt4X4NFfsuOF1geIXd3cQdHsSoIiW0IVu', 'UL3HS8JOI7'),
(45, 'AGNBYIE8', 'paid', 25, 22.50, 'pi_3SXFfCPPL66xhR3q1dGLgvYc', '2025-11-25 06:23:20', '2025-11-26 08:42:51', 'cs_test_a15r6akV4TVBghJ2sbCjnVfAWcK29rwxnONyF64bMFCWphSfZCeYJbIfk0', 'TIRZCJE30G'),
(46, 'AGNBYIE8', 'paid', 25, 22.50, 'pi_3SXFlaPPL66xhR3q0Vn6sJph', '2025-11-25 06:30:00', '2025-11-26 08:42:51', 'cs_test_a1xpU6z6F2rlgtCxZIgZMAamoOuUhzIWFiIcaoiMZJGI3FwCddBp5semwG', 'MKNA8YV8AE'),
(47, 'AGNBYIE8', 'paid', 50, 40.00, 'pi_3SXFnePPL66xhR3q0LaKBaLu', '2025-11-25 06:32:07', '2025-11-26 08:42:51', 'cs_test_a1kV5exFaaEJ7ua19gwAayCTlLsPUGuGcudwlItUhaoKzwL3tEangGsI6d', 'HK18T1HZ91'),
(48, 'AGNBYIE8', 'paid', 25, 22.50, 'pi_3SXJpjPPL66xhR3q025EfrM0', '2025-11-25 10:50:32', '2025-11-26 08:42:51', 'cs_test_a1ftX1r0FgGdBNuts7cvn6HhkiJ8UG1HTis8kCPJoRHCTXPJTtpgtTAkyN', '6XV8DSMG40'),
(49, 'AGNBYIE8', 'pending', 25, 22.50, NULL, '2025-11-25 11:38:05', '2025-11-26 08:42:51', 'cs_test_a1B4bSq8oBS9pQL68mKzrM3xWovOUY4t4aJ6WgF2kjNNGuayVjeuCtGDJu', '7E452OV05H'),
(50, 'AGNZV75V', 'paid', 25, 22.50, 'pi_3SXlafPPL66xhR3q00T15TZ7', '2025-11-26 16:26:31', '2025-11-26 16:29:17', 'cs_test_a1Oo3Qbi0nGSDG5yPCtL3GjDMU3Ig4nbept4QmglCSEPePeoXKI1qNFsf5', 'G4WXM0YID0');

--
-- Triggers `invoices`
--
DELIMITER $$
CREATE TRIGGER `before_invoice_insert` BEFORE INSERT ON `invoices` FOR EACH ROW BEGIN
    -- Set the invoice_number for the new row by calling our function
    SET NEW.invoice_number = generate_unique_invoice_number()$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `member_id` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `gender` enum('male','female','other') DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `occupation` varchar(100) DEFAULT NULL,
  `bio` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`member_id`, `user_id`, `contact`, `gender`, `date_of_birth`, `address`, `profile_picture`, `occupation`, `bio`, `created_at`) VALUES
(43, '6T9LU7', '38468440660', 'male', '1995-12-20', 'rshjieyfuky', '', 'frbaergb', 'hhhh', '2025-11-20 09:16:11'),
(44, '6K020N', '8194067267', 'male', '2025-11-23', 'near forest colony', '', 'student', 'hey buddy\n', '2025-11-20 11:34:49'),
(45, 'B1YFZC', '+6504640480', 'male', '2022-12-19', 'VsdeGVBQERHB', '', 'VWRGSDBV', 'ERBGAGBASB', '2025-11-21 11:25:49'),
(46, 'A0TTD6', '9876546789', 'male', '2023-11-01', 'dwqfFF', '', 'dFEFEG', 'gargrre', '2025-11-21 11:53:06'),
(47, '2TK4LE', '9988776655', 'male', '1989-01-15', 'afdsf afa dasfas', '', 'fasdfasfdasf', 'fadsf asfdasfdas asfdasf', '2025-11-21 15:57:41');

-- --------------------------------------------------------

--
-- Table structure for table `properties`
--

CREATE TABLE `properties` (
  `property_id_1` int NOT NULL,
  `property_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `agent_id` char(8) DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `description` text,
  `price` decimal(15,2) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `zip_code` varchar(20) DEFAULT NULL,
  `property_type` varchar(100) DEFAULT NULL,
  `features` text,
  `bedrooms` int DEFAULT NULL,
  `bathrooms` int DEFAULT NULL,
  `rooms` int DEFAULT NULL,
  `status` enum('available','sold','rented','rent','sale','all') DEFAULT 'available',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `area_sqft` decimal(10,2) DEFAULT NULL,
  `latitude` varchar(200) DEFAULT NULL,
  `logitude` varchar(200) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `is_featured` tinyint(1) NOT NULL DEFAULT '0',
  `average_rating` decimal(3,2) NOT NULL DEFAULT '0.00',
  `review_count` int NOT NULL DEFAULT '0',
  `neighborhood` varchar(255) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `price_unit` varchar(50) DEFAULT NULL,
  `before_label` varchar(100) DEFAULT NULL,
  `after_label` varchar(100) DEFAULT NULL,
  `land_area` varchar(100) DEFAULT NULL,
  `garages` int DEFAULT NULL,
  `garage_size` varchar(100) DEFAULT NULL,
  `year_built` int DEFAULT NULL,
  `private_note` text,
  `video_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `properties`
--

INSERT INTO `properties` (`property_id_1`, `property_id`, `agent_id`, `title`, `description`, `price`, `address`, `city`, `state`, `country`, `zip_code`, `property_type`, `features`, `bedrooms`, `bathrooms`, `rooms`, `status`, `created_at`, `updated_at`, `area_sqft`, `latitude`, `logitude`, `is_deleted`, `is_featured`, `average_rating`, `review_count`, `neighborhood`, `label`, `price_unit`, `before_label`, `after_label`, `land_area`, `garages`, `garage_size`, `year_built`, `private_note`, `video_url`) VALUES
(18, 'R7JS3SC345', 'AGNQNTVL', 'Puteri Bayu, Bandar Puteri Puchong – Apartment For Rent', 'Puteri Bayu Condo, Bandar Puteri Puchong (900sf, 2 Car Park)\n\n-900sf\n-3 Room 2 Bathroom\n-2 Car Park\n-Low Floor\n-Kitchen Cabinet, Build in Wardrobe, 2 unit Air Cond, Water Heater, Fridge\n-24 Hour Security, Swimming Pool\n\n************************\nAsking RM 1,300\n************************\n\nREN 19081\nVivahomes Realty Sdn Bhd (1102810-V)\nNo.25-3, JAlan PJU 5/20E, The Strand, Kota Damansara, 47810 Petaling Jaya, Selangor\n\nFacilities & Security Systems\nFacilities\nSwimming Pool\nGymnasium\nCovered Parking\nMulti Purpose Hall\nConvenient Stores\nCafe & Restaurants\nJogging Track\nPlayground\nNursery Centre\nSecurity Systems\n24 Hours Sec', 1300.00, 'Puteri Bayu, Bandar Puteri Puchong', 'Selangor', 'Shah Alam', 'Malaysia', '202001', 'Apartment', 'Parking, Play Ground, Gym, Swimming Pool, Fire Safety', 3, 2, 3, 'rent', '2025-10-28 09:11:42', '2025-11-26 09:13:35', 900.00, '-2', '', 1, 0, 5.00, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(19, '1GVRUQTMDQ', 'AGNQNTVL', 'Jivan villa', '', 1481.00, 'malacca city', 'Malacca City', 'Malacca', 'Malaysia', '7500', 'Villa', 'Gym, Swimming Pool, Air Conditioning, Club House, Play Ground, Parking, Spa Wellness, Fire Safety, Playgrounds, Gardens/Lawns/Parks', 3, 2, 3, 'rent', '2025-10-28 12:30:55', '2025-11-26 09:13:35', 550.00, NULL, '', 1, 0, 5.00, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(20, 'AYN4C21Q9U', 'AGNBYIE8', '7 bedroom bungalow', '7 bedrooms\n9 bathrooms\n0.28 acres\n-First floor Living Hall\n-Dining room with 10 seater dining table\n-Grand curtains- 2 Tier High -Ceilings\n-Lovely 3 chandeliers\n-2 Kitchens – Dry and wet\n-Pipe-in sound system for whole house with pa system\n-CCTV 16 camera\n-Alarm system\n-Automatic gate from CSA Design\n-Air-conditioners with pipings\n-1 master bedroom with jacuzzi and walk- in wardrobe and large\nbalcony\n-2 large bedrooms with jacuzzi and long bath and walk- in\nwardrobes and personal balconies\n-Private theatre room with electric cinema chairs\n-1 Prayer room\n-Huge library cum office with 8 seater conference table with\nbalcony overlooking KLCC\n-Open Gym and boxing space\n-Open sky garden overlooking KLCC , KL tower and Lake Titiwangsa', 2000.00, 'Jalan Ikan, Seksyen 20', 'Shah Alam', 'Selangor', 'Malaysia', '40160', 'Bunglow', 'Gym, Parking, Swimming Pool, Fire Safety, Garage, Laundry Room, Air Conditioning', 7, 9, 7, 'rent', '2025-10-29 10:10:36', '2025-11-26 09:13:35', 1200.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(22, '4UK04AUZ7Q', 'AGNQNTVL', 'Semi-Detached House', 'Taman Indah Puteri Salak Tinggi Sepang 1 Storey Semi Detached 49×56\n\n===============================\n\nDETAILS :\n– Leasehold,\n– Malay Reserved\n– Land Area : 2,777 sqft\n– 4 Bedrooms,\n– 2 Bathrooms\n– Built-up area: ~ 1,100 sq ft.(approx)\n– Basic unit\n– Currently tenanted\n\nAMENITIES :\n– Aeon Bandar Baru Nilai\n– Mesa Mall, Bandar Baru Nilai With Cinema\n– KIP Mall Kota Warisan\n– Mitsui Outlet Park Sepang\n– KIP Mall Kota Warisan\n– Sek Kebangsaan/menengah\n-SAM Bandar Baru Salak Tinggi\n– ERL Salak Tinggi – 7 KM\n– KLIA & KLIA2 – 10 KM\n– Masjid As-Syakirin\n\nACCESS :\n– Lebuhraya Sepang Nilai\n– Putrajaya-Cyberjaya Expressway (Dengkil bypass)\n– ELITE Highway exit KLIA & SERENIA CITY\n– MEX exit Putrajaya\n– LDP', 40000.00, 'Sepang, Selangor', 'Shah Alam', 'Selangor', 'Malaysia', '43900', 'House', 'Security System, Parking, Play Ground, Laundry Room, Fire Safety', 4, 1, 4, 'sale', '2025-11-04 12:14:52', '2025-11-26 09:13:35', 2777.00, NULL, '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(23, 'SGPUS4ZA95', 'AGNQNTVL', '3 bedroom house', 'ugxuaghduiasghdusighsui', 120000.00, 'near forest colony', 'aligarh', 'up', 'india', '202001', 'Apartment', 'Security System, Gardens/Lawns/Parks, Concierge Services, Air Conditioning', 5, 3, 6, 'sale', '2025-11-13 05:34:02', '2025-11-26 09:13:35', 600.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(27, 'NKJT5Z6NG1', 'AGNBYIE8', 'wsfG', 'gweg', 0.00, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'rent', '2025-11-17 10:59:07', '2025-11-26 09:13:35', NULL, NULL, NULL, 0, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(28, 'I789DP8RRA', 'AGNQNTVL', 'Puteri Bayu, Bandar Puteri Puchong – Apartment For Rent', 'Puteri Bayu Condo, Bandar Puteri Puchong (900sf, 2 Car Park)\r\n\r\n-900sf\r\n-3 Room 2 Bathroom\r\n-2 Car Park\r\n-Low Floor\r\n-Kitchen Cabinet, Build in Wardrobe, 2 unit Air Cond, Water Heater, Fridge\r\n-24 Hour Security, Swimming Pool\r\n\r\n************************\r\nAsking RM 1,300\r\n************************\r\n\r\nREN 19081\r\nVivahomes Realty Sdn Bhd (1102810-V)\r\nNo.25-3, JAlan PJU 5/20E, The Strand, Kota Damansara, 47810 Petaling Jaya, Selangor\r\n\r\nFacilities & Security Systems\r\nFacilities\r\nSwimming Pool\r\nGymnasium\r\nCovered Parking\r\nMulti Purpose Hall\r\nConvenient Stores\r\nCafe & Restaurants\r\nJogging Track\r\nPlayground\r\nNursery Centre\r\nSecurity Systems\r\n24 Hours Sec', 1300.00, 'Puteri Bayu, Bandar Puteri Puchong', 'Shah Alam', 'Selangor', 'Malaysia', '', 'Apartment', '', 3, 2, 3, 'rent', '2025-11-17 10:59:57', '2025-11-26 09:13:35', 400.00, '', '', 1, 0, 4.00, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(29, 'WBO6KYV76Z', 'AGNQNTVL', 'Semi-Detached House', 'Taman Indah Puteri Salak Tinggi Sepang 1 Storey Semi Detached 49×56\r\n\r\n===============================\r\n\r\nDETAILS :\r\n– Leasehold,\r\n– Malay Reserved\r\n– Land Area : 2,777 sqft\r\n– 4 Bedrooms,\r\n– 2 Bathrooms\r\n– Built-up area: ~ 1,100 sq ft.(approx)\r\n– Basic unit\r\n– Currently tenanted\r\n\r\nAMENITIES :\r\n– Aeon Bandar Baru Nilai\r\n– Mesa Mall, Bandar Baru Nilai With Cinema\r\n– KIP Mall Kota Warisan\r\n– Mitsui Outlet Park Sepang\r\n– KIP Mall Kota Warisan\r\n– Sek Kebangsaan/menengah\r\n-SAM Bandar Baru Salak Tinggi\r\n– ERL Salak Tinggi – 7 KM\r\n– KLIA & KLIA2 – 10 KM\r\n– Masjid As-Syakirin\r\n\r\nACCESS :\r\n– Lebuhraya Sepang Nilai\r\n– Putrajaya-Cyberjaya Expressway (Dengkil bypass)\r\n– ELITE Highway exit KLIA & SERENIA CITY\r\n– MEX exit Putrajaya\r\n– LDP', 400000.00, 'Sepang, Selangor', 'Shah Alam', 'Selangor', 'Malaysia', '43900', 'Semi-detached House', 'Security System, Solar Panels, Microwave, Club House, Parking, Play Ground', 4, 2, 4, 'sale', '2025-11-17 11:06:58', '2025-12-01 06:10:12', 1200.00, '', '', 0, 0, 5.00, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(30, '4D6KZ0RK6Z', 'AGNQNTVL', 'awesome home', 'hey', 500000.00, 'near forest colony', 'Taiping', 'Perak', 'Malaysia', '202001', 'Bungalow', 'Security System, Gardens/Lawns/Parks, Air Conditioning, Play Ground', 4, 2, 4, '', '2025-11-17 12:15:54', '2025-11-26 09:13:35', 0.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(31, '11SLCMTZ6P', 'AGNQNTVL', 'awesome ', 'mast hai bhi', 1400.00, 'near forest colony', 'Victoria', 'Labuan', 'Malaysia', '202201', 'Villa', 'Security System, Gardens/Lawns/Parks, Concierge Services, Air Conditioning', 2, 1, 2, 'rent', '2025-11-17 13:00:40', '2025-11-26 09:13:35', 600.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(32, 'NTXV9G8HIT', 'AGNQNTVL', 'fablouse ', 'mast hai bahi', 1500.00, 'near forest colony', 'George Town', 'Penang', 'Malaysia', '202001', 'Apartment', 'Parking, Microwave, Gardens/Lawns/Parks, Security System', 2, 1, 2, 'rent', '2025-11-17 13:10:46', '2025-11-26 09:13:35', 500.00, '-1', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(33, 'BSS9QI5YZR', 'AGNQNTVL', 'fablous', 'nice property', 1000.00, 'near fprest colonyt', 'Bukit Mertajam', 'Penang', 'Malaysia', '202001', 'Apartment', 'Security System, Gardens/Lawns/Parks, Parking', 2, 1, 2, 'rent', '2025-11-18 04:09:15', '2025-11-26 09:13:35', 600.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(34, 'K9DUR1KIL4', 'AGNQNTVL', 'good', 'nice awesome', 1200.00, 'near forest colony', 'George Town', 'Penang', 'Malaysia', '202001', 'Apartment', 'Parking, Air Conditioning, Concierge Services', 1, 1, 1, 'rent', '2025-11-18 04:49:49', '2025-11-26 09:13:35', 600.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(35, 'IYYN38OCFT', 'AGNQNTVL', 'al falha ', 'its is awesome property', 1000.00, 'hamdard nagar d', 'Alor Gajah', 'Melaka', 'Malaysia', '202001', 'Apartment', 'Security System, Parking, Solar Panels, Gym', 1, 1, 1, '', '2025-11-18 04:55:07', '2025-11-26 09:13:35', 400.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(36, 'K4NMWCQCB8', 'AGNQNTVL', 'al fida ', 'bahut acchi hai', 1200.00, 'fm tower', 'Lumut', 'Perak', 'Malaysia', '202001', 'Apartment', 'Security System, Gardens/Lawns/Parks, Parking', 1, 1, 1, 'rent', '2025-11-18 05:14:59', '2025-11-26 09:13:35', 400.00, '', '', 0, 0, 5.00, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(37, 'XPENSQ1O0P', 'AGNQNTVL', 'faheem ka ghar', 'this is awe', 40000.00, 'near ', 'Sipitang', 'Sabah', 'Malaysia', '202001', 'Apartment', 'Swimming Pool, Playgrounds', 2, 3, 2, 'sale', '2025-11-20 12:17:39', '2025-11-26 09:13:35', 600.00, '', '', 1, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(38, '9V9IHL9985', 'AGNQNTVL', 'faheem ', 'nice', 900.00, 'near', 'Kuala Lumpur', 'Kuala Lumpur', 'Malaysia', '202001', 'Apartment', 'Security System, Parking', 2, 1, 2, 'rent', '2025-11-20 12:23:54', '2025-11-26 09:13:35', 300.00, '', '', 0, 0, 3.50, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(39, 'PVXPJAJJRY', 'AGNQNTVL', '3BHK Flat RM1500 for Rent', 'fasdfa sfdasdfasfasfasd', 1500.00, 'hell no', 'Bayan Lepas', 'Penang', 'Malaysia', '200124', 'Apartment', 'Security System, Market, Play Ground, Parking, Fire Safety, Swimming Pool, Gym', 3, 2, 3, 'rent', '2025-11-20 16:59:45', '2025-11-26 09:13:35', 1000.00, '', '', 0, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(40, '5PTLBKIM97', 'AGN9IIPO', 'Ghost House', 'ARGHAREHGERA', 200.00, 'AREHREHAE', 'Alor Setar', 'Kedah', 'Malaysia', '831004', 'Villa', 'Security System, Solar Panels, Gym, Sports Facilities, Swimming Pool, Gardens/Lawns/Parks, Concierge Services, Playgrounds, Central Heating, Dishwasher, Laundry Room, Air Conditioning, Microwave, Garage, Toolshed, Market, Yoga Wellness, Spa Wellness, Fire Safety, Club House, Play Ground, Parking', 7, 14, 7, 'rent', '2025-11-21 11:33:42', '2025-11-26 09:13:35', 1000.00, NULL, '', 0, 1, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(41, 'Z0SNMWDUVH', 'AGNHIVLZ', 'ytcavdad', 'utejcavuicavc', 390.00, 'wegageea', 'Kampar', 'Perak', 'Malaysia', '678009', 'Apartment', '', 6, 4, 6, 'rent', '2025-11-21 12:21:50', '2025-11-26 09:13:35', 10000.00, '', '', 0, 1, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(42, 'K3GR7D2W2A', 'AGNBYIE8', '6 bedroom bungalow', '6 Bedrooms | 4 Bathrooms\r\nA hidden gem nestled in the heart of Perlis, offering a perfect blend of tranquility and accessibility. Surrounded by key landmarks and essential amenities, this home provides a peaceful retreat while staying well-connected to the vibrant pulse of the town.\r\n\r\nLocated in the serene and green neighborhood of Taman U-thant, this charming property offers a quiet escape with nature at your doorstep. Built in 1975, it sits on a generous 19,465 square feet of land with a built-up area of 4,670 square feet—thoughtfully designed for spacious and comfortable family living.\r\n\r\nThe house is beautifully maintained, exuding a vintage charm, and is surrounded by a large garden that enhances its peaceful ambiance.', 4121112.00, 'kangar', 'Kangar', 'Perlis', 'Malaysia', '202001', 'Bungalow', 'other, Parking, Play Ground, Gym, Security System, Swimming Pool', 6, 4, 6, 'sale', '2025-11-24 05:28:37', '2025-11-26 09:13:35', 4670.00, '', '', 0, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(43, 'YPDI4TFFLE', 'AGNZV75V', '4BHK Flat RM1800 for Rent', 'fads asdfasf asfasf asdfasf asdfasf asdfasfa', 1800.00, '123 Main Street', 'Kajang', 'Selangor', 'Malaysia', '43000', 'Apartment', 'Security System, Garage, Club House, Play Ground, Market, other', 3, 3, 4, 'rent', '2025-11-25 17:09:39', '2025-11-26 09:13:35', 1100.00, '2.9221098', '101.7329167', 0, 0, 3.00, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(44, 'W3HTC0SK99', 'AGNTXYM2', '2BHK Flat RM1050 for Rent', 'asdfas afsdfas asfasfa asfasfdas asdfasf asdfasfa asdfasfa dsfdasdf sdfasf asfasfa', 1050.00, '125 Main Street', 'Ranau', 'Sabah', 'Malaysia', '89300', 'Studio', 'Swimming Pool, Parking, Club House, Security System, Gym, other', 1, 1, 2, 'rent', '2025-11-25 17:25:02', '2025-11-26 09:13:35', 900.00, '5.8413342', '115', 0, 0, 0.00, 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(45, '9BG4Z7VGEB', 'AGNBYIE8', 'real top home', 'this is best deal  ever', 300000.00, 'shah alam', 'Shah Alam', 'Selangor', 'Malaysia', '202001', 'Apartment', 'Security System, Parking', 2, 1, 2, 'sale', '2025-11-26 04:28:15', '2025-11-26 09:13:35', 600.00, '3.5092', '101.5248', 0, 0, 0.00, 0, 'heigh school', 'New', 'Total', '300000', '290000', '1100', 1, '100', 2025, '', ''),
(46, 'MLT0CEP1UR', 'AGNBYIE8', 'awesom', 'ehh', 130000.00, 'near', 'Sandakan', 'Sabah', 'Malaysia', '200121', 'Apartment', 'Security System, Laundry Room', 2, 7, 2, 'sale', '2025-11-26 11:39:21', '2025-11-26 12:04:57', 600.00, '', '', 0, 0, 0.00, 0, 'hyhjhi', 'Hot Offer', 'Monthly', '', '', '1000', 7, '100', 2010, 'hiii', ''),
(52, 'V5S8JPMRMJ', 'AGNBYIE8', 'fablous', 'hh', 1500.00, 'ehae', 'Kuala Selangor', 'Selangor', 'Malaysia', '449431', 'Apartment', 'Concierge Services, Fire Safety', 4, 4, 2, 'rent', '2025-11-26 12:04:24', '2025-11-26 13:43:39', 150.00, NULL, '', 0, 0, 0.00, 0, 'gwaegag', 'Hot Offer', 'Monthly', '', '', '20', 6, '150000', 1951, 'ewhqa', '');

--
-- Triggers `properties`
--
DELIMITER $$
CREATE TRIGGER `before_property_insert` BEFORE INSERT ON `properties` FOR EACH ROW BEGIN
    SET NEW.property_id = generate_unique_property_id()$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `property_images`
--

CREATE TABLE `property_images` (
  `image_id` int NOT NULL,
  `property_id` varchar(10) DEFAULT NULL,
  `image_url` varchar(255) NOT NULL,
  `is_cover` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `property_images`
--

INSERT INTO `property_images` (`image_id`, `property_id`, `image_url`, `is_cover`, `created_at`) VALUES
(37, 'R7JS3SC345', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/0RHyuxoMGUh7xbgS4g1f.jpg', 0, '2025-10-28 09:11:42'),
(38, 'R7JS3SC345', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/dDQ3qpFUPOgR64YTGXUV.jpg', 0, '2025-10-28 09:11:42'),
(39, 'R7JS3SC345', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/jktNETMgbiTXMcAzfboG.jpg', 0, '2025-10-28 09:11:42'),
(40, 'R7JS3SC345', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/nBXLWWpgd99hRqgl3mDO.jpg', 0, '2025-10-28 09:11:42'),
(41, 'R7JS3SC345', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/raCbrBSQ0SOdaRAwiIey.jpg', 0, '2025-10-28 09:11:42'),
(47, 'AYN4C21Q9U', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/image-0-1024x1024-1-1-1.webp', 0, '2025-10-29 10:10:36'),
(48, 'AYN4C21Q9U', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/image-1-1024x1024-1-1-1.webp', 0, '2025-10-29 10:10:36'),
(49, 'AYN4C21Q9U', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/image-2-1024x1024-1-1-1.webp', 0, '2025-10-29 10:10:36'),
(50, 'AYN4C21Q9U', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/image-3-1024x1024-1-1-1.webp', 0, '2025-10-29 10:10:36'),
(51, 'AYN4C21Q9U', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/image-4-1024x1024-1-1-1.webp', 0, '2025-10-29 10:10:36'),
(121, '4UK04AUZ7Q', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/66fa31c11952f39120f2860b1e35f7b7-2894978779883353211.jpg', 0, '2025-11-07 11:18:45'),
(122, '4UK04AUZ7Q', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/407ff0a72fbb19f52b327b3166354bfd-2894978757445498962.jpg', 0, '2025-11-07 11:18:45'),
(123, '4UK04AUZ7Q', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/412102bc106469b4abb98dfff1c59c4a-2894978747564746839.jpg', 0, '2025-11-07 11:18:45'),
(124, '4UK04AUZ7Q', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/a08c44223d926972957653686ccdcb3b-2894978753603319890.jpg', 0, '2025-11-07 11:18:45'),
(125, '4UK04AUZ7Q', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/a9e55c3327500792fc4fc83ebe445df2-2894978754395825668.jpg', 0, '2025-11-07 11:18:45'),
(126, '4UK04AUZ7Q', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/bb3f9d73951cf25cdd7f1f42f1ded72b-2894978750583289938.jpg', 0, '2025-11-07 11:18:45'),
(127, '1GVRUQTMDQ', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/imagereader-14.webp', 0, '2025-11-10 06:19:50'),
(128, '1GVRUQTMDQ', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/imagereader-8.webp', 0, '2025-11-10 06:19:50'),
(129, '1GVRUQTMDQ', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/imagereader-3.webp', 0, '2025-11-10 06:19:50'),
(130, '1GVRUQTMDQ', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/imagereader-2.webp', 0, '2025-11-10 06:19:50'),
(131, '1GVRUQTMDQ', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/04/3-4.jpg', 0, '2025-11-10 06:19:50'),
(132, 'SGPUS4ZA95', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/apt.jpg', 0, '2025-11-13 05:34:02'),
(133, 'SGPUS4ZA95', 'https://demo.myhomemarkets.com/wp-content/uploads/2025/05/b8a046853745ff2fd665ef86aa9321eb-2930112960682472567.jpg', 0, '2025-11-13 05:34:02'),
(134, 'NKJT5Z6NG1', '4b077628402d4992a9563b66f97c6c58_image_2.png', 0, '2025-11-17 10:59:07'),
(135, 'NKJT5Z6NG1', '3e69e4b5ea7342b291c977e9e6ed731f_image_1.png', 0, '2025-11-17 10:59:07'),
(136, 'I789DP8RRA', '459f134a0df347b787f46633f4d051c4_raCbrBSQ0SOdaRAwiIey-870x420.jpg', 0, '2025-11-17 10:59:57'),
(137, 'I789DP8RRA', '64d0ad7914f14a56bf09cdb0269d2439_nBXLWWpgd99hRqgl3mDO-870x420.jpg', 0, '2025-11-17 10:59:57'),
(138, 'I789DP8RRA', '74d28d4a852b46f18177624032fcb345_jktNETMgbiTXMcAzfboG-870x420.jpg', 0, '2025-11-17 10:59:57'),
(139, 'I789DP8RRA', 'c723611a63f0406f90856d740bbd738a_dDQ3qpFUPOgR64YTGXUV-870x420.jpg', 0, '2025-11-17 10:59:57'),
(140, 'I789DP8RRA', '5fa281efe15947bea7f4a474c4a1e69b_0RHyuxoMGUh7xbgS4g1f-870x420.jpg', 0, '2025-11-17 10:59:57'),
(141, 'WBO6KYV76Z', 'a12cafa6b1334bba9d3520b589da8b36_a08c44223d926972957653686ccdcb3b-2894978753603319890-870x420.jpg', 0, '2025-11-17 11:06:58'),
(142, 'WBO6KYV76Z', '7d8271c72f684094b78109f0cfa2a445_412102bc106469b4abb98dfff1c59c4a-2894978747564746839-250x130.jpg', 0, '2025-11-17 11:06:58'),
(143, 'WBO6KYV76Z', 'ed6147bbaa384304be64edc0720e5a3e_464cedd613e995057441f8612e8a4880-2894978776018532434-870x420.jpg', 0, '2025-11-17 11:06:58'),
(144, 'WBO6KYV76Z', 'd43797a38ec44483b5c305e802641cec_407ff0a72fbb19f52b327b3166354bfd-2894978757445498962-870x420.jpg', 0, '2025-11-17 11:06:58'),
(145, 'WBO6KYV76Z', 'c814d20b9cbe4826bef7d4a90fdb4f1e_66fa31c11952f39120f2860b1e35f7b7-2894978779883353211-870x420.jpg', 0, '2025-11-17 11:06:58'),
(146, '4D6KZ0RK6Z', '4652bea99453415fb88e3fa8e969f971_a08c44223d926972957653686ccdcb3b-2894978753603319890-870x420.jpg', 0, '2025-11-17 12:15:54'),
(147, '4D6KZ0RK6Z', '9fd4244cbd174a2aaa4d5d7ba5058d81_412102bc106469b4abb98dfff1c59c4a-2894978747564746839-250x130.jpg', 0, '2025-11-17 12:15:54'),
(148, '4D6KZ0RK6Z', 'cce3b8c33ad14b6d9272b2d1cc6fce9c_464cedd613e995057441f8612e8a4880-2894978776018532434-870x420.jpg', 0, '2025-11-17 12:15:54'),
(149, '4D6KZ0RK6Z', '0c2f557bfd204a889432462796edb6ed_407ff0a72fbb19f52b327b3166354bfd-2894978757445498962-870x420.jpg', 0, '2025-11-17 12:15:54'),
(150, '4D6KZ0RK6Z', '41d6bf3778a84310bbbfe25b8bb4683d_66fa31c11952f39120f2860b1e35f7b7-2894978779883353211-870x420.jpg', 0, '2025-11-17 12:15:54'),
(151, 'IYYN38OCFT', 'd03bd477eb864d3b9b7da663328f2b8c_a08c44223d926972957653686ccdcb3b-2894978753603319890-870x420.jpg', 0, '2025-11-18 04:55:07'),
(152, 'IYYN38OCFT', '8d9d91b487de46d5a5ae8813ba684640_412102bc106469b4abb98dfff1c59c4a-2894978747564746839-250x130.jpg', 0, '2025-11-18 04:55:07'),
(153, 'IYYN38OCFT', '66bd915674f1473490d95b2a977bb0f0_464cedd613e995057441f8612e8a4880-2894978776018532434-870x420.jpg', 0, '2025-11-18 04:55:07'),
(154, 'IYYN38OCFT', 'a841ae369ef94c74bf6b0717ae9ff36f_407ff0a72fbb19f52b327b3166354bfd-2894978757445498962-870x420.jpg', 0, '2025-11-18 04:55:07'),
(155, 'K4NMWCQCB8', '8702bcc4dae84ec081992fe0e9288552_a08c44223d926972957653686ccdcb3b-2894978753603319890-870x420.jpg', 0, '2025-11-18 05:14:59'),
(156, 'K4NMWCQCB8', '57738b6728eb42929d5c2bcde2a08259_412102bc106469b4abb98dfff1c59c4a-2894978747564746839-250x130.jpg', 0, '2025-11-18 05:14:59'),
(157, 'K4NMWCQCB8', '8bc9dfed92594f339b8c3eeb4b8a3d7a_464cedd613e995057441f8612e8a4880-2894978776018532434-870x420.jpg', 0, '2025-11-18 05:14:59'),
(158, 'K4NMWCQCB8', '5abf4e5408164f1b8d6c9e88efe7aee5_407ff0a72fbb19f52b327b3166354bfd-2894978757445498962-870x420.jpg', 0, '2025-11-18 05:14:59'),
(159, 'XPENSQ1O0P', '67e1015b77b442c68f7c69a0b45a388a_1b66c908422d2b3c70cd7c40254c17c3-2914060520711618781.jpg', 0, '2025-11-20 12:17:39'),
(160, '9V9IHL9985', '3dda833434c04f26ae5e81b5808fc358_2c2eef27a4ad23516f12bc0ba5988b9e-2925969714941827924.jpg', 0, '2025-11-20 12:23:54'),
(161, 'PVXPJAJJRY', '10f8b7e2d04444608064b3c6623056f4_banner2.jpg', 0, '2025-11-20 16:59:45'),
(163, '5PTLBKIM97', '3f732cf0598a4d1db00d76a4da81e944_ChatGPT_Image_Apr_7_2025_05_28_18_PM.png', 0, '2025-11-21 11:34:10'),
(164, 'Z0SNMWDUVH', '2e40c05a56ba47f796f755f5de4e3c0a_Top10_Podcasts.jpeg', 0, '2025-11-21 12:21:50'),
(165, 'K3GR7D2W2A', 'e841960d65364be99a4bdd2e949f0e65_image-4-1024x1024-1-2-870x420.webp', 0, '2025-11-24 05:28:37'),
(166, 'K3GR7D2W2A', '0f1cfd55321e4813b23d83080aec0a49_image-3-1024x1024-1-2-870x420.webp', 0, '2025-11-24 05:28:37'),
(167, 'K3GR7D2W2A', '65da58ea063d429aa2069d32ee40f2c1_image-2-1024x1024-1-2-870x420.webp', 0, '2025-11-24 05:28:37'),
(168, 'K3GR7D2W2A', 'accddebd7a5e4ad1bf5029f50601820c_image-1-1024x1024-1-2-870x420.webp', 0, '2025-11-24 05:28:37'),
(169, 'K3GR7D2W2A', '582b7f297d934c508f1db194b12f5aab_image-0-1024x1024-1-2-870x420.webp', 0, '2025-11-24 05:28:37'),
(170, 'YPDI4TFFLE', 'f493e1fae29047e0a71341957a5f7f99_images.jpeg', 0, '2025-11-25 17:09:39'),
(171, 'W3HTC0SK99', '3b476ef3a08f48bcb2466ad7a05cd5cc_Olive_Green_and_White_Minimalist_Startup_Company_Presentation.gif', 0, '2025-11-25 17:25:02'),
(172, '9BG4Z7VGEB', '83f9a6476502446290f2ac095330b35c_412102bc106469b4abb98dfff1c59c4a-2894978747564746839-250x130.jpg', 0, '2025-11-26 04:28:16'),
(173, '9BG4Z7VGEB', '4c9aac3144fa41189063a342316d7a9b_464cedd613e995057441f8612e8a4880-2894978776018532434-870x420.jpg', 0, '2025-11-26 04:28:16'),
(174, '9BG4Z7VGEB', '7a7bebbab3314ac4b590ef1187e76aa1_407ff0a72fbb19f52b327b3166354bfd-2894978757445498962-870x420.jpg', 0, '2025-11-26 04:28:16'),
(175, 'MLT0CEP1UR', '904f222c9ae14e27b3f1ca642fd56c90_9c531d26e3d991f75f045966c6e80d54-2914060520164991287_1.jpg', 0, '2025-11-26 11:39:21'),
(177, 'V5S8JPMRMJ', 'f8ba47c03faa4c9392baa784e0232059_1b66c908422d2b3c70cd7c40254c17c3-2914060520711618781.jpg', 0, '2025-11-26 13:43:39');

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `rating_id` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `agent_id` char(8) DEFAULT NULL,
  `property_id` varchar(10) DEFAULT NULL,
  `rating_value` tinyint NOT NULL,
  `comment` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `review_id` int NOT NULL,
  `reviewer_user_id` varchar(6) NOT NULL,
  `review_target_type` enum('user','agent','property') NOT NULL,
  `review_target_id` varchar(50) NOT NULL,
  `rating` tinyint NOT NULL,
  `comment` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`review_id`, `reviewer_user_id`, `review_target_type`, `review_target_id`, `rating`, `comment`, `created_at`) VALUES
(21, '6K020N', 'agent', 'AGNQNTVL', 5, 'nice', '2025-12-01 07:13:52');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `role_id` int NOT NULL,
  `role_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`) VALUES
(4, 'ADMIN'),
(2, 'agent'),
(3, 'SUPPORT'),
(1, 'user');

-- --------------------------------------------------------

--
-- Table structure for table `saved_searches`
--

CREATE TABLE `saved_searches` (
  `search_id` int NOT NULL,
  `user_id` varchar(6) NOT NULL,
  `search_name` varchar(255) NOT NULL,
  `search_params` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ;

--
-- Dumping data for table `saved_searches`
--

INSERT INTO `saved_searches` (`search_id`, `user_id`, `search_name`, `search_params`, `created_at`) VALUES
(10, 'IE6C0P', 'Rent 3BHK', '{\"listing_type\": \"RENT\", \"city\": \"\", \"property_type\": \"\", \"max_price\": \"\", \"min_price\": \"\", \"bedrooms\": \"3\", \"state\": \"\", \"keyword\": \"\"}', '2025-11-14 06:50:40'),
(11, 'IE6C0P', 'Rent apartment 1BHK', '{\"listing_type\": \"RENT\", \"city\": \"\", \"property_type\": \"apartment\", \"max_price\": \"\", \"min_price\": \"\", \"bedrooms\": \"1\", \"state\": \"\", \"keyword\": \"\"}', '2025-11-18 11:34:18'),
(14, '6T9LU7', 'Rent apartment 2BHK', '{\"listing_type\": \"RENT\", \"city\": \"\", \"property_type\": \"apartment\", \"max_price\": \"\", \"min_price\": \"\", \"bedrooms\": \"2\", \"state\": \"\", \"keyword\": \"\"}', '2025-11-21 04:14:49'),
(17, '6K020N', 'Rent 2BHK', '{\"listing_type\": \"RENT\", \"city\": \"\", \"property_type\": \"\", \"max_price\": \"\", \"min_price\": \"\", \"bedrooms\": \"2\", \"state\": \"\", \"keyword\": \"\"}', '2025-11-21 04:34:49'),
(18, '6K020N', 'Rent 1BHK', '{\"listing_type\": \"RENT\", \"city\": \"\", \"property_type\": \"\", \"max_price\": \"\", \"min_price\": \"\", \"bedrooms\": \"1\", \"state\": \"\", \"keyword\": \"\"}', '2025-11-21 05:17:59'),
(20, 'A0TTD6', 'Rent under RM0.0M', '{\"listing_type\": \"RENT\", \"city\": \"\", \"property_type\": \"\", \"max_price\": \"1000\", \"min_price\": \"\", \"bedrooms\": \"\", \"state\": \"\", \"keyword\": \"\"}', '2025-11-21 11:54:17'),
(22, '2TK4LE', 'Rent apartment 3BHK price RM1500', '{\"listing_type\": \"RENT\", \"city\": \"\", \"property_type\": \"apartment\", \"max_price\": \"1500\", \"min_price\": \"500\", \"bedrooms\": \"3\", \"state\": \"\", \"keyword\": \"\"}', '2025-11-21 15:51:02');

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `setting_key` varchar(50) NOT NULL,
  `setting_value` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`setting_key`, `setting_value`) VALUES
('default_free_posts', '3');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `id` int NOT NULL,
  `subject` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `requester` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL,
  `priority` varchar(50) NOT NULL,
  `agent_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `tags_json` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`id`, `subject`, `description`, `requester`, `status`, `priority`, `agent_id`, `created_at`, `updated_at`, `tags_json`) VALUES
(1, 'Login Issue on Mobile App', 'I can\'t seem to log in...', 'altamash@gmail.com', 'Open', 'Urgent', 20, '2025-11-12 17:41:12', '2025-11-17 17:40:45', '[\"login\", \"mobile-app\"]'),
(2, 'I think I need some help regarding property', 'ddfiwuefvavfajFG NP', 'aaban@gmail.com', 'Open', 'Medium', 21, '2025-11-12 17:42:20', '2025-11-12 17:47:37', '[]'),
(3, 'HI I am checking My properties are missing', 'Today when I logged on I found my properties to be missing', 'altamash@gmail.com', 'Open', 'Medium', 20, '2025-11-17 17:50:58', '2025-11-17 17:55:04', '[]');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL,
  `agent_id` char(8) DEFAULT NULL,
  `transaction_type` enum('purchase','spend') NOT NULL,
  `amount` int NOT NULL,
  `description` varchar(255) NOT NULL,
  `reference_id` varchar(15) DEFAULT NULL,
  `transaction_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `transaction_number` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`transaction_id`, `agent_id`, `transaction_type`, `amount`, `description`, `reference_id`, `transaction_date`, `transaction_number`) VALUES
(1, 'AGNBYIE8', 'purchase', 10, 'Purchase of 10 credits.', '1', '2025-11-13 05:26:52', 'X8Z5C58KU8'),
(2, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: 3 bedroom house', NULL, '2025-11-13 05:34:02', 'CSLF2PYKNA'),
(3, 'AGNBYIE8', 'purchase', 50, 'Purchase of credit plan ID: 3 (50 credits).', '2', '2025-11-13 05:49:12', '8Z48LXN9XP'),
(4, 'AGNQNTVL', 'purchase', 10, 'Purchase of 10 credits via Invoice #3', '3', '2025-11-13 11:32:48', 'FR8KXQGY5H'),
(5, 'AGNQNTVL', 'purchase', 25, 'Purchase of 25 credits via Invoice #5', '5', '2025-11-14 05:58:14', 'S9JRSGQW3B'),
(6, 'AGNQNTVL', 'purchase', 10, 'Purchase of 10 credits via Invoice #15', '15', '2025-11-14 09:40:44', '7QQ7HNKKU9'),
(7, 'AGNQNTVL', 'purchase', 10, 'Purchase of 10 credits via Invoice #16', '16', '2025-11-14 09:46:11', 'GBXHCYMU6X'),
(8, 'AGNQNTVL', 'purchase', 10, 'Purchase of 10 credits via Invoice #17', '17', '2025-11-14 09:47:04', 'ZWAG78CQB7'),
(9, 'AGNQNTVL', 'purchase', 25, 'Purchase of 25 credits via Invoice #18', '18', '2025-11-14 09:48:26', 'PLN9Z2VZ5D'),
(10, 'AGNQNTVL', 'purchase', 25, 'Purchase of 25 credits via Invoice #20', '20', '2025-11-14 09:50:15', '8PJCTS9M35'),
(11, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: Puteri Bayu, Bandar Puteri Puchong – Apartment For Rent', NULL, '2025-11-17 10:59:57', 'T6Y8WKUBP9'),
(12, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: Semi-Detached House', NULL, '2025-11-17 11:06:58', 'N9ZXG9HL6R'),
(13, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: awesome home', NULL, '2025-11-17 12:15:54', 'XRPXBH9KQQ'),
(14, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: awesome ', NULL, '2025-11-17 13:00:40', 'ZNZSPSNKNC'),
(15, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: fablouse ', NULL, '2025-11-17 13:10:46', 'JUE6BUZ7PM'),
(16, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: fablous', NULL, '2025-11-18 04:09:15', '5VT775R7BU'),
(17, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: good', NULL, '2025-11-18 04:49:49', 'KPFUQP59LY'),
(18, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: al falha ', NULL, '2025-11-18 04:55:07', '7BRHZ8T4TL'),
(19, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: al fida ', NULL, '2025-11-18 05:14:59', '4WYV5R4X7S'),
(21, 'AGNQNTVL', 'purchase', 10, 'Purchase of 10 credits via Invoice #25', '25', '2025-11-20 10:09:28', 'Z7PNWAEW28'),
(22, 'AGNQNTVL', 'purchase', 50, 'Purchase of 50 credits via Invoice #26', '26', '2025-11-20 10:10:20', 'T4SD9WE69J'),
(23, 'AGNQNTVL', 'purchase', 100, 'Purchase of 100 credits via Invoice #27', '27', '2025-11-20 11:11:05', 'E9RR7E8L5K'),
(28, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: faheem ka ghar', NULL, '2025-11-20 12:17:39', '8WKT5VQPZQ'),
(29, 'AGNQNTVL', 'spend', -1, 'Spent 1 credit to post property: faheem ', NULL, '2025-11-20 12:23:54', 'HKYWBLRR8M'),
(30, 'AGNQNTVL', 'purchase', 25, 'Purchase of 25 credits via Invoice #28', '28', '2025-11-20 12:26:11', 'US3Q42MQJ7'),
(31, 'AGNQNTVL', 'purchase', 25, 'Purchase of 25 credits via Invoice #28', '28', '2025-11-20 12:26:11', 'CFWYV6WSZC'),
(32, 'AGN9IIPO', 'purchase', 25, 'Purchase of 25 credits via Invoice #31', '31', '2025-11-21 11:30:43', 'GTD8MAAA84'),
(33, 'AGNTOREG', 'purchase', 100, 'Purchase of 100 credits via Invoice #32', '32', '2025-11-21 11:40:45', 'BAAA83FMN3'),
(34, 'AGNHIVLZ', 'purchase', 100, 'Purchase of 100 credits via Invoice #33', '33', '2025-11-21 12:17:44', 'BEVVKT5X23'),
(35, 'AGNBYIE8', 'spend', -1, 'Spent 1 credit to post property: 6 bedroom bungalow', NULL, '2025-11-24 05:28:37', 'BP8RTL8Z6G'),
(36, 'AGNBYIE8', 'purchase', 10, 'Purchase of 10 credits via Invoice #37', '37', '2025-11-25 04:57:27', 'V9EW5NMT2F'),
(37, 'AGNBYIE8', 'purchase', 10, 'Purchase of 10 credits via Invoice #38', '38', '2025-11-25 05:14:54', 'VE8NBAABEU'),
(38, 'AGNBYIE8', 'purchase', 10, 'Purchase of 10 credits via Invoice #38', '38', '2025-11-25 05:14:54', '2W5NMU5SAT'),
(39, 'AGNBYIE8', 'purchase', 100, 'Purchase of 100 credits via Invoice #39', '39', '2025-11-25 05:19:39', 'PFTK4J4KBL'),
(40, 'AGNBYIE8', 'purchase', 100, 'Purchase of 100 credits via Invoice #39', '39', '2025-11-25 05:19:39', 'Z2SNLRPW6U'),
(41, 'AGNBYIE8', 'purchase', 50, 'Purchase of 50 credits via Invoice #40', '40', '2025-11-25 05:25:28', '9QLLU9F69F'),
(42, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits via Invoice #41', '41', '2025-11-25 05:26:34', 'ER8L23ZHCU'),
(43, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits via Invoice #42', '42', '2025-11-25 05:34:58', 'XG7CW85PSM'),
(44, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits via Invoice #42', '42', '2025-11-25 05:34:59', 'VBRHXZXCN3'),
(45, 'AGNBYIE8', 'purchase', 10, 'Purchase of 10 credits via Invoice #43', '45', '2025-11-25 05:43:43', 'T5XZWBJHMC'),
(46, 'AGNBYIE8', 'purchase', 10, 'Purchase of 10 credits via Invoice #44', '46', '2025-11-25 06:21:46', '4HWRUMCLN9'),
(47, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits via Invoice #45', '45', '2025-11-25 06:29:46', 'MWCREKDV3C'),
(48, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits via Invoice #45', '45', '2025-11-25 06:29:47', 'TK27KZ48KV'),
(49, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits via Invoice #46', '46', '2025-11-25 06:32:00', 'UCYKM7RYCK'),
(50, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits via Invoice #46', '46', '2025-11-25 06:32:00', 'VYZTS9KUAN'),
(51, 'AGNBYIE8', 'purchase', 50, 'Purchase of 50 credits via Invoice #47', '47', '2025-11-25 06:32:41', 'VXT2FR8LYW'),
(52, 'AGNBYIE8', 'purchase', 25, 'Purchase of 25 credits ', 'V5S8JPMRMJ', '2025-11-25 10:51:00', 'K84J5TGJZ5'),
(54, 'AGNBYIE8', 'spend', -1, 'Spent 1 credit to post property: real top home', NULL, '2025-11-26 04:28:15', 'JRUS3SC8PL'),
(55, 'AGNBYIE8', 'spend', -1, 'Spent 1 credit to post property: awesom', NULL, '2025-11-26 11:39:21', '9LZW9BKLXR'),
(61, 'AGNBYIE8', 'spend', -1, 'Spent 1 credit to post property: fgg', NULL, '2025-11-26 12:04:23', 'CEQ2US65XY'),
(62, 'AGNZV75V', 'purchase', 25, 'Purchase of 25 credits ', '50', '2025-11-26 16:29:17', 'WDW7UEB33X');

--
-- Triggers `transactions`
--
DELIMITER $$
CREATE TRIGGER `before_transaction_insert_alphanum` BEFORE INSERT ON `transactions` FOR EACH ROW BEGIN
    -- If a transaction number isn't already provided, generate one.
    IF NEW.transaction_number IS NULL OR NEW.transaction_number = '' THEN
        SET NEW.transaction_number = generate_random_alphanum(10)$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id_1` int NOT NULL,
  `role_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` char(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `average_rating` decimal(3,2) NOT NULL DEFAULT '0.00',
  `review_count` int NOT NULL DEFAULT '0',
  `reset_token` varchar(100) DEFAULT NULL,
  `reset_token_expires` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id_1`, `role_id`, `name`, `email`, `password_hash`, `is_active`, `created_at`, `updated_at`, `user_id`, `average_rating`, `review_count`, `reset_token`, `reset_token_expires`) VALUES
(17, 2, 'farman', 'farman@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-10-27 09:45:51', '2025-12-01 08:12:22', 'UNG2OZ', 0.00, 0, NULL, NULL),
(18, 2, 'altamash', 'altamash3321@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-10-28 07:25:29', '2025-12-01 08:12:22', 'IE6C0P', 0.00, 0, '3ff19907-22b7-4945-814b-f4ca6c9706ba', '2025-11-26 13:24:43'),
(19, 1, 'aabanhn', 'aabanfarr@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-10-28 08:31:55', '2025-12-01 08:12:22', '6K020N', 0.00, 0, NULL, NULL),
(20, 3, 'faheem', 'faheem@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-11 05:07:32', '2025-12-01 08:12:22', '0DH1FT', 0.00, 0, NULL, NULL),
(21, 3, 'farru', 'farman123@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-11 05:53:39', '2025-12-01 08:12:22', '0EQ469', 0.00, 0, NULL, NULL),
(30, 4, 'farru', 'farru@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-14 12:19:20', '2025-12-01 08:12:22', 'GR9OA8', 0.00, 0, NULL, NULL),
(32, 1, 'faheem', 'faheem123@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-14 12:42:16', '2025-12-01 08:12:22', 'XWGD5B', 0.00, 0, NULL, NULL),
(33, 1, 'rahul', 'rahul@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-14 12:54:22', '2025-12-01 08:12:22', 'K19VDV', 0.00, 0, NULL, NULL),
(34, 1, 'Basheer', 'basheer@atxlearning.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1, '2025-11-14 13:35:03', '2025-12-01 08:12:22', '2TK4LE', 0.00, 0, NULL, NULL),
(35, 1, 'saqib', 'saqib@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-18 06:21:23', '2025-12-01 08:12:22', 'IHONZM', 0.00, 0, NULL, NULL),
(37, 1, 'sameer', 'sameer@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-18 06:24:45', '2025-12-01 08:12:22', 'RASWT2', 0.00, 0, NULL, NULL),
(41, 1, 'rehan', 'rehan@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-18 06:50:18', '2025-12-01 08:12:22', 'JIMBFV', 0.00, 0, NULL, NULL),
(43, 1, 'pooja', 'pooja@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-18 06:56:26', '2025-12-01 08:12:22', 'PGWWGA', 0.00, 0, NULL, NULL),
(44, 2, 'ankit', 'ankit@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-18 07:14:22', '2025-12-01 08:12:22', '4UNG3R', 0.00, 0, NULL, NULL),
(45, 2, 'Himanshu', 'Himanshu@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-18 07:49:54', '2025-12-01 08:12:22', '579F1P', 0.00, 0, NULL, NULL),
(48, 1, 'rekha', 'rekha@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-19 12:17:23', '2025-12-01 08:12:22', 'RI1DGY', 0.00, 0, NULL, NULL),
(49, 1, 'tabish', 'tabish@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-19 12:27:40', '2025-12-01 08:12:22', 'ZRMKN9', 0.00, 0, NULL, NULL),
(55, 1, 'Farzan', 'farzan@atxlearning.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1, '2025-11-19 15:38:33', '2025-12-01 08:12:22', '5BUZ4F', 0.00, 0, NULL, NULL),
(56, 1, 'altamash', 'md.altamash7257@gmail.com', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1, '2025-11-20 05:56:24', '2025-12-01 08:12:22', '6T9LU7', 0.00, 0, NULL, NULL),
(57, 1, 'eggaeg', 'altamash2@gmail.com', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1, '2025-11-20 07:17:04', '2025-12-01 08:12:22', 'I9LT3P', 0.00, 0, NULL, NULL),
(58, 1, 'alta', 'alta@gmail.com', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1, '2025-11-20 09:49:54', '2025-12-01 08:12:22', 'WU775U', 0.00, 0, NULL, NULL),
(59, 1, 'talha', 'talha@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-20 13:36:00', '2025-12-01 08:12:22', 'DB4GK8', 0.00, 0, NULL, NULL),
(60, 2, 'Basheer', 'basheer.mca@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1, '2025-11-20 16:00:32', '2025-12-01 08:12:22', '96S4X2', 0.00, 0, NULL, NULL),
(61, 2, 'Basheer Ahmad', 'basheer.atxlearning@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 1, '2025-11-20 16:17:39', '2025-12-01 08:12:22', '1US551', 0.00, 0, NULL, NULL),
(62, 1, 'naim', 'naim@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-21 09:15:45', '2025-12-01 08:12:22', 'S8L0YG', 0.00, 0, NULL, NULL),
(63, 2, 'altaaa', 'altamash3328@gmail.com', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1, '2025-11-21 11:24:30', '2025-12-01 08:12:22', 'B1YFZC', 0.00, 0, NULL, NULL),
(64, 2, 'saggy', 'saggy@gmail.com', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1, '2025-11-21 11:37:02', '2025-12-01 08:12:22', 'OZN0SL', 0.00, 0, NULL, NULL),
(65, 1, 'basheer', 'basheer@yahoo.com', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1, '2025-11-21 11:51:57', '2025-12-01 08:12:22', 'A0TTD6', 0.00, 0, NULL, NULL),
(66, 2, 'farmaaaaan', 'farmaaaan@gmail.com', '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1, '2025-11-21 12:10:54', '2025-12-01 08:12:22', '1GWT5Y', 0.00, 0, NULL, NULL),
(67, 1, 'ravi', 'ravi@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-24 10:16:26', '2025-12-01 08:12:22', 'VNFVS3', 0.00, 0, NULL, NULL),
(69, 1, 'mohd', 'mohd@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-25 04:15:39', '2025-12-01 08:12:22', 'XN8VGC', 0.00, 0, NULL, NULL),
(70, 1, 'print', 'print@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-25 04:16:36', '2025-12-01 08:12:22', 'CUYXG8', 0.00, 0, NULL, NULL),
(71, 1, 'sagar', 'sagar@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-25 04:26:50', '2025-12-01 08:12:22', '1ZJGEE', 0.00, 0, NULL, NULL),
(72, 1, 'ramu', 'ramu@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-25 04:28:33', '2025-12-01 08:12:22', 'KKVCX8', 0.00, 0, NULL, NULL),
(81, 1, 'arun', 'arun@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-26 10:47:54', '2025-12-01 08:12:22', 'LT2NPD', 0.00, 0, NULL, NULL),
(82, 1, 'home', 'home@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-26 12:05:44', '2025-12-01 08:12:22', 'BTVM7V', 0.00, 0, NULL, NULL),
(83, 1, 'dream', 'dream@gmail.com', '6c69d00baef0f8b17fdc6756e4bbc1d8d6e527b4f4e9d010817efa798ccb1e26', 1, '2025-11-26 12:16:10', '2025-12-01 08:12:22', 'V4ORGS', 0.00, 0, NULL, NULL);

--
-- Triggers `users`
--
DELIMITER $$
CREATE TRIGGER `before_user_insert` BEFORE INSERT ON `users` FOR EACH ROW BEGIN
    -- Call our new, corrected function to generate the ID
    SET NEW.user_id = generate_unique_user_id()$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `hash_password_insert` BEFORE INSERT ON `users` FOR EACH ROW BEGIN
    -- This takes the plain text password and replaces it with a SHA-256 Hash
    SET NEW.password_hash = SHA2(NEW.password_hash, 256)$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `hash_password_update` BEFORE UPDATE ON `users` FOR EACH ROW BEGIN
    -- Only hash if the password actually changed
    IF NEW.password_hash != OLD.password_hash THEN
        SET NEW.password_hash = SHA2(NEW.password_hash, 256)$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_user_activity_date` (`user_id`,`activity_type`,`created_at`);

--
-- Indexes for table `agents`
--
ALTER TABLE `agents`
  ADD PRIMARY KEY (`agent_id_1`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `uk_agent_public_id` (`agent_id`),
  ADD KEY `company_id` (`company_id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_company_id` (`company_id`),
  ADD KEY `idx_agent_status` (`agent_status`);

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`),
  ADD KEY `property_id` (`property_id`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_agent_date` (`agent_id`,`appointment_date`),
  ADD KEY `idx_property_id` (`property_id`),
  ADD KEY `idx_user_property_status` (`user_id`,`property_id`,`status`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `property_id` (`property_id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_property_id` (`property_id`),
  ADD KEY `idx_status_scheduled_date` (`status`,`scheduled_date`);

--
-- Indexes for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `sender_user_id` (`sender_user_id`),
  ADD KEY `idx_conversation` (`conversation_id`),
  ADD KEY `idx_conversation_sent` (`conversation_id`,`sent_at`),
  ADD KEY `idx_sender_user_id` (`sender_user_id`);

--
-- Indexes for table `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `author_id` (`author_id`),
  ADD KEY `ticket_id` (`ticket_id`),
  ADD KEY `idx_ticket_timestamp` (`ticket_id`,`timestamp`),
  ADD KEY `idx_author` (`author_type`,`author_id`);

--
-- Indexes for table `companies`
--
ALTER TABLE `companies`
  ADD PRIMARY KEY (`company_id`),
  ADD UNIQUE KEY `idx_company_name_unique` (`company_name`),
  ADD KEY `idx_location` (`state`,`city`);

--
-- Indexes for table `conversations`
--
ALTER TABLE `conversations`
  ADD PRIMARY KEY (`conversation_id`),
  ADD UNIQUE KEY `uk_user_agent` (`user_id`,`agent_id`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `idx_agent_id` (`agent_id`);

--
-- Indexes for table `credit_plans`
--
ALTER TABLE `credit_plans`
  ADD PRIMARY KEY (`plan_id`);

--
-- Indexes for table `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`favorite_id`),
  ADD UNIQUE KEY `unique_fav` (`user_id`,`property_id`),
  ADD KEY `property_id` (`property_id`);

--
-- Indexes for table `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`invoice_id`),
  ADD UNIQUE KEY `uk_invoice_number` (`invoice_number`),
  ADD UNIQUE KEY `uk_stripe_session_id` (`stripe_session_id`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `idx_agent_id` (`agent_id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`member_id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD UNIQUE KEY `uk_user_id` (`user_id`);

--
-- Indexes for table `properties`
--
ALTER TABLE `properties`
  ADD PRIMARY KEY (`property_id_1`),
  ADD UNIQUE KEY `property_id` (`property_id`),
  ADD UNIQUE KEY `property_id_2` (`property_id`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `idx_search_main` (`is_deleted`,`city`,`property_type`,`price`,`bedrooms`),
  ADD KEY `idx_sorting_featured` (`is_deleted`,`is_featured`,`created_at`);

--
-- Indexes for table `property_images`
--
ALTER TABLE `property_images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `property_id` (`property_id`),
  ADD KEY `idx_property_id` (`property_id`),
  ADD KEY `idx_property_cover` (`property_id`,`is_cover`);

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`rating_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `property_id` (`property_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`review_id`),
  ADD UNIQUE KEY `uk_unique_review` (`reviewer_user_id`,`review_target_type`,`review_target_id`),
  ADD KEY `idx_review_target` (`review_target_type`,`review_target_id`),
  ADD KEY `idx_reviewer_user_id` (`reviewer_user_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Indexes for table `saved_searches`
--
ALTER TABLE `saved_searches`
  ADD PRIMARY KEY (`search_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`setting_key`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `agent_id` (`agent_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD UNIQUE KEY `transaction_number` (`transaction_number`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `idx_agent_date` (`agent_id`,`transaction_date` DESC),
  ADD KEY `idx_transaction_type` (`transaction_type`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id_1`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `uk_public_id` (`user_id`),
  ADD KEY `role_id` (`role_id`),
  ADD KEY `idx_login_credentials` (`email`,`password_hash`),
  ADD KEY `idx_role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `log_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `agents`
--
ALTER TABLE `agents`
  MODIFY `agent_id_1` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `chat_messages`
--
ALTER TABLE `chat_messages`
  MODIFY `message_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT for table `comment`
--
ALTER TABLE `comment`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `companies`
--
ALTER TABLE `companies`
  MODIFY `company_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `conversations`
--
ALTER TABLE `conversations`
  MODIFY `conversation_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `credit_plans`
--
ALTER TABLE `credit_plans`
  MODIFY `plan_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `favorites`
--
ALTER TABLE `favorites`
  MODIFY `favorite_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=255;

--
-- AUTO_INCREMENT for table `invoices`
--
ALTER TABLE `invoices`
  MODIFY `invoice_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `member_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `properties`
--
ALTER TABLE `properties`
  MODIFY `property_id_1` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `property_images`
--
ALTER TABLE `property_images`
  MODIFY `image_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=178;

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `rating_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `review_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `saved_searches`
--
ALTER TABLE `saved_searches`
  MODIFY `search_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ticket`
--
ALTER TABLE `ticket`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `transaction_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id_1` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `agents`
--
ALTER TABLE `agents`
  ADD CONSTRAINT `agents_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`) ON DELETE SET NULL;

--
-- Constraints for table `comment`
--
ALTER TABLE `comment`
  ADD CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`id`);

--
-- Constraints for table `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `fk_invoices_public_agent` FOREIGN KEY (`agent_id`) REFERENCES `agents` (`agent_id`);

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `users` (`user_id_1`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
