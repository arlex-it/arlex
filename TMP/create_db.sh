#!/bin/bash


echo "CREATE USER IF NOT EXISTS 'corentin_local'@'127.0.0.1' IDENTIFIED BY 'corentinlocal';
GRANT ALL ON Arlex.* TO 'corentin_local'@'127.0.0.1';
FLUSH PRIVILEGES;
source scriptArlexDB.sql;" | mysql -u root -p