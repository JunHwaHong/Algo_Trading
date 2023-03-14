CREATE TABLE exchange (
id INT NOT NULL AUTO_INCREMENT,
abbrev VARCHAR(32) NOT NULL,
name VARCHAR(255) NOT NULL,
city VARCHAR(255) NULL,
country VARCHAR(255) NULL,
currency VARCHAR(64) NULL,
timezone_offset time NULL,
created_date datetime NOT NULL,
last_updated_date datetime NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;