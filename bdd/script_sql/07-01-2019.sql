/* arlex_db database creation */
CREATE DATABASE arlex_db;

/*user table creation*/

CREATE TABLE IF NOT EXISTS `arlex_db`.`user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(5) NOT NULL,
  `status` tinyint(10) NOT NULL,
  `gender` tinyint(10) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `mail` varchar(45) NOT NULL,
  `password` varchar(100) NOT NULL,
  `country` varchar(45) NOT NULL,
  `town` varchar(45) NOT NULL,
  `street` varchar(255) NOT NULL,
  `street_number` varchar(45) NOT NULL,
  `region` varchar(45) NOT NULL,
  `postal_code` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `idx_date_insert` (`date_insert`),
  KEY `idx_date_update` (`date_update`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/* token table creation*/
CREATE TABLE IF NOT EXISTS `arlex_db`.`token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `access_token` varchar(255) NOT NULL,
  `refresh_token` varchar(255) NOT NULL,
  `id_user` int(11) NOT NULL,
  `expiration_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `app_id` varchar(255) NOT NULL,
  `type` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `access_token_UNIQUE` (`access_token`),
  UNIQUE KEY `refresh_token_UNIQUE` (`refresh_token`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/* sensor table creation*/
CREATE TABLE IF NOT EXISTS `arlex_db`.`sensor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(5) NOT NULL,
  `id_user` int(11) NOT NULL,
  `type` tinyint(5) NOT NULL,
  `name` varchar(255) NOT NULL,
  `sensorcol` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `idx_date_insert` (`date_insert`),
  KEY `idx_date_update` (`date_update`),
  KEY `idx_id_user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/* product table creation*/
CREATE TABLE IF NOT EXISTS `arlex_db`.`product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_update` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expiration_date` datetime NOT NULL,
  `status` tinyint(5) NOT NULL,
  `id_rfid` int(11) NOT NULL,
  `id_ean` varchar(130) NOT NULL,
  `position` varchar(255) NOT NULL,
  `id_user` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `idx_date_insert` (`date_insert`),
  KEY `idx_date_update` (`date_update`),
  KEY `idx_id_rfid` (`id_rfid`),
  KEY `idx_id_ean` (`id_ean`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/* log table creation*/
CREATE TABLE TABLE IF NOT EXISTS `arlex_db`.`log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `code` int(11) NOT NULL,
  `data` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `idx_date_insert` (`date_insert`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
