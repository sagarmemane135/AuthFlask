CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY,
       	name VARCHAR(50) NOT NULL,
       	email VARCHAR(150) UNIQUE NOT NULL,
       	password VARCHAR(200)
);
