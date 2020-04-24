-- MySQL Script generated by MySQL Workbench
<<<<<<<<< Temporary merge branch 1
-- mer. 06 nov. 2019 15:52:42 CET
=========
-- dim. 15 déc. 2019 19:55:17 CET
>>>>>>>>> Temporary merge branch 2
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Arlex
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `Arlex` ;

-- -----------------------------------------------------
-- Schema Arlex
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Arlex` ;
USE `Arlex` ;

-- -----------------------------------------------------
-- Table `Arlex`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Arlex`.`user` ;

CREATE TABLE IF NOT EXISTS `Arlex`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
<<<<<<<<< Temporary merge branch 1
  `date_insert` DATETIME NOT NULL,
  `date_update` DATETIME NOT NULL,
  `is_active` INT NOT NULL,
  `status` INT NOT NULL,
  `gender` INT NOT NULL,
=========
  `date_insert` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` TINYINT(5) NOT NULL,
  `status` TINYINT(10) NOT NULL,
  `gender` TINYINT(10) NOT NULL,
>>>>>>>>> Temporary merge branch 2
  `lastname` VARCHAR(45) NOT NULL,
  `firstname` VARCHAR(45) NOT NULL,
  `mail` VARCHAR(45) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `town` VARCHAR(45) NOT NULL,
  `street` VARCHAR(255) NOT NULL,
  `street_number` VARCHAR(45) NOT NULL,
  `region` VARCHAR(45) NOT NULL,
<<<<<<<<< Temporary merge branch 1
  `postal_code` INT NOT NULL,
=========
>>>>>>>>> Temporary merge branch 2
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `idx_date_insert` (`date_insert` ASC),
  INDEX `idx_date_update` (`date_update` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Arlex`.`sensor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Arlex`.`sensor` ;

CREATE TABLE IF NOT EXISTS `Arlex`.`sensor` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date_insert` DATETIME NOT NULL,
  `date_update` DATETIME NOT NULL,
<<<<<<<<< Temporary merge branch 1
  `is_active` INT NOT NULL,
  `id_user` INT NOT NULL,
  `type` INT NOT NULL,
=========
  `is_active` TINYINT(5) NOT NULL,
  `id_user` INT NOT NULL,
  `type` TINYINT(5) NOT NULL,
>>>>>>>>> Temporary merge branch 2
  `name` VARCHAR(255) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_sensor_user_idx` (`user_id` ASC),
  INDEX `idx_date_insert` (`date_insert` ASC),
  INDEX `idx_date_update` (`date_update` ASC),
  CONSTRAINT `fk_sensor_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `Arlex`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Arlex`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Arlex`.`product` ;

CREATE TABLE IF NOT EXISTS `Arlex`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
<<<<<<<<< Temporary merge branch 1
  `date_insert` DATETIME NOT NULL,
  `date_update` DATETIME NOT NULL,
  `expiration_date` DATE NOT NULL,
  `status` INT NOT NULL,
  `id_rfid` INT NOT NULL,
  `id_ean` INT NOT NULL,
  `position` VARCHAR(255) NOT NULL,
  `id_user` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_product_user1_idx` (`user_id` ASC),
=========
  `date_insert` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expiration_date` DATETIME NOT NULL,
  `status` TINYINT(5) NOT NULL,
  `id_rfid` INT NOT NULL,
  `id_ean` VARCHAR(130) NOT NULL,
  `position` VARCHAR(255) NOT NULL,
  `id_user` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
>>>>>>>>> Temporary merge branch 2
  INDEX `idx_date_insert` (`date_insert` ASC),
  INDEX `idx_date_update` (`date_update` ASC),
  INDEX `idx_id_rfid` (`id_rfid` ASC),
  INDEX `idx_id_ean` (`id_ean` ASC),
<<<<<<<<< Temporary merge branch 1
  CONSTRAINT `fk_product_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Arlex`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
=========
  INDEX `idx_id_user` (`user_id` ASC))
>>>>>>>>> Temporary merge branch 2
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Arlex`.`log`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Arlex`.`log` ;

CREATE TABLE IF NOT EXISTS `Arlex`.`log` (
  `id` INT NOT NULL AUTO_INCREMENT,
<<<<<<<<< Temporary merge branch 1
  `date_insert` DATETIME NOT NULL,
=========
  `date_insert` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
>>>>>>>>> Temporary merge branch 2
  `code` INT NOT NULL,
  `data` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `idx_date_insert` (`date_insert` ASC),
  INDEX `idx_code` (`code` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Arlex`.`token`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Arlex`.`token` ;

CREATE TABLE IF NOT EXISTS `Arlex`.`token` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date_insert` DATETIME NOT NULL,
  `access_token` VARCHAR(255) NOT NULL,
  `refresh_token` VARCHAR(255) NOT NULL,
  `id_user` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `access_token_UNIQUE` (`access_token` ASC),
  UNIQUE INDEX `refresh_token_UNIQUE` (`refresh_token` ASC),
  INDEX `fk_token_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_token_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Arlex`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


<<<<<<<<< Temporary merge branch 1
-- -----------------------------------------------------
-- Table `Arlex`.`user_1`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Arlex`.`user_1` ;

CREATE TABLE IF NOT EXISTS `Arlex`.`user_1` (
  `username` VARCHAR(16) NOT NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(32) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);


-- -----------------------------------------------------
-- Table `Arlex`.`timestamps`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Arlex`.`timestamps` ;

CREATE TABLE IF NOT EXISTS `Arlex`.`timestamps` (
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP NULL);


=========
>>>>>>>>> Temporary merge branch 2
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
