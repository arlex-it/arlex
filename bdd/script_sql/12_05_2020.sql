ALTER TABLE arlex_db.product
ADD COLUMN product_name varchar(100) AFTER date_update;
ALTER TABLE arlex_db.product
ADD COLUMN product_name_gen varchar(100) AFTER product_name;