# ************************************************************
# Sequel Pro SQL dump
# バージョン 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# ホスト: 127.0.0.1 (MySQL 5.7.26)
# データベース: 42hackathon
# 作成時刻: 2020-04-30 10:03:04 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# テーブルのダンプ codeworks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `codeworks`;

CREATE TABLE `codeworks` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL DEFAULT '',
  `subject` varchar(50) NOT NULL DEFAULT '',
  `title` varchar(100) NOT NULL DEFAULT '',
  `code` longtext NOT NULL,
  `description` longtext NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `codeworks` WRITE;
/*!40000 ALTER TABLE `codeworks` DISABLE KEYS */;

INSERT INTO `codeworks` (`id`, `username`, `subject`, `title`, `code`, `description`, `created_at`)
VALUES
	(1,'ydoi','Pre Open 02','ex00について','<span>Hello World!</span>','This code is awesome','2020-04-29 17:32:42'),
	(2,'ydoi','Pre Open 02','ex01の傑作','<span>Hello Japan!</span>','This code is fabulous.','2020-04-29 17:32:42'),
	(3,'ydoi','Pre Open 01','ex01模範','<span>python3 app.py</span>','This code is amazing.','2020-04-29 17:32:42'),
	(4,'ydoi','C Piscine C 10','ex09','<span>TEST TEST</span>','This code is fantastic','2020-04-30 18:41:17'),
	(5,'ydoi','C Piscine C 13','ex09','<span>TEST TEST</span>','This code is fantastic','2020-04-30 18:50:07'),
	(6,'ydoi','C Piscine C 11','ex09','<span>TEST TEST</span>','This code is fantastic','2020-04-30 18:51:14');

/*!40000 ALTER TABLE `codeworks` ENABLE KEYS */;
UNLOCK TABLES;


# テーブルのダンプ users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ft_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`username`),
  UNIQUE KEY `42_id` (`ft_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `ft_id`, `username`, `password`)
VALUES
	(1,67719,'ydoi','password'),
	(4,67644,'ksuzuki','password');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
