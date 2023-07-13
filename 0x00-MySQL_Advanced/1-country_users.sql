-- A script that create a table
-- with attributes id, email, name, country
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255), UNIQUE(email),
    country ENUM('US', 'CO', 'TN') NOT NULL
)