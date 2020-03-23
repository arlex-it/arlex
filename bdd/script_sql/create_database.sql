/* Made By Simon Bauchet */
/* Create the database and user, token, sensor, product and log tables */

/* arlex_db database creation */
CREATE DATABASE arlex_db;

CREATE USER 'unit_test'@'127.0.0.1' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON arlex_db.* TO 'unit_test'@'127.0.0.1';

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

/* token table creation*/
CREATE TABLE IF NOT EXISTS `arlex_db`.`token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `token` varchar(255) NOT NULL,
  `id_user` int(11) NOT NULL,
  `expiration_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `app_id` varchar(255) NOT NULL,
  `type` varchar(100) NOT NULL,
  `is_enable` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `access_token_UNIQUE` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


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
CREATE TABLE IF NOT EXISTS `arlex_db`.`log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `code` int(11) NOT NULL,
  `data` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `idx_date_insert` (`date_insert`),
  KEY `idx_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `arlex_db`.`auth_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(45) NOT NULL,
  `client_id` varchar(100) NOT NULL,
  `project_id` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `arlex_db`.`access_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `token` varchar(255) NOT NULL,
  `id_user` int(11) NOT NULL,
  `expiration_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `app_id` varchar(255) NOT NULL,
  `type` varchar(100) NOT NULL,
  `is_enable` int(4) NOT NULL,
  `scopes` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `arlex_db`.`refresh_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_insert` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `token` varchar(255) NOT NULL,
  `app_id` varchar(255) NOT NULL,
  `is_enable` int(4) NOT NULL,
  `access_token_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
