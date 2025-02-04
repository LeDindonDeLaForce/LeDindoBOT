-- MySQL dump 10.16  Distrib 10.1.48-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: TWITCH_BOT
-- ------------------------------------------------------
-- Server version       10.1.48-MariaDB-0+deb9u2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CHANNEL_LIST`
--

DROP TABLE IF EXISTS `CHANNEL_LIST`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CHANNEL_LIST` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `channel` varchar(25) NOT NULL,
  `queue` tinyint(1) NOT NULL DEFAULT '0',
  `roulette` varchar(7) NOT NULL DEFAULT 'stopped',
  PRIMARY KEY (`id`),
  UNIQUE KEY `channel` (`channel`)
) ENGINE=InnoDB AUTO_INCREMENT=889 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `commands`
--

DROP TABLE IF EXISTS `commands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commands` (
  `command` varchar(40) NOT NULL,
  `channel` int(10) NOT NULL,
  `text` text,
  PRIMARY KEY (`command`,`channel`),
  KEY `channel` (`channel`),
  CONSTRAINT `commands_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `quoteauthors`
--

DROP TABLE IF EXISTS `quoteauthors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `quoteauthors` (
  `channel` int(10) NOT NULL,
  `allowedauthor` varchar(40) NOT NULL,
  PRIMARY KEY (`channel`,`allowedauthor`),
  CONSTRAINT `quoteauthors_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `routines`
--

DROP TABLE IF EXISTS `routines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `routines` (
  `channel` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `seconds` int(11) NOT NULL,
  `minutes` int(11) NOT NULL,
  `hours` int(11) NOT NULL,
  `routine_text` text NOT NULL,
  PRIMARY KEY (`channel`),
  CONSTRAINT `routines_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `stream_queue`
--

DROP TABLE IF EXISTS `stream_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stream_queue` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `channel` int(10) NOT NULL,
  `user` varchar(25) NOT NULL,
  PRIMARY KEY (`channel`,`user`),
  UNIQUE KEY `id_2` (`id`),
  KEY `channel` (`channel`),
  KEY `id` (`id`),
  CONSTRAINT `stream_queue_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `CHANNEL_LIST` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-14  8:16:09
