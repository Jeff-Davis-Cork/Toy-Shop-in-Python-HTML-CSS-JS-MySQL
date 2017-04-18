DROP TABLE IF EXISTS toys;

CREATE TABLE toys
(id_num INT NOT NULL AUTO_INCREMENT,
toy_name VARCHAR(50) NOT NULL,
toy_cat	VARCHAR(20) NOT NULL,
price decimal(4,2) NOT NULL,
age_min VARCHAR(20) NOT NULL,
stock INT NOT NULL,
photo VARCHAR(20),
PRIMARY KEY (id_num)
);

INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Transformers','Boys',020.55,'toddler',10, 'transformers.jpg');
INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Barbi', 'Girls',018.25,'toddler',50,'barbi.jpg');
INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Ninja Turtles','Boys',013.21,'toddler',22,'ninja.jpg');
INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Jump Rope', 'Girls',005.10,'toddler',40,'jump.jpg');  
INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Baseball Set','Boys',030.65,'toddler',35,'ball.jpg');
INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Cars', 'Boys',007.82,'toddler',100,'car.jpg');
INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Blocks', 'Girls',003.27,'baby',52,'blocks.jpg');
INSERT INTO toys (toy_name,toy_cat,price,age_min,stock,photo) VALUES ('Doll House', 'Girls',007.86,'baby',86,'doll.jpg');

DROP TABLE IF EXISTS customers;

CREATE TABLE customers
(
    cust_id_num INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(25) NOT NULL,
	fname VARCHAR(25) NOT NULL,
	lname VARCHAR(25) NOT NULL,
    full_address VARCHAR(50) NOT NULL,
	phone VARCHAR(20) NOT NULL,
	password VARCHAR(1000) NOT NULL,
	email VARCHAR(35) NOT NULL,
	high_score int,
    PRIMARY KEY(cust_id_num)
);

INSERT INTO customers (cust_id_num,fname,lname,full_address,phone ,password,email ,high_score,username)
VALUES (0100,'John','Doe','123 Main Street, Cork, Co. Cork','0861234567','password123','johndoe@gmail.com',8,'big john');



