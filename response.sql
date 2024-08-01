CREATE DATABASE IF NOT EXISTS my_database;

USE my_database;

CREATE TABLE IF NOT EXISTS responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    situation VARCHAR(255),
    answer TEXT,
    wrong1 TEXT,
    wrong2 TEXT,
    similar1 TEXT,
    similar2 TEXT,
    similar3 TEXT
);
