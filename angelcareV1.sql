-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: angelcare
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accelerometer_readings`
--

DROP TABLE IF EXISTS `accelerometer_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accelerometer_readings` (
  `id_reading` bigint NOT NULL AUTO_INCREMENT,
  `id_smartwatch` int NOT NULL,
  `axis_x` decimal(10,6) NOT NULL,
  `axis_y` decimal(10,6) NOT NULL,
  `axis_z` decimal(10,6) NOT NULL,
  `is_fall` tinyint(1) DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_reading`),
  KEY `id_smartwatch` (`id_smartwatch`),
  CONSTRAINT `accelerometer_readings_ibfk_1` FOREIGN KEY (`id_smartwatch`) REFERENCES `smartwatches` (`id_smartwatch`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accelerometer_readings`
--

LOCK TABLES `accelerometer_readings` WRITE;
/*!40000 ALTER TABLE `accelerometer_readings` DISABLE KEYS */;
/*!40000 ALTER TABLE `accelerometer_readings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `action_logger`
--

DROP TABLE IF EXISTS `action_logger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `action_logger` (
  `id_log` int NOT NULL AUTO_INCREMENT,
  `id_admin` int NOT NULL,
  `action_type` varchar(50) NOT NULL,
  `target_user_id` int DEFAULT NULL,
  `details` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_log`),
  KEY `id_admin` (`id_admin`),
  CONSTRAINT `action_logger_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `users` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action_logger`
--

