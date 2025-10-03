-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: angelcarev1
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accelerometer_readings`
--

LOCK TABLES `accelerometer_readings` WRITE;
/*!40000 ALTER TABLE `accelerometer_readings` DISABLE KEYS */;
INSERT INTO `accelerometer_readings` VALUES (1,2,0.010000,-9.800000,0.050000,0,'2025-10-05 19:45:26'),(2,2,0.030000,-9.790000,0.040000,0,'2025-10-05 19:55:26'),(3,1,2.500000,-8.500000,3.100000,0,'2025-10-05 20:45:26'),(4,3,15.500000,-20.100000,18.200000,1,'2025-10-05 20:20:26'),(5,3,0.500000,-9.500000,1.200000,0,'2025-10-05 20:21:26'),(6,5,1.200000,-9.200000,2.500000,0,'2025-10-05 21:00:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action_logger`
--

LOCK TABLES `action_logger` WRITE;
/*!40000 ALTER TABLE `action_logger` DISABLE KEYS */;
INSERT INTO `action_logger` VALUES (1,2,'CREATE_TUTOR',14,'Se creó el usuario tutor Fernando Flores para la guardería 1.','2025-10-05 21:15:26'),(2,5,'UPDATE_CHILD',3,'Se actualizó la información médica del niño Santiago Moreno. Alergia al maní agregada.','2025-10-05 21:15:26'),(3,1,'DEACTIVATE_SMARTWATCH',6,'La pulsera DEV-SN006-TJN se marcó para mantenimiento por batería baja.','2025-10-05 21:15:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_profiles`
--

LOCK TABLES `app_profiles` WRITE;
/*!40000 ALTER TABLE `app_profiles` DISABLE KEYS */;
INSERT INTO `app_profiles` VALUES (1,1,'Default Profile - Mi Pequeño Mundo',38.50,36.00,160,75,94.00,'2025-10-05 21:15:26'),(2,2,'Default Profile - El Sol de Tijuana',38.00,36.20,165,80,95.00,'2025-10-05 21:15:26'),(3,3,'Default Profile - Kinderspace Otay',38.20,36.10,162,78,94.50,'2025-10-05 21:15:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audio_recordings`
--

LOCK TABLES `audio_recordings` WRITE;
/*!40000 ALTER TABLE `audio_recordings` DISABLE KEYS */;
INSERT INTO `audio_recordings` VALUES (1,2,'/audio/daycare1/20251005_121500_dev2.wav',45.50,30,'2025-10-05 19:45:26'),(2,1,'/audio/daycare1/20251005_133000_dev1.wav',75.20,60,'2025-10-05 20:45:26'),(3,3,'/audio/daycare2/20251005_130500_dev3.wav',88.00,15,'2025-10-05 20:20:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children`
--

LOCK TABLES `children` WRITE;
/*!40000 ALTER TABLE `children` DISABLE KEYS */;
INSERT INTO `children` VALUES (1,1,9,1,'Mateo','Peralta','2022-05-15','2025-10-05 21:15:26'),(2,1,10,2,'Valentina','González','2023-01-20','2025-10-05 21:15:26'),(3,2,11,3,'Santiago','Moreno','2021-11-10','2025-10-05 21:15:26'),(4,2,12,4,'Camila','Ramírez','2022-08-01','2025-10-05 21:15:26'),(5,3,13,5,'Leo','Castillo','2023-03-30','2025-10-05 21:15:26'),(6,3,14,6,'Isabella','Flores','2021-09-05','2025-10-05 21:15:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daycares`
--

LOCK TABLES `daycares` WRITE;
/*!40000 ALTER TABLE `daycares` DISABLE KEYS */;
INSERT INTO `daycares` VALUES (1,'Estancia Infantil Mi Pequeño Mundo','Blvd. Agua Caliente 10534, Col. Aviación, 22014 Tijuana, B.C.','664-123-4567','2025-10-05 21:15:26'),(2,'Guardería El Sol de Tijuana','Paseo de los Héroes 9350, Zona Urbana Rio, 22010 Tijuana, B.C.','664-234-5678','2025-10-05 21:15:26'),(3,'Kinderspace Otay','Blvd. Lázaro Cárdenas 405, Otay Constituyentes, 22457 Tijuana, B.C.','664-345-6789','2025-10-05 21:15:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exception_logger`
--

LOCK TABLES `exception_logger` WRITE;
/*!40000 ALTER TABLE `exception_logger` DISABLE KEYS */;
INSERT INTO `exception_logger` VALUES (1,'java.lang.NullPointerException: Cannot invoke \"com.example.Sensor.getValue()\" because \"sensor\" is null','at com.example.service.SensorService.processData(SensorService.java:42)','/api/v1/sensor/reading','2025-10-05 21:15:27'),(2,'502 Bad Gateway: Upstream service unavailable','N/A','/api/v1/notifications/send','2025-10-05 21:15:27');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `heart_rate_readings`
--

LOCK TABLES `heart_rate_readings` WRITE;
/*!40000 ALTER TABLE `heart_rate_readings` DISABLE KEYS */;
INSERT INTO `heart_rate_readings` VALUES (1,1,95,'2025-10-05 19:15:26'),(2,1,98,'2025-10-05 20:15:26'),(3,1,145,'2025-10-05 20:45:26'),(4,2,85,'2025-10-05 19:45:26'),(5,2,82,'2025-10-05 20:15:26'),(6,2,88,'2025-10-05 21:05:26'),(7,3,130,'2025-10-05 19:15:26'),(8,3,155,'2025-10-05 20:15:26'),(9,4,105,'2025-10-05 20:45:26'),(10,5,140,'2025-10-05 21:00:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oxygenation_readings`
--

LOCK TABLES `oxygenation_readings` WRITE;
/*!40000 ALTER TABLE `oxygenation_readings` DISABLE KEYS */;
INSERT INTO `oxygenation_readings` VALUES (1,1,98.50,'2025-10-05 19:15:26'),(2,1,99.00,'2025-10-05 20:15:26'),(3,2,97.80,'2025-10-05 19:45:26'),(4,3,99.50,'2025-10-05 20:15:26'),(5,4,98.00,'2025-10-05 20:45:26'),(6,5,99.10,'2025-10-05 21:05:26'),(7,1,98.80,'2025-10-05 21:10:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smartwatches`
--

LOCK TABLES `smartwatches` WRITE;
/*!40000 ALTER TABLE `smartwatches` DISABLE KEYS */;
INSERT INTO `smartwatches` VALUES (1,'DEV-SN001-TJN','KidsFit 2.0','active','2025-10-05 21:15:26'),(2,'DEV-SN002-TJN','KidsFit 2.0','active','2025-10-05 21:15:26'),(3,'DEV-SN003-TJN','WeeWatch Pro','active','2025-10-05 21:15:26'),(4,'DEV-SN004-TJN','WeeWatch Pro','active','2025-10-05 21:15:26'),(5,'DEV-SN005-TJN','KidsFit 2.0','active','2025-10-05 21:15:26'),(6,'DEV-SN006-TJN','WeeWatch Pro','maintenance','2025-10-05 21:15:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperature_readings`
--

LOCK TABLES `temperature_readings` WRITE;
/*!40000 ALTER TABLE `temperature_readings` DISABLE KEYS */;
INSERT INTO `temperature_readings` VALUES (1,1,37.10,'2025-10-05 19:15:26'),(2,1,37.20,'2025-10-05 20:15:26'),(3,1,38.50,'2025-10-05 20:45:26'),(4,2,36.80,'2025-10-05 19:15:26'),(5,2,36.90,'2025-10-05 20:15:26'),(6,3,37.00,'2025-10-05 19:45:26'),(7,4,36.70,'2025-10-05 20:30:26'),(8,5,37.30,'2025-10-05 21:05:26');
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,NULL,'admin','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Armando','Paredes','super@admin.com','admin','2025-10-05 21:15:26'),(2,1,'admin_mundo','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Laura','Gómez','laura.gomez@pequenomundo.com','admin','2025-10-05 21:15:26'),(3,1,'teacher_ana','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Ana','Martínez','ana.martinez@pequenomundo.com','teacher','2025-10-05 21:15:26'),(4,1,'teacher_carlos','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Carlos','Rodríguez','carlos.rodriguez@pequenomundo.com','teacher','2025-10-05 21:15:26'),(5,2,'admin_sol','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Sofía','López','sofia.lopez@elsoltj.com','admin','2025-10-05 21:15:26'),(6,2,'teacher_juan','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Juan','Hernández','juan.hernandez@elsoltj.com','teacher','2025-10-05 21:15:26'),(7,3,'admin_otay','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Miguel','Pérez','miguel.perez@kinderspace.com','admin','2025-10-05 21:15:26'),(8,3,'teacher_lucia','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Lucía','García','lucia.garcia@kinderspace.com','teacher','2025-10-05 21:15:26'),(9,1,'tutor_juanp','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Juan','Peralta','juan.peralta@email.com','tutor','2025-10-05 21:15:26'),(10,1,'tutor_mariag','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Maria','González','maria.gonzalez@email.com','tutor','2025-10-05 21:15:26'),(11,2,'tutor_pedrom','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Pedro','Moreno','pedro.moreno@email.com','tutor','2025-10-05 21:15:26'),(12,2,'tutor_sofiar','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Sofia','Ramírez','sofia.ramirez@email.com','tutor','2025-10-05 21:15:26'),(13,3,'tutor_dianac','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Diana','Castillo','diana.castillo@email.com','tutor','2025-10-05 21:15:26'),(14,3,'tutor_fernandof','scrypt:32768:8:1$kDzPJ3hiZhoc99bb$53be1fd8625d54652a0161fa3915d2969e52828f341c9a0dcdea9337e4305a410ef915383b73b233faac17dddc9941d2e6ca1fced347155171d062b4f80f871b','Fernando','Flores','fernando.flores@email.com','tutor','2025-10-05 21:15:26');
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

-- Dump completed on 2025-10-06 18:14:19
