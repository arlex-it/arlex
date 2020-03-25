CREATE TABLE arlex_db.`auth_application` (
  id INT NOT NULL AUTO_INCREMENT,
  app_name VARCHAR(45) NOT NULL,
  client_id VARCHAR(100) NOT NULL,
  project_id VARCHAR(45) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX id_UNIQUE (id ASC));