LOCK TABLES `action_logger` WRITE;
/*!40000 ALTER TABLE `action_logger` DISABLE KEYS */;
/*!40000 ALTER TABLE `action_logger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_profiles`
--

DROP TABLE IF EXISTS `app_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_profiles` (
  `id_profile` int NOT NULL AUTO_INCREMENT,
  `id_daycare` int NOT NULL,
  `profile_name` varchar(100) NOT NULL DEFAULT 'Default Profile',
  `max_temp_threshold` decimal(4,2) DEFAULT '38.00',
  `min_temp_threshold` decimal(4,2) DEFAULT '36.00',
  `max_hr_threshold` int DEFAULT '160',
  `min_hr_threshold` int DEFAULT '80',
  `min_spo2_threshold` decimal(5,2) DEFAULT '95.00',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_profile`),
  KEY `id_daycare` (`id_daycare`),
  CONSTRAINT `app_profiles_ibfk_1` FOREIGN KEY (`id_daycare`) REFERENCES `daycares` (`id_daycare`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_profiles`
--

LOCK TABLES `app_profiles` WRITE;
/*!40000 ALTER TABLE `app_profiles` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audio_recordings`
--

DROP TABLE IF EXISTS `audio_recordings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audio_recordings` (
  `id_recording` bigint NOT NULL AUTO_INCREMENT,
  `id_smartwatch` int NOT NULL,
  `file_identifier` varchar(255) NOT NULL,
  `decibel_level` decimal(5,2) DEFAULT NULL,
  `duration_seconds` int DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_recording`),
  KEY `id_smartwatch` (`id_smartwatch`),
  CONSTRAINT `audio_recordings_ibfk_1` FOREIGN KEY (`id_smartwatch`) REFERENCES `smartwatches` (`id_smartwatch`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audio_recordings`
--

LOCK TABLES `audio_recordings` WRITE;
/*!40000 ALTER TABLE `audio_recordings` DISABLE KEYS */;
/*!40000 ALTER TABLE `audio_recordings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `children`
--

DROP TABLE IF EXISTS `children`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `children` (
  `id_child` int NOT NULL AUTO_INCREMENT,
  `id_daycare` int NOT NULL,
  `id_tutor` int NOT NULL,
  `id_smartwatch` int NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_child`),
  UNIQUE KEY `id_tutor` (`id_tutor`),
  UNIQUE KEY `id_smartwatch` (`id_smartwatch`),
  KEY `id_daycare` (`id_daycare`),
  CONSTRAINT `children_ibfk_1` FOREIGN KEY (`id_daycare`) REFERENCES `daycares` (`id_daycare`),
  CONSTRAINT `children_ibfk_2` FOREIGN KEY (`id_tutor`) REFERENCES `users` (`id_user`),
  CONSTRAINT `children_ibfk_3` FOREIGN KEY (`id_smartwatch`) REFERENCES `smartwatches` (`id_smartwatch`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children`
--

LOCK TABLES `children` WRITE;
/*!40000 ALTER TABLE `children` DISABLE KEYS */;
/*!40000 ALTER TABLE `children` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `daycares`
--

DROP TABLE IF EXISTS `daycares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `daycares` (
  `id_daycare` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_daycare`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daycares`
--

LOCK TABLES `daycares` WRITE;
/*!40000 ALTER TABLE `daycares` DISABLE KEYS */;
INSERT INTO `daycares` VALUES (1,'Estancia El Solecito','Av. Revolución 123','664-555-0101','2025-10-03 08:33:17');
/*!40000 ALTER TABLE `daycares` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exception_logger`
--

DROP TABLE IF EXISTS `exception_logger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exception_logger` (
  `id_exception` int NOT NULL AUTO_INCREMENT,
  `error_message` text,
  `stack_trace` text,
  `endpoint` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_exception`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exception_logger`
--

LOCK TABLES `exception_logger` WRITE;
/*!40000 ALTER TABLE `exception_logger` DISABLE KEYS */;
/*!40000 ALTER TABLE `exception_logger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `heart_rate_readings`
--

DROP TABLE IF EXISTS `heart_rate_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `heart_rate_readings` (
  `id_reading` bigint NOT NULL AUTO_INCREMENT,
  `id_smartwatch` int NOT NULL,
  `beats_per_minute` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_reading`),
  KEY `id_smartwatch` (`id_smartwatch`),
  CONSTRAINT `heart_rate_readings_ibfk_1` FOREIGN KEY (`id_smartwatch`) REFERENCES `smartwatches` (`id_smartwatch`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `heart_rate_readings`
--

LOCK TABLES `heart_rate_readings` WRITE;
/*!40000 ALTER TABLE `heart_rate_readings` DISABLE KEYS */;
/*!40000 ALTER TABLE `heart_rate_readings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oxygenation_readings`
--

DROP TABLE IF EXISTS `oxygenation_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oxygenation_readings` (
  `id_reading` bigint NOT NULL AUTO_INCREMENT,
  `id_smartwatch` int NOT NULL,
  `spo2_level` decimal(5,2) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_reading`),
  KEY `id_smartwatch` (`id_smartwatch`),
  CONSTRAINT `oxygenation_readings_ibfk_1` FOREIGN KEY (`id_smartwatch`) REFERENCES `smartwatches` (`id_smartwatch`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oxygenation_readings`
--

LOCK TABLES `oxygenation_readings` WRITE;
/*!40000 ALTER TABLE `oxygenation_readings` DISABLE KEYS */;
/*!40000 ALTER TABLE `oxygenation_readings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smartwatches`
--

DROP TABLE IF EXISTS `smartwatches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smartwatches` (
  `id_smartwatch` int NOT NULL AUTO_INCREMENT,
  `device_id` varchar(100) NOT NULL,
  `model` varchar(100) DEFAULT NULL,
  `status` enum('active','inactive','maintenance') DEFAULT 'inactive',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_smartwatch`),
  UNIQUE KEY `device_id` (`device_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smartwatches`
--

LOCK TABLES `smartwatches` WRITE;
/*!40000 ALTER TABLE `smartwatches` DISABLE KEYS */;
/*!40000 ALTER TABLE `smartwatches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temperature_readings`
--

DROP TABLE IF EXISTS `temperature_readings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temperature_readings` (
  `id_reading` bigint NOT NULL AUTO_INCREMENT,
  `id_smartwatch` int NOT NULL,
  `temperature` decimal(4,2) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_reading`),
  KEY `id_smartwatch` (`id_smartwatch`),
  CONSTRAINT `temperature_readings_ibfk_1` FOREIGN KEY (`id_smartwatch`) REFERENCES `smartwatches` (`id_smartwatch`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperature_readings`
--

LOCK TABLES `temperature_readings` WRITE;
/*!40000 ALTER TABLE `temperature_readings` DISABLE KEYS */;
/*!40000 ALTER TABLE `temperature_readings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `id_daycare` int DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('admin','teacher','tutor') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `id_daycare` (`id_daycare`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`id_daycare`) REFERENCES `daycares` (`id_daycare`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,1,'admin','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Brayan','Alvarez','brayanalvcod@gmail.com','admin','2025-10-03 08:57:43');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-03  2:39:38
