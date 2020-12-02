CREATE TABLE IF NOT EXISTS `arlex_db`.`id_arlex` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int,
  `patch_id` varchar(100),
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE arlex_db.product
DROP COLUMN id_rfid;
